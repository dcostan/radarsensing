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

    def change_coordinates(self, P_):
        RP_ = np.matmul(self.R, P_)
        P = np.add(RP_, [self.t])
        return P
    
    def points_incoming(self, trackobserver):
        for track_id in trackobserver.keys():
            P = self.change_coordinates(trackobserver[track_id]["pos"])
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


if __name__ == "__main__":

    s1 = Sensor(np.array([-2, 2]), np.matrix([[0, 1], [-1, 0]]), 0, 45, 2)
    central = Central()
    
    track_0 = { "id": 0, "pos": [ [1, 3], 
                                  [1, 2],
                                  [55, 31],
                                  [55, 32],
                                  [54, 33],
                                  [53, 34],
                                  [52, 35],
                                  [51, 36],
                                  [51, 37],
                                  [50, 38]  ], "start_time": 0 }
    
    track_1 = { "id": 1, "pos": [ [56, 29], 
                                  [56, 30],
                                  [55, 31],
                                  [55, 32],
                                  [54, 33],
                                  [53, 34],
                                  [52, 35],
                                  [51, 36],
                                  [51, 37],
                                  [50, 38]  ], "start_time": 1 }
    
    central.add_track(track_0)
    central.add_track(track_1)

    central.generate_next()
    central.send_to_sensors([s1])
    central.generate_next()
    central.send_to_sensors([s1])

    print(central.trackobserver)
    print(s1.tracks_observed)
