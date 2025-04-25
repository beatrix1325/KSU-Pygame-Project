# Code related to the run-time game state

import pygame
import random

STAGE_BLOCK_HEIGHT = 40
STAGE_BLOCK_WIDTH = 10

PHYSICS_STEP_EVENT = pygame.USEREVENT + 1
INPUT_STEP_EVENT = pygame.USEREVENT + 2

# Represents the various tetris blocks that may occur
class Tetromino:
    # All the rectangles needed to represent the space taken up by the block
    # If the block can be represented by one rectangle then the second rectangle will be size 0,0
    collision_box: list[pygame.Rect]
    # RGBA data to be displayed on TetrisBlock.position
    texture: pygame.Surface
    # Represents the location of where to render the texture
    position: tuple[int, int]

    # Stage width should be in block widths
    # A block width is just the width, in pixels, of a single given sub-block of a tetromino
    def __init__(self, block_width: int):
        self.position = (random.randint(0, 9) * block_width, 0)
        piece_type = random.randint(0, 6)
        if piece_type == 0:
            # O Tetromino - Yellow
            self.collision_box = [
                pygame.Rect(self.position[0], self.position[1], 2 * block_width, 2 * block_width),
                pygame.Rect(0, 0, 0, 0)
            ]
            self.texture = pygame.Surface((2 * block_width, 2 * block_width))
            self.texture.fill((255, 255, 0))  # Yellow
        elif piece_type == 1:
            # I Tetromino - Cyan
            self.collision_box = [
                pygame.Rect(self.position[0], self.position[1], 4 * block_width, block_width),
                pygame.Rect(0, 0, 0, 0)
            ]
            self.texture = pygame.Surface((4 * block_width, block_width))
            self.texture.fill((0, 255, 255))  # Cyan
        elif piece_type == 2:
            # T Tetromino - Purple
            self.collision_box = [
                pygame.Rect(self.position[0], self.position[1], 3 * block_width, block_width),
                pygame.Rect(self.position[0] + block_width, self.position[1] + block_width, block_width, block_width)
            ]
            self.texture = pygame.Surface((3 * block_width, 2 * block_width))
            self.texture.fill((128, 0, 128))  # Purple
        elif piece_type == 3:
            # J Tetromino - Blue
            self.collision_box = [
                pygame.Rect(self.position[0], self.position[1], block_width, 2 * block_width),
                pygame.Rect(self.position[0] + block_width, self.position[1] + block_width, 2 * block_width, block_width)
            ]
            self.texture = pygame.Surface((3 * block_width, 2 * block_width))
            self.texture.fill((0, 0, 255))  # Blue
        elif piece_type == 4:
            # L Tetromino - Orange
            self.collision_box = [
                pygame.Rect(self.position[0] + 2 * block_width, self.position[1], block_width, 2 * block_width),
                pygame.Rect(self.position[0], self.position[1] + block_width, 2 * block_width, block_width)
            ]
            self.texture = pygame.Surface((3 * block_width, 2 * block_width))
            self.texture.fill((255, 165, 0))  # Orange
        elif piece_type == 5:
            # S Tetromino - Green
            self.collision_box = [
                pygame.Rect(self.position[0] + block_width, self.position[1], 2 * block_width, block_width),
                pygame.Rect(self.position[0], self.position[1] + block_width, 2 * block_width, block_width)
            ]
            self.texture = pygame.Surface((3 * block_width, 2 * block_width))
            self.texture.fill((0, 255, 0))  # Green
        elif piece_type == 6:
            # Z Tetromino - Red
            self.collision_box = [
                pygame.Rect(self.position[0], self.position[1], 2 * block_width, block_width),
                pygame.Rect(self.position[0] + block_width, self.position[1] + block_width, 2 * block_width, block_width)
            ]
            self.texture = pygame.Surface((3 * block_width, 2 * block_width))
            self.texture.fill((255, 0, 0))  # Red

    def move(self, distance: tuple[int, int]):
        new_tetromino = self
        new_tetromino.position = (new_tetromino.position[0] + distance[0], new_tetromino.position[1] + distance[1])
        if new_tetromino.collision_box[1].size != (0, 0):
            new_tetromino.collision_box = [
                new_tetromino.collision_box[0].move(distance[0], distance[1]),
                new_tetromino.collision_box[1].move(distance[0], distance[1])
            ]
        else:
            new_tetromino.collision_box[0] = new_tetromino.collision_box[0].move(distance[0], distance[1])

        return new_tetromino

    def render(self, local_screen: pygame.Surface):
        local_screen.blit(self.texture, self.position)

    def rotate(self):
        if hasattr(self, 'texture') and self.texture:
            self.texture = pygame.transform.rotate(self.texture, 90)
            width, height = self.texture.get_size()
            self.collision_box[0] = pygame.Rect(self.position[0], self.position[1], width, height)
        return self

class GameState:
    game_surface: pygame.Surface
    # The "stage" is where blocks will fall and can move
    stage: pygame.Rect
    # The different blocks that have already been dropped
    stage_pieces: [Tetromino]
    # The currently falling block
    stage_drop: Tetromino
    # The 'floor' of the stage, used to prevent blocks from entering free-fall
    floor: pygame.Rect
    # Size, in pixels, of the blocks making up the stage
    block_size: int

    def __init__(self, dimensions: tuple[int, int], block_size: int):
        self.game_surface = pygame.Surface(dimensions)
        self.stage_pieces = []
        self.stage = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        self.block_size = block_size
        self.paused = False
        self.new_tetromino()
        self.floor = pygame.Rect(0, dimensions[1], dimensions[0], block_size)


    def render(self, local_screen: pygame.Surface):
        self.game_surface.fill((0, 0, 0))
        for tetromino in self.stage_pieces:
            tetromino.render(self.game_surface)
        self.game_surface.fill((0, 0, 0),
        pygame.Rect(0, 0, self.stage_width(), STAGE_BLOCK_HEIGHT / 2 * self.block_size))
        self.stage_drop.render(self.game_surface)
        pygame.draw.line(self.game_surface, (255, 255, 255), (300, 0), (300, self.stage.height))
        local_screen.blit(self.game_surface, self.stage)

    def new_tetromino(self):
        self.stage_drop = Tetromino(self.block_size)


    def step(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.stage_drop.rotate()
        if self.paused:
            return

        new_position = self.stage_drop.move((0, self.block_size))
        # Check if the new position of the dropped tetromino collides with anything
        stage_collisions = []
        for piece in self.stage_pieces:
            stage_collisions.append(piece.collision_box[0])
            stage_collisions.append(piece.collision_box[1])
        if (
                new_position.collision_box[0].collidelist(stage_collisions) != -1
        ) or (
                new_position.collision_box[1].collidelist(stage_collisions) != -1
        ) or self.floor.collidelist(new_position.collision_box) != -1:
            self.stage_pieces.append(self.stage_drop.move((0, -self.block_size)))
            self.new_tetromino()
        else:
            self.stage_drop = new_position

    def stage_width(self):
        return STAGE_BLOCK_WIDTH * self.block_size

    def stage_height(self):
        return STAGE_BLOCK_HEIGHT * self.block_size