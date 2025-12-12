Othello Board Game Project
===================

Author: Angelos Pappas (Angelosp07)
Licence: MIT Licence





## components.py
### GAME LOGIC:

initialise_board() 
--------------------
initialises the board as a list of lists, and sets the centre pieces.

<img width="711" height="971" alt="initialise_board()" src="https://github.com/user-attachments/assets/8e1a68b8-46a4-478f-bf8c-d9f3ebbaf248" />

legal_move()
--------------------
Checks if the move provided with colour, coordinate, and board is legal in that spot.

<img width="685" height="1058" alt="legal_move()" src="https://github.com/user-attachments/assets/658b4932-2dbd-4cb6-bd7c-4df394596dfc" />

flip_pieces() 
--------------------
Flips all possible pieces of the made move when provided with colour, coordinate, and board.

<img width="831" height="1012" alt="flip_pieces()" src="https://github.com/user-attachments/assets/2138a12f-228e-4942-a26e-9eb4ad122163" />

legal_move_exists() 
--------------------
Applies legal_move() onto each square of the board to check if the current player can move or has to pass.

<img width="567" height="991" alt="legal_move_exists()" src="https://github.com/user-attachments/assets/0fe1b87c-8f77-4f33-9cfb-616f568d0ba5" />

calculate_winner() 
--------------------
Counts the number of each colour's pieces, compares them, returns them and the winner.

<img width="731" height="1033" alt="calculate_winner()" src="https://github.com/user-attachments/assets/2ba35ec9-aa21-4825-b244-7dafbe9a6288" />

### AI SECTION:

find_possible_squares() 
--------------------
Similarly to legal_move_exists() applies legal_move() square by square onto the board and returns a list of tuples containing the coordinates of legal moves for the AI.

<img width="731" height="1033" alt="find_possible_squares()" src="https://github.com/user-attachments/assets/7a9bc7ac-d975-4e58-b68b-8f004143b917" />

count_flipped() 
--------------------
Compares the board before and after the Ai's move and returns the number of flipped pieces.

<img width="682" height="982" alt="count_flipped()" src="https://github.com/user-attachments/assets/f07b4c56-3cf9-4c4e-9a30-86258a29a799" />

ai_move() 
--------------------
Used to count the squares flipped by each possible move for the AI, and applies a small random number (0-1) in order to give the human player a slight advantage, returns 'best' move.

<img width="762" height="1093" alt="ai_move()" src="https://github.com/user-attachments/assets/207b42f6-ded8-4dac-a1fa-557637f2c307" />


## flask_game_engine.py
### API's:

index()
--------------------
Returns the html representation of the board state.

move() 
--------------------
Retrieves (x,y) coords of clicked square, checks if move is legal, applies it if legal and updates the game state.
If the game isn't over the ai makes a move after the player, checks to see if game is over and calculates winner if so.
<img width="909" height="1093" alt="move()" src="https://github.com/user-attachments/assets/91f056cf-5f29-4c6d-b4f8-b36759e09d21" />

restart()
--------------------
Uses initialise_board() to set board to original state, sets colour as dark, finished as False.

<img width="631" height="791" alt="restart()" src="https://github.com/user-attachments/assets/8c25283e-4cf5-4ef2-9ab7-bc3a6ea98bf4" />

save() 
--------------------
Saves game state (board, current colour) to a .json file called 'othello_game_file.json'.

<img width="631" height="791" alt="save()" src="https://github.com/user-attachments/assets/4c937d40-8d0d-43d2-89c2-bf85860ae37b" />

load() 
--------------------
Loads 'othello_game_file.json' and updates game state (board, current colour) with file contents.

<img width="920" height="856" alt="load()" src="https://github.com/user-attachments/assets/1e073992-1033-44e5-a7c5-bf4ebc67b04f" />

## OthelloBoard.html
### JS FUNCTIONS:

restartGame() 
--------------------
calls my /restart api, updates message box

<img width="657" height="762" alt="restartGame()" src="https://github.com/user-attachments/assets/d5e6a9d1-0f09-468b-a117-5673b5e0502f" />

saveGame() 
--------------------
calls my /save api, updates message box


<img width="865" height="499" alt="saveGame()" src="https://github.com/user-attachments/assets/d3fef91f-24d4-49b3-8af1-83def69ee2a2" />

loadGame() 
--------------------
calls my /load api, updates message box


<img width="758" height="882" alt="loadGame()" src="https://github.com/user-attachments/assets/81ba7230-e9e3-4ca8-989c-d228f0fb13e9" />


