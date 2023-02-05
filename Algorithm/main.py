import astarclass
from grid import Grid
from simulation import Simulation
'''
Example obstacle input
6
5 5 N
7 9 E
15 5 S
4 17 W
20 20 S
1 20 N

6
7 3 S
12 4 W
10 10 E
2 12 N
19 19 W
8 15 W

6
10 1 N
17 3 N
13 15 E
4 18 S
20 20 W
10 10 W

6
6 1 N
1 6 E
8 8 W
14 2 E
10 20 W
18 13 S
'''

if __name__ == "__main__":
    # grid, obstacles = initGrid()
    # runAlgo(grid, obstacles)
    sim = Simulation()
    sim.runSimulation()    