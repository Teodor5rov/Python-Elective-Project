import os
import subprocess

import pygame
import sys

# define programme_path
start_path = sys.argv[0]
programme_path = start_path.replace("starter.py", "")


class Starter:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.games = ["Tic-Tac-Toe", "Minesweeper"]
        self.selected_game = None

        # Load images
        self.tic_tac_toe_image = pygame.image.load(programme_path + "assets/images/tictactoe.png")
        self.minesweeper_image = pygame.image.load(programme_path + "assets/images/minesweeper.png")

        # Resize images to a fitting size
        self.tic_tac_toe_image = pygame.transform.scale(self.tic_tac_toe_image, (200, 200))
        self.minesweeper_image = pygame.transform.scale(self.minesweeper_image, (200, 200))

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Choose a game to play:", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(text, text_rect)

        tic_tac_toe_text = self.font.render("Tic-Tac-Toe", True, (255, 255, 255))
        tic_tac_toe_rect = tic_tac_toe_text.get_rect(center=(self.width // 4, 200))
        self.screen.blit(tic_tac_toe_text, tic_tac_toe_rect)

        minesweeper_text = self.font.render("Minesweeper", True, (255, 255, 255))
        minesweeper_rect = minesweeper_text.get_rect(center=(3 * self.width // 4, 200))
        self.screen.blit(minesweeper_text, minesweeper_rect)

        # Display Tic-Tac-Toe image
        tic_tac_toe_image_rect = self.tic_tac_toe_image.get_rect(center=(self.width // 4, 350))
        self.screen.blit(self.tic_tac_toe_image, tic_tac_toe_image_rect)

        # Display Minesweeper image
        minesweeper_image_rect = self.minesweeper_image.get_rect(center=(3 * self.width // 4, 350))
        self.screen.blit(self.minesweeper_image, minesweeper_image_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if (100 <= mouse_pos[0] <= 300) and (175 <= mouse_pos[1] <= 450):
                        tictactoe_path = programme_path + "tictactoe" + "\\tictactoeRunner.py"

                        if os.path.isfile(tictactoe_path):
                            self.selected_game = self.games[0]  # Tic-Tac-Toe selected
                            try:
                                pygame.quit()
                                subprocess.run([sys.executable, tictactoe_path], check=True)
                            except subprocess.CalledProcessError as e:
                                print(f"Error: {e}")
                        else:
                            print(f"Error: File not found - {tictactoe_path}")

                    elif (500 <= mouse_pos[0] <= 700) and (175 <= mouse_pos[1] <= 450):
                        minesweeper_path = programme_path + "minesweeper" + "\\minesweeperRunner.py"

                        if os.path.isfile(minesweeper_path):
                            self.selected_game = self.games[1]  # Minesweeper selected
                            try:
                                pygame.quit()
                                subprocess.run([sys.executable, minesweeper_path], check=True)
                            except subprocess.CalledProcessError as e:
                                print(f"Error: {e}")
                        else:
                            print(f"Error: File not found - {minesweeper_path}")

            if self.selected_game:
                pygame.quit()
                return self.selected_game

            self.clock.tick(30)


if __name__ == "__main__":
    starter = Starter()
    selected_game = starter.run()
    print("Selected Game:", selected_game)
