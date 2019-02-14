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
CYCLES_PER_FRAME = int(CLOCKSPEED / REFRESH_RATE)
CYCLES_PER_HALF_FRAME = int(CYCLES_PER_FRAME / 2)

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

        self.vram = [0] * (0x3FFF - 0x2400)
        self.last_interrupt_0x8 = 0
        self.last_interrupt_0x10 = 1/120
        self.first_interrupt = True

    def RunFrame(self):
        interrupt_1 = True
        cycles = cycle_tot = cycle_var = 0
        while(cycle_tot <= CYCLES_PER_FRAME):
            cycles = self.interp.ExecInstr(self.i8080)
            cycle_tot += cycles
            cycle_var += cycles

            if(cycle_var >= CYCLES_PER_HALF_FRAME - 19 and self.i8080.interrupt):  # Make sure the second interrupt gets called
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
            if(event.type == pygame.KEYDOWN):
                pass # Key handling
            elif(event.type == pygame.KEYUP):
                pass # Key handling
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
