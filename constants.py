import pygame
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')

# Fonts
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

# Game timing
timer = pygame.time.Clock()
fps = 60

# Game state variables
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
counter = 0
winner = ''
game_over = False
white_ep = (100, 100)
black_ep = (100, 100)
white_promote = False
black_promote = False
promo_index = 100
check = False
castling_moves = []
white_promotions = ['bishop', 'knight', 'rook', 'queen']
black_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False] * 16
black_moved = [False] * 16
move_history = []

# Player IDs (set after login)
player1_id = None
player2_id = None

# Image directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')  # Changed from 'assets/images' to match your path

small_font = pygame.font.SysFont('Arial', 20)  # For small text elements


def load_piece_image(color, piece, size, fallback_size=None):
    """Helper function to load piece images with fallback"""
    if fallback_size is None:
        fallback_size = size

    try:
        img_path = os.path.join(IMAGE_DIR, f'{color} {piece}.png')
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, size)
        return img
    except:
        # Create fallback image
        surf = pygame.Surface(size, pygame.SRCALPHA)
        if color == 'white':
            pygame.draw.circle(surf, (255, 255, 255), (size[0] // 2, size[1] // 2), size[0] // 2 - 5)
            pygame.draw.circle(surf, (200, 200, 200), (size[0] // 2, size[1] // 2), size[0] // 2 - 8)
        else:
            pygame.draw.circle(surf, (50, 50, 50), (size[0] // 2, size[1] // 2), size[0] // 2 - 5)
            pygame.draw.circle(surf, (100, 100, 100), (size[0] // 2, size[1] // 2), size[0] // 2 - 8)

        # Add piece letter
        font = pygame.font.SysFont('Arial', size[0] // 2)
        text = font.render(piece[0].upper(), True, (0, 0, 0) if color == 'white' else (255, 255, 255))
        text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2))
        surf.blit(text, text_rect)
        return surf


# Load all piece images using the helper function
piece_types = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# White pieces
white_images = [
    load_piece_image('white', piece, (80, 80) if piece != 'pawn' else (65, 65))
    for piece in piece_types
]
small_white_images = [
    pygame.transform.scale(img, (45, 45)) for img in white_images
]

# Black pieces
black_images = [
    load_piece_image('black', piece, (80, 80) if piece != 'pawn' else (65, 65))
    for piece in piece_types
]
small_black_images = [
    pygame.transform.scale(img, (45, 45)) for img in black_images
]

# Assign to named variables for easier access
white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop = white_images
black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop = black_images
white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small = small_white_images
black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small = small_black_images