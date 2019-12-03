### TicTacToe #pwn

#### inputs 

- `tictactoe ` - ELF 64-bit LSB executable, x86-64 (game frontend) 
- `server.py` - server code (game backend)

#### recon

After connecting to provided host we can see implementation of TicTacToe game:

```console
$ nc pwn-tictactoe.ctfz.one 8889
Welcome to tictactoe game! Please, enter your name: elklepo
                                                                     
+---+---+---+    Session: ATuJ5lkz9qgmxinXMIun5JM2WOWHZn6f           
|   |   |   |                                                        
| X |   |   |     Player: elklepo                                        
|  1|  2|  3|                                                        
|---+---+---|      Level: 1/100                                      
|   |   |   |                                                        
|   |   |   |      Rules: You play with 0s. Now it's your turn.      
|  4|  5|  6|             Enter number 1-9 to make your move.        
|---+---+---|             In order to get the flag you need to win   
|   |   |   |             100 times in a row, buy your enemy is a    
|   |   |   |             really smart AI. Good luck!                
|  7|  8|  9|                                                        
+---+---+---+      Enter your move (1-9):
```

So we have to win 100 games to get the flag. After some manual tries I was not able to win a single game (no surprise here - it's `pwn` task :) ).

Next, I jumped to server code analysis and reverse engineering (symbols were not stripped so it was quite easy). That's how, in simplified way, the game infrastructure works:

```
+-------------------------------player------+
|                                           |
+-------------------------------------------+
  |                    ^
  |                    | board state
  | human_move         | [next/win/lose/flag]
  |                    |
  v                    |
+-------------------------------tictactoe---+
| board_state                               |
+-------------------------------------------+
  |                    ^
  | session_x_id       | [next/win/lose/flag]
  | human move         | board state
  | computer move      |
  v                    |
+-------------------------------server.py---+
| +-session_x----+                          |
| | games won    |                          |
| | board state  |                          |
| +--------------+                          |
+-------------------------------------------+

```

`tictactoe` gets human move and computes computer move basing on board state after human move.

Both human move and computer move are sent to `server.py` which is responsible for moves validation, win/lose decision and informing `tictactoe` that user won 100 games and the flag is available.

When flag availability is signaled, `tictactoe` is sending "get flag" request to `server.py` which sends flag back if 100 games were won (for simplicity - this call is omitted on above diagram).

It is impossible for user to communicate to `server.py` directly so we have to exploit `tictactoe`.

#### tictactoe exploitation

 

