import itertools
import random


class Minesweeper:
    def __init__(self, height=16, width=16, mines=40):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # First, player has found no mines
        self.mines_found = set()

    # def print(self):
    #
    #     for i in range(self.height):
    #         print("--" * self.width + "-")
    #         for j in range(self.width):
    #             if self.board[i][j]:
    #                 print("|X", end="")
    #             else:
    #                 print("| ", end="")
    #         print("|")
    #     print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        # If all mines found game is won
        return self.mines_found == self.mines


class Sentence:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        # If number of cells in a sentence = the count of mines then all cells are mines.
        if self.count == len(self.cells):
            return self.cells
        return None

    def known_safes(self):
        # If the count is 0 then all cells in a sentence are not mines.
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        # Remove the cell from the sentence and subtract 1 from the count of mines.
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        # Remove the cell from the sentence
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    def __init__(self, height=16, width=16):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        # Marks a cell as a mine in ALL sentences in the knowledge
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        # Marks a cell as a safe in ALL sentences in the knowledge
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # Handle the new cell
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Add new sentence from the information in the cell only if there is new knowledge
        new_sentence_cells = set()
        added_new_knowledge = False
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                next_to_cell = (i, j)
                if 0 <= i < self.height and 0 <= j < self.width and next_to_cell != cell:
                    # If the cell is a known mine, do not add it to the sentence and decrease the count by 1
                    if next_to_cell in self.mines:
                        count -= 1
                    # If the cell is not in known safes, add it to the new sentence
                    elif next_to_cell not in self.safes:
                        new_sentence_cells.add(next_to_cell)
                        added_new_knowledge = True

        new_sentence = Sentence(new_sentence_cells, count)
        # If there have been unknown cells added to the sentence then add the sentence to the knowledge
        if added_new_knowledge:
            self.knowledge.append(new_sentence)

        # Rethink to be sure that all new possible inferred sentences are added to the knowledge
        # While this is not efficient it also reduces the number of sentences in the knowledge thus making it faster
        for think in range(16):
            for sentence in self.knowledge:
                # Mark all safes from the sentences
                if sentence.known_safes() is not None:
                    to_be_marked = []
                    for cell in sentence.known_safes():
                        to_be_marked.append(cell)
                    for cell in to_be_marked:
                        self.mark_safe(cell)
                    # Remove the sentence as it no longer contains useful knowledge
                    self.knowledge.remove(sentence)
                # Mark all mines from the sentences
                elif sentence.known_mines() is not None:
                    to_be_marked = []
                    for cell in sentence.known_mines():
                        to_be_marked.append(cell)
                    for cell in to_be_marked:
                        self.mark_mine(cell)
                    # Remove the sentence as it no longer contains useful knowledge
                    self.knowledge.remove(sentence)

            sentences_to_add = []
            sentences_to_remove = []
            # Go through all possible sentence vs sentence
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    # Remove sentences that have the same information:
                    if sentence1 is sentence2:
                        continue
                    if sentence1 == sentence2:
                        self.knowledge.remove(sentence2)
                    # If a sentence cells are a subset of another sentence's cells then infer a new sentence
                    if sentence1.cells > sentence2.cells:
                        inferred_cells = sentence1.cells - sentence2.cells
                        inferred_count = sentence1.count - sentence2.count
                        inferred_sentence = Sentence(inferred_cells, inferred_count)
                        # Remove the big sentence as it no longer contains useful knowledge
                        sentences_to_remove.append(sentence1)
                        # Add the new inferred sentence
                        sentences_to_add.append(inferred_sentence)

            # Remove all sentences marked for removal
            for sentence in sentences_to_remove:
                # Sometimes from the same big sentence can be inferred multiple new sentences
                # Check that the big sentence has not been already removed
                if sentence in self.knowledge:
                    self.knowledge.remove(sentence)

            # Add all new inferred sentences
            for sentence in sentences_to_add:
                self.knowledge.append(sentence)

        # for sentence in self.knowledge:
        #     print(sentence.__str__())

    def make_safe_move(self):
        # Find all possible moves
        possible_moves = self.safes - self.moves_made

        if len(possible_moves) == 0:
            return None

        # If there is a safe move return it
        else:
            move = possible_moves.pop()
            return move

    def make_random_move(self):
        # Use itertools to get all possible board moves
        all_positions = set(itertools.product(range(self.height), range(self.width)))
        # Find all moves not already made or a mine on the board
        legal_moves = list(all_positions - self.moves_made - self.mines)
        # If all moves on the board are already made return None
        if len(legal_moves) == 0:
            return None
        else:
            return random.choice(legal_moves)
