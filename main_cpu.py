import os

from system import Interpreter, Intel8080


romname = 'ROMS/Space Invaders.rom'
i8080 = Intel8080()
i8080.LoadROM(romname)
interp = Interpreter()

with open(romname, 'rb') as rom:
    for i in range(os.path.getsize(romname)):
        i8080.memory[i] = ord(rom.read(1))  # Write ROM to the memory

while(True):
    interp.ExecInstr(i8080)
