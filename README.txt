CHESS PROBLEM PERMUTER
This is a simple script which can perform the following permutations on a chess problem (that is, a starting position followed by a set of moves):
- Mirroring (flip the color of pieces and flip the board vertically)
- Vertical flipping (flip the board along an axis running from left to right. i.e. b2 becomes b6)
- Horizontal flipping (flip the board along an axis running from top to bottom i.e. b2 becomes g2)
- 180 degree rotation (equivalent to vertical and horizontal flipping. b2 becomes g6)
Not all of these permutations can be performed on all problems. In particular,
- Mirroring is possible for all problems
- Horizontal flipping is possible unless the solution requires castling
- Vertical flipping and 180 degree rotation is possibe unless the position includes pawns or the solution requires castling
If the code encounters a problem which cannot be subjected to a given permutation, it simply skips it.

The program takes input in the form of .pgn files placed in the "in" folder (you can put as many there as you want but be warned) and puts outputs in the "out" folder. Which permutations you want performed can be selected using command line arguments (run "python main.py -h" for details) or you can just run the included bat files (sorry linux users). 

Copyright Matthew Tromp 2022. This code is hereby released under a CC-BY 4.0 license: https://creativecommons.org/licenses/by/4.0/legalcode

Requires the chess pip module for python.