import pygame

def DrawFrame(native, memory):
    cdef unsigned int i, j, k
    cdef int index
    for i in range(256):  # Height
        index = 0x2400 + (i << 5)
        for j in range(32):
            vram_byte = memory[index]
            index += 1
            for k in range(8):
                if(vram_byte & 1):
                    native.set_at((i, 255 - j*8 - k), pygame.Color(255, 255, 255, 0))
                vram_byte = vram_byte >> 1
