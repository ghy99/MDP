from path_finding.Hamiltonian import Hamiltonian
from robot.robot import Robot
from Grid.grid import Grid
from Grid.obstacle import Obstacle
from Misc.positioning import Position
from Misc.direction import Direction

tmp = [[30, 30, Direction.RIGHT], [60, 60, Direction.TOP],
       [90, 110, Direction.LEFT], [20, 160, Direction.BOTTOM],
       [100, 170, Direction.BOTTOM], [170, 170, Direction.LEFT],
       [160, 40, Direction.BOTTOM], [130, 10, Direction.LEFT]]

obstacles = []
i = 0
for x, y, direction in tmp:
    position: Position = Position(x, y, direction)
    obstacle: Obstacle = Obstacle(position, i)
    i += 1
    obstacles.append(obstacle)

# print("List of obstacles: ")
# print(obstacles)
grid = Grid(obstacles)
# print("List of target positions")

for x in grid.obstacles:
    print(x.target_position)

robot = Robot(grid)
test = Hamiltonian(grid=grid, robot=robot)
test.plan_path()
