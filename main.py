import numpy as np
import matplotlib.pyplot as plt

from radar import Central, Sensor

# sensor 1
t1 = np.array([-5, 1]).reshape(2, 1)  # position (column vector)
theta1 = np.deg2rad(-30)  # rotation
R1 = np.array([[np.cos(theta1), -np.sin(theta1)],
                [np.sin(theta1), np.cos(theta1)]])
s1 = Sensor(t1, R1, 0, opening=120, range=8)

# sensor 2
theta2 = np.deg2rad(30)  # position (column vector)
t2 = np.array([5, 2]).reshape(2, 1)  # rotation
R2 = np.array([[np.cos(theta2), -np.sin(theta2)],
                [np.sin(theta2), np.cos(theta2)]])
s2 = Sensor(t2, R2, 0, opening=120, range=8)

sensors = [s1, s2]

central = Central()

track_0 = {"id": 0, "pos": [[1, 3],
                            [1, 2],
                            [55, 31],
                            [55, 32],
                            [54, 33],
                            [53, 34],
                            [52, 35],
                            [51, 36],
                            [51, 37],
                            [50, 38]], "start_time": 0}

track_1 = {"id": 1, "pos": [[0, 3],
                            [56, 30],
                            [55, 31],
                            [55, 32],
                            [54, 33],
                            [53, 34],
                            [52, 35],
                            [51, 36],
                            [51, 37],
                            [50, 38]], "start_time": 0 }

# generate track from (0, 0) to (0, 0.5*5^2) with an additional gaussian noise
pos_x = np.linspace(start=0, stop=5, num=50).reshape(-1, 1)
noise = np.random.normal(0, 0.5, 50).reshape(-1, 1)  # mean=0, std=0.5, 50 points
pos_y = (0.5 * pos_x ** 2 + noise).reshape(-1, 1)
pos = np.concatenate((pos_x, pos_y), axis=1).tolist()
track_3 = {"id": 2, "pos": pos, "start_time": 1 }

central.add_track(track_0)
central.add_track(track_1)
central.add_track(track_3)

# run the system for some time
for i in range(50):
    central.generate_next()
    central.send_to_sensors(sensors)

ax = central.show_room([s1, s2]) # when you plot, you plot on an ax object, and you can plot multiple things on the same ax

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
        track_array = (R @ np.asarray(track["pos"]).squeeze().T + t).T  # transform track from radar to abs ref sys
        ax.plot(track_array[:, 0], track_array[:, 1], label=f"obs_track-{track_id}")

plt.legend()
plt.show()

