"""
This is the main driver file. It is responsible for handling user input and displaying the current GameState
"""
import pygame as p
from Chess import ChessEngine, ChessAI as ai


WIDTH = HEIGHT = 512
DIMENSION = 8
# Length of Chess Board (typically 8x8)
SQ_SIZE = HEIGHT // DIMENSION
# The length and height of each square in pixels
MAX_FPS = 15
IMAGES = {}


def load_images():
    """
    Initiates a global dictionary of images
    """
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wP", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: Images can now be accessed by reference of "IMAGE[piece]


def main():
    """
    User input and graphics
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    # checking for valid moves is very expensive, thus we should only check right after each move,
    # this is "flagged" by a "flag variable" called "move_made"

    load_images()
    # only do this once

    running = True

    sq_selected = ()
    # keeps track of most recent click
    player_clicks = []
    # keeps a list of most recent two clicks

    game_over = False

    player_one = True
    # White
    player_two = False
    # Black
    # True if white is human, false if AI

    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mouse Handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sq_selected == (row, col):
                        # "if the previously selected square is selected again", unselect the square
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)

                    if len(player_clicks) == 2:
                        # if the user has selected two squares (they have decided what they want to move and where)
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print("attempted move: " + move.get_sudo_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True

                                sq_selected = ()
                                player_clicks = []
                                # Resets click history
                        if not move_made:
                            player_clicks = [sq_selected]

            # Key Handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
                    # undoing a move should be treated as a move because it flips whose turn it is,
                    # and the engine needs to re-analyze the position
                elif e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    gs.white_to_move = True
                    game_over = False

            # ai Move maker
            if not game_over and not human_turn:
                ai_move = ai.min_max(gs, gs.get_valid_moves())
                if ai_move is None:
                    ai_move = ai.find_random_move(valid_moves)
                gs.make_move(ai_move)
                move_made = True

            if move_made:
                valid_moves = gs.get_valid_moves()
                move_made = False

            draw_game_state(screen, gs, valid_moves, sq_selected)

            if gs.checkmate:
                game_over = True
                if gs.white_to_move:
                    draw_text(screen, "Black wins by checkmate!")
                if not gs.white_to_move:
                    draw_text(screen, "White wins by checkmate!")
            elif gs.stalemate:
                game_over = True
                draw_text(screen, "Stalemate")

            clock.tick(MAX_FPS)
            p.display.flip()


def highlight_sqs(screen, gs, valid_moves, sq_selected):
    """
    highlights squares that a piece can move to
    """
    if sq_selected != ():
        # If they select a non-empty square
        r, c = sq_selected
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
            # A piece that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            # Transparency Value
            s.fill(p.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # Fills in the selected square

            s.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))


def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen)
    highlight_sqs(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, 0, p.Color("Red"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2,
                                                     HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)


if __name__ == "__main__":
    main()
