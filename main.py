import numpy as np
import matplotlib.pyplot as plt

from radar import Central, Sensor

# sensors data
sensors = []


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

track_0 = {"id": 0, "pos": [[-9.36, 9.33],
                            [-9.17, 9.35],
                            [-8.72, 9.4],
                            [-8.17, 9.44],
                            [-7.68, 9.45],
                            [-7.27, 9.44],
                            [-6.87, 9.44],
                            [-6.41, 9.46],
                            [-5.88, 9.52],
                            [-5.31, 9.6],
                            [-4.76, 9.65],
                            [-4.26, 9.68],
                            [-3.78, 9.68],
                            [-3.28, 9.69],
                            [-2.73, 9.72],
                            [-2.13, 9.75],
                            [-1.51, 9.76],
                            [-0.93, 9.71],
                            [-0.4, 9.58],
                            [0.09, 9.41],
                            [0.53, 9.24],
                            [0.94, 9.11],
                            [1.35, 9.02],
                            [1.79, 8.97],
                            [2.29, 8.96],
                            [2.82, 8.97],
                            [3.32, 8.97],
                            [3.71, 8.94],
                            [3.99, 8.87],
                            [4.19, 8.76],
                            [4.39, 8.63],
                            [4.63, 8.5],
                            [4.89, 8.38],
                            [5.16, 8.26],
                            [5.4, 8.15],
                            [5.61, 8.06],
                            [5.78, 7.96],
                            [5.91, 7.87],
                            [6.0, 7.76],
                            [6.11, 7.63],
                            [6.27, 7.45],
                            [6.5, 7.21],
                            [6.75, 6.91],
                            [6.92, 6.53],
                            [6.94, 6.08],
                            [6.8, 5.61],
                            [6.54, 5.16],
                            [6.2, 4.82],
                            [5.8, 4.6],
                            [5.3, 4.49],
                            [4.68, 4.43],
                            [3.92, 4.4],
                            [3.1, 4.4],
                            [2.27, 4.42],
                            [1.51, 4.45],
                            [0.85, 4.49],
                            [0.26, 4.51],
                            [-0.27, 4.5],
                            [-0.75, 4.48],
                            [-1.22, 4.53],
                            [-1.69, 4.71],
                            [-2.17, 5.08],
                            [-2.58, 5.49],
                            [-2.81, 5.75] ], "start_time": 0}

track_1 = {"id": 1, "pos": [[-8.02, 2.63],
                            [-8.04, 2.8],
                            [-8.09, 3.24],
                            [-8.18, 3.79],
                            [-8.31, 4.32],
                            [-8.47, 4.79],
                            [-8.62, 5.23],
                            [-8.73, 5.65],
                            [-8.78, 6.07],
                            [-8.79, 6.5],
                            [-8.8, 6.92],
                            [-8.81, 7.35],
                            [-8.81, 7.77],
                            [-8.77, 8.19],
                            [-8.68, 8.61],
                            [-8.52, 9.02],
                            [-8.3, 9.45],
                            [-8.02, 9.89],
                            [-7.71, 10.34],
                            [-7.39, 10.76],
                            [-7.1, 11.09],
                            [-6.85, 11.31],
                            [-6.6, 11.45],
                            [-6.27, 11.55],
                            [-5.82, 11.65],
                            [-5.27, 11.77],
                            [-4.72, 11.91],
                            [-4.25, 12.07],
                            [-3.91, 12.23],
                            [-3.63, 12.38],
                            [-3.33, 12.5],
                            [-2.95, 12.58],
                            [-2.5, 12.62],
                            [-1.97, 12.67],
                            [-1.38, 12.73],
                            [-0.78, 12.8],
                            [-0.24, 12.83],
                            [0.18, 12.78],
                            [0.46, 12.63],
                            [0.71, 12.39],
                            [1.03, 12.07],
                            [1.49, 11.69],
                            [2.04, 11.25],
                            [2.56, 10.77],
                            [2.98, 10.26],
                            [3.29, 9.74],
                            [3.55, 9.22],
                            [3.83, 8.72],
                            [4.15, 8.24],
                            [4.46, 7.82],
                            [4.7, 7.47],
                            [4.84, 7.22],
                            [4.91, 6.98],
                            [4.94, 6.68],
                            [4.97, 6.24],
                            [4.99, 5.69],
                            [4.98, 5.14],
                            [4.91, 4.71],
                            [4.76, 4.42],
                            [4.56, 4.21],
                            [4.32, 3.98],
                            [4.07, 3.67],
                            [3.86, 3.37],
                            [3.74, 3.19]  ], "start_time": 0}

# generate track from (0, 0) to (0, 0.5*5^2) with an additional gaussian noise
pos_x = np.linspace(start=0, stop=5, num=50).reshape(-1, 1)
noise = np.random.normal(0, 0.5, 50).reshape(-1, 1)  # mean=0, std=0.5, 50 points
pos_y = (0.5 * pos_x ** 2 + noise).reshape(-1, 1)
pos = np.concatenate((pos_x, pos_y), axis=1).tolist()
track_3 = {"id": 2, "pos": pos, "start_time": 1}

#central.add_track(track_0)
#central.add_track(track_1)
#central.add_track(track_3)

# run the system for some time
for i in range(100):
    central.generate_next()
    central.send_to_sensors()

# Debug DMCA
for sensor in sensors:
    if sensor.Ch:
        print("Sensor " + str(sensor.ID) + " is CH with cluster " + str(sensor.Cluster))
    else:
        print("Sensor " + str(sensor.ID) + " is in the cluster of sensor " + str(sensor.Clusterhead))

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
fig2, axs = plt.subplots(1, len(central.sensors), figsize=(len(central.sensors)*2,2.5), facecolor='w', edgecolor='k')
axs = axs.ravel()

for i in range(len(central.sensors)):
    t = np.array([0, 0]).reshape(2, 1)
    R = np.array([[1, 0],
                  [0, 1]])
    s = Sensor(t, R, 0, opening=central.sensors[i].opening, range=central.sensors[i].range)
    polygon = central.calculate_polygon(s)
    x,y = polygon.exterior.xy
    axs[i].plot(x,y)
    axs[i].text(-3, -1.5, "Radar " + str(central.sensors[i].ID))
    axs[i].grid()
    axs[i].set_xlim(-10, 10)  # for now I limited it this way... can be changed
    axs[i].set_ylim(-5, 15)
    for track_id, track in central.sensors[i].tracks_observed.items():
        pos = np.asarray(track["pos"])
        if pos.shape == (1, 2):
            track_array = pos
        else:
            track_array = pos.squeeze()
        axs[i].plot(track_array[:, 0], track_array[:, 1], label=f"obs_track-{track_id}")

plt.show()
