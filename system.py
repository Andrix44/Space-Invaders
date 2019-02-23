import pygame
import sys
import os


class Intel8080:
    def __init__(self):
        self.memory = [0] * 0xFFFF
        self.a = self.b = self.c = self.d = self.e = self.h = self.l = 0
        self.S = self.Z = self.AC = self.P = self.C = 0
        self.pc = self.sp = 0
        self.shift_hi = self.shift_lo = self.shift_offset = 0
        self.interrupt = False
        self.input_byte_1 = 1
        self.input_byte_2 = 0

        self.cpudiag = False

    def LoadROM(self, path):
        with open(path, 'rb') as rom:
            for i in range(os.path.getsize(path)):
                if(self.cpudiag):
                    self.memory[i + 0x100] = ord(rom.read(1))
                else:
                    self.memory[i] = ord(rom.read(1))

        if(self.cpudiag):
            self.pc = 0x100  # The program starts from 0x100
            self.memory[0x170] = 0x7  # Patch a bug
            self.memory[0x59C] = 0xC3  # Patch the check for DAA
            self.memory[0x59D] = 0xC2  #
            self.memory[0x59E] = 0x5   #


class Interpreter:
    def __init__(self):
        self.condition_met = False

        self.audio_enabled = self.SetupAudio()
        self.last_out_3 = self.last_out_5 = 0


        self.operator = ("+", "+ state.C +", "-", "- state.C -", "&", "^", "|")
        self.registers = ("state.b", "state.c", "state.d", "state.e", "state.h", "state.l", "state.memory[(state.h << 8) | state.l]", "state.a")
        self.cached_operations = {}

        self.instruction_table = (self.NoOperation, self.Immediate, self.DataTransfer,
                                  self.RegisterPair, self.SingleRegister, self.SingleRegister,
                                  self.Immediate, self.RotateAccumulator, self.NoOperation,
                                  self.RegisterPair, self.DataTransfer, self.RegisterPair,
                                  self.SingleRegister, self.SingleRegister, self.Immediate,
                                  self.RotateAccumulator, self.NoOperation, self.Immediate,
                                  self.DataTransfer, self.RegisterPair, self.SingleRegister,
                                  self.SingleRegister, self.Immediate, self.RotateAccumulator,
                                  self.NoOperation, self.RegisterPair, self.DataTransfer,
                                  self.RegisterPair, self.SingleRegister, self.SingleRegister,
                                  self.Immediate, self.RotateAccumulator, self.NoOperation,
                                  self.Immediate, self.DirectAddressing, self.RegisterPair,
                                  self.SingleRegister, self.SingleRegister, self.Immediate,
                                  self.SingleRegister, self.NoOperation, self.RegisterPair,
                                  self.DirectAddressing, self.RegisterPair, self.SingleRegister,
                                  self.SingleRegister, self.Immediate, self.SingleRegister,
                                  self.NoOperation, self.Immediate, self.DirectAddressing,
                                  self.RegisterPair, self.SingleRegister, self.SingleRegister,
                                  self.Immediate, self.CarryBit, self.NoOperation,
                                  self.RegisterPair, self.DirectAddressing, self.RegisterPair,
                                  self.SingleRegister, self.SingleRegister, self.Immediate,
                                  self.CarryBit, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.Halt, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.DataTransfer,
                                  self.DataTransfer, self.DataTransfer, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator, self.RegisterOrMemoryToAccumulator,
                                  self.ReturnFromSubroutine, self.RegisterPair, self.Jump,
                                  self.Jump, self.CallSubroutine, self.RegisterPair,
                                  self.Immediate, self.RST, self.ReturnFromSubroutine,
                                  self.ReturnFromSubroutine, self.Jump, self.NoOperation,
                                  self.CallSubroutine, self.CallSubroutine, self.Immediate,
                                  self.RST, self.ReturnFromSubroutine, self.RegisterPair,
                                  self.Jump, self.InputOutput, self.CallSubroutine,
                                  self.RegisterPair, self.Immediate, self.RST,
                                  self.ReturnFromSubroutine, self.NoOperation, self.Jump,
                                  self.InputOutput, self.CallSubroutine, self.NoOperation,
                                  self.Immediate, self.RST, self.ReturnFromSubroutine,
                                  self.RegisterPair, self.Jump, self.RegisterPair,
                                  self.CallSubroutine, self.RegisterPair, self.Immediate,
                                  self.RST, self.ReturnFromSubroutine, self.Jump,
                                  self.Jump, self.RegisterPair, self.CallSubroutine,
                                  self.NoOperation, self.Immediate, self.RST,
                                  self.ReturnFromSubroutine, self.RegisterPair, self.Jump,
                                  self.Interrupt, self.CallSubroutine, self.RegisterPair,
                                  self.Immediate, self.RST, self.ReturnFromSubroutine,
                                  self.RegisterPair, self.Jump, self.Interrupt,
                                  self.CallSubroutine, self.NoOperation, self.Immediate,
                                  self.RST)

        self.cycle_table = (4, 10, 7,  5,  5,  5,  7,  4,  4, 10, 7,  5,  5,  5,  7, 4,   # 0x0X
                            4, 10, 7,  5,  5,  5,  7,  4,  4, 10, 7,  5,  5,  5,  7, 4,   # 0x1X
                            4, 10, 16, 5,  5,  5,  7,  4,  4, 10, 16, 5,  5,  5,  7, 4,   # 0x2X
                            4, 10, 13, 5,  10, 10, 10, 4,  4, 10, 13, 5,  5,  5,  7, 4,   # 0x3X
                            5, 5,  5,  5,  5,  5,  7,  5,  5, 5,  5,  5,  5,  5,  7, 5,   # 0x4X
                            5, 5,  5,  5,  5,  5,  7,  5,  5, 5,  5,  5,  5,  5,  7, 5,   # 0x5X
                            5, 5,  5,  5,  5,  5,  7,  5,  5, 5,  5,  5,  5,  5,  7, 5,   # 0x6X
                            7, 7,  7,  7,  7,  7,  7,  7,  5, 5,  5,  5,  5,  5,  7, 5,   # 0x7X
                            4, 4,  4,  4,  4,  4,  7,  4,  4, 4,  4,  4,  4,  4,  7, 4,   # 0x8X
                            4, 4,  4,  4,  4,  4,  7,  4,  4, 4,  4,  4,  4,  4,  7, 4,   # 0x9X
                            4, 4,  4,  4,  4,  4,  7,  4,  4, 4,  4,  4,  4,  4,  7, 4,   # 0xAX
                            4, 4,  4,  4,  4,  4,  7,  4,  4, 4,  4,  4,  4,  4,  7, 4,   # 0xBX
                            5, 10, 10, 10, 11, 11, 7,  11, 5, 10, 10, 10, 11, 17, 7, 11,  # 0xCX
                            5, 10, 10, 10, 11, 11, 7,  11, 5, 10, 10, 10, 11, 11, 7, 11,  # 0xDX
                            5, 10, 10, 18, 11, 11, 7,  11, 5, 5,  10, 5,  11, 11, 7, 11,  # 0xEX
                            5, 10, 10, 4,  11, 11, 7,  11, 5, 5,  10, 4,  11, 11, 7, 11)  # 0xFX

    def SetupAudio(self):
        try:
            self.sound_ufo = pygame.mixer.Sound("samples/0.wav")
            self.sound_shot = pygame.mixer.Sound("samples/1.wav")
            self.sound_flash = pygame.mixer.Sound("samples/2.wav")
            self.sound_death = pygame.mixer.Sound("samples/3.wav")
            self.sound_fleet_1 = pygame.mixer.Sound("samples/4.wav")
            self.sound_fleet_2 = pygame.mixer.Sound("samples/5.wav")
            self.sound_fleet_3 = pygame.mixer.Sound("samples/6.wav")
            self.sound_fleet_4 = pygame.mixer.Sound("samples/7.wav")
            self.sound_ufo_hit = pygame.mixer.Sound("samples/8.wav")
            return True
        except:
            print("Error while loading sound samples, please refer to the readme for more info.",
                "Audio disabled.")
            return False

    def GetRegValue(self, state, reg):
        if(reg == 6):  # It might try to access an invalid memory region otherwise
            return state.memory[(state.h << 8) | state.l]
        regs = (state.b, state.c, state.d, state.e, state.h, state.l, None, state.a)
        return regs[reg]

    def SetRegValue(self, state, reg, value):
        if(reg == 0x0):
            state.b = value
        elif(reg == 0x1):
            state.c = value
        elif(reg == 0x2):
            state.d = value
        elif(reg == 0x3):
            state.e = value
        elif(reg == 0x4):
            state.h = value
        elif(reg == 0x5):
            state.l = value
        elif(reg == 0x6):
            state.memory[(state.h << 8) | state.l] = value
        elif(reg == 0x7):
            state.a = value

    def GetPairValue(self, state, pair):
        pairs = ((state.b, state.c), (state.d, state.e), (state.h, state.l))
        if(pair == 3):  # SP
            return state.sp
        else:
            return (pairs[pair][0] << 8) | pairs[pair][1]

    def SetPairValue(self, state, pair, low, high):
        if(pair == 0x0):
            state.b = high
            state.c = low
        elif(pair == 0x1):
            state.d = high
            state.e = low
        elif(pair == 0x2):
            state.h = high
            state.l = low

    def CheckCondition(self, state, condition):
        conds = (not state.Z, state.Z, not state.C, state.C,
                 not state.P, state.P, not state.S, state.S)
        return conds[condition]

    def SetFlagsCalc(self, state, reg_a, operator, reg_b, carry=False, auxiliary=True):
        op = f"{reg_a}{operator}{reg_b}"
        if(op not in self.cached_operations):
            self.cached_operations[op] = compile(op, "", "eval")
        precise = eval(self.cached_operations[op])
        state.S = (precise & 0x80) >> 7
        state.Z = (precise & 0xFF) == 0
        if(auxiliary):
            aux_op = f"(({reg_a} & 0xF) {operator} ({reg_b} & 0xF)) > 0xF"
            if(aux_op not in self.cached_operations):
                self.cached_operations[aux_op] = compile(aux_op, "", "eval")
            state.AC = eval(self.cached_operations[aux_op])
        state.P = (bin(precise & 0xFF).count('1') % 2) == 0
        if(carry):
            state.C = (precise > 0xFF) or (precise < 0)
        return precise & 0xFF

    def SetCall(self, state, addr, instr_len=3):
        state.memory[state.sp - 1] = (state.pc + instr_len) >> 8
        state.memory[state.sp - 2] = (state.pc + instr_len) & 0xFF
        state.sp -= 2
        state.pc = addr

    def SetReturn(self, state):
        state.pc = ((state.memory[state.sp + 1] << 8) | state.memory[state.sp])
        state.sp += 2

    def Input(self, state, port):
        if(port == 1):
            return state.input_byte_1
        elif(port == 2):
            return state.input_byte_2
        elif(port == 3):
            temp = format((state.shift_hi << 8) | state.shift_lo, "016b")
            return int(temp[state.shift_offset: state.shift_offset + 8], 2)

    def Output(self, state, port):
        if(port == 2):
            state.shift_offset = state.a & 0x7
        elif(port == 3):
            if(self.audio_enabled and self.last_out_3 != state.a):
                if(state.a & 1 and not self.last_out_3 & 1):
                    self.sound_ufo.play(-1)
                elif(not state.a & 1 and self.last_out_3 & 1):
                    self.sound_ufo.stop()
                if(state.a & 2 and not self.last_out_3 & 2):
                    self.sound_shot.play()
                if(state.a & 4 and not self.last_out_3 & 4):
                    self.sound_flash.play()
                if(state.a & 8 and not self.last_out_3 & 8):
                    self.sound_death.play()
                self.last_out_3 = state.a
        elif(port == 4):
            state.shift_lo = state.shift_hi
            state.shift_hi = state.a
        elif(port == 5):
            if(self.audio_enabled and self.last_out_5 != state.a):
                if(state.a & 1 and not self.last_out_5 & 1):
                    self.sound_fleet_1.play()
                if(state.a & 2 and not self.last_out_5 & 2):
                    self.sound_fleet_2.play()
                if(state.a & 4 and not self.last_out_5 & 4):
                    self.sound_fleet_3.play()
                if(state.a & 8 and not self.last_out_5 & 8):
                    self.sound_fleet_4.play()
                if(state.a & 16 and not self.last_out_5 & 16):
                    self.sound_ufo_hit.play()
                self.last_out_5 = state.a

