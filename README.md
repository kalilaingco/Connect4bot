# Connect4bot by Kali Ingco, Alyssa Bustos, and Theresa Nguyen 
This is an artificial intelligence agent that will play Connect 4 against a player. This uses the alpha-beta algorithm to pick optimal moves. 
This program references code from the aima-python repository 

link: https://github.com/aimacode/aima-python

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- **Python 3.8+**
- **Git**
- **pip**
   ```bash
  pip install --upgrade pip
  ```

### 1. Install Dependencies

Install the required dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```
### 2. File structure information

#### connect4.py
  This file uses the TicTacToe function from games.py to make the Connect4 game. This file also has the evaluation function, and the function to find the best moves using the alpha-beta pruning algorithm with a depth of 5. Lastly, the file has the query function to get input from the non-agent player. 

#### games.py, search.py, and utils.py
   These files are taken from the aima-python repository and used to get the TicTacToe function, alpha-beta pruning algorithm, search algorithm, etc.

#### ui.py 
   This file created the UI of the game. 

### 3. Running the application

   - ##To run the game without the UI, go to the root of the project and input this command##
   ```bash
connect4.py
```
   Then the game will start, the AI agent will make the first move. To play against the agent, input a valid column number (1-7) and press enter.
   
   - ## To run the game WITH the UI, go to the root of the project and input this command ## 
   ```bash
ui.py
```
   The game will show a brief welcome message, after this you may click on the columns where you'd like to place your piece to play against the agent.




