import sys
import os


class Intel8080:
    def __init__(self):
        self.memory = [0] * 0xFFFF
        self.a = self.b = self.c = self.d = self.e = self.h = self.l = 0
        self.S = self.Z = self.AC = self.P = self.C = 0
        self.pc = self.sp = 0
        self.shift_hi = self.shift_lo = self.shift_offset = 0
        self.interrupt = 0

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
        self.operator = ("+", "+ state.C +", "-", "- state.C -", "&", "^", "|")
        self.registers = ("state.b", "state.c", "state.d", "state.e", "state.h", "state.l", "state.memory[(state.h << 8) | state.l]", "state.a")
        self.last_interrupt = [0, 0, 0, True]  # The fourth is for the first time it generates an interrupt
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

    def SetFlagsCalc(self, state, reg_a, op, reg_b, carry=False, auxiliary=True):
        op = f"{reg_a}{op}{reg_b}"
        if(op not in self.cached_operations):
            self.cached_operations[op] = compile(op, "", "eval")
        precise = eval(self.cached_operations[op])
        state.S = (precise & 0x80) >> 7
        state.Z = (precise & 0xFF) == 0
        if(auxiliary and False):  # This is costly and DAA is not implemented anyway so I disabled it
            state.AC = eval(f"{reg_a & 0xF}{op}{reg_b & 0xF} > 0xF")
        state.P = (bin(precise & 0xFF).count('1') % 2) == 0  # todo: maybe I should use the full precise result
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

    def Input(self, state, port):  # Right now it will only run in attract mode because of the hardcoded inputs
        if(port == 0):
            return 1
        elif(port == 1):
            return 0
        elif(port == 2):
            return 0
        elif(port == 3):
            temp = (state.shift_hi << 8) | state.shift_lo
            return (temp >> (8 - state.shift_offset))
    
    def Output(self, state, port):
        if(port == 2):
            state.shift_offset = state.a & 0x7
        elif(port == 4):
            state.shift_lo = state.shift_hi
            state.shift_hi = state.a

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
            sys.exit("DAA unimplemented")
            """ if((state.a & 0xF) > 9 or state.AC):
                state.a = (state.a + 6) & 0xFF
                state.AC = True
                #state.a = self.SetFlagsCalc(state, "state.a", "+", "6")
                if(((state.a & 0xF0) >> 4) > 9 or state.C):
                    state.S = ((state.a + 0x60) & 0x80) >> 7
                    state.C = (state.a + 0x60) > 0xFF
                    state.a = (state.a + 0x60) & 0xFF """

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
                state.memory[state.sp - 2] = (state.S << 7) | (state.Z << 6) | (state.AC << 4) | (state.P << 2) | (state.C << 7)
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
        else:
            state.pc += 3

    def ReturnFromSubroutine(self, state):
        if(self.instr & 0x1):  # RET
            self.SetReturn(state)
            return

        op = (self.instr >> 3) & 0x7
        if(self.CheckCondition(state, op)):  # RNZ, RZ, RNC, RC, RPO, RPE, RP, RM
            self.SetReturn(state)
        else:
            state.pc += 1

    def RST(self, state):  # RST
        addr = self.instr & 0x38
        self.SetCall(state, addr, 1)

    def Interrupt(self, state):
        if((self.instr >> 3) & 0x1):  # EI
            state.interrupt = 1
        else:  # DI
            state.interrupt = 0

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
        self.instr = state.memory[state.pc]

        # print(hex(state.pc))
        # print(hex(state.a), hex(state.b), hex(state.c), hex(state.d), hex(state.e), hex(state.h), hex(state.l), hex(state.pc), hex(state.sp))

        self.instruction_table[self.instr](state)

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

    def GenerateInterrupt(self, state, interrupt):
        sys.exit("Do this properly")  # Maybe with an interrupt returned flag?

        generate = (self.last_interrupt[3] or
                   (state.memory[self.last_interrupt[0] - 1] != self.last_interrupt[1]) or
                   (state.memory[self.last_interrupt[0] - 2] != self.last_interrupt[2]))

        if(generate):
            self.last_interrupt[0] = state.sp
            self.last_interrupt[1] = state.memory[state.sp - 1] = state.pc >> 8
            self.last_interrupt[2] = state.memory[state.sp - 2] = state.pc & 0xFF
            self.last_interrupt[3] = False
            state.sp -= 2
            state.pc = interrupt * 8
            state.interrupt = False
