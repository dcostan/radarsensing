import numpy as np
import matplotlib.pyplot as plt

from radar import Central, Sensor

# sensors data
sensors = []

# data set 1
sensors_data = [ {"t": [-5, 1] ,  "theta": -30, "opening": 120, "range": 8},
                 {"t": [5, 2]  ,  "theta": 30 , "opening": 120, "range": 8},
                 {"t": [7, 12] ,  "theta": 90 , "opening": 120, "range": 8},
                 {"t": [-3, 18],  "theta": 180, "opening": 120, "range": 8} ]

# data set 2
sensors_data = [ {"t": [-5, 1] ,  "theta": -15, "opening": 120, "range": 8},
                 {"t": [8, 2]  ,  "theta": 30 , "opening": 120, "range": 8},
                 {"t": [7, 15] ,  "theta": 135, "opening": 100, "range": 7},
                 {"t": [-5, 12],  "theta": 225, "opening": 140, "range": 6} ]

# data set 3
sensors_data = [ {"t": [-5, 1] ,  "theta": 0  , "opening": 90 , "range": 8},
                 {"t": [8, 2]  ,  "theta": 30 , "opening": 120, "range": 8},
                 {"t": [5, 13] ,  "theta": 160, "opening": 100, "range": 9},
                 {"t": [-8, 12],  "theta": 200, "opening": 110, "range": 6} ]

for s_data in sensors_data:
    t = np.array(s_data["t"]).reshape(2, 1)  # position (column vector)
    theta = np.deg2rad(s_data["theta"])  # rotation
    R = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta), np.cos(theta)]])
    s = Sensor(t, R, 0, opening=s_data["opening"], range=s_data["range"])
    sensors.append(s)


central = Central()

central.add_sensors(sensors)

track_0 = {"id": 0, "pos": [[7, 1],
                            [7, 2],
                            [6, 3],
                            [5, 4],
                            [4, 5],
                            [3, 6],
                            [3, 7],
                            [2, 8]], "start_time": 0}

track_1 = {"id": 1, "pos": [[0, 3],
                            [1, 2]], "start_time": 0}

# generate track from (0, 0) to (0, 0.5*5^2) with an additional gaussian noise
pos_x = np.linspace(start=0, stop=5, num=50).reshape(-1, 1)
noise = np.random.normal(0, 0.5, 50).reshape(-1, 1)  # mean=0, std=0.5, 50 points
pos_y = (0.5 * pos_x ** 2 + noise).reshape(-1, 1)
pos = np.concatenate((pos_x, pos_y), axis=1).tolist()
track_3 = {"id": 2, "pos": pos, "start_time": 1}

central.add_track(track_0)
central.add_track(track_1)
central.add_track(track_3)

# run the system for some time
for i in range(50):
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
