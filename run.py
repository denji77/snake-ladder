import os
import random
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

# Define board size and cell dimensions
BOARD_SIZE = (500, 500)
CELL_SIZE = BOARD_SIZE[0] // 10  # Assuming a 10x10 board

# Define font and colors
try:
    FONT = ImageFont.truetype("arial.ttf", 20)
except IOError:
    FONT = ImageFont.load_default()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Function to draw a board cell
def draw_cell(draw, row, col, value, color=WHITE):
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    draw.rectangle((x1, y1, x2, y2), fill=color, outline=BLACK)
    bbox = draw.textbbox((0, 0), str(value), font=FONT)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text((x1 + (CELL_SIZE - text_width) // 2, y1 + (CELL_SIZE - text_height) // 2), str(value), fill=BLACK, font=FONT)

# Function to draw snake and ladders
def draw_snakes_ladders(draw, snakes, ladders):
    for head, tail in snakes.items():
        x1, y1 = get_cell_coords(head)
        x2, y2 = get_cell_coords(tail)
        draw.line((x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2, x2 + CELL_SIZE // 2, y2 + CELL_SIZE // 2), fill=RED, width=3)
    for bottom, top in ladders.items():
        x1, y1 = get_cell_coords(bottom)
        x2, y2 = get_cell_coords(top)
        draw.line((x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2, x2 + CELL_SIZE // 2, y2 + CELL_SIZE // 2), fill=GREEN, width=3)

# Function to get cell coordinates from position
def get_cell_coords(position):
    row = 9 - (position - 1) // 10  # Reverse row order for top-down board
    col = 9 - (position - 1) % 10 if row % 2 == 0 else (position - 1) % 10  # Adjust column for snake-like pattern
    return col * CELL_SIZE, row * CELL_SIZE

# Function to update board with player position
def update_board(board, position, player_symbol="@"):
    draw = ImageDraw.Draw(board)
    x, y = get_cell_coords(position)
    bbox = draw.textbbox((0, 0), player_symbol, font=FONT)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text((x + (CELL_SIZE - text_width) // 2, y + (CELL_SIZE - text_height) // 2), player_symbol, fill=BLACK, font=FONT)

# Sample snakes and ladders (modify as needed)
snakes = {58: 6, 49: 11, 99: 21, 84: 47, 70: 42}
ladders = {86: 94, 56: 14, 9: 31, 54: 72, 4: 39}

# Function to create and update the game board image
def create_board(position):
    board = Image.new("RGB", BOARD_SIZE, color=WHITE)
    draw = ImageDraw.Draw(board)

    # Draw the grid
    for i in range(11):
        draw.line((0, i * CELL_SIZE, BOARD_SIZE[0], i * CELL_SIZE), fill=BLACK)
        draw.line((i * CELL_SIZE, 0, i * CELL_SIZE, BOARD_SIZE[1]), fill=BLACK)

    # Draw cell numbers for top-down board
    for i in range(1, 101):
        row = 9 - (i - 1) // 10  # Reverse row order
        col = 9 - (i - 1) % 10 if row % 2 == 0 else (i - 1) % 10  # Adjust column for snake-like pattern
        draw_cell(draw, row, col, i)

    # Draw snakes and ladders
    draw_snakes_ladders(draw, snakes, ladders)

    # Update board with player position
    update_board(board, position, player_symbol="@P1")

    # Save the board image
    board.save("board.png")
    return board

# Roll dice function
def roll_dice():
    return random.randint(1, 6)

# Handle /start command
def start(update: Update, context: CallbackContext):
    context.user_data['position'] = 1
    update.message.reply_text("Welcome to Snakes and Ladders! Use /roll to roll the dice.")

# Handle /roll command
def roll(update: Update, context: CallbackContext):
    roll_value = roll_dice()
    position = context.user_data.get('position', 1)
    new_position = position + roll_value

    # Check for snakes or ladders
    if new_position in snakes:
        new_position = snakes[new_position]
    elif new_position in ladders:
        new_position = ladders[new_position]

    # Update position
    context.user_data['position'] = new_position

    # Create and send board image
    board = create_board(new_position)
    board.save('current_board.png')
    update.message.reply_photo(photo=open('current_board.png', 'rb'), caption=f"You rolled a {roll_value}. Your new position is {new_position}.")

# Main function to start the bot
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("roll", roll))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
