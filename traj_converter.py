'''
Example input:

  Columns 1 through 15

    2.6400    2.8300    3.2800    3.8300    4.3200    4.7300    5.1300    5.5900    6.1200    6.6900    7.2400    7.7400    8.2200    8.7200    9.2700
    9.3300    9.3500    9.4000    9.4400    9.4500    9.4400    9.4400    9.4600    9.5200    9.6000    9.6500    9.6800    9.6800    9.6900    9.7200

  Columns 16 through 30

    9.8700   10.4900   11.0700   11.6000   12.0900   12.5300   12.9400   13.3500   13.7900   14.2900   14.8200   15.3200   15.7100   15.9900   16.1900
    9.7500    9.7600    9.7100    9.5800    9.4100    9.2400    9.1100    9.0200    8.9700    8.9600    8.9700    8.9700    8.9400    8.8700    8.7600

  Columns 31 through 45

   16.3900   16.6300   16.8900   17.1600   17.4000   17.6100   17.7800   17.9100   18.0000   18.1100   18.2700   18.5000   18.7500   18.9200   18.9400
    8.6300    8.5000    8.3800    8.2600    8.1500    8.0600    7.9600    7.8700    7.7600    7.6300    7.4500    7.2100    6.9100    6.5300    6.0800

  Columns 46 through 60

   18.8000   18.5400   18.2000   17.8000   17.3000   16.6800   15.9200   15.1000   14.2700   13.5100   12.8500   12.2600   11.7300   11.2500   10.7800
    5.6100    5.1600    4.8200    4.6000    4.4900    4.4300    4.4000    4.4000    4.4200    4.4500    4.4900    4.5100    4.5000    4.4800    4.5300

  Columns 61 through 64

   10.3100    9.8300    9.4200    9.1900
    4.7100    5.0800    5.4900    5.7500

Example output:
                            [-9.36, 9.33],
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
                            [-2.81, 5.75],
'''

import re
from decimal import Decimal

x = []
y = []

with open("traj.txt", "r") as file:
    column_zero = True
    for line in file:
        numbers = re.findall("\d+\.\d+", line)
        if len(numbers) > 0:
            if column_zero:
                for n in numbers:
                    x.append(float(Decimal(n) - 12))
            else:
                for n in numbers:
                    y.append(float(n)) 
            column_zero = not column_zero

for i in range(len(x)):
    print("                            " + str([x[i], y[i]]) + ",")