import random

piece_score = {"R": 5, "N": 3, "B": 3, "Q": 9, "K": 0, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def find_best_move(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = CHECKMATE
    # Max score opponent can get
    random.shuffle(valid_moves)

    best_player_move = None
    for player_move in valid_moves:
        # Find opponent's best move
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()
        opponent_max_score = -CHECKMATE
        if gs.stalemate:
            score = STALEMATE
        elif gs.checkmate:
            opponent_max_score = -CHECKMATE
        else:
            for opponent_move in opponent_moves:
                gs.make_move(opponent_move)
                gs.get_valid_moves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = - turn_multiplier * (get_score(gs.board))
                if score > opponent_max_score:
                    opponent_max_score = score
                gs.undo_move()
        if opponent_max_score < opponent_min_max_score:
            # Minimize their best move
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()

    print(best_player_move)
    return best_player_move


def find_best_move_2(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = CHECKMATE
    # Max score opponent can get
    random.shuffle(valid_moves)

    best_player_move = None
    for player_move in valid_moves:
        # Find opponent's best move
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()
        opponent_max_score = -CHECKMATE
        for opponent_move in opponent_moves:
            gs.make_move(opponent_move)
            gs.get_valid_moves()

            score = - turn_multiplier * (get_score(gs.board))
            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()
        if opponent_max_score < opponent_min_max_score:
            # Minimize their best move
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()

    return best_player_move

#
# def self_find_best_move_2(gs, valid_moves):
#     if gs.white_to_move:
#         best_player_move = None
#         for player_move in valid_moves:
#             gs.make_move(player_move)
#             opponent_moves = gs.get_valid_moves()
#             opponent_max_score = -CHECKMATE
#             for opponent_move in opponent_moves:
#                 gs.make_move(opponent_move)
#                 gs.get_valid_moves()
#
#                 score = - get_score(gs.board)
#                 if score > opponent_max_score


def min_max(gs, valid_moves):
    random.shuffle(valid_moves)
    if gs.white_to_move:
        max_score = -CHECKMATE
        # Max score opponent can get

        best_move = None
        for move in valid_moves:
            gs.make_move(move)
            score = get_score(gs.board)
            if score > max_score:
                max_score = score
                best_move = move
            gs.undo_move()

    else:
        max_score = CHECKMATE
        # Max score opponent can get

        best_move = None
        for move in valid_moves:
            gs.make_move(move)
            score = get_score(gs.board)
            if score < max_score:
                max_score = score
                best_move = move
            gs.undo_move()
    return best_move


def min_max_2(gs, valid_moves):
    random.shuffle(valid_moves)

    if gs.white_to_move:
        max_score = -CHECKMATE
        # Max score opponent can get

        best_move = None
        for move in valid_moves:
            gs.make_move(move)
            valid_moves_2 = gs.get_valid_moves()
            for move_2 in valid_moves_2:
                gs.make_move(move_2)
                score = - get_score(gs.board)
                print(score)
                if score > max_score:
                    max_score = score
                    best_move = move
                gs.undo_move()
            gs.undo_move()

    else:
        max_score = CHECKMATE
        # Max score opponent can get

        best_move = None
        for move in valid_moves:
            gs.make_move(move)
            valid_moves_2 = gs.get_valid_moves()
            for move_2 in valid_moves_2:
                gs.make_move(move_2)
                score = get_score(gs.board)
                print(score)
                if score > max_score:
                    max_score = score
                    best_move = move
                gs.undo_move()
            gs.undo_move()
    return best_move


def max_min(gs, valid_moves):
    random.shuffle(valid_moves)
    best_move = None
    score_move_dict = {}
    if gs.white_to_move:
        worst_score = -CHECKMATE
        white_possible_moves = valid_moves
        for white_move in white_possible_moves:
            gs.make_move(white_move)
            black_possible_responses = gs.get_valid_moves()

            white_move_final_results = []

            for black_response in black_possible_responses:
                gs.make_move(black_response)
                final_score = score_board(gs)
                white_move_final_results.append(final_score)
                gs.undo_move()
            score_move_dict[white_move.move_id] = white_move_final_results
            gs.undo_move()

            for j in score_move_dict.keys():
                minimum = -1000
                for i in range(len(score_move_dict[j]) - 1):
                    print((score_move_dict[j])[i])
                    if minimum < (score_move_dict[j])[i]:
                        minimum = (score_move_dict[j])[i]
                        best_move = white_move



        # print(score_move_dict[i] for i in range(len(valid_moves) -1))


            #     if final_score > worst_score:
            #         worst_score = final_score
            #         best_move = white_move
            #     gs.undo_move()
            # gs.undo_move()
    else:
        worst_score = CHECKMATE
        black_possible_moves = valid_moves
        for black_move in black_possible_moves:
            gs.make_move(black_move)
            white_possible_responses = gs.get_valid_moves()
            for white_response in white_possible_responses:
                gs.make_move(white_response)
                final_score = score_board(gs)
                if final_score < worst_score:
                    worst_score = final_score
                    best_move = black_move
                gs.undo_move()
            gs.undo_move()
    return best_move


def find_best_move_min_max(gs, valid_moves):
    global next_move
    next_move = None
    find_move_min_max(gs, valid_moves, DEPTH, gs.white_to_move)
    return next_move


def find_move_min_max(gs, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return get_score(gs.board)

    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score

    else:
        min_score = CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score


def score_board(gs):
    """
    a positive score is good for white, a negative score is good for black
    """
    if gs.checkmate:
        if gs.white_to_move:
            score = -CHECKMATE
        else:
            score = CHECKMATE
    if gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            if square[0] == "b":
                score -= piece_score[square[1]]

    return score


def get_score(board):
    score = 0

    for row in board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            if square[0] == "b":
                score -= piece_score[square[1]]

    return score
