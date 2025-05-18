import pygame
from constants import *
from database import ChessDB


class LoginScreen:
    def __init__(self):
        self.db = ChessDB()
        self.username = ""
        self.password = ""
        self.active_input = "username"  # or "password"
        self.error_message = ""
        self.player_id = None

    def draw_login_screen(self):
        screen.fill('white')

        # Title
        title = big_font.render("Chess Login", True, 'black')
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Username input
        pygame.draw.rect(screen, 'light gray' if self.active_input == "username" else 'gray',
                         [WIDTH // 2 - 200, 250, 400, 50], 0, 5)
        pygame.draw.rect(screen, 'black', [WIDTH // 2 - 200, 250, 400, 50], 2, 5)
        username_text = font.render("Username:", True, 'black')
        screen.blit(username_text, (WIDTH // 2 - 200, 220))
        username_input = font.render(self.username, True, 'black')
        screen.blit(username_input, (WIDTH // 2 - 190, 260))

        # Password input
        pygame.draw.rect(screen, 'light gray' if self.active_input == "password" else 'gray',
                         [WIDTH // 2 - 200, 350, 400, 50], 0, 5)
        pygame.draw.rect(screen, 'black', [WIDTH // 2 - 200, 350, 400, 50], 2, 5)
        password_text = font.render("Password:", True, 'black')
        screen.blit(password_text, (WIDTH // 2 - 200, 320))
        password_input = font.render("*" * len(self.password), True, 'black')
        screen.blit(password_input, (WIDTH // 2 - 190, 360))

        # Login button
        pygame.draw.rect(screen, 'green', [WIDTH // 2 - 100, 450, 200, 50], 0, 5)
        login_text = font.render("Login", True, 'black')
        screen.blit(login_text, (WIDTH // 2 - login_text.get_width() // 2, 465))

        # Register button
        pygame.draw.rect(screen, 'blue', [WIDTH // 2 - 100, 520, 200, 50], 0, 5)
        register_text = font.render("Register", True, 'black')
        screen.blit(register_text, (WIDTH // 2 - register_text.get_width() // 2, 535))

        # Error message
        if self.error_message:
            error_text = font.render(self.error_message, True, 'red')
            screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, 600))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if clicked on username input
            if WIDTH // 2 - 200 <= mouse_pos[0] <= WIDTH // 2 + 200 and 250 <= mouse_pos[1] <= 300:
                self.active_input = "username"

            # Check if clicked on password input
            elif WIDTH // 2 - 200 <= mouse_pos[0] <= WIDTH // 2 + 200 and 350 <= mouse_pos[1] <= 400:
                self.active_input = "password"

            # Check if clicked on login button
            elif WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and 450 <= mouse_pos[1] <= 500:
                if self.username and self.password:
                    self.player_id = self.db.authenticate_player(self.username, self.password)
                    if self.player_id:
                        return "game"  # Proceed to game
                    else:
                        self.error_message = "Invalid username or password"
                else:
                    self.error_message = "Please enter both username and password"

            # Check if clicked on register button
            elif WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and 520 <= mouse_pos[1] <= 570:
                if self.username and self.password:
                    if self.db.register_player(self.username, self.password):
                        self.error_message = "Registration successful! Please login."
                    else:
                        self.error_message = "Username already exists"
                else:
                    self.error_message = "Please enter both username and password"

        elif event.type == pygame.KEYDOWN:
            if self.active_input == "username":
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode

            elif self.active_input == "password":
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode

        return "login"  # Stay on login screen