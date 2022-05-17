from radar import *

central = Central()

s1 = Sensor(np.array([-2, 2]), np.matrix([[0, 1], [-1, 0]]), 0, 45, 2)
s2 = Sensor(np.array([-3, -6]), np.matrix([[1, 0], [0, 1]]), 0, 45, 2)

adj_matrix = np.matrix([[1, 0], [0, 1]])

central.set_adjacency(adj_matrix)

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

track_1 = { "id": 1, "pos": [ [0, 3], 
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
central.send_to_sensors([s1, s2])
central.generate_next()
central.send_to_sensors([s1, s2])

print(central.trackobserver)
print(s1.tracks_observed)

central.show_room([s1, s2])
