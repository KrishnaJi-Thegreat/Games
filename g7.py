import math

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board, player):
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    return [player, player, player] in win_states

def get_empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def minimax(board, depth, is_maximizing):
    if check_win(board, "O"):
        return 1
    if check_win(board, "X"):
        return -1
    if not get_empty_cells(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for r, c in get_empty_cells(board):
            board[r][c] = "O"
            score = minimax(board, depth + 1, False)
            board[r][c] = " "
            best = max(best, score)
        return best
    else:
        best = math.inf
        for r, c in get_empty_cells(board):
            board[r][c] = "X"
            score = minimax(board, depth + 1, True)
            board[r][c] = " "
            best = min(best, score)
        return best

def best_move(board):
    best_score = -math.inf
    move = None
    for r, c in get_empty_cells(board):
        board[r][c] = "O"
        score = minimax(board, 0, False)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

def main():
    board = [[" "]*3 for _ in range(3)]
    print_board(board)

    while True:
        # Human
        r, c = map(int, input("Enter row and col (0-2): ").split())
        if board[r][c] != " ":
            print("Invalid move!")
            continue
        board[r][c] = "X"
        if check_win(board, "X"):
            print_board(board)
            print("You win!")
            break

        if not get_empty_cells(board):
            print("Draw!")
            break

        # AI
        ai_r, ai_c = best_move(board)
        board[ai_r][ai_c] = "O"
        print("AI played:")
        print_board(board)

        if check_win(board, "O"):
            print("AI wins!")
            break
        if not get_empty_cells(board):
            print("Draw!")
            break

if __name__ == "__main__":
    main()
