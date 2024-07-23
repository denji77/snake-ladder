#include <iostream>
#include <cstdlib>
#include <ctime>
#include <fstream>
using namespace std;

const int WINNING_POSITION = 100;

int rollDice() {
    return (rand() % 6) + 1;
}

void displayBoardState(int player1Pos, int player2Pos) {
    ofstream boardFile("board_state.txt");
    boardFile << player1Pos << " " << player2Pos << endl;
    boardFile.close();
}

int main() {
    srand(time(0));
    int player1Pos = 0, player2Pos = 0;
    int currentPlayer = 1;
    int diceRoll;

    int snake[101] = {0};
    int ladder[101] = {0};

    // snakes
    snake[16] = 6;
    snake[47] = 26;
    snake[49] = 11;
    snake[56] = 53;
    snake[62] = 19;
    snake[64] = 60;
    snake[87] = 24;
    snake[93] = 73;
    snake[95] = 75;
    snake[98] = 78;

    // ladders
    ladder[1] = 38;
    ladder[4] = 14;
    ladder[9] = 31;
    ladder[21] = 42;
    ladder[28] = 84;
    ladder[36] = 44;
    ladder[51] = 67;
    ladder[71] = 91;
    ladder[80] = 100;

    while (player1Pos < WINNING_POSITION && player2Pos < WINNING_POSITION) {
        cout << "Player " << currentPlayer << "'s turn. Press Enter to roll the dice.";
        cin.ignore();
        diceRoll = rollDice();
        cout << "Player " << currentPlayer << " rolled a " << diceRoll << endl;

        if (currentPlayer == 1) {
            player1Pos += diceRoll;
            player1Pos = (player1Pos > WINNING_POSITION) ? (player1Pos - diceRoll) : player1Pos;
            player1Pos = (snake[player1Pos] != 0) ? snake[player1Pos] : player1Pos;
            player1Pos = (ladder[player1Pos] != 0) ? ladder[player1Pos] : player1Pos;
            currentPlayer = 2;
        } else {
            player2Pos += diceRoll;
            player2Pos = (player2Pos > WINNING_POSITION) ? (player2Pos - diceRoll) : player2Pos;
            player2Pos = (snake[player2Pos] != 0) ? snake[player2Pos] : player2Pos;
            player2Pos = (ladder[player2Pos] != 0) ? ladder[player2Pos] : player2Pos;
            currentPlayer = 1;
        }

        displayBoardState(player1Pos, player2Pos);
        system("python display_board.py");
    }

    cout << ((player1Pos >= WINNING_POSITION) ? "Player 1 wins!" : "Player 2 wins!") << endl;

    return 0;
}
