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


CLOCK = 2000000  # Hz
REFRESH = 60  # Hz

class EmuCore():
    def __init__(self, path, cpudiag=False):
        pygame.init()
        self.native = pygame.Surface((224, 256))
        self.scaled = pygame.display.set_mode((672, 768))
        pygame.display.set_icon(pygame.image.load("icon.bmp"))
        pygame.display.set_caption("Space Invaders")
        pygame.event.set_allowed(None)
        pygame.event.set_allowed((pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT, pygame.USEREVENT))
        pygame.time.set_timer(pygame.USEREVENT, 16)

        self.i8080 = Intel8080()
        self.i8080.cpudiag = cpudiag
        self.i8080.LoadROM(path)
        self.interp = Interpreter()

        self.vram = [0] * (0x3FFF - 0x2400)
        self.last_interrupt_0x8 = 0
        self.last_interrupt_0x10 = 1/120
        self.first_interrupt = True
        self.req_new_frame = False

    def DrawFrame(self):  # todo: Add colors
        self.native.fill(pygame.Color(0, 0, 0, 0))
        hotcode.GenBitmap(self.native, self.i8080.memory)
        pygame.transform.scale(self.native, (672, 768), self.scaled)
        pygame.display.update()
        self.req_new_frame = False

    def HandleEvents(self):
        for event in pygame.event.get():
            if(event.type == pygame.USEREVENT):
                self.req_new_frame = True
            elif(event.type == pygame.KEYDOWN):
                pass # Key handling
            elif(event.type == pygame.KEYUP):
                pass # Key handling
            elif(event.type == pygame.QUIT):
                sys.exit(0)

    def HandleInterrupts(self):
        interrupt_executed = False
        curr_time = time.process_time()  # It should be fine to use this for all of them
        if(((curr_time - self.last_interrupt_0x8) > 1/60) and self.i8080.interrupt and self.first_interrupt):
            self.interp.GenerateInterrupt(self.i8080, 1)
            self.last_interrupt_0x8 = curr_time
            interrupt_executed = True
        elif(((curr_time - self.last_interrupt_0x10) > 1/60) and self.i8080.interrupt and not self.first_interrupt):
            self.interp.GenerateInterrupt(self.i8080, 2)
            self.last_interrupt_0x10 = curr_time
            interrupt_executed = True
        if(interrupt_executed and not self.i8080.interrupt):
            self.first_interrupt = not self.first_interrupt
            interrupt_executed = False

    

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
    hotcode.Run(core)
