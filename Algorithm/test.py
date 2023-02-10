from path_finding.Hamiltonian import Hamiltonian
from robot.robot import Robot
from Grid.grid import Grid
from Grid.obstacle import Obstacle
from Misc.positioning import Position
from Misc.direction import Direction

tmp = [[50, 50, Direction.TOP], [90, 90, Direction.BOTTOM],
       [40, 180, Direction.LEFT], [120, 150, Direction.RIGHT]]
obstacles = []
i = 0
for x, y, direction in tmp:
    position: Position = Position(x, y, direction)
    obstacle: Obstacle = Obstacle(position, i)
    i += 1
    obstacles.append(obstacle)

grid = Grid(obstacles)
robot = Robot(grid)
test = Hamiltonian(grid=grid, robot=robot)
test.plan_path()
