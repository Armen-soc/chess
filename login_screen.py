import pygame
from constants import *
from database import ChessDB


class LoginScreen:
    def __init__(self):
        self.db = ChessDB()
        self.username = ""
        self.password = ""
        self.active_input = "username"
        self.error_message = ""
        self.success_message = ""
        self.player_id = None
        self.players = []
        self.show_password = False
        self.input_rect_username = pygame.Rect(WIDTH // 2 - 200, 250, 400, 50)
        self.input_rect_password = pygame.Rect(WIDTH // 2 - 200, 350, 400, 50)
        self.login_button_rect = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)
        self.register_button_rect = pygame.Rect(WIDTH // 2 - 100, 520, 200, 50)
        self.toggle_password_rect = pygame.Rect(WIDTH // 2 + 220, 350, 30, 30)

    def draw_login_screen(self):
        screen.fill('white')

        # Title
        title = big_font.render("Chess Login", True, 'black')
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Username input
        pygame.draw.rect(screen, 'light gray' if self.active_input == "username" else 'gray',
                         self.input_rect_username, 0, 5)
        pygame.draw.rect(screen, 'black', self.input_rect_username, 2, 5)
        username_text = font.render("Username:", True, 'black')
        screen.blit(username_text, (self.input_rect_username.x, self.input_rect_username.y - 30))
        username_input = font.render(self.username, True, 'black')
        screen.blit(username_input, (self.input_rect_username.x + 10, self.input_rect_username.y + 15))

        # Password input
        pygame.draw.rect(screen, 'light gray' if self.active_input == "password" else 'gray',
                         self.input_rect_password, 0, 5)
        pygame.draw.rect(screen, 'black', self.input_rect_password, 2, 5)
        password_text = font.render("Password:", True, 'black')
        screen.blit(password_text, (self.input_rect_password.x, self.input_rect_password.y - 30))
        
        # Show password or asterisks based on toggle
        password_display = self.password if self.show_password else "*" * len(self.password)
        password_input = font.render(password_display, True, 'black')
        screen.blit(password_input, (self.input_rect_password.x + 10, self.input_rect_password.y + 15))
        
        # Toggle password visibility button
        pygame.draw.rect(screen, 'light blue', self.toggle_password_rect, 0, 5)
        toggle_text = "👁" if self.show_password else "👁", True, 'black'
        pygame.draw.rect(screen, 'light blue', self.toggle_password_rect, 0, 5)
        # Use text instead of emoji for better compatibility
        toggle_text = small_font.render("Show" if self.show_password else "Hide", True, 'black')
        screen.blit(toggle_text, (self.toggle_password_rect.x + 5, self.toggle_password_rect.y + 5))
        screen.blit(toggle_text, (self.toggle_password_rect.x + 5, self.toggle_password_rect.y + 5))

        # Login button
        pygame.draw.rect(screen, 'green', self.login_button_rect, 0, 5)
        login_text = font.render("Login", True, 'black')
        screen.blit(login_text, (self.login_button_rect.x + self.login_button_rect.width // 2 - login_text.get_width() // 2, 
                                self.login_button_rect.y + self.login_button_rect.height // 2 - login_text.get_height() // 2))

        # Register button
        pygame.draw.rect(screen, 'blue', self.register_button_rect, 0, 5)
        register_text = font.render("Register", True, 'black')
        screen.blit(register_text, (self.register_button_rect.x + self.register_button_rect.width // 2 - register_text.get_width() // 2, 
                                   self.register_button_rect.y + self.register_button_rect.height // 2 - register_text.get_height() // 2))

        # Success message (green)
        if self.success_message:
            success_text = font.render(self.success_message, True, 'green')
            screen.blit(success_text, (WIDTH // 2 - success_text.get_width() // 2, 600))

        # Error message (red)
        if self.error_message:
            error_text = font.render(self.error_message, True, 'red')
            screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, 650))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if clicked on username input
            if self.input_rect_username.collidepoint(mouse_pos):
                self.active_input = "username"
                self.error_message = ""
                self.success_message = ""

            # Check if clicked on password input
            elif self.input_rect_password.collidepoint(mouse_pos):
                self.active_input = "password"
                self.error_message = ""
                self.success_message = ""

            # Check if clicked on login button
            elif self.login_button_rect.collidepoint(mouse_pos):
                if self.username.strip() and self.password.strip():
                    self.player_id = self.db.authenticate_player(self.username, self.password)
                    if self.player_id:
                        print(f"✅ Login successful. Player ID: {self.player_id}")
                        self.players.append(self.username)
                        return "game"  # Proceed to game
                    else:
                        print("❌ Invalid username or password")
                        self.error_message = "Invalid username or password"

                    # if self.player_id:
                    #     return "game"  # Proceed to game
                    # else:
                    #     self.error_message = "Invalid username or password"
                else:
                    self.error_message = "Please enter both username and password"

            # Check if clicked on register button
            elif self.register_button_rect.collidepoint(mouse_pos):
                try:
                    if self.username.strip() and self.password.strip():
                        success = self.db.register_player(self.username, self.password)
                        if success:
                            self.error_message = ""
                            self.success_message = "Registration successful! Please login."
                        else:
                            self.error_message = "Registration failed"
                    else:
                        self.error_message = "Please enter both username and password"
                except ValueError as e:
                    self.error_message = str(e)
                except RuntimeError as e:
                    # Handle specific database errors more gracefully
                    if "too long" in str(e).lower():
                        self.error_message = "System error: Please try a different password"
                    else:
                        self.error_message = "Registration error. Please try again."
                    print(f"Database error: {e}")  # For debugging
                        
            # Check if clicked on password toggle
            elif self.toggle_password_rect.collidepoint(mouse_pos):
                self.show_password = not self.show_password

        elif event.type == pygame.KEYDOWN:
            if self.active_input == "username":
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_TAB:
                    self.active_input = "password"
                elif len(self.username) < 20:  # Limit username length
                    self.username += event.unicode

            elif self.active_input == "password":
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                elif event.key == pygame.K_TAB:
                    self.active_input = "username"
                elif event.key == pygame.K_RETURN:
                    # Try to login when pressing enter
                    if self.username.strip() and self.password.strip():
                        self.player_id = self.db.authenticate_player(self.username, self.password)
                        if self.player_id:
                            return "game"
                        else:
                            self.error_message = "Invalid username or password"
                elif len(self.password) < 30:  # Limit password length
                    self.password += event.unicode

        return "login"  # Stay on login screen