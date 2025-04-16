# Imports
import sys, pygame

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

def fade_out_screen(fade_time_ms):
    surface = pygame.Surface((width, height))
    surface.fill((0, 0, 0))
    step = 5
    alpha_values = range(0, 256, step)
    steps = len(list(alpha_values))
    delay_per_step = fade_time_ms / steps if steps else 0
    for alpha in alpha_values:
        surface.set_alpha(alpha)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(delay_per_step))

def startGame():
    old_vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(0.3)     # lower the background music
    s = pygame.mixer.Sound('assets/music/winning-game-sound-effect.wav')
    s.play()
    duration_ms = int(s.get_length() * 1000)
    fade_out_screen(duration_ms)
    pygame.mixer.music.set_volume(old_vol)
    import main
    main.run()
def startButtonPressed():
    global title_screen
    global fpsClock
    title_screen = False
    pygame.time.set_timer(GameState.PHYSICS_STEP_EVENT, 100)

def exitButtonPressed():
    global running
    running = False

def openSettings():
    old_vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(0.3)
    s = pygame.mixer.Sound('assets/music/menu-button-89141.mp3')
    s.play()
    duration_ms = int(s.get_length() * 1000)
    fade_out_screen(duration_ms)
    pygame.mixer.music.set_volume(old_vol)
    import settings
    settings.run()

def quitGame():
    old_vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(0.3)
    s = pygame.mixer.Sound('assets/music/game-over-arcade-6435.mp3')
    s.play()
    duration_ms = int(s.get_length() * 1000)
    fade_out_screen(duration_ms)
    pygame.mixer.music.set_volume(old_vol)
    pygame.quit()
    sys.exit()

startButton = Button(150, 195, 200, 100, 'Start', startButtonPressed)
exitButton = Button(150, 305, 200, 100, 'Exit', exitButtonPressed)
settingsButton = Button(125, 305, 250, 100, 'SETTINGS', openSettings)
# Stores whether we are rendering the title screen
title_screen = True
running = True

game_state = GameState.GameState((width, height), 10)

# Game loop.
while running:
    screen.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == GameState.PHYSICS_STEP_EVENT:
            game_state.step()
            pygame.time.set_timer(GameState.PHYSICS_STEP_EVENT, 100)

    if title_screen:
        screen.blit(title_image, title_rect)
        for object in objects:
            object.process()
    else:
        game_state.render(screen)

    pygame.display.flip()
    fpsClock.tick(fps)