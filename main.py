import numpy as np
import matplotlib.pyplot as plt

from radar import Central, Sensor

# sensors data
sensors = []

'''
# data set 1
sensors_data = [ {"t": [-7, 17] ,  "theta": 180, "opening": 50, "range": 6},
                 {"t": [-14, 11],  "theta": 270, "opening": 50, "range": 7},
                 {"t": [5, 5]   ,  "theta": 0  , "opening": 65, "range": 7},
                 {"t": [5, 18]  ,  "theta": 180, "opening": 60, "range": 8},
                 {"t": [13, 11] ,  "theta": 90 , "opening": 60, "range": 7},
                 {"t": [-5, 1]  ,  "theta": 0  , "opening": 70, "range": 6},
                 {"t": [-1, 1]  ,  "theta": 0  , "opening": 70, "range": 6} ]
'''
# data set 2
sensors_data = [ {"t": [-5, 1] ,  "theta": 0  , "opening": 65, "range": 8},
                 {"t": [-5, 15],  "theta": 180, "opening": 60, "range": 8},
                 {"t": [-13, 8],  "theta": 270, "opening": 60, "range": 7},
                 {"t": [5, 1]  ,  "theta": 0  , "opening": 65, "range": 8},
                 {"t": [5, 15] ,  "theta": 180, "opening": 60, "range": 8},
                 {"t": [13, 8] ,  "theta": 90 , "opening": 60, "range": 7} ]
'''
# data set 3
sensors_data = [ {"t": [0, 1]  ,  "theta": 0  , "opening": 50, "range": 9},
                 {"t": [8, 8]  ,  "theta": 90 , "opening": 50, "range": 9},
                 {"t": [0, 17] ,  "theta": 180, "opening": 50, "range": 9},
                 {"t": [-8, 8] ,  "theta": 270, "opening": 50, "range": 9} ]
'''
for s_data in sensors_data:
    t = np.array(s_data["t"]).reshape(2, 1)  # position (column vector)
    theta = np.deg2rad(s_data["theta"])  # rotation
    R = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta), np.cos(theta)]])
    s = Sensor(t, R, 0, opening=s_data["opening"], range=s_data["range"])
    sensors.append(s)


central = Central()

central.add_sensors(sensors)

track_0 = {"id": 0, "pos": [[-12.7, 10.36],
                            [-12.55, 10.51],
                            [-12.18, 10.87],
                            [-11.76, 11.28],
                            [-11.41, 11.59],
                            [-11.14, 11.79],
                            [-10.83, 11.93],
                            [-10.39, 12.06],
                            [-9.79, 12.21],
                            [-9.12, 12.4],
                            [-8.49, 12.63],
                            [-7.97, 12.88],
                            [-7.52, 13.14],
                            [-7.07, 13.36],
                            [-6.56, 13.52],
                            [-5.99, 13.63],
                            [-5.38, 13.74],
                            [-4.79, 13.92],
                            [-4.23, 14.17],
                            [-3.7, 14.43],
                            [-3.2, 14.65],
                            [-2.7, 14.77],
                            [-2.16, 14.83],
                            [-1.52, 14.88],
                            [-0.72, 14.95],
                            [0.23, 15.05],
                            [1.25, 15.15],
                            [2.28, 15.22],
                            [3.26, 15.26],
                            [4.11, 15.28],
                            [4.8, 15.33],
                            [5.28, 15.39],
                            [5.62, 15.41],
                            [5.91, 15.29],
                            [6.24, 14.95],
                            [6.58, 14.42],
                            [6.88, 13.82],
                            [7.06, 13.24],
                            [7.1, 12.75],
                            [7.07, 12.33],
                            [7.01, 11.95],
                            [6.99, 11.58],
                            [6.96, 11.23],
                            [6.91, 10.89],
                            [6.77, 10.58],
                            [6.56, 10.26],
                            [6.26, 9.9],
                            [5.88, 9.46],
                            [5.44, 8.94],
                            [4.97, 8.39],
                            [4.51, 7.9],
                            [4.1, 7.52],
                            [3.72, 7.23],
                            [3.4, 7.03],
                            [3.11, 6.9],
                            [2.82, 6.78],
                            [2.43, 6.6],
                            [1.88, 6.32],
                            [1.13, 5.9],
                            [0.26, 5.4],
                            [-0.63, 4.9],
                            [-1.46, 4.44],
                            [-2.11, 4.1],
                            [-2.46, 3.93] ], "start_time": 0}

track_1 = {"id": 1, "pos": [[7.3, 10.97],
                            [7.31, 10.84],
                            [7.33, 10.54],
                            [7.36, 10.17],
                            [7.39, 9.83],
                            [7.41, 9.53],
                            [7.43, 9.23],
                            [7.45, 8.88],
                            [7.46, 8.45],
                            [7.46, 7.95],
                            [7.44, 7.41],
                            [7.39, 6.84],
                            [7.3, 6.27],
                            [7.15, 5.74],
                            [6.94, 5.27],
                            [6.65, 4.88],
                            [6.26, 4.57],
                            [5.76, 4.34],
                            [5.17, 4.18],
                            [4.56, 4.06],
                            [4.01, 3.98],
                            [3.59, 3.9],
                            [3.25, 3.82],
                            [2.92, 3.75],
                            [2.54, 3.69],
                            [2.08, 3.63],
                            [1.55, 3.58],
                            [0.95, 3.53],
                            [0.3, 3.48],
                            [-0.32, 3.42],
                            [-0.84, 3.36],
                            [-1.22, 3.3],
                            [-1.52, 3.24],
                            [-1.85, 3.19],
                            [-2.31, 3.16],
                            [-2.9, 3.15],
                            [-3.55, 3.16],
                            [-4.2, 3.19],
                            [-4.79, 3.24],
                            [-5.34, 3.32],
                            [-5.84, 3.42],
                            [-6.31, 3.57],
                            [-6.71, 3.74],
                            [-7.04, 3.92],
                            [-7.28, 4.09],
                            [-7.44, 4.29],
                            [-7.59, 4.52],
                            [-7.76, 4.82],
                            [-7.97, 5.19],
                            [-8.18, 5.58],
                            [-8.34, 5.94],
                            [-8.43, 6.23],
                            [-8.48, 6.48],
                            [-8.53, 6.71],
                            [-8.63, 6.98],
                            [-8.78, 7.27],
                            [-8.95, 7.58],
                            [-9.1, 7.88],
                            [-9.23, 8.18],
                            [-9.37, 8.49],
                            [-9.56, 8.82],
                            [-9.8, 9.18],
                            [-10.04, 9.49],
                            [-10.19, 9.67]  ], "start_time": 0}

