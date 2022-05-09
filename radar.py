from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import numpy as np
import math

class Sensor:

    def __init__(self, t, R, D, opening, range):
        self.t = t
        self.R = R
        self.D = D
        self.opening = opening
        self.range = range
        self.tracks_observed = {}
    
    def add_point_to_track(self, track_id, point):
        if track_id not in self.tracks_observed.keys():
            self.tracks_observed[track_id] = { "pos": [ point ] }
        else:
            self.tracks_observed[track_id]["pos"].append(point)
    
    def is_point_in_fov(self, point):
        m1 = math.tan( ( 90 - self.opening ) * math.pi / 180 )
        first_straight_condition = ( point.flat[1] > m1 * point.flat[0] )
        
        m2 = math.tan( ( 90 + self.opening ) * math.pi / 180 )
        second_straight_condition = ( point.flat[1] > m2 * point.flat[0] )

        return first_straight_condition and second_straight_condition

    def rel_coordinates(self, P_):
        P = self.R @ P_ + [self.t]
        return np.array(P)
    
    def points_incoming(self, trackobserver):
        for track_id in trackobserver.keys():
            P = self.rel_coordinates(trackobserver[track_id]["pos"])
            if self.is_point_in_fov(P):
                self.add_point_to_track(track_id, P)
            

class Central:

    def __init__(self):
        self.tracks = []
        self.timestep = 0
        self.trackobserver = {}
    
    def add_track(self, track):
        self.tracks.append(track)
    
    def generate_next(self):
        self.trackobserver = {}
        for track in self.tracks:
            if 0 <= self.timestep - track["start_time"] <= len(track["pos"]):
                self.trackobserver[track["id"]] = { "pos": np.array(track["pos"][self.timestep-track["start_time"]]) }
        self.timestep = self.timestep + 1
    
    def send_to_sensors(self, sensors):
        for s in sensors:
            s.points_incoming(self.trackobserver)
            
    def abs_coordinates(self, s, P):
        P_ = s.R.T @ ( P - [s.t] ).T
        return np.array(P_)
    
    def show_room(self, sensors):
        plt.rcParams["figure.figsize"] = [6.50, 6.50]
        plt.rcParams["figure.autolayout"] = True
        
        for sensor in sensors:
        
            origin = self.abs_coordinates(sensor, np.array([0,0])).flat
            limit1 = self.abs_coordinates(sensor, np.array([math.cos(( 90 - ( sensor.opening/2) ) * math.pi / 180 ) * sensor.range,
                                                            math.sin(( 90 - ( sensor.opening/2) ) * math.pi / 180 ) * sensor.range])).flat
            limit2 = self.abs_coordinates(sensor, np.array([math.cos(( 90 + ( sensor.opening/2) ) * math.pi / 180 ) * sensor.range,
                                                            math.sin(( 90 + ( sensor.opening/2) ) * math.pi / 180 ) * sensor.range])).flat
            x_line1 = [origin[0], limit1[0]]
            y_line1 = [origin[1], limit1[1]]
            x_line2 = [origin[0], limit2[0]]
            y_line2 = [origin[1], limit2[1]]
            
            rotation = np.degrees(np.arccos(sensor.R.flat[0]))
            theta_zero = 90 - sensor.opening / 2
            theta_one = 90 + sensor.opening / 2
            t = np.linspace(theta_zero + rotation, theta_one + rotation, 360)
            x_arc = sensor.range * np.cos(np.radians(t)) + origin[0]
            y_arc = sensor.range * np.sin(np.radians(t)) + origin[1]
            
            plt.plot(x_arc, y_arc, 'b')
            plt.plot(x_line1, y_line1, 'b', linestyle="-")
            plt.plot(x_line2, y_line2, 'b', linestyle="-")
            plt.text(origin[0]-0.015, origin[1]+0.05, "Radar")

        plt.show()
