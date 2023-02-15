from main import Main
from main import initialize
from path_finding.Hamiltonian import Hamiltonian
from robot.robot import Robot
from Grid.grid import Grid
from Grid.obstacle import Obstacle
from Misc.positioning import Position
from Misc.direction import Direction

# tmp = [[50, 50, Direction.TOP], [90, 90, Direction.BOTTOM],
#        [40, 180, Direction.LEFT], [120, 150, Direction.RIGHT]]
# obstacles = []
# i = 0
# for x, y, direction in tmp:
#     position: Position = Position(x, y, direction)
#     obstacle: Obstacle = Obstacle(position, i)
#     i += 1
#     obstacles.append(obstacle)
#
# print("list of obstacles: ")
# print(obstacles)
# grid = Grid(obstacles)
# print("list of target positions")
# for x in grid.obstacles:
#     print(x.target_position)
# robot = Robot(grid)
# test = Hamiltonian(grid=grid, robot=robot)
# test.plan_path()

x = 'ALG:10,17,S,0;17,17,W,1;2,16,S,2;16,4,S,3;13,1,W,4;6,6,N,5;9,11,W,6;3,3,E,7;'.encode('utf-8')
initialize()