track_2 = {"id": 2, "pos": [[-11.56, 18.15],
                            [-11.42, 18.06],
                            [-11.07, 17.84],
                            [-10.59, 17.56],
                            [-10.07, 17.3],
                            [-9.59, 17.09],
                            [-9.18, 16.9],
                            [-8.91, 16.75],
                            [-8.77, 16.61],
                            [-8.66, 16.43],
                            [-8.49, 16.18],
                            [-8.17, 15.83],
                            [-7.76, 15.39],
                            [-7.33, 14.93],
                            [-6.96, 14.47],
                            [-6.66, 14.06],
                            [-6.38, 13.72],
                            [-6.1, 13.48],
                            [-5.79, 13.33],
                            [-5.44, 13.21],
                            [-5.06, 13.06],
                            [-4.63, 12.82],
                            [-4.21, 12.52],
                            [-3.82, 12.23],
                            [-3.49, 11.97],
                            [-3.23, 11.74],
                            [-2.97, 11.48],
                            [-2.66, 11.16],
                            [-2.31, 10.76],
                            [-1.95, 10.36],
                            [-1.63, 10.05],
                            [-1.38, 9.88],
                            [-1.17, 9.78],
                            [-0.94, 9.67],
                            [-0.62, 9.47],
                            [-0.25, 9.19],
                            [0.11, 8.91],
                            [0.38, 8.7],
                            [0.54, 8.59],
                            [0.66, 8.51],
                            [0.8, 8.39],
                            [1.0, 8.19],
                            [1.25, 7.94],
                            [1.5, 7.67],
                            [1.74, 7.45],
                            [1.95, 7.27],
                            [2.15, 7.1],
                            [2.38, 6.92],
                            [2.63, 6.71],
                            [2.87, 6.51],
                            [3.09, 6.37],
                            [3.26, 6.3],
                            [3.42, 6.25],
                            [3.64, 6.17],
                            [3.94, 5.99],
                            [4.31, 5.74],
                            [4.67, 5.48],
                            [4.95, 5.26],
                            [5.13, 5.11],
                            [5.29, 4.99],
                            [5.51, 4.83],
                            [5.86, 4.63],
                            [6.21, 4.42],
                            [6.43, 4.29]  ], "start_time": 0}

# generate track from (0, 0) to (0, 0.5*5^2) with an additional gaussian noise
pos_x = np.linspace(start=0, stop=5, num=50).reshape(-1, 1)
noise = np.random.normal(0, 0.5, 50).reshape(-1, 1)  # mean=0, std=0.5, 50 points
pos_y = (0.5 * pos_x ** 2 + noise).reshape(-1, 1)
pos = np.concatenate((pos_x, pos_y), axis=1).tolist()
track_3 = {"id": 2, "pos": pos, "start_time": 1}

#central.add_track(track_0)
central.add_track(track_1)
#central.add_track(track_2)

# run the system for some time
for i in range(0):
    central.generate_next()
    central.send_to_sensors()

# Debug DMCA
print("DISPOSITIVO\tPESO\tCH\tCLUSTER\t\tCLUSTER HEAD")
for sensor in sensors:
    if sensor.Ch:
        print("Sensor " + str(sensor.ID) + "\t" + str(round(sensor.weight, 2)) + "\t✔\t" + str(sensor.Cluster))
    else:
        print("Sensor " + str(sensor.ID) + "\t" + str(round(sensor.weight, 2)) + "\t\t\t\tSensor " + str(sensor.Clusterhead))

ax = central.show_room() # when you plot, you plot on an ax object, and you can plot multiple things on the same ax

# plot all the tracks provided
for track in central.tracks:
    track_array = np.asarray(track["pos"])
    track_id = track["id"]
    ax.plot(track_array[:, 0], track_array[:, 1], '--', label=f"generated_track-{track_id}")

# plot the tracks seen by the radars
for sensor in sensors:
    R = sensor.R
    t = sensor.t
    for track_id, track in sensor.tracks_observed.items():
        pos = np.asarray(track["pos"])
        if pos.shape == (1, 2):  # handle special case of track with only one point, if not handled after squeeze and transpose the coordinates are switched
            track_array = (R @ pos.T + t).T  # transform track from radar to abs ref sys
        else:
            track_array = (R @ pos.squeeze().T + t).T  # transform track from radar to abs ref sys
        ax.plot(track_array[:, 0], track_array[:, 1], label=f"obs_track-{track_id}")
ax.legend()

# plot single radars
central.show_single_radars()

# plot topology
central.show_topology()

plt.show()