############################################################################################################
############################################################################################################

    def CarryBit(self, state):
        if(self.instr == 0x3F):  # CMC
            state.C = not state.C

        elif(self.instr == 0x37):  # STC
            state.C = 1

        state.pc += 1

    def SingleRegister(self, state):
        ver = self.instr & 0x7
        if(ver == 0x4 or ver == 0x5):
            reg = self.instr >> 3
            if(ver == 0x4):  # INR
                op = "+"
            elif(ver == 0x5):  # DCR
                op = "-"
            self.SetRegValue(state, reg, self.SetFlagsCalc(state, self.registers[reg], op, "1"))

        elif(self.instr == 0x2F):  # CMA
            state.a = 0xFF - state.a

        elif(self.instr == 0x27):  # DAA
            if((state.a & 0xF) > 9 or state.AC):
                temp_low = state.a & 0xF
                temp_high = state.a >> 4
                temp_low += 6
                state.AC = temp_low > 0xF
                state.a =  (temp_high << 4) | (temp_low & 0xF)
            if((state.a >> 4) > 9 or state.C):
                temp_low = state.a & 0xF
                temp_high = state.a >> 4
                temp_high += 6
                if(temp_high > 0xF):
                    state.C = True
                state.a =  ((temp_high & 0xF) << 4) | temp_low

        state.pc += 1

    def NoOperation(self, state):
        state.pc += 1

    def DataTransfer(self, state):
        if((self.instr & 0x40) >> 6):  # MOV
            dst = (self.instr >> 3) & 0x7
            src = self.instr & 0x7
            assert(dst != 6 or src != 6)  # The source and destination cannot be both on the memory
            self.SetRegValue(state, dst, self.GetRegValue(state, src))
            state.pc += 1
            return

        regs = self.instr >> 4  # Sets up which register pair to use in the next two instructions

        if(self.instr & 0x40 == 0 and self.instr & 0xF == 0x2):  # STAX
            state.memory[self.GetPairValue(state, regs)] = state.a

        elif(self.instr & 0x40 == 0 and self.instr & 0xF == 0xA):  # LDAX
            state.a = state.memory[self.GetPairValue(state, regs)]

        state.pc += 1

    def RegisterOrMemoryToAccumulator(self, state):
        op = (self.instr >> 3) & 0x7
        reg = self.instr & 0x7

        if(op == 7):  # CMP
            self.SetFlagsCalc(state, "state.a", "-", self.registers[reg], True)
        else:  # ADD, ADC, SUB, SBB, ANA, XRA, ORA
            state.a = self.SetFlagsCalc(state, "state.a", self.operator[op], self.registers[reg], True)

        state.pc += 1

    def RotateAccumulator(self, state):
        if(self.instr == 0x7):  # RLC
            state.C = (state.a & 0x80) >> 7
            state.a = ((state.a << 1) | state.C) & 0xFF

        elif(self.instr == 0xF):  # RRC
            state.C = state.a & 1
            state.a = (state.a >> 1) | (state.C << 7)

        elif(self.instr == 0x17):  # RAL
            temp_C = state.C
            state.C = (state.a & 0x80) >> 7
            state.a = ((state.a << 1) | temp_C) & 0xFF

        elif(self.instr == 0x1F):  # RAR
            temp_C = state.C
            state.C = state.a & 1
            state.a = (state.a >> 1) | (temp_C << 7)

        state.pc += 1

    def RegisterPair(self, state):
        descr = self.instr & 0xCF
        rp = (self.instr >> 4) & 0x3  # Get the register pair to use

        if(descr == 0xC5):  # PUSH
            if(rp == 3):  # PSW
                state.memory[state.sp - 1] = state.a
                state.memory[state.sp - 2] = (state.S << 7) | (state.Z << 6) | (state.AC << 4) | (state.P << 2) | state.C
            else:  # B, D, H
                pair_value = self.GetPairValue(state, rp)
                state.memory[state.sp - 1] = pair_value >> 8
                state.memory[state.sp - 2] = pair_value & 0xFF
            state.sp -= 2

        elif(descr == 0xC1):  # POP
            if(rp == 3):  # PSW
                state.a = state.memory[state.sp + 1]
                flags = state.memory[state.sp]
                state.S = flags >> 7
                state.Z = (flags & 0b01000000) >> 6
                state.AC = (flags & 0b00010000) >> 4
                state.P = (flags & 0b00000100) >> 2
                state.C = flags & 1
            else:  # B, D, H
                low = state.memory[state.sp]
                high = state.memory[state.sp + 1]
                self.SetPairValue(state, rp, low, high)

            state.sp += 2

        elif(descr == 0x9):  # DAD
            HL = self.GetPairValue(state, 2) + self.GetPairValue(state, rp)
            state.C = HL > 0xFFFF
            state.h = (HL >> 8) & 0xFF
            state.l = HL & 0xFF

        elif((descr == 0x3) or (descr == 0xB)):  # INX and DCX
            if(descr == 0x3):  # INX
                result = (self.GetPairValue(state, rp) + 1) & 0xFFFF
            else:  # DCX
                result = (self.GetPairValue(state, rp) - 1) & 0xFFFF

            if(rp == 3):  # SP
                state.sp = result
            else:  # B, D, H
                low = result & 0xFF
                high = result >> 8
                self.SetPairValue(state, rp, low, high)

        elif(self.instr == 0xEB):  # XCHG
            state.h, state.d = state.d, state.h
            state.l, state.e = state.e, state.l

        elif(self.instr == 0xE3):  # XTHL
            state.l, state.memory[state.sp] = state.memory[state.sp], state.l
            state.h, state.memory[state.sp + 1] = state.memory[state.sp + 1], state.h

        elif(self.instr == 0xF9):  # SPHL
            state.sp = (state.h << 8) | state.l

        state.pc += 1

    def Immediate(self, state):
        if(self.instr & 0xCF == 0x1):  # LXI
            rp = (self.instr >> 4) & 0x3
            low = state.memory[state.pc + 1]
            high = state.memory[state.pc + 2]

            if(rp == 3):  # sp
                state.sp = (high << 8) | low
            else:  # B, D, H
                self.SetPairValue(state, rp, low, high)

            state.pc += 1

        elif(self.instr & 0xC7 == 0x6):  # MVI
            reg = (self.instr >> 3) & 0x7
            self.SetRegValue(state, reg, state.memory[state.pc + 1])

        elif(self.instr & 0xC7 == 0xC6):
            if(self.instr == 0xFE):  # CPI
                self.SetFlagsCalc(state, "state.a", "-", "state.memory[state.pc + 1]", True)
            else:  # ADI, ACI, SUI, SBI, ANI, XRI, ORI
                op = (self.instr >> 3) & 0x7
                aux = not(op == 4 or op == 5 or op == 6)  # ANI, XRI, ORI have this disabled
                state.a = self.SetFlagsCalc(state, "state.a", self.operator[op], "state.memory[state.pc + 1]", True, aux)

        state.pc += 2

    def DirectAddressing(self, state):
        op = (self.instr >> 3) & 0x3
        addr = (state.memory[state.pc + 2] << 8) | state.memory[state.pc + 1]

        if(op == 0):  # SHLD
            state.memory[addr] = state.l
            state.memory[addr + 1] = state.h

        elif(op == 1):  # LHLD
            state.l = state.memory[addr]
            state.h = state.memory[addr + 1]

        elif(op == 2):  # STA
            state.memory[addr] = state.a

        elif(op == 3):  # LDA
            state.a = state.memory[addr]

        state.pc += 3

    def Jump(self, state):
        addr = (state.memory[state.pc + 2] << 8) | state.memory[state.pc + 1]

        if(self.instr == 0xE9):  # PCHL
            state.pc = (state.h << 8) | state.l
            return

        elif(self.instr & 0x1):  # JMP
            state.pc = addr
            return

        op = (self.instr >> 3) & 0x7
        if(self.CheckCondition(state, op)):  # JNZ, JZ, JNC, JC, JPO, JPE, JP, JM
            state.pc = addr
        else:
            state.pc += 3

    def CallSubroutine(self, state):
        addr = (state.memory[state.pc + 2] << 8) | state.memory[state.pc + 1]

        if(self.instr & 0x1):  # CALL
            ##########################################################
            if(addr == 0x5):  # Temporary hack for the cpudiag program
                if(state.c == 0x9):
                    offset = ((state.d << 8) | state.e) + 3
                    i = 0
                    output = ""
                    while(not output.endswith("$")):
                        output += chr(state.memory[offset + i])
                        i += 1
                    print(output, hex((state.h << 8) | state.l))
                    state.memory[state.sp - 1] = (state.pc + 3) >> 8
                    state.memory[state.sp - 2] = (state.pc + 3) & 0xFF
                    state.sp -= 2
                    return

                elif(state.c == 0x2):
                    print("Character output routine called")
                    sys.exit(0)
            ##########################################################
            self.SetCall(state, addr)
            return

        op = (self.instr >> 3) & 0x7
        if(self.CheckCondition(state, op)):  # CNZ, CZ, CNC, CC, CPO, CPE, CP, CM
            self.SetCall(state, addr)
            self.condition_met = True
        else:
            state.pc += 3

    def ReturnFromSubroutine(self, state):
        if(self.instr & 0x1):  # RET
            self.SetReturn(state)
            return

        op = (self.instr >> 3) & 0x7
        if(self.CheckCondition(state, op)):  # RNZ, RZ, RNC, RC, RPO, RPE, RP, RM
            self.SetReturn(state)
            self.condition_met = True
        else:
            state.pc += 1

    def RST(self, state):  # RST
        addr = self.instr & 0x38
        self.SetCall(state, addr, 1)

    def Interrupt(self, state):
        if((self.instr >> 3) & 0x1):  # EI
            state.interrupt = True
        else:  # DI
            state.interrupt = False

        state.pc += 1

    def InputOutput(self, state):
        port = state.memory[state.pc + 1]

        if((self.instr >> 3) & 0x1):  # IN
            state.a = self.Input(state, port)
        else:  # OUT
            self.Output(state, port)

        state.pc += 2

    def Halt(self, state):
        sys.exit("Halt not implemented")


