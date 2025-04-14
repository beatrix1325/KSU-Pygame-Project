# Imports
import sys, pygame, GameState

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 500, 600
screen = pygame.display.set_mode((width, height))

title_image = pygame.image.load('assets/tetris.png')
title_image = pygame.transform.scale(title_image, (300, 100))  # optional
title_rect = title_image.get_rect(center=(width // 2, 130))


font = pygame.font.Font('assets/modern-tetris.ttf', 40)

objects = []


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#000000',
            'hover': '#9e9e9e',
            'pressed': '#ffffff',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

def startButtonPressed():
    global title_screen
    global fpsClock
    title_screen = False
    pygame.time.set_timer(GameState.PHYSICS_STEP_EVENT, 1000)

def exitButtonPressed():
    global running
    running = False

startButton = Button(150, 195, 200, 100, 'Start', startButtonPressed)
exitButton = Button(150, 305, 200, 100, 'Exit', exitButtonPressed)

# Stores whether we are rendering the title screen
title_screen = True

running = True

game_state = GameState.GameState((width - 100, height - 100))

# Game loop.
while running:
    screen.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == GameState.PHYSICS_STEP_EVENT:
            game_state.step()
            pygame.time.set_timer(GameState.PHYSICS_STEP_EVENT, 250)

    if title_screen:
        screen.blit(title_image, title_rect)
        for object in objects:
            object.process()
    else:
        game_state.render(screen)

    pygame.display.flip()
    fpsClock.tick(fps)