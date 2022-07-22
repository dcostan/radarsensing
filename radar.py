import matplotlib.pyplot as plt
import numpy as np
import math
import re


class Sensor:

    def __init__(self, t, R, D, opening, range, weight):
        # Position variables
        self.t = t
        self.R = R
        self.D = D
        self.opening = opening
        self.range = range
        self.tracks_observed = {}
        
        # DMAC variables
        self.ID = -1
        self.Ch = False
        self.weight = weight
        self.Cluster = []
        self.Clusterhead = -1


    def add_point_to_track(self, track_id, point):
        if track_id not in self.tracks_observed.keys():
            self.tracks_observed[track_id] = {"pos": [point]}
        else:
            self.tracks_observed[track_id]["pos"].append(point)


    def is_point_in_fov(self, point):
        point = np.array(point)
        m1 = math.tan((90 - self.opening) * math.pi / 180)
        first_straight_condition = (point[1] > m1 * point[0])

        m2 = math.tan((90 + self.opening) * math.pi / 180)
        second_straight_condition = (point[1] > m2 * point[0])

        range_condition = np.linalg.norm(point) <= self.range

        return first_straight_condition and second_straight_condition and range_condition


    def rel_coordinates(self, P_):
        """Transforms point P_ from absolute reference system to the sensor reference system
        :param P_: the point to be transformed; the point is assumed to be a column vector.
        :type P_: np.ndarray
        :returns: the transformed point"""
        # P = self.R @ P_ + [self.t]
        P = self.R.T @ (P_ - self.t)
        return P.squeeze().tolist()


    def points_incoming(self, trackobserver):
        for track_id in trackobserver.keys():
            P = self.rel_coordinates(trackobserver[track_id]["pos"])
            if self.is_point_in_fov(P):
                self.add_point_to_track(track_id, P)
    
    
    def find_mw_ch_node(self, sensors, adj_matrix):
        node = self
        for i in range(len(sensors) - 1):
            if adj_matrix[self.ID, i]:    # [self.ID, i] is the row corresponding to the current sensor index
                if sensors[i].weight > node.weight and sensors[i].Ch:
                    node = sensors[i]
        if node == self:
            return None
        else:
            return node
    
    
    def send_message(self, msg, sensors, adj_matrix):
        for sensor in sensors:
            if adj_matrix[self.ID, sensor.ID]:
                sensor.receive_message(msg, sensors, adj_matrix)
    
    
    def receive_message(self, msg, sensors, adj_matrix):
        
        if bool(re.match(r"CH\([0-9]+\)", msg)):
            u = int(re.findall(r'\d+', msg)[0])
            if sensors[u].weight > sensors[self.Clusterhead].weight:
                if self.Ch:
                    self.Ch = False
                self.Clusterhead = u
                msg = "JOIN(" + str(self.ID) + "," + str(u) + ")"
                self.send_message(msg, sensors, adj_matrix)
        
        elif bool(re.match(r"JOIN\([0-9]+\,[0-9]+\)", msg)):
            u = int(re.findall(r'\d+', msg)[0])
            z = int(re.findall(r'\d+', msg)[1])
            if self.Ch:
                if z == self.ID:
                    self.Cluster.append(u)
                elif u in self.Cluster:
                    i = self.Cluster.index(u)
                    self.Cluster.remove(i)
            elif self.Clusterhead == u:
                mw_ch_node = self.find_mw_ch_node(sensors, adj_matrix)
                if mw_ch_node != None:
                    self.Clusterhead = mw_ch_node.ID
                    msg = "JOIN(" + str(self.ID) + "," + str(mw_ch_node.ID) + ")"
                    self.send_message(msg, sensors, adj_matrix)
                else:
                    self.Ch = True
                    self.Clusterhead = self.ID
                    self.Cluster = [ self.ID ]
                    msg = "CH(" + str(self.ID) + ")"
                    self.send_message(msg, sensors, adj_matrix)
                
                    
    def init_clustering(self, sensors, adj_matrix):
        self.ID = len(sensors) - 1    # Obtain the current sensor id form adj matrix
        mw_ch_node = self.find_mw_ch_node(sensors, adj_matrix)
        
        if mw_ch_node != None:
            self.Clusterhead = mw_ch_node.ID
            msg = "JOIN(" + str(self.ID) + "," + str(mw_ch_node.ID) + ")"
            self.send_message(msg, sensors, adj_matrix)
        else:
            self.Ch = True
            self.Clusterhead = self.ID
            self.Cluster = [ self.ID ]
            msg = "CH(" + str(self.ID) + ")"
            self.send_message(msg, sensors, adj_matrix)
    
                    
    def link_failure(self, u, sensors, adj_matrix):

        if self.Ch and u in self.Cluster:
            i = self.Cluster.index(u)
            self.Cluster.remove(i)

        elif self.Clusterhead == u:
            mw_ch_node = self.find_mw_ch_node(sensors, adj_matrix)
            if mw_ch_node != None:
                self.Clusterhead = mw_ch_node.ID
                msg = "JOIN(" + str(self.ID) + "," + str(mw_ch_node.ID) + ")"
                self.send_message(msg, sensors, adj_matrix)
            else:
                self.Ch = True
                self.Clusterhead = self.ID
                self.Cluster = [ self.ID ]
                msg = "CH(" + str(self.ID) + ")"
                self.send_message(msg, sensors, adj_matrix)
    
                    
    def new_link(self, u, sensors, adj_matrix):
        if sensors[u].Ch and sensors[u].weight > sensors[self.Clusterhead].weight:
            if self.Ch:
                self.Ch = False
            self.Clusterhead = u
            msg = "JOIN(" + str(self.ID) + "," + str(u) + ")"
            self.send_message(msg, sensors, adj_matrix)


