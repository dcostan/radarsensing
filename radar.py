import numpy
from random import randint

class Sensor:

    def __init__(self, t, R, D, opening, range):
        self.t = t
        self.R = R
        self.D = D
        self.opening = opening
        self.range = range
        self.tracks_observed = []
    
    def add_point_to_track(self, tid, point):
        tid_found = False
        for track in self.tracks_observed:
            if track["id"] == tid:
                tid_found = True
                track["pos"].append(point)
        if not tid_found:
            self.tracks_observed.append({ "id": tid, "pos": [ point ] })
    
    def points_incoming(self, trackobserver):
        for point in trackobserver:
            self.add_point_to_track(point["id"], point["pos"])

class Central:

    def __init__(self):
        self.tracks = []
        self.timestamp = 0
        self.trackobserver = []
    
    def add_track(self, track):
        self.tracks.append(track)
    
    def generate_next(self):
        self.trackobserver = []
        for track in self.tracks:
            if 0 <= self.timestamp - track["start_time"] <= len(track["pos"]):
                self.trackobserver.append({ "id": track["id"], "pos": track["pos"][self.timestamp-track["start_time"]] })
        self.timestamp = self.timestamp + 1
    
    def send_to_sensors(self, sensors):
        for s in sensors:
            s.points_incoming(self.trackobserver)


if __name__ == "__main__":

    s1 = Sensor(1, 1, 1, 1, 1)
    central = Central()
    
    track_0 = { "id": 0, "pos": [ [56, 29], 
                                  [56, 30],
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
