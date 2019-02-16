# Space-Invaders
An experimental Space Invaders emulator written in Python as an exercise.
## Launching
You need to have Pygame and Cython installed with pip, then you can run build.bat to compile the Cython code. Now you can execute main.py with the path to your rom as an argument.
## Controls
                      Player 1: A - left    Player 2 : left arrow  - left
                                D - right              right arrow - right
                                W - shoot              up arrow    - shoot
                                E - start              right CTRL  - start

                      space       - tilt
                      enter       - insert coin
                      numbers 0-3 - sets the amount of lives to: pressed number + 3
                      numbers 4-5 - bonus life at 4: 1000 points
                                                  5: 1500 points
                      numbers 6-7 - coin info 6: off
                                              7: on
