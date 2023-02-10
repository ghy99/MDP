import constants as constants
from Misc.direction import Direction
from commands.command import Command
from Misc.positioning import Position


class StraightCommand(Command):
    def __init__(self, dist):
        """
        Specified distance is scaled. Do not divide the provided distance by the scaling factor!
        """
        # Calculate the time needed to travel the required distance.
        time = abs(dist / constants.ROBOT_SPEED_PER_SECOND)
        super().__init__(time)

        self.dist = dist

    def __str__(self):
        return f"StraightCommand(dist={self.dist / constants.SCALING_FACTOR}, {self.total_ticks} ticks)"

    __repr__ = __str__

    def process_one_tick(self, robot):
        """
        Used in the AlgoSimulator to update the pygame simulator in each time tick
        """
        if self.total_ticks == 0:
            return

        self.tick()  # -1 tick from total ticks
        distance = self.dist / self.total_ticks
        robot.straight(distance)  # to move distance in one tick

    def apply_on_pos(self, curr_pos: Position):
        """
        Apply this command onto a current Position object. Returns the end result position.
        """
        if curr_pos.direction == Direction.RIGHT:
            curr_pos.x += self.dist
        elif curr_pos.direction == Direction.TOP:
            curr_pos.y += self.dist
        elif curr_pos.direction == Direction.BOTTOM:
            curr_pos.y -= self.dist
        else:
            curr_pos.x -= self.dist

        return self

    def convert_to_message(self):
        """
        convention for message to rpi: XXX represents number of cm to traverse
        FFXXX
        RRXXX
        """
        # Check if forward or backward.
        if int(self.dist) < 0:
            comm = f"RR{-self.dist}"
            for x in range(0, 5-len(comm)):
                comm = comm + "_"
            return comm
        else:
            comm = f"FF{self.dist}"
            for x in range(0, 5-len(comm)):
                comm = comm + "_"
            return comm
