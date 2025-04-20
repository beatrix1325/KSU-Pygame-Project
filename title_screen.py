# Imports
import sys, pygame, GameState

# Configuration
pygame.init()
pygame.mixer.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 500, 600
screen = pygame.display.set_mode((width, height))

pygame.mixer.music.load('assets/music/video-game-sounds_120bpm.wav')
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

title_image = pygame.image.load('assets/img/tetris.png')
title_image = pygame.transform.scale(title_image, (300, 100))  # optional
title_rect = title_image.get_rect(center=(width // 2, 130))

font = pygame.font.Font('assets/fonts/modern-tetris.ttf', 40)
small_font = pygame.font.Font('assets/fonts/modern-tetris.ttf', 20)
ctrl_font = pygame.font.SysFont(None, 24)
header_font = pygame.font.Font('assets/fonts/modern-tetris.ttf', 40)

objects = []

class Button:
    def __init__(self, x, y, w, h, text, onclick=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.onclick = onclick
        self.color_normal = (0, 0, 0)
        self.color_hover = (158, 158, 158)
        self.color_press = (255, 255, 255)
        self.current_color = self.color_normal
        self.text_surf = font.render(self.text, True, (255, 255, 255))

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        lines = self.text.split('\n')
        font_to_use = small_font if len(lines) > 1 else font
        line_height = font_to_use.get_height()
        total_height = line_height * len(lines)
        start_y = self.rect.y + (self.rect.h - total_height) // 2
        for idx, line in enumerate(lines):
            text_surf = font_to_use.render(line, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(
                self.rect.x + self.rect.w // 2,
                start_y + idx * line_height + line_height // 2
            ))
            surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.current_color = self.color_press
                if self.onclick:
                    self.onclick()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.current_color = self.color_hover
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.color_hover
            else:
                self.current_color = self.color_normal


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


def Gameinstructions():
    old_vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(0.3)
    s = pygame.mixer.Sound('assets/music/menu-button-89141.mp3')
    s.play()
    duration_ms = int(s.get_length() * 1000)
    fade_out_screen(duration_ms)
    pygame.mixer.music.set_volume(old_vol)

    prompt_lines = ["Do you seriously not know", "how to play Tetris?"]
    btn_w, btn_h = width , 80
    btn_x = 0
    btn1_y = height - btn_h*2 - 60
    btn2_y = height - btn_h - 40

    btn1 = Button(btn_x, btn1_y, btn_w, btn_h,
    "No, I do.\nI was just seeing what '?' was",
        onclick=lambda: exit_instructions())

    btn2 = Button(btn_x, btn2_y, btn_w, btn_h,
        "Tetris?\nI've never even heard of it",
        onclick=real_instructions)

    active = True
    def exit_instructions():
        nonlocal active
        active = False

    while active:
        fpsClock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                active = False
            btn1.handle_event(event)
            btn2.handle_event(event)


        screen.fill((0, 0, 0))

        start_y = height // 3
        spacing = small_font.get_height() + 20
        for idx, line in enumerate(prompt_lines):
            line_surf = small_font.render(line, True, (255, 255, 255))
            x = width // 2 - line_surf.get_width() // 2
            y = start_y + idx * spacing
            screen.blit(line_surf, (x, y))
        btn1.draw(screen)
        btn2.draw(screen)
        pygame.display.flip()

def real_instructions():
    controls = [
        " Left Arrow - Move block left",
        " Right Arrow - Move block right",
        " Up Arrow or W - Rotate block",
        " Down Arrow or S - Soft drop",
        " Space - Hard drop",
        " C - Hold current block",
        " P or ESC - Pause / Settings",
    ]
    active = True
    while active:
        fpsClock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                active = False

        screen.fill((0, 0, 0))
        header = ctrl_font.render("TETRIS INSTRUCTIONS", True, (255, 255, 255))
        screen.blit(header, (width//2 - header.get_width()//2, 50))
        y_start = height // 3
        line_spacing = ctrl_font.get_height() + 5
        for idx, line in enumerate(controls):
            surf = ctrl_font.render(line, True, (200, 200, 200))
            x = width // 2 - surf.get_width() // 2
            y = y_start + idx * line_spacing
            screen.blit(surf, (x, y))

        pygame.display.flip()

def startGame():
    global title_screen, fpsClock
    old_vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(0.3)
    s = pygame.mixer.Sound('assets/music/winning-game-sound-effect.wav')
    s.play()
    duration_ms = int(s.get_length() * 1000)
    fade_out_screen(duration_ms)
    pygame.mixer.music.set_volume(old_vol)
    title_screen = False
    pygame.time.set_timer(GameState.PHYSICS_STEP_EVENT, 1000)
    pygame.time.set_timer(GameState.INPUT_STEP_EVENT, 300)

def openSettings():
    global title_screen
    import settings
    result = settings.run(return_to_game=not title_screen)
    if result:
        title_screen = True


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

objects = []

startButton = Button(100, 195, 300, 100, 'START', startGame)
objects.append(startButton)

exitButton = Button(100, 415, 300, 100, 'EXIT', quitGame)
objects.append(exitButton)

settingsButton = Button(100, 305, 300, 100, 'SETTINGS', openSettings)
objects.append(settingsButton)

tutorialButton = Button(0, 550, 50, 50, '?', Gameinstructions)
objects.append(tutorialButton)


title_screen = True

game_state = GameState.GameState((width, height), 10)
# idx 0: Movement key
# idx 1: Rotation key
# idx 2: Drop key
waiting_key = [0, False, False]

physics_speed = 1000

# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == GameState.PHYSICS_STEP_EVENT:
            game_state.step()
            pygame.time.set_timer(GameState.PHYSICS_STEP_EVENT, physics_speed)
        elif event.type == GameState.INPUT_STEP_EVENT:
            pygame.time.set_timer(GameState.INPUT_STEP_EVENT, 350)
            if waiting_key[0] == pygame.K_RIGHT:
                if game_state.stage_drop.texture.get_width() + game_state.stage_drop.position[0] <= game_state.stage_width():
                    game_state.stage_drop = game_state.stage_drop.move((game_state.block_size, 0))
                waiting_key[0] = 0
            elif waiting_key[0] == pygame.K_LEFT:
                if game_state.stage_drop.position[0] > 0:
                    game_state.stage_drop = game_state.stage_drop.move((-game_state.block_size, 0))
                waiting_key[0] = 0

            if waiting_key[1]:
                # TODO: handle rotation
                pass
            if waiting_key[2]:
                physics_speed = 250
            else:
                physics_speed = 1000

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            waiting_key[0] = pygame.K_RIGHT
        elif keys[pygame.K_LEFT]:
            waiting_key[0] = pygame.K_LEFT

        if keys[pygame.K_UP]:
            waiting_key[1] = True
        if keys[pygame.K_DOWN]:
            waiting_key[2] = True

    elif event.type == pygame.KEYDOWN and not title_screen:
        if event.key == pygame.K_ESCAPE:
            openSettings()
    for button in objects:
        button.handle_event(event)

    if title_screen:
        screen.blit(title_image, title_rect)
        for object in objects:
            object.draw(screen)
    else:
        game_state.render(screen)

    pygame.display.flip()
    fpsClock.tick(fps)
