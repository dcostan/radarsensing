from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
import re


class Sensor:

    newid = itertools.count()

    def __init__(self, t, R, D, opening, range):
        # Position variables
        self.t = t
        self.R = R
        self.D = D
        self.opening = opening
        self.range = range
        self.tracks_observed = {}
        
        # DMAC variables
        self.ID = next(Sensor.newid)
        self.Ch = False
        self.weight = 0
        self.Cluster = []
        self.Clusterhead = -1


    def add_point_to_track(self, track_id, point):
        if track_id not in self.tracks_observed.keys():
            self.tracks_observed[track_id] = {"pos": [point]}
        else:
            self.tracks_observed[track_id]["pos"].append(point)


    def is_point_in_fov(self, point):
        point = np.array(point)
        m1 = math.tan((90 - self.opening / 2) * math.pi / 180)
        first_straight_condition = (point[1] > m1 * point[0])

        m2 = math.tan((90 + self.opening / 2) * math.pi / 180)
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
                    if u not in self.Cluster:
                        self.Cluster.append(u)
                elif u in self.Cluster:
                    self.Cluster.remove(u)
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
            self.Cluster.remove(u)

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
        self.sensors_polygon = []
        self.adjacency_matrix = np.array([])

    def add_track(self, track):
        self.tracks.append(track)
        
    def add_sensors(self, sensors):
        for sensor in sensors:
            poly = self.calculate_polygon(sensor)
            self.sensors_polygon.append(poly)
            self.sensors.append(sensor)
        
        self.calculate_weight()
        for sensor in sensors:
            sensor.init_clustering(self.sensors, self.adjacency_matrix)

    def set_adjacency(self, matrix):
        if len(self.adjacency_matrix) == len(matrix):
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if self.adjacency_matrix[i,j] != matrix[i,j]:
                        if matrix[i,j]:
                            self.sensors[i].new_link(j, self.sensors, matrix)
                        else:
                            self.sensors[i].link_failure(j, self.sensors, matrix)
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
    
    def calculate_polygon(self, sensor):
        origin = self.abs_coordinates(sensor, np.array([[0], [0]])).flat  # vectors are columns
        rotation = np.degrees(
            np.arctan2(sensor.R[1, 0], sensor.R[0, 0]))  # usando arctan2, tiene conto del quadrante corretto
        theta_zero = 90 - sensor.opening / 2
        theta_one = 90 + sensor.opening / 2
        t = np.linspace(theta_zero + rotation, theta_one + rotation, 360)
        x_arc = sensor.range * np.cos(np.radians(t)) + origin[0]
        y_arc = sensor.range * np.sin(np.radians(t)) + origin[1]
        
        radar_vertex = []
        for i in range(len(t)+1):
            if i == 0:
                radar_vertex.append( (origin[0], origin[1]) )
            else:
                radar_vertex.append( (x_arc[i-1], y_arc[i-1]) )
        
        return Polygon(radar_vertex)
    
    def calculate_weight(self):
        adj = np.zeros((len(self.sensors), len(self.sensors)))
        for i in range(len(self.sensors)):
            inter_area = 0
            for j in range(len(self.sensors)):
                if i != j:
                    partial_area = self.sensors_polygon[i].intersection(self.sensors_polygon[j]).area
                    if partial_area > 0:
                        adj[i][j] = 1
                    inter_area = inter_area + partial_area
            self.sensors[i].weight = inter_area
        self.set_adjacency(adj)

    def show_room(self):
        plt.rcParams["figure.figsize"] = [10, 6.66]
        plt.rcParams["figure.autolayout"] = True

        fig, ax = plt.subplots()  # this way you create an ax object that you can return and plot on it other things

        for i in range(len(self.sensors)):
            origin = self.abs_coordinates(self.sensors[i], np.array([[0], [0]])).flat  # vectors are columns
            x,y = self.sensors_polygon[i].exterior.xy
            ax.plot(x,y)
            ax.text(origin[0] - 0.015, origin[1] + 0.05, "Radar " + str(self.sensors[i].ID))
        ax.grid()
        ax.set_xlim(-15, 15)  # for now I limited it this way... can be changed
        ax.set_ylim(0, 20)

        return ax
    
    def show_single_radars(self):
        fig2, axs = plt.subplots(1, len(self.sensors), figsize=(len(self.sensors)*2,2.0), facecolor='w', edgecolor='k')
        axs = axs.ravel()

        for i in range(len(self.sensors)):
            t = np.array([0, 0]).reshape(2, 1)
            R = np.array([[1, 0],
                          [0, 1]])
            s = Sensor(t, R, 0, opening=self.sensors[i].opening, range=self.sensors[i].range)
            polygon = self.calculate_polygon(s)
            x,y = polygon.exterior.xy
            axs[i].plot(x,y)
            axs[i].text(-3, -1.5, "Radar " + str(self.sensors[i].ID))
            axs[i].grid()
            axs[i].set_xlim(-10, 10)  # for now I limited it this way... can be changed
            axs[i].set_ylim(-5, 15)
            for track_id, track in self.sensors[i].tracks_observed.items():
                pos = np.asarray(track["pos"])
                if pos.shape == (1, 2):
                    track_array = pos
                else:
                    track_array = pos.squeeze()
                axs[i].plot(track_array[:, 0], track_array[:, 1], label=f"obs_track-{track_id}")
    
    def show_topology(self):
        plt.rcParams["figure.figsize"] = [10, 6.66]
        plt.rcParams["figure.autolayout"] = True

        fig, ax = plt.subplots()  # this way you create an ax object that you can return and plot on it other things

        for i in range(len(self.sensors)):
            origin = self.abs_coordinates(self.sensors[i], np.array([[0], [0]])).flat  # vectors are columns
            ax.plot(origin[0], origin[1], 'ko', ms=15)
            #ax.text(origin[0] - 0.015, origin[1] + 0.05, "Radar " + str(self.sensors[i].ID))
            for j in range(len(self.sensors)):
                if i != j:
                    intersection = self.sensors_polygon[i].intersection(self.sensors_polygon[j]).area
                    if intersection > 0:
                        origin_j = self.abs_coordinates(self.sensors[j], np.array([[0], [0]])).flat
                        ax.plot([origin[0], origin_j[0]], [origin[1], origin_j[1]], 'k')
        ax.set_xlim(-15, 15)
        ax.set_ylim(0, 20)
