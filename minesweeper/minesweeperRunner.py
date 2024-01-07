import os
import subprocess

import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

# find programme path
minesweeper_path = sys.argv[0]
programme_path = minesweeper_path.replace("minesweeper\\minesweeperRunner.py", "")

# Colors
black = (0, 0, 0)
gray = (180, 180, 180)
white = (255, 255, 255)
red = (255, 0, 0)

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)

# Initiate variables
settings = False
difficulty = "easy"
easy_selected = True
medium_selected = False
hard_selected = False

# Fonts
OPEN_SANS = programme_path + "assets/fonts/OpenSans-Regular.ttf"
small_font = pygame.font.Font(OPEN_SANS, 20)
medium_font = pygame.font.Font(OPEN_SANS, 28)
large_font = pygame.font.Font(OPEN_SANS, 40)
neighbors_font = pygame.font.Font(OPEN_SANS, 50)


# Create game
HEIGHT = 16
WIDTH = 16
MINES = 40

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load(programme_path + "assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load(programme_path + "assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Show game instructions
    if settings is False:

        # Title
        title = large_font.render("Play Minesweeper", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!",
            "",
            "If you don't know your next move you can click the Help-Button.",
            "The Help-Button will make an AI-move. However, even an AI can fail this game with missing information."
        ]
        for i, rule in enumerate(rules):
            line = small_font.render(rule, True, white)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)


        # Menu Button
        menuButton = pygame.Rect((width / 15), (height / 23), width / 6, 75)
        Menu = medium_font.render("Menu", True, white)
        menuRect = Menu.get_rect()
        menuRect.center = menuButton.center
        pygame.draw.rect(screen, black, menuButton)
        pygame.draw.rect(screen, white, menuButton, 2)
        screen.blit(Menu, menuRect)



        # Difficulty buttons
        difficultyEasyButton = pygame.Rect((width / 6 * 0.5), (2 / 4) * height, width / 4, 50)
        difficultyEasy = medium_font.render("Easy", True, white)
        difficultyEasyRect = difficultyEasy.get_rect()
        difficultyEasyRect.center = difficultyEasyButton.center
        pygame.draw.rect(screen, black, difficultyEasyButton)
        pygame.draw.rect(screen, white, difficultyEasyButton, 2)  # Weisser Rand
        screen.blit(difficultyEasy, difficultyEasyRect)

        # Easy button click
        if easy_selected:
            pygame.draw.rect(screen, gray, difficultyEasyButton)
        else:
            pygame.draw.rect(screen, black, difficultyEasyButton)
        pygame.draw.rect(screen, white, difficultyEasyButton, 2)
        screen.blit(difficultyEasy, difficultyEasyRect)

        difficultyMediumButton = pygame.Rect((width / 6 * 2.25), (2 / 4) * height, width / 4, 50)
        difficultyMedium = medium_font.render("Medium", True, white)
        difficultyMediumRect = difficultyMedium.get_rect()
        difficultyMediumRect.center = difficultyMediumButton.center
        pygame.draw.rect(screen, black, difficultyMediumButton)
        pygame.draw.rect(screen, white, difficultyMediumButton, 2)  # Weisser Rand
        screen.blit(difficultyMedium, difficultyMediumRect)

        # Medium button click
        if medium_selected:
            pygame.draw.rect(screen, gray, difficultyMediumButton)
        else:
            pygame.draw.rect(screen, black, difficultyMediumButton)
        pygame.draw.rect(screen, white, difficultyMediumButton, 2)
        screen.blit(difficultyMedium, difficultyMediumRect)

        difficultyHardButton = pygame.Rect((width / 6 * 4), (2 / 4) * height, width / 4, 50)
        difficultyHard = medium_font.render("Hard", True, white)
        difficultyHardRect = difficultyHard.get_rect()
        difficultyHardRect.center = difficultyHardButton.center
        pygame.draw.rect(screen, black, difficultyHardButton)
        pygame.draw.rect(screen, white, difficultyHardButton, 2)  # Weisser Rand
        screen.blit(difficultyHard, difficultyHardRect)

        # hard button click
        if hard_selected:
            pygame.draw.rect(screen, gray, difficultyHardButton)
        else:
            pygame.draw.rect(screen, black, difficultyHardButton)
        pygame.draw.rect(screen, white, difficultyHardButton, 2)
        screen.blit(difficultyHard, difficultyHardRect)


        # Play game button
        playButton = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        play = medium_font.render("Play Game", True, white)
        playRect = play.get_rect()
        playRect.center = playButton.center
        pygame.draw.rect(screen, black, playButton)
        pygame.draw.rect(screen, white, playButton, 2)  # Weisser Rand
        screen.blit(play, playRect)

        # Check if play button clicked
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

            #Difficulty
            elif difficultyEasyButton.collidepoint(mouse):
                difficulty = "easy"
                easy_selected = True
                medium_selected = False
                hard_selected = False
            elif difficultyMediumButton.collidepoint(mouse):
                difficulty = "medium"
                easy_selected = False
                medium_selected = True
                hard_selected = False
            elif difficultyHardButton.collidepoint(mouse):
                difficulty = "hard"
                easy_selected = False
                medium_selected = False
                hard_selected = True
            elif playButton.collidepoint(mouse):
                if difficulty == "easy":
                    HEIGHT = 9
                    WIDTH = 9
                    MINES = 10
                    # Create game and AI agent
                    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

                    # Compute cell and font size
                    cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
                    neighbors_font = pygame.font.Font(OPEN_SANS, 50)

                    # Add images
                    flag = pygame.image.load(programme_path + "assets/images/flag.png")
                    flag = pygame.transform.scale(flag, (cell_size, cell_size))
                    mine = pygame.image.load(programme_path + "assets/images/mine.png")
                    mine = pygame.transform.scale(mine, (cell_size, cell_size))

                    settings = True
                    time.sleep(0.3)
                elif difficulty == "medium":

                    # Create game
                    HEIGHT = 16
                    WIDTH = 16
                    MINES = 40

                    # Create game and AI agent
                    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

                    # Compute cell and font size
                    cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
                    neighbors_font = pygame.font.Font(OPEN_SANS, 30)

                    # Add images
                    flag = pygame.image.load(programme_path + "assets/images/flag.png")
                    flag = pygame.transform.scale(flag, (cell_size, cell_size))
                    mine = pygame.image.load(programme_path + "assets/images/mine.png")
                    mine = pygame.transform.scale(mine, (cell_size, cell_size))

                    settings = True
                    time.sleep(0.3)
                else:

                    # Create game
                    HEIGHT = 16
                    WIDTH = 30
                    MINES = 99

                    # Create game and AI agent
                    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

                    # Compute cell and font size
                    cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
                    neighbors_font = pygame.font.Font(OPEN_SANS, 20)

                    # Add images
                    flag = pygame.image.load(programme_path + "assets/images/flag.png")
                    flag = pygame.transform.scale(flag, (cell_size, cell_size))
                    mine = pygame.image.load(programme_path + "assets/images/mine.png")
                    mine = pygame.transform.scale(mine, (cell_size, cell_size))

                    settings = True
                    time.sleep(0.3)
        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, gray, rect)
            pygame.draw.rect(screen, white, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                nearby_mines = game.nearby_mines((i, j))
                neighbors = neighbors_font.render(str(nearby_mines), True, black
                                                  )
                # change colors of the numbers
                if nearby_mines == 1:
                    neighbors = neighbors_font.render(str(nearby_mines), True, (0, 0, 255))  # Blau
                elif nearby_mines == 2:
                    neighbors = neighbors_font.render(str(nearby_mines), True, (34, 139, 34))  # Grün
                elif nearby_mines >= 3:
                    neighbors = neighbors_font.render(str(nearby_mines), True, (255, 0, 0))  # Rot

                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # Help button
    if not lost:  # help button only shown while not lost
        aiButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = medium_font.render("Help", True, white)
        playButton = buttonText.get_rect()
        playButton.center = aiButton.center
        pygame.draw.rect(screen, black, aiButton)
        pygame.draw.rect(screen, white, aiButton, 2)
        screen.blit(buttonText, playButton)

    # Menu Button
    menuButton = pygame.Rect(width - (width / 35) - (width / 6), height - (height / 23) - 75, width / 6, 75)
    menu = medium_font.render("Menu", True, white)
    menuRect = menu.get_rect()
    menuRect.center = menuButton.center
    pygame.draw.rect(screen, black, menuButton)
    pygame.draw.rect(screen, white, menuButton, 2)
    screen.blit(menu, menuRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = medium_font.render("Reset", True, white)
    playButton = buttonText.get_rect()
    playButton.center = resetButton.center
    pygame.draw.rect(screen, black, resetButton)
    pygame.draw.rect(screen, white, resetButton, 2)
    screen.blit(buttonText, playButton)

    # Settings1 Button
    settingsButton = pygame.Rect(width - (width / 35) - (width / 6), height / 23, width / 6, 75)
    settings1 = medium_font.render("Settings", True, white)
    settings1Rect = settings1.get_rect()
    settings1Rect.center = settingsButton.center
    pygame.draw.rect(screen, black, settingsButton)
    pygame.draw.rect(screen, white, settingsButton, 2)
    screen.blit(settings1, settings1Rect)

    # Check if button is clicked
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

            # Setting button clicked
            if settingsButton.collidepoint(mouse):
                settings = False  # settings are reset to false
                lost = False
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)  # Reset the field
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)  # Reset AI
                revealed = set()  # Set back the visible fields
                flags = set()  # Set back the flags
                time.sleep(0.3)

    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = medium_font.render(text, True, red)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost and not (game.mines == flags):
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Reset game state
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            continue

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

        # Make move and update AI knowledge
        if move:
            if game.is_mine(move):
                lost = True
            else:
                nearby = game.nearby_mines(move)
                revealed.add(move)
                ai.add_knowledge(move, nearby)

    pygame.display.flip()
