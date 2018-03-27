# AI Project - Miniature Camelot Game - Fall 2017
## AI
The AI uses an alpha-beta pruning algorithm to determine the moves it will take based on the current game state. The limit to the search of possible moves (nodes generated) is based on the difficulty level. 
## Objective of the Game
The objective of the game is to either capture the castles relative to one's starting position. 
The board arrangement starts from the top left corner. There are 8 columns (0 to 7 starting from the left) and 14 rows (0 to 13 starting from the top). Red-colored areas are not part of the game board.

One way to win is to capture **both** of the castles of the opposing piece
1) White pieces (circled in green) are attempting to capture (13, 3) and (13, 4).
2) Black pieces (circled in blue) are attempting to capture (0, 3) and (0, 4).

Another way to win is to capture all of the other pieces (i.e. white wins if there is at least 1 white piece on the board and 0 black pieces).

Ties only occur when there is only 1 black and white piece.

![alt text](https://github.com/nate0203/AIProject/blob/master/Board.PNG)

## Movement
Pieces can move in any direction if there is a valid move.

There are 3 types of movement:
1) Adjacent Step - If the adjacent square is open (other white and black pieces are not on that location) and valid (on the game board), then the selected piece can move there.
2) Cantering Move - If the same colored piece is adjacent to the selected piece, then the selected piece can jump over the same colored piece to a square that is directly after the same direction of the jump granted that the new location is open and valid.
3) Capturing Move - If an opposing piece is adjacent to the selected piece, then the selected piece could capture the opposing piece by jumping over it and landing at a new location directly after the direction of the jump. Again, this new location must be open and valid.

## Rules/General Gameplay
- **In this implementation of the game, capturing Moves are mandatory**
- White always go first.
- The player faces an AI that makes a move based on the current state of the game.
- The player can pick if they want to go first.
- The player can select the difficulty level.
- The console is the interface to play the game.  
  * Player's turn as seen on the console:
    + The possible pieces that can be moved are shown and one must be selected.
    + The possible moves of the selected piece are shown. The user can go back to select another piece or pick the move.
    + The summary of the move is shown on the console and board.
    + Confirmation is needed to end one's turn to let the AI run.  
  * AI's turn:
    + Summary of the AI's turn including the number of nodes generated, depth limit of the search, pruning in both max and min, and the selected move.
