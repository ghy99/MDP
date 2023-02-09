import math
from Algorithm.Misc.type_of_turn import TypeOfTurn
import Algorithm.constants as constants
from Algorithm.Misc.direction import Direction
from Algorithm.Misc.positioning import Position, RobotPosition
from Algorithm.commands.command import Command


class TurnCommand(Command):
    def __init__(self, type_of_turn, left, right, reverse):
        """
        Angle to turn and whether the turn is done in reverse or not. Note that this is in degrees.

        Note that negative angles will always result in the robot being rotated clockwise.
        """
        time = 0
        match type_of_turn:
            case TypeOfTurn.SMALL:
                time = 10  # SOME VALUE TO BE EMPIRICALLY DETERMINED
            case TypeOfTurn.MEDIUM:
                time = 20  # SOME VALUE TO BE EMPIRICALLY DETERMINED
            case TypeOfTurn.LARGE:
                time = 30  # SOME VALUE TO BE EMPIRICALLY DETERMINED

        super().__init__(time)
        self.type_of_turn = type_of_turn
        self.left = left
        self.right = right
        self.reverse = reverse

    def __str__(self):
        return f"TurnCommand:{self.type_of_turn}, {self.total_ticks} ticks, rev={self.reverse}, left={self.left}, \
        right= {self.right}) "

    __repr__ = __str__

    def process_one_tick(self, robot):
        if self.total_ticks == 0:
            return

        self.tick()
        robot.turn(self.type_of_turn, self.left, self.right, self.reverse)

    def apply_on_pos(self, curr_pos: Position):
        """
        changes the robot position according to what command it is and where the robot is currently at
        """
        assert isinstance(curr_pos, RobotPosition), print("Cannot apply turn command on non-robot positions!")

        # Get change in (x, y) coordinate.

        # turn left and forward
        if self.left and not self.right and not self.reverse:
            if self.type_of_turn == TypeOfTurn.SMALL:
                match curr_pos.direction:
                    case Direction.TOP:
                        curr_pos.x -= 10
                        curr_pos.y += 40
                    case Direction.LEFT:
                        curr_pos.x -= 40
                        curr_pos.y -= 10
                    case Direction.RIGHT:
                        curr_pos.x += 40
                        curr_pos.y += 10
                    case Direction.BOTTOM:
                        curr_pos.x += 10
                        curr_pos.y -= 40
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                match curr_pos.direction:
                    case Direction.TOP:
                        curr_pos.x -= 40
                        curr_pos.y += 30
                        curr_pos.direction = Direction.LEFT
                    case Direction.LEFT:
                        curr_pos.x -= 30
                        curr_pos.y -= 40
                        curr_pos.direction = Direction.BOTTOM
                    case Direction.RIGHT:
                        curr_pos.x += 30
                        curr_pos.y += 40
                        curr_pos.direction = Direction.TOP
                    case Direction.BOTTOM:
                        curr_pos.x += 40
                        curr_pos.y -= 30
                        curr_pos.direction = Direction.RIGHT
            # else:
            #     match curr_pos.direction:
            #         case Direction.TOP:
            #             curr_pos.x -= 30  # TO CHANGE ARBITRARY VALUE
            #             curr_pos.y += 30  # TO CHANGE ARBITRARY VALUE
            #             curr_pos.direction = Direction.LEFT
            #         case Direction.LEFT:
            #             curr_pos.x -= 30
            #             curr_pos.y -= 30
            #             curr_pos.direction = Direction.BOTTOM
            #         case Direction.RIGHT:
            #             curr_pos.x += 30
            #             curr_pos.y += 30
            #             curr_pos.direction = Direction.TOP
            #         case Direction.BOTTOM:
            #             curr_pos.x += 30
            #             curr_pos.y -= 30
            #             curr_pos.direction = Direction.RIGHT
        # turn right and forward
        if self.right and not self.left and not self.reverse:
            if self.type_of_turn == TypeOfTurn.SMALL:
                match curr_pos.direction:
                    case Direction.TOP:
                        curr_pos.x += 10
                        curr_pos.y += 40
                    case Direction.LEFT:
                        curr_pos.x -= 40
                        curr_pos.y += 10
                    case Direction.RIGHT:
                        curr_pos.x += 40
                        curr_pos.y -= 10
                    case Direction.BOTTOM:
                        curr_pos.x -= 10
                        curr_pos.y -= 40
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                match curr_pos.direction:
                    case Direction.TOP:
                        curr_pos.x += 50
                        curr_pos.y += 30
                        curr_pos.direction = Direction.RIGHT
                    case Direction.LEFT:
                        curr_pos.x -= 30
                        curr_pos.y += 50
                        curr_pos.direction = Direction.TOP
                    case Direction.RIGHT:
                        curr_pos.x += 30
                        curr_pos.y -= 50
                        curr_pos.direction = Direction.BOTTOM
                    case Direction.BOTTOM:
                        curr_pos.x -= 50
                        curr_pos.y -= 30
                        curr_pos.direction = Direction.LEFT
            # else:
            #     match curr_pos.direction:
            #         case Direction.TOP:
            #             curr_pos.x += 30  # TO CHANGE ARBITRARY VALUE
            #             curr_pos.y += 30  # TO CHANGE ARBITRARY VALUE
            #             curr_pos.direction = Direction.RIGHT
            #         case Direction.LEFT:
            #             curr_pos.x -= 30
            #             curr_pos.y += 30
            #             curr_pos.direction = Direction.TOP
            #         case Direction.RIGHT:
            #             curr_pos.x += 30
            #             curr_pos.y -= 30
            #             curr_pos.direction = Direction.BOTTOM
            #         case Direction.BOTTOM:
            #             curr_pos.x -= 30
            #             curr_pos.y -= 30
            #             curr_pos.direction = Direction.LEFT
        # turn front wheels left and reverse
        if self.left and not self.right and self.reverse:
            if self.type_of_turn == TypeOfTurn.SMALL:
                match curr_pos.direction:
                    case Direction.TOP:
                        curr_pos.x -= 10  # TO CHANGE ARBITRARY VALUE
                        curr_pos.y -= 40  # TO CHANGE ARBITRARY VALUE
                    case Direction.LEFT:
                        curr_pos.x += 40
                        curr_pos.y -= 10
                    case Direction.RIGHT:
                        curr_pos.x -= 40
                        curr_pos.y += 10
                    case Direction.BOTTOM:
                        curr_pos.x += 10
                        curr_pos.y += 40
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                match curr_pos.direction:
                    case Direction.TOP:
                        curr_pos.x -= 40
                        curr_pos.y -= 30
                        curr_pos.direction = Direction.RIGHT
                    case Direction.LEFT:
                        curr_pos.x += 30
                        curr_pos.y -= 40
                        curr_pos.direction = Direction.TOP
                    case Direction.RIGHT:
                        curr_pos.x -= 30
                        curr_pos.y += 40
                        curr_pos.direction = Direction.BOTTOM
                    case Direction.BOTTOM:
                        curr_pos.x += 40
                        curr_pos.y += 30
                        curr_pos.direction = Direction.LEFT
            # else:
            #     match curr_pos.direction:
            #         case Direction.TOP:
            #             curr_pos.x -= 30  # TO CHANGE ARBITRARY VALUE
            #             curr_pos.y -= 30  # TO CHANGE ARBITRARY VALUE
            #             curr_pos.direction = Direction.RIGHT
            #         case Direction.LEFT:
            #             curr_pos.x += 30
            #             curr_pos.y -= 30
            #             curr_pos.direction = Direction.TOP
            #         case Direction.RIGHT:
            #             curr_pos.x -= 30
            #             curr_pos.y += 30
            #             curr_pos.direction = Direction.BOTTOM
            #         case Direction.BOTTOM:
            #             curr_pos.x += 30
            #             curr_pos.y += 30
            #             curr_pos.direction = Direction.LEFT
        # turn front wheels right and reverse
        if self.right and not self.left and self.reverse:
            if self.type_of_turn == TypeOfTurn.SMALL:
                match curr_pos.direction:
                    case Direction.TOP:
                        curr_pos.x += 10
                        curr_pos.y -= 40
                    case Direction.LEFT:
                        curr_pos.x += 40
                        curr_pos.y += 10
                    case Direction.RIGHT:
                        curr_pos.x -= 40
                        curr_pos.y -= 10
                    case Direction.BOTTOM:
                        curr_pos.x -= 10
                        curr_pos.y += 40
            elif self.type_of_turn == TypeOfTurn.MEDIUM:
                match curr_pos.direction:
                    case Direction.TOP:
                        curr_pos.x += 10
                        curr_pos.y -= 40
                        curr_pos.direction = Direction.LEFT
                    case Direction.LEFT:
                        curr_pos.x += 40
                        curr_pos.y += 10
                        curr_pos.direction = Direction.BOTTOM
                    case Direction.RIGHT:
                        curr_pos.x -= 40
                        curr_pos.y -= 10
                        curr_pos.direction = Direction.TOP
                    case Direction.BOTTOM:
                        curr_pos.x -= 10
                        curr_pos.y += 40
                        curr_pos.direction = Direction.RIGHT
            # else:
            #     match curr_pos.direction:
            #         case Direction.TOP:
            #             curr_pos.x += 30  # TO CHANGE ARBITRARY VALUE
            #             curr_pos.y -= 30  # TO CHANGE ARBITRARY VALUE
            #             curr_pos.direction = Direction.LEFT
            #         case Direction.LEFT:
            #             curr_pos.x += 30
            #             curr_pos.y += 30
            #             curr_pos.direction = Direction.BOTTOM
            #         case Direction.RIGHT:
            #             curr_pos.x -= 30
            #             curr_pos.y -= 30
            #             curr_pos.direction = Direction.TOP
            #         case Direction.BOTTOM:
            #             curr_pos.x -= 30
            #             curr_pos.y += 30
            #             curr_pos.direction = Direction.RIGHT
        return self

    def convert_to_message(self):
        if self.left and not self.right and not self.reverse:
            # This is going forward left.
            match self.type_of_turn:
                case TypeOfTurn.SMALL:
                    return "TLSF_"  # turn left small forward!
                case TypeOfTurn.MEDIUM:
                    return "TLMF_"  # turn left medium forward!
                case TypeOfTurn.LARGE:
                    return "TLLF_"  # turn left large forward!
        elif self.left and not self.right and self.reverse:
            # This is going backward and front wheels are turned to left
            match self.type_of_turn:
                case TypeOfTurn.SMALL:
                    return "TLSR_"  # turn left small reverse!
                case TypeOfTurn.MEDIUM:
                    return "TLMR_"  # turn left medium reverse!
                case TypeOfTurn.LARGE:
                    return "TLLR_"  # turn left large reverse!
        elif self.right and not self.left and not self.reverse:
            # This is going forward right.
            match self.type_of_turn:
                case TypeOfTurn.SMALL:
                    return "TRSF_"  # turn right small forward!
                case TypeOfTurn.MEDIUM:
                    return "TRMF_"  # turn right medium forward!
                case TypeOfTurn.LARGE:
                    return "TRLF_"  # turn right large forward!
        else:
            # This is going backward and the front wheels turned to the right.
            match self.type_of_turn:
                case TypeOfTurn.SMALL:
                    return "TRSR_"  # turn right small reverse!
                case TypeOfTurn.MEDIUM:
                    return "TRMR_"  # turn right medium reverse!
                case TypeOfTurn.LARGE:
                    return "TRLR_"  # turn right large reverse!