############################################################################################################
############################################################################################################

    def ExecInstr(self, state):
        cycles = 0
        self.instr = state.memory[state.pc]

        # print(hex(state.pc))
        # print(hex(state.a), hex(state.b), hex(state.c), hex(state.d), hex(state.e), hex(state.h), hex(state.l), hex(state.pc), hex(state.sp))

        self.instruction_table[self.instr](state)
        cycles = self.cycle_table[self.instr]
        if(self.condition_met):
            cycles += 6
            self.condition_met = False

        """ assert(state.sp > 0x22FF or state.sp == 0)  # If it goes lower, it overwrites data
        assert(state.S == 1 or state.S == 0)
        assert(state.Z == 1 or state.Z == 0)
        assert(state.P == 1 or state.P == 0)
        assert(state.C == 1 or state.C == 0)

        assert(state.pc >= 0 and state.sp <= 0xFFFF)
        assert(state.sp >= 0 and state.sp <= 0xFFFF)

        assert(state.a >= 0 and state.a <= 0xFF)
        assert(state.b >= 0 and state.b <= 0xFF)
        assert(state.c >= 0 and state.c <= 0xFF)
        assert(state.d >= 0 and state.d <= 0xFF)
        assert(state.e >= 0 and state.e <= 0xFF)
        assert(state.h >= 0 and state.h <= 0xFF)
        assert(state.l >= 0 and state.l <= 0xFF) """

        return cycles

    def GenerateInterrupt(self, state, interrupt):
        # print("Entering interrupt", interrupt, "pc=", state.pc, "sp=", state.sp)
        state.memory[state.sp - 1] = state.pc >> 8
        state.memory[state.sp - 2] = state.pc & 0xFF
        state.sp -= 2
        state.pc = interrupt * 8
        state.interrupt = False
