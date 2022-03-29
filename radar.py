from random import randint

class Sensor:
    def __init__(self, t, R, D, opening, range):
        self.t = t
        self.R = R
        self.D = D
        self.opening = opening
        self.range = range

def fake_track_gen(width, height, x0, y0, t):
    track = []
    track.append([x0, y0])
    for i in list(range(t)):
        if i != 0:
            xp = track[i-1][0]
            yp = track[i-1][1]
            
            if xp == 0:
                xm = randint(0, 1)
            elif xp == width:
                xm = randint(-1, 0)
            else:
                xm = randint(-1, 1)
            
            if yp == 0:
                ym = randint(0, 1)
            elif yp == height:
                ym = randint(-1, 0)
            else:
                ym = randint(-1, 1)
            
            xn = xp + xm
            yn = yp + ym
            track.append([xn, yn])
    return track
    
# https://stackoverflow.com/questions/13430231/how-i-can-get-cartesian-coordinate-system-in-matplotlib
# Lo scopo del programma è fare che?

print(fake_track_gen(100, 100, 10, 10, 60))