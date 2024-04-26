class GameState:
    """
    This class is responsible for storing info about the GameState, current legal moves, and keeping a move log
    """

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # self.board = [
        #     ["bR", "--", "bB", "--", "--", "--", "--", "bR"],
        #     ["bP", "--", "bP", "--", "--", "bP", "--", "bP"],
        #     ["--", "bP", "--", "bP", "--", "--", "bK", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "bQ", "--", "bP", "--", "--", "--", "--"],
        #     ["--", "--", "bP", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "wK", "--", "--", "--", "--"]
        # ]

        self.white_to_move = True
        # Keeps track of whose turn it is, to change this, it can be written self.white_to_move = not self.white_to_move
        self.move_log = []
        # Keeps track of all moves
        self.move_functions = {"R": self.add_rook_moves, "N": self.add_knight_moves, "B": self.add_bishop_moves,
                               "Q": self.add_queen_moves, "K": self.add_king_moves, "P": self.add_pawn_moves}
        # Dictionary of which piece (Value) corresponds to which function to find possible moves (Key)
        self.white_king_location = [7, 4]
        self.black_king_location = [0, 4]
        # Updating rows and columns of both kings (used for checks, castling, checkmate ect.)
        self.checkmate = False
        self.stalemate = False
        self.enpassant_square = ()
        # Coords of the one possible enpassant square for any position
        # (the square that the opposing pawn would move to in the event of enpassant)
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs)]

    def make_move(self, move):
        self.board[move.end_row][move.end_col] = move.piece_moved
        # Places piece on target square
        self.board[move.start_row][move.start_col] = "--"
        # Removes the piece from its square
        self.move_log.append(move)
        # Records the move in the move_log
        self.white_to_move = not self.white_to_move
        # Changes whose turn it is to play

        # KINGS
        # Update Kings' position
        if move.piece_moved == "wK":
            self.white_king_location = [move.end_row, move.end_col]
        elif move.piece_moved == "bK":
            self.black_king_location = [move.end_row, move.end_col]

        # Castling
        if move.is_castling:
            if move.end_col - move.start_col == 2:
                # King moved to the right two, (kingside castling)
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                # Moves the rook to the right of the final position of the king to the left of the final
                # position of the king
                self.board[move.end_row][move.end_col + 1] = "--"
                # Removes the rook from the right of the final position of the king

            else:
                # Queenside Castle
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                # Moves the rook two squares to the left of the final position of the king directly to the right
                # of the king
                self.board[move.end_row][move.end_col - 2] = "--"
                # Removes the rook two squares to the left of the final position of the king from the board

        # Update castle rights
        self.update_caste_rights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                   self.current_castling_rights.wqs, self.current_castling_rights.bqs))

        # PAWNS
        # Promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"
            # Logic becomes very messy if we ask the user what they would like to promote to

        # Enpassant
        if move.is_enpassant:
            self.board[move.start_row][move.end_col] = "--"
            print("enpassant")
            # Removes the pawn behind the enpassant square

        # Update is_enpassant variable
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
            # "If the piece is a pawn, and it just advanced twice:"
            self.enpassant_square = ((move.start_row + move.end_row)//2, move.start_col)
        else:
            self.enpassant_square = ()

    def undo_move(self):
        # Undoes the most recent move, can be executed consecutively
        if len(self.move_log) != 0:
            # "if it is not the first move:"
            move = self.move_log.pop()
            # .pop() returns AND removes the last element of a list
            self.board[move.start_row][move.start_col] = move.piece_moved
            # Places the most recently moved piece back onto its previous square
            self.board[move.end_row][move.end_col] = move.piece_captured
            # Replaces the most recently captured piece
            self.white_to_move = not self.white_to_move
            # Flips whose turn it is

            # PAWNS
            # Enpassant
            if move.is_enpassant:
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.board[move.end_row][move.end_col] = "--"
                self.enpassant_square = (move.end_row, move.end_col)

            # Two square pawn advance
            if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.enpassant_square = ()

            # KINGS
            # Update king's position
            if move.piece_moved == "wK":
                self.white_king_location = [move.start_row, move.start_col]
            elif move.piece_moved == "bK":
                self.black_king_location = [move.start_row, move.start_col]

            # Undo Castling Rights
            self.castle_rights_log.pop()
            last_rights = self.castle_rights_log[-1]
            self.current_castling_rights = CastleRights(last_rights.wks, last_rights.bks,
                                                        last_rights.wqs, last_rights.bqs)

            if move.is_castling:
                if move.end_col - move.start_col == 2:
                    # King moves two squares to the right (from whites POV) -> "if kingside castling:"
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:
                    # Queenside
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"

        self.checkmate = False
        self.stalemate = False

    def update_caste_rights(self, move):
        if move.piece_moved == "wK":
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.piece_moved == "bK":
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.piece_moved == "wR":
            if move.start_row == 7:
                if move.start_col == 0:
                    # Left Rook
                    self.current_castling_rights.wqs = False
            elif move.start_row == 7:
                if move.start_col == 7:
                    # Right Rook
                    self.current_castling_rights.wks = False
        elif move.piece_moved == "bR":
            if move.start_row == 0:
                if move.start_col == 0:
                    # Left Rook
                    self.current_castling_rights.bqs = False
            elif move.start_row == 0:
                if move.start_col == 7:
                    # Right Rook
                    self.current_castling_rights.bks = False

    def get_valid_moves(self):
        """
        Gets all moves considering checks (adds castling)
        """
        temp_enpassant_square = self.enpassant_square
        temp_current_castle_rights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                  self.current_castling_rights.bks, self.current_castling_rights.bqs)
        # 1. get all possible moves
        possible_moves = self.get_possible_moves()
        if self.white_to_move:
            self.add_castling_moves(self.white_king_location[0], self.white_king_location[1], possible_moves)
        else:
            self.add_castling_moves(self.black_king_location[0], self.black_king_location[1], possible_moves)

        # 2. for each move, make the move
        for i in range(len(possible_moves)-1, -1, -1):
            # Goes through list backwards
            self.make_move(possible_moves[i])
            # NOTE: THIS SWITCHED WHOSE TURN IT WAS
            # -> Switch back:
            self.white_to_move = not self.white_to_move

        # 3. get all opponent's possible moves
            if self.in_check():
                possible_moves.remove(possible_moves[i])

            # 4. if they do, the original move was not valid
            self.white_to_move = not self.white_to_move
            self.undo_move()

        # 5. Check for Checkmate and Stalemate
        if len(possible_moves) == 0:
            # Either checkmate or stalemate
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            # reverts checkmate and stalemate to false if a move is undone
            self.checkmate = False
            self.stalemate = False
        self.enpassant_square = temp_enpassant_square
        self.current_castling_rights = temp_current_castle_rights

        return possible_moves

    def in_check(self):
        """
        Checks to see if a king is in check
        """
        if self.white_to_move:
            return self.sq_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.sq_under_attack(self.black_king_location[0], self.black_king_location[1])

    def sq_under_attack(self, r, c):
        """
        Checks to see if a square (r, c) is under attack
        """
        self.white_to_move = not self.white_to_move
        # switches to opponents POV

        opp_possible_moves = self.get_possible_moves()
        # Gets all of opponent's moves
        self.white_to_move = not self.white_to_move
        # Switches back to normal POV

        for m in opp_possible_moves:
            if m.end_row == r and m.end_col == c:
                return True
        return False

    def get_possible_moves(self):
        """
        Gets all moves without considering checks
        """
        possible_moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                # Look through all pieces with row r and column c for all r and c
                color = self.board[r][c][0]
                # Either "w" or "b"
                if (color == "w" and self.white_to_move) or (color == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    # "R", "N", "B", "Q", "K", or "P"
                    self.move_functions[piece](r, c, possible_moves, "b" if self.white_to_move else "w")

        return possible_moves

    def add_rook_moves(self, r, c, possible_moves, enemy_color):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        # Up, left, down, right

        self.add_directional_moves(r, c, possible_moves, enemy_color, directions)

    def add_knight_moves(self, r, c, possible_moves, enemy_color):
        squares = ((-2, 1), (-2, -1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        # All possible squares

        for s in squares:
            for i in range(1, len(self.board)):
                end_row = r + s[0]
                end_col = c + s[1]

                if (0 <= end_row <= (len(self.board) - 1)) and (0 <= end_col <= (len(self.board) - 1)):
                    # on board
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":
                        # Blank
                        possible_moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        # Enemy Piece
                        possible_moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        # Friendly piece
                        break
                else:
                    # Off board
                    break

    def add_bishop_moves(self, r, c, possible_moves, enemy_color):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        # Up-left, up-right, down-left, down-right

        self.add_directional_moves(r, c, possible_moves, enemy_color, directions)

    def add_queen_moves(self, r, c, possible_moves, enemy_color):
        self.add_rook_moves(r, c, possible_moves, enemy_color)
        self.add_bishop_moves(r, c, possible_moves, enemy_color)

    def add_king_moves(self, r, c, possible_moves, enemy_color):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        # Up-left, up-right, down-left, down-right

        for d in directions:
            for i in range(1, len(self.board)):
                end_row = r + d[0]
                end_col = c + d[1]

                if (0 <= end_row <= (len(self.board) - 1)) and (0 <= end_col <= (len(self.board) - 1)):
                    # on board
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":
                        # Blank
                        possible_moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        # Enemy Piece
                        possible_moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        # Friendly piece
                        break
                else:
                    # Off board
                    break

    def add_pawn_moves(self, r, c, possible_moves, enemy_color):
        """
        Gets possible pawn moves, without considering checks for a given pawn
        """

        if self.white_to_move:
            # White pawns
            if self.board[r-1][c] == "--":
                # Square above is empty
                possible_moves.append(Move((r, c), (r-1, c), self.board))
                # Advance one square

                if (r == 6) and (self.board[r-2][c] == "--"):
                    # Two squares above are empty and pawn is on the 6th row (2nd rank)
                    possible_moves.append(Move((r, c), (r-2, c), self.board))
                    # Advance two squares

            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    # Black piece to the left and up
                    possible_moves.append(Move((r, c), (r-1, c-1), self.board))
                    # Capture black piece

                elif (r-1, c-1) == self.enpassant_square:
                    possible_moves.append(Move((r, c), (r-1, c-1), self.board, is_enpassant=True))

            if c+1 <= len(self.board) - 1:
                if self.board[r-1][c+1][0] == "b":
                    # Black piece to the right and up
                    possible_moves.append(Move((r, c), (r-1, c+1), self.board))

                elif (r-1, c+1) == self.enpassant_square:
                    possible_moves.append(Move((r, c), (r-1, c+1), self.board, is_enpassant=True))

        if not self.white_to_move:
            # Black pawns
            if self.board[r+1][c] == "--":
                possible_moves.append(Move((r, c), (r+1, c), self.board))

                if (r == 1) and (self.board[r+2][c] == "--"):
                    possible_moves.append(Move((r, c), (r+2, c), self.board))

            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    possible_moves.append(Move((r, c), (r+1, c-1), self.board))

                elif (r+1, c-1) == self.enpassant_square:
                    possible_moves.append(Move((r, c), (r+1, c-1), self.board, is_enpassant=True))

            if c+1 <= len(self.board) - 1:
                if self.board[r+1][c+1][0] == "w":
                    possible_moves.append(Move((r, c), (r+1, c+1), self.board))

                elif (r+1, c+1) == self.enpassant_square:
                    possible_moves.append(Move((r, c), (r+1, c+1), self.board, is_enpassant=True))

    def add_directional_moves(self, r, c, possible_moves, enemy_color, directions):
        for d in directions:
            for i in range(1, len(self.board)):
                end_row = r + d[0] * i
                end_col = c + d[1] * i

                if (0 <= end_row <= (len(self.board) - 1)) and (0 <= end_col <= (len(self.board) - 1)):
                    # on board
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":
                        # Blank
                        possible_moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        # Enemy Piece
                        possible_moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        # Friendly piece
                        break
                else:
                    # Off board
                    break

    def add_castling_moves(self, king_r, king_c, possible_moves):
        if self.sq_under_attack(king_r, king_c):
            # The in_check() method could have also been used without king_r and king_c
            return
            # We cannot castle if we are in check

        if ((self.white_to_move and self.current_castling_rights.wks) or
                (not self.white_to_move and self.current_castling_rights.bks)):
            self.add_kingside_castle_moves(king_r, king_c, possible_moves)

        if ((self.white_to_move and self.current_castling_rights.wqs) or
                (not self.white_to_move and self.current_castling_rights.bqs)):
            self.add_queenside_castle_moves(king_r, king_c, possible_moves)

    def add_kingside_castle_moves(self, r, c, possible_moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if (not self.sq_under_attack(r, c+1)) and (not self.sq_under_attack(r, c+2)):
                possible_moves.append(Move((r, c), (r, c+2), self.board, is_castling=True))
            # The two squares to the left of the king are empty

    def add_queenside_castle_moves(self, r, c, possible_moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if (not self.sq_under_attack(r, c-1)) and (not self.sq_under_attack(r, c-2)):
                possible_moves.append(Move((r, c), (r, c-2), self.board, is_castling=True))


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {k: v for v, k in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {k: v for v, k in files_to_cols.items()}
    # Conversions

    def __init__(self, start_sq, end_sq, board, is_enpassant=False, is_castling=False):
        # start_sq and end_sq are a two element tuples, and the board is a 2d list of where all pieces are.
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        # PAWNS
        # Promotion
        self.is_pawn_promotion = False
        if (self.piece_moved == "wP" and self.end_row == 0) or (self.piece_moved == "bP" and self.end_row == 7):
            self.is_pawn_promotion = True

        # Enpassant
        self.is_enpassant = is_enpassant
        if self.is_enpassant:
            self.piece_captured = "bP" if self.piece_moved == "wP" else "wP"

        # KINGS
        self.is_castling = is_castling

        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # 4-digit number representing the starting square and ending square for every move

    def __eq__(self, other):
        # this in a way defines what it means for two instances of "Move" to be equivalent: their ids are equal
        # this is called "overriding the 'equals' method"
        if isinstance(other, Move):
            return self.move_id == other.move_id
        else:
            return False

    def get_sudo_chess_notation(self):
        ##########################################################################################################
        # Can make proper chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_chess_notation(self):
        # Check if more than one piece of the same color and same piece type can move to that square
        # Check if move is a capture / enpassant
        # Use "x"
        # Check if move is a check
        # append "+"
        # Check if move is a checkmate
        # remove "+" and append "#"
        # Else just use piece and coords
        pass

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
