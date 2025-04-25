import pygame
import sys
import title_screen
import GameState
import High_score

pygame.init()

# Define screen size
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris Clone")


clock = pygame.time.Clock()
fps = 60

def run_game():
    game_state = GameState.GameState((screen_width, screen_height), 10)

    physics_speed = 600
    waiting_key = [0, False, False]

    running = True
    while running:
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
                    game_state.stage_drop = game_state.stage_drop.rotate()
                if waiting_key[2]:
                    physics_speed = 200
                else:
                    physics_speed = 600
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = pause_menu()
                    if choice == "exit":
                        return  # Exit to title screen
                elif event.key == pygame.K_UP:
                    game_state.stage_drop = game_state.stage_drop.rotate()
                elif event.key == pygame.K_DOWN:
                    waiting_key[2] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    waiting_key[1] = False
                elif event.key == pygame.K_DOWN:
                    waiting_key[2] = False

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                waiting_key[0] = pygame.K_RIGHT
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                waiting_key[0] = pygame.K_LEFT

        game_state.render(screen)
        pygame.display.flip()
        clock.tick(fps)

def pause_menu():
    paused = True
    font = pygame.font.Font('assets/fonts/modern-tetris.ttf', 20)

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
            text_rect = self.text_surf.get_rect(center=self.rect.center)
            surface.blit(self.text_surf, text_rect)

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
                self.current_color = self.color_hover if self.rect.collidepoint(event.pos) else self.color_normal

    button_width = 300
    button_height = 80
    button_spacing = 20

    return_button = Button(
        (screen_width - button_width) // 2, 200, button_width, button_height,
        "Return"
    )
    settings_button = Button(
        (screen_width - button_width) // 2, 200 + button_height + button_spacing, button_width, button_height,
        "Settings"
    )
    exit_button = Button(
        (screen_width - button_width) // 2, 200 + 2 * (button_height + button_spacing), button_width, button_height,
        "Title Screen"
    )

    buttons = [return_button, settings_button, exit_button]

    while paused:
        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()


        # Draw buttons (their own draw() method handles label rendering)
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for button in buttons:
                button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.rect.collidepoint(event.pos):
                    paused = False
                elif settings_button.rect.collidepoint(event.pos):
                    import settings
                    settings.run(screen, clock, return_to_game=True)
                elif exit_button.rect.collidepoint(event.pos):
                    return "exit"


# High Scores Screen
def show_high_scores_screen():
    showing = True
    font = pygame.font.Font('assets/fonts/modern-tetris.ttf', 15)

    button_width = 200
    button_height = 60
    button_spacing = 20

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
            text_rect = self.text_surf.get_rect(center=self.rect.center)
            surface.blit(self.text_surf, text_rect)

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
                self.current_color = self.color_hover if self.rect.collidepoint(event.pos) else self.color_normal

    def play_again_action():
        nonlocal showing
        showing = False
        run_game()
        show_high_scores_screen()

    def exit_action():
        nonlocal showing
        showing = False

    play_again_button = Button(
        (screen_width - button_width * 2 - button_spacing) // 2,
        450,
        button_width, button_height,
        "Play Again", play_again_action
    )

    exit_button = Button(
        (screen_width + button_spacing) // 2,
        450,
        button_width, button_height,
        "Exit", exit_action
    )

    while showing:
        screen.fill((0, 0, 0))

        title = font.render("High Scores", True, (255, 255, 255))
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

        highscores = High_score.get_highscores()
        for idx, entry in enumerate(highscores):
            text = f"{entry['name']} - {entry['score']}"
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, 150 + idx * 50))

        play_again_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            play_again_button.handle_event(event)
            exit_button.handle_event(event)


def main():
    while True:
        title_screen.run_title_screen(screen, clock)
        run_game()
        show_high_scores_screen()

if __name__ == "__main__":
    main()