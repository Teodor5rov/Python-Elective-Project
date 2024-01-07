import os
import subprocess

import pygame
import sys
import time

import tictactoe as ttt

# Create game
pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

# find programme path
tictactoe_path = sys.argv[0]
programme_path = tictactoe_path.replace("tictactoe\\tictactoeRunner.py", "")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (169, 169, 169)

# Fonts
medium_font = pygame.font.Font(programme_path + "assets/fonts/OpenSans-Regular.ttf", 28)
large_font = pygame.font.Font(programme_path + "assets/fonts/OpenSans-Regular.ttf", 40)
move_font = pygame.font.Font(programme_path + "assets/fonts/OpenSans-Regular.ttf", 60)
x_font = pygame.font.Font(programme_path + "assets/fonts/OpenSans-Regular.ttf", 120)
o_font = pygame.font.Font(programme_path + "assets/fonts/OpenSans-Regular.ttf", 120)

# Initiate variables
difficulty = "easy"
user = ttt.playerX
settings = False
board = ttt.initial_state()
ai_turn = False

# Click status for buttons
clicked_easy = True
clicked_medium = False
clicked_hard = False
clicked_impossible = False
clicked_play_x = True
clicked_play_o = False
clicked_play = False
clicked_reset = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # **********************
    # Settings
    # **********************
    if settings is False:

        # Draw title
        title = large_font.render("Tic-Tac-Toe Setting", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw Opponent
        title = large_font.render("Opponent", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 100)
        screen.blit(title, titleRect)

        # Draw Play as
        title = large_font.render("Play As", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 430)
        screen.blit(title, titleRect)

        # Menu Button
        menuButton = pygame.Rect((width / 15), (height / 23), width / 6, 75)
        menu = medium_font.render("Menu", True, white)
        menuRect = menu.get_rect()
        menuRect.center = menuButton.center
        pygame.draw.rect(screen, black, menuButton)
        pygame.draw.rect(screen, white, menuButton, 2)
        screen.blit(menu, menuRect)

        # Difficulty buttons
        difficultyEasyButton = pygame.Rect((width / 8), (height / 4), width / 4, 50)
        difficultyEasy = medium_font.render("Easy", True, white)
        difficultyEasyRect = difficultyEasy.get_rect()
        difficultyEasyRect.center = difficultyEasyButton.center
        pygame.draw.rect(screen, black, difficultyEasyButton)
        pygame.draw.rect(screen, white, difficultyEasyButton, 2)
        screen.blit(difficultyEasy, difficultyEasyRect)

        if clicked_easy:
            pygame.draw.rect(screen, gray, difficultyEasyButton)
        screen.blit(difficultyEasy, difficultyEasyRect)

        difficultyMediumButton = pygame.Rect(5 * (width / 8), (height / 4), width / 4, 50)
        difficultyMedium = medium_font.render("Medium", True, white)
        difficultyMediumRect = difficultyMedium.get_rect()
        difficultyMediumRect.center = difficultyMediumButton.center
        pygame.draw.rect(screen, black, difficultyMediumButton)
        pygame.draw.rect(screen, white, difficultyMediumButton, 2)
        screen.blit(difficultyMedium, difficultyMediumRect)

        if clicked_medium:
            pygame.draw.rect(screen, gray, difficultyMediumButton)
        screen.blit(difficultyMedium, difficultyMediumRect)

        difficultyHardButton = pygame.Rect((width / 8), (height / 2.5), width / 4, 50)
        difficultyHard = medium_font.render("Hard", True, white)
        difficultyHardRect = difficultyHard.get_rect()
        difficultyHardRect.center = difficultyHardButton.center
        pygame.draw.rect(screen, black, difficultyHardButton)
        pygame.draw.rect(screen, white, difficultyHardButton, 2)
        screen.blit(difficultyHard, difficultyHardRect)

        if clicked_hard:
            pygame.draw.rect(screen, gray, difficultyHardButton)
        screen.blit(difficultyHard, difficultyHardRect)

        difficultyImpossibleButton = pygame.Rect(5 * (width / 8), (height / 2.5), width / 4, 50)
        difficultyImpossible = medium_font.render("Impossible", True, white)
        difficultyImpossibleRect = difficultyImpossible.get_rect()
        difficultyImpossibleRect.center = difficultyImpossibleButton.center
        pygame.draw.rect(screen, black, difficultyImpossibleButton)
        pygame.draw.rect(screen, white, difficultyImpossibleButton, 2)
        screen.blit(difficultyImpossible, difficultyImpossibleRect)

        if clicked_impossible:
            pygame.draw.rect(screen, gray, difficultyImpossibleButton)
        screen.blit(difficultyImpossible, difficultyImpossibleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 1.75), width / 4, 120)
        playX = x_font.render("X", True, red)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, black, playXButton)
        pygame.draw.rect(screen, white, playXButton, 2)
        screen.blit(playX, playXRect)

        if clicked_play_x:
            pygame.draw.rect(screen, gray, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 1.75), width / 4, 120)
        playO = o_font.render("O", True, blue)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, black, playOButton)
        pygame.draw.rect(screen, white, playOButton, 2)
        screen.blit(playO, playORect)

        if clicked_play_o:
            pygame.draw.rect(screen, gray, playOButton)
        screen.blit(playO, playORect)

        # Play button
        playButton = pygame.Rect((width / 2.66), (height / 1.2), width / 4, 50)
        play = medium_font.render("Start game", True, white)
        playRect = play.get_rect()
        playRect.center = playButton.center
        pygame.draw.rect(screen, black, playButton)
        pygame.draw.rect(screen, white, playButton, 2)
        screen.blit(play, playRect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()

            # Menu button
            if menuButton.collidepoint(mouse):
                start_path = programme_path + "starter.py"

                if os.path.isfile(start_path):
                    try:
                        pygame.quit()
                        subprocess.run([sys.executable, start_path], check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error: {e}")
                else:
                    print(f"Error: File not found - {start_path}")

            # Difficulty buttons
            elif difficultyEasyButton.collidepoint(mouse):
                time.sleep(0.2)
                difficulty = "easy"
                clicked_easy = True
                clicked_medium = False
                clicked_hard = False
                clicked_impossible = False

            elif difficultyMediumButton.collidepoint(mouse):
                time.sleep(0.2)
                difficulty = "medium"
                clicked_easy = False
                clicked_medium = True
                clicked_hard = False
                clicked_impossible = False

            elif difficultyHardButton.collidepoint(mouse):
                time.sleep(0.2)
                difficulty = "hard"
                clicked_easy = False
                clicked_medium = False
                clicked_hard = True
                clicked_impossible = False

            elif difficultyImpossibleButton.collidepoint(mouse):
                time.sleep(0.2)
                difficulty = "impossible"
                clicked_easy = False
                clicked_medium = False
                clicked_hard = False
                clicked_impossible = True

            elif playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.playerX
                clicked_play_x = True
                clicked_play_o = False
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.playerO
                clicked_play_x = False
                clicked_play_o = True
            elif playButton.collidepoint(mouse):
                time.sleep(0.2)
                settings = True

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = move_font.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Menu Button
        menuButton = pygame.Rect(width / 35, height / 23, width / 6, 75)
        menu = medium_font.render("Menu", True, white)
        menuRect = menu.get_rect()
        menuRect.center = menuButton.center
        pygame.draw.rect(screen, black, menuButton)
        pygame.draw.rect(screen, white, menuButton, 2)
        screen.blit(menu, menuRect)

        # Settings1 Button
        settingsButton = pygame.Rect(width - (width / 35) - (width / 6), height / 23, width / 6, 75)
        settings1 = medium_font.render("Settings", True, white)
        settings1Rect = settings1.get_rect()
        settings1Rect.center = settingsButton.center
        pygame.draw.rect(screen, black, settingsButton)
        pygame.draw.rect(screen, white, settingsButton, 2)
        screen.blit(settings1, settings1Rect)

        # Check if Settings button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()

                # Menu button
                if menuButton.collidepoint(mouse):
                    start_path = programme_path + "starter.py"

                    if os.path.isfile(start_path):
                        try:
                            pygame.quit()
                            subprocess.run([sys.executable, start_path], check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"Error: {e}")
                    else:
                        print(f"Error: File not found - {start_path}")

                # Check if Settings button is clicked
                elif settingsButton.collidepoint(mouse):
                    settings = False  # Set settings variable back to False
                    board = ttt.initial_state()  # Reset the board
                    ai_turn = False  # Reset the AI turn

        # Reset button
        ResetButton = pygame.Rect((width / 2.66), (height / 1.2), width / 4, 50)
        Reset = medium_font.render("Reset", True, white)
        ResetRect = Reset.get_rect()
        ResetRect.center = ResetButton.center
        pygame.draw.rect(screen, black, ResetButton)
        pygame.draw.rect(screen, white, ResetButton, 2)  # Weisser Rand
        screen.blit(Reset, ResetRect)

        # Check if reset button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if ResetButton.collidepoint(mouse):
                time.sleep(0.2)
                board = ttt.initial_state()  # Set back the board
                ai_turn = False  # Set back the AI turn

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = large_font.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.1)
                if difficulty == "easy":
                    move = ttt.easy(board)
                elif difficulty == "medium":
                    move = ttt.medium(board)
                elif difficulty == "hard":
                    move = ttt.hard(board)
                else:
                    move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = medium_font.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
