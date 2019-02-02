import sys
import subprocess
import time

from system import Interpreter, Intel8080

try:
    import pygame
except:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'pygame'])
    import pygame


DEBUG = True
CLOCK = 2000000  # Hz
REFRESH = 60  # Hz


def DebugPrint(text):
    if(DEBUG):
        print(text)


def main(path, cpudiag=False):
    pygame.init()
    native = pygame.Surface((224, 256))
    scaled = pygame.display.set_mode((672, 768))
    pygame.display.set_icon(pygame.image.load("icon.bmp"))
    pygame.display.set_caption("Space Invaders")

    pygame.event.set_allowed((pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT))

    i8080 = Intel8080()
    i8080.cpudiag = cpudiag
    i8080.LoadROM(path)
    interp = Interpreter()

    vram = [0]
    last_interrupt = 0

    while(True):
        interp.ExecInstr(i8080)
        if((time.process_time() - last_interrupt) > 1/60 and i8080.interrupt):
            # print(time.process_time() - last_interrupt)
            interp.GenerateInterrupt(i8080, 2) #It keeps reseting the pc to the interrupt before it could finish
            last_interrupt = time.process_time()
        """ elif(i8080.interrupt):
            print("Have to wait more, pc =", hex(i8080.pc)) """

        for event in pygame.event.get():
            if(event.type == pygame.KEYDOWN):
                pass # Key handling
            elif(event.type == pygame.KEYUP):
                pass # Key handling
            elif(event.type == pygame.QUIT):
                return

        if(vram != i8080.memory[0x2400:0x3FFF]):  # Drawing is still broken probably and doesn't have a timer yet
            native.fill(pygame.Color(0, 0, 0, 0))
            for i in range(256):  # Height
                index = 0x2400 + (i << 5)
                for j in range(32):
                    vram_byte = i8080.memory[index]
                    index += 1
                    for k in range(8):
                        if(vram_byte & 1):
                            native.set_at((i, 255 - j*8 - k), pygame.Color(255, 255, 255, 0))
                        vram_byte = vram_byte >> 1
            vram = i8080.memory[0x2400:0x3FFF]
            pygame.transform.scale(native, (672, 768), scaled)
            pygame.display.update()

if __name__ == '__main__':
    cpudiag = False
    try:
        sys.argv[2]
        cpudiag = True
    except:
        try:
            sys.argv[1]
        except:
            sys.exit("Please enter the ROM path as an argument")

    if(cpudiag):
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1])
