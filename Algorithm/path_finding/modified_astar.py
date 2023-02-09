import math
from queue import PriorityQueue
from typing import List, Tuple

import Algorithm.constants as constants
from Algorithm.Misc.type_of_turn import TypeOfTurn
from Algorithm.commands.command import Command
from Algorithm.commands.go_straight_command import StraightCommand
from Algorithm.commands.turn_command import TurnCommand
from Algorithm.Grid.grid import Grid
from Algorithm.Grid.grid_cell import GridCell
from Algorithm.Misc.positioning import RobotPosition


class ModifiedAStar:
    def __init__(self, grid, brain, start: RobotPosition, end: RobotPosition):
        # We use a copy of the grid rather than use a reference
        # to the exact grid.
        self.grid: Grid = grid.copy()
        self.brain = brain  # the hamiltonian object

        self.start = start
        self.end = end

    def get_neighbours(self, pos: RobotPosition) -> List[Tuple[GridCell, RobotPosition, int, Command]]:
        """
        Get movement neighbours from this position.

        Note that all values in the Position object (x, y, direction) are all with respect to the grid!

        We also expect the return Positions to be with respect to the grid.
        """
        # We assume the robot will move by 10 when travelling straight, while moving a fixed x and y value when turning
        # a fix distance of 10 when travelling straight.
        neighbours = []

        # Check travel straights.
        straight_dist = 10
        straight_commands = [
            StraightCommand(straight_dist),
            StraightCommand(-straight_dist)
        ]
        for command in straight_commands:
            # Check if doing this command does not bring us to any invalid position.
            after, p = self.check_valid_command(command, pos)
            if after:
                neighbours.append((after, p, straight_dist, command))

        # Check turns
        turn_penalty = 40  # SOME HEURISTIC VALUE (need to account for turns travelling more also!)
        turn_commands = [  # type of turn, Left, Right, Reverse
            TurnCommand(TypeOfTurn.SMALL, True, False, False),  # L SMALL turn, forward
            TurnCommand(TypeOfTurn.MEDIUM, True, False, False),  # L MEDIUM turn, forward
            # TurnCommand(TypeOfTurn.LARGE, True, False, False),  # L LARGE turn, forward
            TurnCommand(TypeOfTurn.SMALL, True, False, True),  # L SMALL turn, reverse
            TurnCommand(TypeOfTurn.MEDIUM, True, False, True),  # L MEDIUM turn, reverse
            # TurnCommand(TypeOfTurn.LARGE, True, False, True),  # L LARGE turn, reverse
            TurnCommand(TypeOfTurn.SMALL, False, True, False),  # R SMALL turn, forward
            TurnCommand(TypeOfTurn.MEDIUM, False, True, False),  # R MEDIUM turn, forward
            # TurnCommand(TypeOfTurn.LARGE, False, True, False),  # R LARGE turn, forward
            TurnCommand(TypeOfTurn.SMALL, False, True, True),  # R SMALL turn, reverse
            TurnCommand(TypeOfTurn.MEDIUM, False, True, True),  # R MEDIUM turn, reverse
            # TurnCommand(TypeOfTurn.LARGE, False, True, True),  # R LARGE turn, reverse
        ]
        for c in turn_commands:
            # Check if doing this command does not bring us to any invalid position.
            after, p = self.check_valid_command(c, pos)
            if after:
                neighbours.append((after, p, turn_penalty, c))
        print(neighbours)
        return neighbours

    def check_valid_command(self, command: Command, p: RobotPosition):
        """
        Checks if a command will bring a point into any invalid position.

        If invalid, we return None for both the resulting grid location and the resulting position.
        """
        # Check specifically for validity of turn command. Robot should not exceed the grid or hit the obstacles
        p = p.copy()
        if isinstance(command, TurnCommand):
            p_c = p.copy()
            command.apply_on_pos(p_c)
            # make sure that the final position is a valid one
            if not (self.grid.check_valid_position(p_c) and self.grid.get_grid_cell_corresponding_to_coordinate(
                    *p_c.xy())):
                return None, None
            diff_in_x = p_c.x - p.x  # if positive means the new position is to the right, else to the left side
            diff_in_y = p_c.y - p.y  # if positive means the new position is on top of old position, else otherwise
            for x in range(1, diff_in_x):
                temp = p_c.copy()
                if diff_in_x < 0:
                    temp.x -= x
                else:
                    temp.x += x
                if not (self.grid.check_valid_position(temp) and self.grid.get_grid_cell_corresponding_to_coordinate(
                        *temp.xy())):
                    return None, None
            for y in range(1, diff_in_y):
                temp = p.copy()
                temp.x = p_c.x
                if diff_in_y < 0:
                    temp.y -= y
                else:
                    temp.y += y
                if not (self.grid.check_valid_position(temp) and self.grid.get_grid_cell_corresponding_to_coordinate(
                        *temp.xy())):
                    return None, None

        command.apply_on_pos(p)
        if self.grid.check_valid_position(p) and (
                after := self.grid.get_grid_cell_corresponding_to_coordinate(*p.xy())):
            after.pos.direction = p.direction
            return after.copy(), p
        return None, None

    def distance_heuristic(self, curr_pos: RobotPosition):
        """
        Measure the difference in distance between the provided position and the
        end position.
        """
        dx = abs(curr_pos.x - self.end.x)
        dy = abs(curr_pos.y - self.end.y)
        return math.sqrt(dx ** 2 + dy ** 2)

    def direction_heuristic(self, curr_pos: RobotPosition):
        """
        If not same direction as my target end position, incur penalty!
        """
        if self.end.direction == curr_pos.direction:
            return -10
        else:
            return 0

    def start_astar(self):
        frontier = PriorityQueue()  # Store frontier nodes to travel to.
        backtrack = dict()  # Store the sequence of grid cells being travelled.
        cost = dict()  # Store the cost to travel from start to a target grid cell.

        # We can check what the goal grid cell is
        goal_node = self.grid.get_grid_cell_corresponding_to_coordinate(*self.end.xy()).copy()  # Take note of copy!
        goal_node.pos.direction = self.end.direction  # Set the required direction at this grid cell.

        # Add starting node set into the frontier.
        start_node: GridCell = self.grid.get_grid_cell_corresponding_to_coordinate(
            *self.start.xy()).copy()  # Take note of copy!
        start_node.direction = self.start.direction  # Know which direction the robot is facing.

        offset = 0  # Used to tie-break.(?)
        frontier.put((0, offset, (start_node, self.start)))  # Extra time parameter to tie-break same priority.
        cost[start_node] = 0
        # Having None as the parent means this key is the starting node.
        backtrack[start_node] = (None, None)  # Parent, Command

        while not frontier.empty():  # While there are still nodes to process.
            # Get the highest priority node.
            priority, _, (current_node, current_position) = frontier.get()
            # If the current node is our goal.
            if current_node == goal_node:
                # Get the commands needed to get to destination.
                self.extract_commands(backtrack, goal_node)
                return current_position

            # Otherwise, we check through all possible locations that we can
            # travel to from this node.
            for new_node, new_pos, weight, c in self.get_neighbours(current_position):
                new_cost = cost.get(current_node) + weight  # weight here stands for cost of moving forward or turning

                if new_node not in backtrack or new_cost < cost[new_node]:
                    offset += 1
                    priority = new_cost + self.distance_heuristic(new_pos) + self.direction_heuristic(new_pos)

                    frontier.put((priority, offset, (new_node, new_pos)))
                    backtrack[new_node] = (current_node, c)
                    cost[new_node] = new_cost
        # If we are here, means that there was no path that we could find.
        # We return None to show that we cannot find a path.
        return None

    def extract_commands(self, backtrack, goal_node):
        """
        Extract required commands to get to destination.
        """
        commands = []
        curr = goal_node
        while curr:
            curr, c = backtrack.get(curr, (None, None))
            if c:
                commands.append(c)
        commands.reverse()
        self.brain.commands.extend(commands)
