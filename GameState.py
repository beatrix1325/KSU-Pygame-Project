# Code related to the run-time game state
import pygame
import sys
import random

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE
}

# Tetromino colors (RGB)
COLORS = {
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
    'J': (0, 0, 255),
    'L': (255, 127, 0),
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'T': (128, 0, 128)
}

STAGE_BLOCK_HEIGHT = 20
STAGE_BLOCK_WIDTH = 10
COLS = STAGE_BLOCK_WIDTH
ROWS = STAGE_BLOCK_HEIGHT


PHYSICS_STEP_EVENT = pygame.USEREVENT + 1
INPUT_STEP_EVENT = pygame.USEREVENT + 2

# Convert PIECES templates to grid offsets for each rotation
TETROMINOES = {}
for key, rotations in PIECES.items():
    states = []
    for tmpl in rotations:
        cells = []
        for y, row in enumerate(tmpl):
            for x, ch in enumerate(row):
                if ch == 'O':
                    cells.append((x, y))
        states.append(cells)
    TETROMINOES[key] = states

class Tetromino:
    def __init__(self, block_size: int):
        self.block_size = block_size
        self.kind = random.choice(list(TETROMINOES.keys()))
        self.states = TETROMINOES[self.kind]
        self.rot = 0
        # Start above the top center
        self.x = COLS // 2 - TEMPLATEWIDTH // 2
        self.y = -TEMPLATEHEIGHT

    def cells(self) -> list[tuple[int,int]]:
        return [(self.x + dx, self.y + dy) for dx, dy in self.states[self.rot]]

    def move(self, dx: int, dy: int, board: list[list[int]]) -> bool:
        old_x, old_y = self.x, self.y
        self.x += dx; self.y += dy
        for cx, cy in self.cells():
            if cx < 0 or cx >= COLS or cy >= ROWS or (cy >= 0 and board[cy][cx]):
                self.x, self.y = old_x, old_y
                return False
        return True

    def rotate(self, board: list[list[int]]):
        old = self.rot
        self.rot = (self.rot + 1) % len(self.states)
        # revert if invalid
        for cx, cy in self.cells():
            if cx < 0 or cx >= COLS or cy >= ROWS or (cy >= 0 and board[cy][cx]):
                self.rot = old
                break

    def render(self, surf: pygame.Surface):
        for cx, cy in self.cells():
            if cy >= 0:
                r = pygame.Rect(cx*self.block_size, cy*self.block_size,
                                self.block_size, self.block_size)
                pygame.draw.rect(surf, COLORS[self.kind], r)
                pygame.draw.rect(surf, (30,30,30), r, 1)

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
        # initialize empty board grid: 0 = empty, nonzero = filled
        self.board = [[0 for _ in range(STAGE_BLOCK_WIDTH)] for _ in range(STAGE_BLOCK_HEIGHT)]
        self.stage_pieces = []
        self.stage = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        self.block_size = block_size
        self.paused = False
        self.score = 0
        self.level = 1
        self.new_tetromino()
        self.game_over = False
        # gravity timing
        self.drop_timer = 0
        self.drop_interval = 500  # ms between automatic drops
        self.floor = pygame.Rect(0, dimensions[1], dimensions[0], block_size)
        self.score_level_font = pygame.font.Font('assets/fonts/tetris-2-bombliss.otf', 10)


    def render(self, local_screen: pygame.Surface):
        self.game_surface.fill((0, 0, 0))
        for tetromino in self.stage_pieces:
            tetromino.render(self.game_surface)
        self.game_surface.fill((0, 0, 0),
        pygame.Rect(0, 0, self.stage_width(), STAGE_BLOCK_HEIGHT / 2 * self.block_size))
        self.stage_drop.render(self.game_surface)
        pygame.draw.line(self.game_surface, (255, 255, 255), (300, 0), (300, self.stage.height))
        score_text = self.score_level_font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.score_level_font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.game_surface.blit(score_text, (310, 50))
        self.game_surface.blit(level_text, (310, 100))
        local_screen.blit(self.game_surface, self.stage)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.stage_drop.move(-1, 0, self.board)
            elif event.key == pygame.K_RIGHT:
                self.stage_drop.move(1, 0, self.board)
            elif event.key == pygame.K_DOWN:
                self.stage_drop.move(0, 1, self.board)
            elif event.key == pygame.K_UP:
                self.stage_drop.rotate(self.board)
            elif event.key == pygame.K_SPACE:
                while self.stage_drop.move(0, 1, self.board):
                    pass


    def run(self):
        running = True
        while running:
            dt = pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)

            self.update(dt)
            self.render(self.game_surface)
            pygame.display.get_surface().blit(self.game_surface, (0, 0))
            pygame.display.flip()

            if self.game_over:
                running = False

    def new_tetromino(self):
        self.stage_drop = Tetromino(self.block_size)


    def step(self, dt):
        if self.paused:
            return
        # accumulate time and only drop every drop_interval ms
        self.drop_timer += dt
        if self.drop_timer < self.drop_interval:
            return
        self.drop_timer = 0

        # attempt to move down one block
        moved = self.stage_drop.move(0, 1, self.board)
        # collect rectangles of all placed pieces
        stage_rects = [
            (cx, cy) for piece in self.stage_pieces
            for cx, cy in piece.cells()
        ]
        # detect collision with existing pieces
        collided = False
        if moved:
            for cx, cy in self.stage_drop.cells():
                if (cx, cy) in stage_rects:
                    collided = True
                    break
        # lock if hit wall/floor (move failed) or landed on a piece
        if not moved or collided:
            # if collided after moving, revert that last drop
            if moved and collided:
                self.stage_drop.move(0, -1, self.board)
            # add piece cells to board
            for cx, cy in self.stage_drop.cells():
                if 0 <= cy < ROWS and 0 <= cx < COLS:
                    self.board[cy][cx] = 1
            self.stage_pieces.append(self.stage_drop)
            self.score += 100
            if len(self.stage_pieces) % 5 == 0:
                self.level += 1
            self.new_tetromino()

    def update(self, dt):
        """Alias for step to match run() call."""
        self.step(dt)

    def stage_width(self):
        return STAGE_BLOCK_WIDTH * self.block_size

    def stage_height(self):
        return STAGE_BLOCK_HEIGHT * self.block_size