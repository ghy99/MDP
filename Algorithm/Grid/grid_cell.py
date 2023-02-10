import pygame
import constants as constants
from Misc.positioning import Position


#
#
# class GridCell:
#     def __init__(self, x, y, occupied, direction=None):
#         """
#         x and y coordinates are in terms of the grid.
#         grid cell does not have direction, just getting direction as input to reuse the Position class
#         """
#         self.pos = Position(x, y, direction)
#         self.occupied = occupied
#
#     def __str__(self):
#         return f"Cell({self.pos})"
#
#     __repr__ = __str__
#
#     def __eq__(self, other):
#         return self.pos.xy_dir() == other.pos.xy_dir()
#
#     def __hash__(self):
#         return hash(self.pos.xy_dir())
#
#     def copy(self):
#         """
#         Return a copy of this grid cell.
#         """
#         return GridCell(self.pos.x, self.pos.y, self.occupied, self.pos.direction)
#
#     def draw_self(self, screen):
#         # if self.occupied:  # If current node is not permissible to the robot
#         #     rect = pygame.Rect(0, 0, constants.GRID_CELL_LENGTH, constants.GRID_CELL_LENGTH)
#         #     rect.center = self.pos.xy_pygame()
#         #     pygame.draw.rect(screen, constants.WHITE, rect)
#
#         if (0 <= self.pos.x <= 4 * constants.GRID_CELL_LENGTH) and (0 <= self.pos.y <= 4 * constants.GRID_CELL_LENGTH):
#             rect = pygame.Rect(self.pos.x, self.pos.y, constants.GRID_CELL_LENGTH, constants.GRID_CELL_LENGTH)
#             rect.center = self.pos.xy_pygame()
#             pygame.draw.rect(screen, constants.LIGHT_YELLOW, rect)
#
#
#     def draw_boundary(self, screen):
#         x_pygame, y_pygame = self.pos.xy_pygame()
#
#         left = x_pygame - constants.GRID_CELL_LENGTH // 2
#         right = x_pygame + constants.GRID_CELL_LENGTH // 2
#         top = y_pygame - constants.GRID_CELL_LENGTH // 2
#         bottom = y_pygame + constants.GRID_CELL_LENGTH // 2
#
#         # Draw
#         pygame.draw.line(screen, constants.PLATINUM, (left, top), (left, bottom))  # Left border
#         pygame.draw.line(screen, constants.PLATINUM, (left, top), (right, top))  # Top border
#         pygame.draw.line(screen, constants.PLATINUM, (right, top), (right, bottom))  # Right border
#         pygame.draw.line(screen, constants.PLATINUM, (left, bottom), (right, bottom))  # Bottom border
#
#     def draw(self, screen):
#         # Draw self
#         self.draw_self(screen)
#         # Draw node border
#         self.draw_boundary(screen)

class GridCell:
    def __init__(self, position, occupied):
        self.position = position
        self.occupied = occupied

    def __str__(self):
        return f"Cell({self.position})"

    __repr__ = __str__

    def __eq__(self, other):
        return self.position.x == other.position.x and self.position.y == other.position.y

    def __hash__(self):
        return hash(self.position.xy_dir())

    def copy(self):
        """
        Return a copy of this grid cell.
        """
        return GridCell(Position(self.position.x, self.position.y, self.position.direction), self.occupied)

    def draw_cell(self):
        pass

    def draw_boundary_of_cell(self):
        pass

    def draw_all(self):
        pass
