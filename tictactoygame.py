from random import randint
class TicTacToe():
    board=list()
    game_letters = list()
    turn = ''
    next_player = ''

    def init_board(self):
        self.board = [' '] * 10

    def get_board(self):
        return self.board

    def get_drawn_board(self, board):
        row_0 = '✎\n'
        row_1 = self.board[7] + '|' + self.board[8] + '|' + \
                self.board[9] + '\n'
        row_2 = '--+--+--\n'
        row_3 = self.board[4] + '|' + self.board[5] + '|' + \
                self.board[6] + '\n'
        row_4 = '--+--+--\n'
        row_5 = self.board[1] + '|' + self.board[2] + '|' + \
                self.board[3] + '\n'

        drawn_board = row_0 + row_1 + row_2 + row_3 + row_4 + row_5

        return drawn_board

    def set_game_letters(self, user_game_letter):

        if user_game_letter == 'X':
            self.game_letters = ['X', 'O']
        else:
            self.game_letters = ['O', 'X']

    def get_user_game_letter(self):
        return self.game_letters[0]

    def get_bot_game_letter(self):
        return self.game_letters[1]

    def set_turn(self):
        """Randomly choose which player goes first.
        """

        if randint(0, 1) == 0:
            self.turn = 'bot'
        else:
            self.turn = 'user'

    def get_turn(self):
        return self.turn

    def set_next_turn(self, current_turn):
        if current_turn == 'bot':
            self.turn = 'user'
        else:
            self.turn = 'bot'

    def make_move(self, board, game_letter, move):
        board[move] = game_letter

    def is_winner(self, board, game_letter):
        # -1- check the top row
        top_row_check = board[7] == game_letter and \
                        board[8] == game_letter and board[9] == game_letter

        # -2- check the middle row
        middle_row_check = board[4] == game_letter and \
                           board[5] == game_letter and board[6] == game_letter

        # -3- check the bottom row
        bottom_row_check = board[1] == game_letter and \
                           board[2] == game_letter and board[3] == game_letter

        # -4- check the left column
        left_column_check = board[7] == game_letter and \
                            board[4] == game_letter and board[1] == game_letter

        # -5- check the middle column
        middle_column_check = board[8] == game_letter and \
                              board[5] == game_letter and board[2] == game_letter

        # -6- check the right column
        right_column_check = board[9] == game_letter and \
                             board[6] == game_letter and board[3] == game_letter

        # -7- check the main diagonal
        main_diagonal_check = board[7] == game_letter and \
                              board[5] == game_letter and board[3] == game_letter

        # -8- check the secondary diagonal
        secondary_diagonal_check = board[9] == game_letter and \
                                   board[5] == game_letter and board[1] == game_letter

        # check all winner combinations
        is_winner_check = top_row_check or middle_row_check or \
                          bottom_row_check or left_column_check or \
                          middle_column_check or right_column_check or \
                          main_diagonal_check or secondary_diagonal_check

        return is_winner_check

    def get_board_copy(self, board):

        board_copy = []

        for i in board:
            board_copy.append(i)

        return board_copy