class Central:

    def __init__(self):
        self.tracks = []
        self.sensors = []
        self.timestep = 0
        self.trackobserver = {}
        self.adjacency_matrix = np.array([])

    def add_track(self, track):
        self.tracks.append(track)
        
    def add_sensors(self, sensors):
        for sensor in sensors:
            self.sensors.append(sensor)
            sensor.init_clustering(self.sensors, self.adjacency_matrix)

    def set_adjacency(self, matrix):
        self.adjacency_matrix = matrix

    def generate_next(self):
        self.trackobserver = {}
        for track in self.tracks:
            if 0 <= self.timestep - track["start_time"] < len(track["pos"]):  # TODO: bisogna mettere < e non <= altrimenti va fuori array
                self.trackobserver[track["id"]] = {
                    "pos": np.array(track["pos"][self.timestep - track["start_time"]]).reshape(2, 1)}  # TODO: reshaped to column vector
        self.timestep = self.timestep + 1

    def send_to_sensors(self):
        for s in self.sensors:
            s.points_incoming(self.trackobserver)

    def abs_coordinates(self, s, P):
        # P_ = s.R.T @ ( P - [s.t] ).T
        P_ = s.R @ P + s.t
        return np.array(P_)

    def show_room(self):
        plt.rcParams["figure.figsize"] = [6.50, 6.50]
        plt.rcParams["figure.autolayout"] = True

        fig, ax = plt.subplots()  # this way you create an ax object that you can return and plot on it other things

        for sensor in self.sensors:
            origin = self.abs_coordinates(sensor, np.array([[0], [0]])).flat  # vectors are columns
            limit1 = self.abs_coordinates(sensor, np.array(
                [[math.cos((90 - (sensor.opening / 2)) * math.pi / 180) * sensor.range],
                 [math.sin((90 - (sensor.opening / 2)) * math.pi / 180) * sensor.range]]))
            limit2 = self.abs_coordinates(sensor, np.array(
                [[math.cos((90 + (sensor.opening / 2)) * math.pi / 180) * sensor.range],
                 [math.sin((90 + (sensor.opening / 2)) * math.pi / 180) * sensor.range]]))
            x_line1 = [origin[0], limit1[0]]
            y_line1 = [origin[1], limit1[1]]
            x_line2 = [origin[0], limit2[0]]
            y_line2 = [origin[1], limit2[1]]

            # rotation = np.degrees(np.arccos(sensor.R.flat[0]))  # TODO: il coseno è simmetrico rispetto all'asse x, quindi dopo 180° l'arccos "torna indietro"
            rotation = np.degrees(
                np.arctan2(sensor.R[1, 0], sensor.R[0, 0]))  # usando arctan2, tiene conto del quadrante corretto
            theta_zero = 90 - sensor.opening / 2
            theta_one = 90 + sensor.opening / 2
            t = np.linspace(theta_zero + rotation, theta_one + rotation, 360)
            x_arc = sensor.range * np.cos(np.radians(t)) + origin[0]
            y_arc = sensor.range * np.sin(np.radians(t)) + origin[1]

            ax.plot(x_arc, y_arc, 'b')
            ax.plot(x_line1, y_line1, 'b', linestyle="-")
            ax.plot(x_line2, y_line2, 'b', linestyle="-")
            ax.text(origin[0] - 0.015, origin[1] + 0.05, "Radar")
        ax.grid()
        ax.set_xlim(-10, 10)  # for now I limited it this way... can be changed
        ax.set_ylim(0, 20)

        return ax
