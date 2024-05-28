#coding=utf-8
# How to translate comments into English?
import pygame
import game as game
from argparse import ArgumentParser
from Agent import Search

ROWS = 15
SIDE = 30

SCREEN_WIDTH = ROWS * SIDE
SCREEN_HEIGHT = ROWS * SIDE

EMPTY = -1
BLACK = 1
WHITE = 0
DIRE = [(1, 0), (0, 1), (1, 1), (1, -1)]
RGB = {BLACK: (0,0,0), WHITE: (255,255,255)}


class Gobang(game.Game):
    def __init__(self, title, size, fps=15, chess_file=None): 
        super(Gobang, self).__init__(title, size, fps)
        self.board = [[EMPTY for i in range(ROWS)] for j in range(ROWS)]

        # Initialize the board according to the chess_file, # represents empty, 1 represents black, 0 represents white
        if chess_file is not None:
            with open(chess_file, "r") as f:
                for i, line in enumerate(f.readlines()):
                    for j, x in enumerate(line.strip().split(" ")):
                        if x=="1":
                            self.board[i][j]=BLACK
                        if x=="0":
                            self.board[i][j]=WHITE
        
        self.select = (-1, -1)
        self.black = True
        self.draw_board()
        self.bind_click(1, self.click)
        # Modify the following lines to use AI as the player
        self.player1=self.AI_player
        self.player2=self.Human_player

    def click(self, x, y): 
        if self.end:
            return False
        i, j = y // SIDE, x // SIDE 
        if self.board[i][j] != EMPTY:
            pygame.display.set_caption("Gobang Game ---- %s's turn. Invalid move." %("Black" if self.black else "White"))
            return False
        self.board[i][j] = BLACK if self.black else WHITE
        self.draw_chess(RGB[self.board[i][j]], i, j)
        self.black = not self.black

        chess = self.check_win()
        if chess:
            self.end = True
            i, j = chess[0]
            winner = "Black"
            if self.board[i][j] == WHITE:
                winner = "White"
            pygame.display.set_caption("Gobang Game ---- %s wins!" % (winner))
            for c in chess:
                i, j = c
                self.draw_chess((100, 255, 255), i, j)
                self.timer.tick(5)
        
        return True

    def check_win(self):
        for i in range(ROWS):
            for j in range(ROWS):
                win = self.check_chess(i, j)
                if win:
                    return win
        return None

    def check_chess(self, i, j):
        if self.board[i][j] == EMPTY:
            return None
        color = self.board[i][j]
        for dire in DIRE:
            x, y = i, j
            chess = []
            while self.board[x][y] == color:
                chess.append((x, y))
                x, y = x+dire[0], y+dire[1]
                if x < 0 or y < 0 or x >= ROWS or y >= ROWS:
                    break
            if len(chess) >= 5:
                return chess
        return None

    def draw_chess(self, color, i, j):
        center = (j*SIDE+SIDE//2, i*SIDE+SIDE//2)
        pygame.draw.circle(self.screen, color, center, SIDE//2-2)
        pygame.display.update(pygame.Rect(j*SIDE, i*SIDE, SIDE, SIDE))

    def draw_board(self):
        self.screen.fill((139, 87,66))
        for i in range(ROWS):
            start = (i*SIDE + SIDE//2, SIDE//2)
            end = (i*SIDE + SIDE//2, ROWS*SIDE - SIDE//2)
            pygame.draw.line(self.screen, 0x000000, start, end)
            start = (SIDE//2, i*SIDE + SIDE//2)
            end = (ROWS*SIDE - SIDE//2, i*SIDE + SIDE//2)
            pygame.draw.line(self.screen, 0x000000, start, end)
        center = ((ROWS//2)*SIDE+SIDE//2, (ROWS//2)*SIDE+SIDE//2)
        pygame.draw.circle(self.screen, (0,0,0), center, 4)
        pygame.display.update()

        for i in range(ROWS):
            for j in range(ROWS):
                if self.board[i][j] is not EMPTY:
                    self.draw_chess(RGB[self.board[i][j]], i, j)
    
    def AI_player(self, latest):
        pygame.display.set_caption("Gobang Game ---- AI's turn")
        x, y, alpha=Search(EMPTY, BLACK, WHITE, self.black, latest, self.board, )
        pygame.display.set_caption("Gobang Game")
        self.click(y*SIDE, x*SIDE)
        print(x, y, alpha)
        return (x, y)  

if __name__ == '__main__':
    print('''
    Welcome to Gobang Game!
    Click the LEFT MOUSE BUTTON to play the game.
    ''')
    parser=ArgumentParser(description='gobang')
    parser.add_argument('--chess_file', type=str, default=None)
    args=parser.parse_args()
    gobang = Gobang("Gobang Game", (SCREEN_WIDTH, SCREEN_HEIGHT), chess_file=args.chess_file)
    gobang.run()
