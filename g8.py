import pygame
import chess
import sys

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 640, 700  # extra height for buttons
SQ_SIZE = WIDTH // 8
LIGHT, DARK = (240, 217, 181), (181, 136, 99)
HIGHLIGHT_COLOR = (118, 150, 86, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess (Legal Moves)")

# Load images
def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk',
              'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    images = {}
    for piece in pieces:
        img = pygame.image.load(f"images/{piece}.png")
        images[piece] = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))
    return images

images = load_images()

# Chess engine
board = chess.Board()

# Font for messages
font = pygame.font.SysFont("comicsansms", 36)
small_font = pygame.font.SysFont("comicsansms", 28)

# Mapping for drawing
def piece_to_str(piece):
    if piece is None:
        return ''
    color = 'w' if piece.color == chess.WHITE else 'b'
    kind = piece.symbol().lower()
    return color + kind

# Draw the board, pieces, buttons and messages
def draw_board(selected_square=None, legal_moves=[], message=None):
    # Draw board squares and pieces
    for r in range(8):
        for c in range(8):
            color = LIGHT if (r + c) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (c*SQ_SIZE, r*SQ_SIZE+60, SQ_SIZE, SQ_SIZE))

            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            piece_str = piece_to_str(piece)
            if piece_str:
                screen.blit(images[piece_str], (c*SQ_SIZE, r*SQ_SIZE+60))

    # Highlight selected square and legal moves
    if selected_square is not None:
        col = chess.square_file(selected_square)
        row = 7 - chess.square_rank(selected_square)
        s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT_COLOR)
        screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE+60))

        for move in legal_moves:
            to_square = move.to_square
            col = chess.square_file(to_square)
            row = 7 - chess.square_rank(to_square)
            center = (col*SQ_SIZE + SQ_SIZE//2, row*SQ_SIZE + SQ_SIZE//2 + 60)
            pygame.draw.circle(screen, (0, 255, 0), center, 12)

    # Draw message if any
    if message:
        text_surface = font.render(message, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH//2, 30))
        screen.blit(text_surface, text_rect)

    # Draw buttons
    pygame.draw.rect(screen, (70, 130, 180), (20, 10, 140, 40))
    pygame.draw.rect(screen, (70, 130, 180), (WIDTH-160, 10, 140, 40))

    undo_text = small_font.render("Undo Move", True, (255, 255, 255))
    screen.blit(undo_text, (30, 15))

    restart_text = small_font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (WIDTH-140, 15))

def get_square(pos):
    x, y = pos
    col = x // SQ_SIZE
    row = 7 - ((y-60) // SQ_SIZE)
    if 0 <= col < 8 and 0 <= row < 8:
        return chess.square(col, row)
    return None

def main():
    selected_square = None
    running = True
    clock = pygame.time.Clock()
    legal_moves = []
    message = None

    while running:
        draw_board(selected_square, legal_moves, message)
        pygame.display.flip()
        clock.tick(60)

        if board.is_checkmate():
            winner = "White Wins!" if board.turn == chess.BLACK else "Black Wins!"
            message = "Checkmate! "

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Check if undo button clicked
                if 20 <= x <= 160 and 10 <= y <= 50:
                    if len(board.move_stack) > 0:
                        board.pop()
                        selected_square = None
                        legal_moves = []
                        message = None

                # Check if restart button clicked
                elif WIDTH-160 <= x <= WIDTH-20 and 10 <= y <= 50:
                    board.reset()
                    selected_square = None
                    legal_moves = []
                    message = None

                # Click on board
                elif 60 <= y <= HEIGHT:
                    if board.is_game_over():
                        continue

                    square = get_square((x, y))
                    if square is not None:
                        if selected_square is None:
                            piece = board.piece_at(square)
                            if piece and piece.color == board.turn:
                                selected_square = square
                                legal_moves = [move for move in board.legal_moves if move.from_square == selected_square]
                        else:
                            move = chess.Move(selected_square, square)
                            if move in board.legal_moves:
                                board.push(move)
                            selected_square = None
                            legal_moves = []
                            message = None

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
