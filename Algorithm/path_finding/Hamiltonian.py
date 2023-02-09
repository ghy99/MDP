import itertools
import math
from collections import deque
from typing import Tuple

import Algorithm.constants as constants
from Algorithm.Grid.grid import Grid
from Algorithm.commands.scan_obstacle_command import ScanCommand
from Algorithm.commands.go_straight_command import StraightCommand
from Algorithm.Misc.direction import Direction
from Algorithm.Grid.obstacle import Obstacle
from Algorithm.path_finding.modified_astar import ModifiedAStar
from Algorithm.robot.robot import Robot


class Hamiltonian:
    def __init__(self, robot: Robot, grid: Grid):
        self.robot = robot
        self.grid = grid

        # Compute the simple Hamiltonian path for all obstacles
        self.simple_hamiltonian = tuple()

        # Create all the commands required to finish the course.
        self.commands = deque()

    def get_simple_hamiltonian(self):
        return self.simple_hamiltonian

    def compute_simple_hamiltonian_path(self) -> Tuple[Obstacle]:
        """
        Get the Hamiltonian Path to all points with the best possible effort.
        This is a simple calculation where we assume that we travel directly to the next obstacle.
        """
        # Generate all possible permutations for the image obstacles
        perms = list(itertools.permutations(self.grid.obstacles))

        # Get the path that has the least distance travelled.
        def calc_distance(path):
            def weight_factor(source_dir: Direction, dest_dir: Direction) -> int:
                # Right Grid to Left Grid, Top of Grid to Bottom of Grid unlikely
                # if same direction (robot and targeted position has same direction)
                if source_dir.value - dest_dir.value == 0:
                    weight = 1
                # if opposite direction
                elif source_dir.value - dest_dir.value == -180 or source_dir.value - dest_dir.value == 180:
                    weight = 1.8
                # if turn right or left
                else:
                    weight = 1.2

                return weight

            # Create all target points, including the start.
            targets = [self.robot.pos.xy()]
            # Try out all the different permutations
            for obstacle in path:
                targets.append(obstacle.target_pos.xy())

            dist = 0
            multiplier = 1
            for i in range(len(targets)-1):
                # Weight factor
                multiplier = weight_factor(path[i].target_pos.get_dir(), path[i+1].target_pos.get_dir())
                dist += multiplier * math.sqrt(((targets[i][0] - targets[i + 1][0]) ** 2) +
                                               ((targets[i][1] - targets[i + 1][1]) ** 2))

            print("Path = ", targets, "\nTotal weighted Euclidean distance = ", dist)
            return dist

        print("Calculating Distance for all possible permutation\n")
        # Change to max to show paths change
        # simple now holds the permutation that gives the lowest distance
        simple = min(perms, key=calc_distance)
        print("\nFound a simple hamiltonian path: ")
        # print out every obstacle in order of visitation
        for ob in simple:
            print(f"\t{ob}")
        print()
        print("Found Shortest Hamiltonian Path")
        calc_distance(simple)
        # returns order of visitation of obstacles (the lowest cost)
        return simple

    def compress_paths(self):
        """
        Compress similar commands into one command.
        Compressing many straight line commands into one.
        Helps to reduce the number of commands.
        """
        print("Compressing commands... ", end="")
        index = 0
        new_commands = deque()
        while index < len(self.commands):
            command = self.commands[index]
            if isinstance(command, StraightCommand):
                new_length = 0
                while index < len(self.commands) and isinstance(self.commands[index], StraightCommand):
                    new_length += self.commands[index].dist
                    index += 1
                command = StraightCommand(new_length)
                new_commands.append(command)
            else:
                new_commands.append(command)
                index += 1
        self.commands = new_commands
        print("Done!")

    def plan_path(self):
        print("-" * 40)
        print("STARTING PATH COMPUTATION...")
        self.simple_hamiltonian = self.compute_simple_hamiltonian_path()
        print()

        curr = self.robot.pos.copy()  # We use a copy rather than get a reference.
        for obstacle in self.simple_hamiltonian:
            target = obstacle.get_robot_target_pos()
            print(f"Planning {curr} to {target}")
            res = ModifiedAStar(self.grid, self, curr, target).start_astar()
            if res is None:
                print(f"\tNo path found from {curr} to {obstacle}")
            else:
                print("\tPath found.")
                curr = res
                self.commands.append(ScanCommand(constants.ROBOT_SCAN_TIME, obstacle.index))

        self.compress_paths()
        print("-" * 40)