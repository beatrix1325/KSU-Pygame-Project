import sys, pygame

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 500, 600
screen = pygame.display.set_mode((width, height))

pygame.mixer.music.load('assets/music/video-game-sounds_120bpm.wav')
pygame.mixer.music.play(-1)

title_image = pygame.image.load('assets/img/tetris.png')
title_image = pygame.transform.scale(title_image, (300, 100))  # optional
title_rect = title_image.get_rect(center=(width // 2, 130))


font = pygame.font.Font('assets/fonts/modern-tetris.ttf', 30)

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


customButton = Button(125, 195, 250, 100, 'START', startGame)
customButton = Button(125, 415, 250, 100, 'EXIT', quitGame)
customButton = Button(125, 305, 250, 100, 'SETTINGS', openSettings)

# Game loop.
while True:
    screen.fill((0, 0, 0))

    screen.blit(title_image, title_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for object in objects:
        object.process()

    pygame.display.flip()
    fpsClock.tick(fps)