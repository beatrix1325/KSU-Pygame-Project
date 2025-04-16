import sys
import pygame

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settings Menu")

font = pygame.font.Font('assets/fonts/modern-tetris.ttf', 25)
small_font = pygame.font.Font('assets/fonts/modern-tetris.ttf', 20)
clock = pygame.time.Clock()
fps = 60
title_text = font.render("SETTINGS", True, (255, 255, 255))

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
            if self.rect.collidepoint(event.pos):
                self.current_color = self.color_hover
            else:
                self.current_color = self.color_normal

def run_secret_menu():
    user_text = ""
    active = True
    s = pygame.mixer.Sound('assets/music/cute-level-up-3-189853.mp3')
    s.play()
    BG_COLOR = (10, 10, 60)

    while active:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    active = False
                elif event.key == pygame.K_RETURN:
                    print("Cheat code entered:", user_text)
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill(BG_COLOR)

        line1 = small_font.render("ENTER GAMEPLAY MODIFYER.", True, (255, 255, 255))
        line2 = small_font.render("PRESS ESC TO GO BACK.", True, (255, 255, 255))

        line1_rect = line1.get_rect(midtop=(WIDTH // 2, 30))
        line2_rect = line2.get_rect(midtop=(WIDTH // 2, line1_rect.bottom + 10))

        screen.blit(line1, line1_rect)
        screen.blit(line2, line2_rect)

        box_width = 460
        box_height = 50
        box_x = (WIDTH - box_width) // 2
        box_y = line2_rect.bottom + 30
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)

        text_surf = small_font.render(user_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(x=box_rect.x + 10, centery=box_rect.centery)
        screen.blit(text_surf, text_rect)

        pygame.display.flip()

def run():
    is_muted = False

    def fade_out_screen(fade_time_ms):
        surface = pygame.Surface((WIDTH, HEIGHT))
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

    def toggle_mute():
        nonlocal is_muted
        is_muted = not is_muted
        if is_muted:
            mute_button.text = "UNMUTE"
            mute_button.text_surf = font.render(mute_button.text, True, (255, 255, 255))
            pygame.mixer.music.set_volume(0)
            for ch in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(ch).set_volume(0)
        else:
            mute_button.text = "MUTE"
            mute_button.text_surf = font.render(mute_button.text, True, (255, 255, 255))
            pygame.mixer.music.set_volume(1.0)
            for ch in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(ch).set_volume(1.0)

    def back_to_title_screen():
        old_vol = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(0.3)
        s = pygame.mixer.Sound('assets/music/menu-button-89141.mp3')
        s.play()
        duration_ms = int(s.get_length() * 1000)
        fade_out_screen(duration_ms)
        pygame.mixer.music.set_volume(old_vol)
        import title_screen
        title_screen.run()

    mute_button = Button(150, 150, 200, 80, "MUTE", toggle_mute)
    back_button = Button(150, 250, 200, 80, "BACK", back_to_title_screen)

    cheat_code = [
        pygame.K_UP,
        pygame.K_DOWN,
        pygame.K_UP,
        pygame.K_DOWN,
        pygame.K_a,
        pygame.K_b,
        pygame.K_RETURN
    ]
    cheat_index = 0

    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            mute_button.handle_event(event)
            back_button.handle_event(event)

            # Check cheat code
            if event.type == pygame.KEYDOWN:
                if event.key == cheat_code[cheat_index]:
                    cheat_index += 1
                    if cheat_index == len(cheat_code):
                        run_secret_menu()
                        cheat_index = 0
                else:
                    cheat_index = 0

        screen.fill((0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        mute_button.draw(screen)
        back_button.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()