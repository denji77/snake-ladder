import os

def display_board(player1_pos, player2_pos):
    os.system('cls')  # Use 'cls' for Windows
    board = [" " for _ in range(100)]
    board[player1_pos - 1] = "1"
    board[player2_pos - 1] = "2"
    
    for i in range(10):
        print(" | ".join(board[i*10:(i+1)*10]))
        print("-" * 41)

def read_board_state():
    with open("board_state.txt", "r") as f:
        positions = f.readline().strip().split()
        return int(positions[0]), int(positions[1])

if __name__ == "__main__":
    player1_pos, player2_pos = read_board_state()
    display_board(player1_pos, player2_pos)
