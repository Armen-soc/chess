import pygame
from login_screen import *
from constants import *
from game import run_game

def main():
    pygame.init()

    login_screen = LoginScreen()
    current_screen = "login"
    players_logged_in = 0

    player1_id = None
    player2_id = None
    player_1_name = None
    player_2_name = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_screen == "login":
                result = login_screen.handle_event(event)
                users = []
                if result == "game":
                    if login_screen.player_id is None:
                        print("❌ Login failed: No player ID returned.")
                        continue
                    

                    if players_logged_in == 0:
                        player1_id = login_screen.player_id
                        player_1_name = login_screen.username
                        users.append(login_screen)
                        print(f"✅ Player 1 logged in. ID: {player1_id}")
                        players_logged_in += 1
                        login_screen = LoginScreen()  # Reset for player 2
                    else:
                        player2_id = login_screen.player_id
                        player_2_name = login_screen.username
                        users.append(login_screen.player_id)
                        print(f"✅ Player 2 logged in. ID: {player2_id}")
                        current_screen = "game"

                        run_game(player1_id, player2_id, player_1_name, player_2_name)

                login_screen.draw_login_screen()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
