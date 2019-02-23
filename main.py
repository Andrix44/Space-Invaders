import sys
import subprocess
import time

from system import Interpreter, Intel8080
import hotcode

try:
    import pygame
except:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'pygame'])
    import pygame

CLOCKSPEED = 2000000
REFRESH_RATE = 60
CYCLES_PER_FRAME = CLOCKSPEED // REFRESH_RATE
CYCLES_PER_HALF_FRAME = CYCLES_PER_FRAME // 2

class EmuCore():
    def __init__(self, path, cpudiag=False):
        pygame.init()
        self.native = pygame.Surface((224, 256))
        self.scaled = pygame.display.set_mode((672, 768))
        pygame.display.set_icon(pygame.image.load("icon.bmp"))
        pygame.display.set_caption("Space Invaders")
        pygame.event.set_allowed(None)
        pygame.event.set_allowed((pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT))

        self.i8080 = Intel8080()
        self.i8080.cpudiag = cpudiag
        self.i8080.LoadROM(path)
        self.interp = Interpreter()

    def RunFrame(self):
        interrupt_1 = True
        cycles = cycle_tot = cycle_var = 0
        while(cycle_tot <= CYCLES_PER_FRAME):
            cycles = self.interp.ExecInstr(self.i8080)
            cycle_tot += cycles
            cycle_var += cycles

            if(cycle_var >= CYCLES_PER_HALF_FRAME - 19 and self.i8080.interrupt):  # Make sure the second interrupt gets called by making the first execute a bit earlier
                if(interrupt_1):
                    self.interp.GenerateInterrupt(self.i8080, 1)
                    interrupt_1 = False
                    cycle_var = 0
                else:
                    self.interp.GenerateInterrupt(self.i8080, 2)

    def DrawFrame(self):  # todo: Add colors
        self.native.fill(pygame.Color(0, 0, 0, 0))
        hotcode.GenBitmap(self.native, self.i8080.memory)
        pygame.transform.scale(self.native, (672, 768), self.scaled)
        pygame.display.update()

    def Run(self):
        clock = pygame.time.Clock()
        while(True):
            clock.tick(REFRESH_RATE)
            self.HandleEvents()
            self.RunFrame()
            self.DrawFrame()

    def HandleEvents(self):
        for event in pygame.event.get():
            """
            Controls: Player 1: A - left    Player 2 : left arrow  - left
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
            """
            if(event.type == pygame.KEYDOWN):  # A.W.D for player 1, left.up.right for player 2
                key = pygame.key.name(event.key)
                if(key == "a"): self.i8080.input_byte_1 |= 0b00100000
                elif(key == "d"): self.i8080.input_byte_1 |= 0b01000000
                elif(key == "w"): self.i8080.input_byte_1 |= 0b00010000
                elif(key == "e"): self.i8080.input_byte_1 |= 0b00000100
                elif(key == "left"): self.i8080.input_byte_2 |= 0b00100000
                elif(key == "right"): self.i8080.input_byte_2 |= 0b01000000
                elif(key == "up"): self.i8080.input_byte_2 |= 0b00010000
                elif(key == "right ctrl"): self.i8080.input_byte_1 |= 0b00000010
                elif(key == "space"): self.i8080.input_byte_2 |= 0b00000100
                # Dipswitches(they don't need a keyup event) and exit:
                elif(key == "return"): self.i8080.input_byte_1 &= 0b11111110
                elif(key == "`"): self.i8080.input_byte_2 &= 0b11111100
                elif(key == "1"): self.i8080.input_byte_2 &= 0b11111100; self.i8080.input_byte_2 += 1
                elif(key == "2"): self.i8080.input_byte_2 &= 0b11111100; self.i8080.input_byte_2 += 2
                elif(key == "3"): self.i8080.input_byte_2 &= 0b11111100; self.i8080.input_byte_2 += 3
                elif(key == "4"): self.i8080.input_byte_2 |= 0b00001000
                elif(key == "5"): self.i8080.input_byte_2 &= 0b11110111
                elif(key == "6"): self.i8080.input_byte_2 |= 0b10000000
                elif(key == "7"): self.i8080.input_byte_2 &= 0b01111111
                elif(key == "escape"): sys.exit(0)
            elif(event.type == pygame.KEYUP):
                key = pygame.key.name(event.key)
                if(key == "a"): self.i8080.input_byte_1 &= 0b11011111
                elif(key == "d"): self.i8080.input_byte_1 &= 0b10111111
                elif(key == "w"): self.i8080.input_byte_1 &= 0b11101111
                elif(key == "e"): self.i8080.input_byte_1 &= 0b11111011
                elif(key == "left"): self.i8080.input_byte_2 &= 0b11011111
                elif(key == "right"): self.i8080.input_byte_2 &= 0b10111111
                elif(key == "up"): self.i8080.input_byte_2 &= 0b11101111
                elif(key == "right ctrl"): self.i8080.input_byte_1 &= 0b11111101
                elif(key == "space"): self.i8080.input_byte_2 &= 0b11111011
                elif(key == "return"): self.i8080.input_byte_1 |= 0b1
            elif(event.type == pygame.QUIT):
                sys.exit(0)

if __name__ == '__main__':
    cpudiag = False
    try:
        sys.argv[2]
        cpudiag = True
    except:
        try:
            sys.argv[1]
        except:
            print("Please enter the ROM path as an argument")
            sys.exit(1)

    if(cpudiag):
        core = EmuCore(sys.argv[1], sys.argv[2])
    else:
        core = EmuCore(sys.argv[1])
    core.Run()
