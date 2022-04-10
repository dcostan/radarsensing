import numpy
from random import randint

class Sensor:

    def __init__(self, t, R, D, opening, range):
        self.t = t
        self.R = R
        self.D = D
        self.opening = opening
        self.range = range
        self.track_data = []
    
    def point_incoming(self, point):
        if 1 == 1:
            self.track_data.append(point)
        else:
            self.track_data.append([])

class Central:

    def __init__(self, width, height, t):
        self.t = t
        self.width = width
        self.height = height
        self.track = self.fake_track_gen(width, height, t)
        self.position_counter = 0
        self.current_position = self.track[self.position_counter]
        
    def fake_track_gen(self, width, height, t):
        track = []
        track.append([56, 29])
        track.append([56, 30])
        track.append([55, 31])
        track.append([55, 32])
        track.append([54, 33])
        track.append([53, 34])
        track.append([52, 35])
        track.append([51, 36])
        track.append([51, 37])
        track.append([50, 38])
        return track
    
    def generate_next(self):
        self.position_counter = self.position_counter + 1
        self.current_position = self.track[self.position_counter]
    
    def send_to_sensors(self, sensors):
        for s in sensors:
            s.point_incoming([self.current_position])
    
# https://stackoverflow.com/questions/13430231/how-i-can-get-cartesian-coordinate-system-in-matplotlib
# Lo scopo del programma è fare che?
# La traccia non la generiamo random ma facciamo che si disegna a mano
# Idea implementativa: creiamo una finestra Tkinter e leggiamo periodicamente la posizione del mouse
# mentre è cliccato
# Poi abbiamo il main che fa
# for k in range(600):
#   ...
#   central.generate_next()
#   central.send_to_sensors()
#   sensor.step()

s1 = Sensor(1, 1, 1, 1, 1)
central = Central(100, 100, 10)

central.send_to_sensors([s1])
central.generate_next()
central.send_to_sensors([s1])

print(s1.track_data)
