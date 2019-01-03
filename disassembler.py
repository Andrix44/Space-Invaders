import sys

def Disassemble8080(codebuff):
    byte = codebuff[0]
    try:
        single = hex(codebuff[1])
    except:
        single = None
    try:
        double = hex(codebuff[2]) + hex(codebuff[1])[2:]
    except:
        double = None
    oplen = 1 # Lenght of the instruction, default is 1 byte
    print(hex(pc), end = ' ')

    if(byte == 0x0): print('NOP')
    elif(byte == 0x1): print(f'LXI    B,{double}'); oplen = 3
    elif(byte == 0x2): print('STAX   B')
    elif(byte == 0x3): print('INX    B')
    elif(byte == 0x4): print('INR    B')
    elif(byte == 0x5): print('DCR    B')
    elif(byte == 0x6): print(f'MVI    B,{single}'); oplen = 2
    elif(byte == 0x7): print('RLC')
    elif(byte == 0x8): print('NOP')
    elif(byte == 0x9): print('DAD    B')
    elif(byte == 0xA): print('LDAX   B')
    elif(byte == 0xB): print('DCX    B')
    elif(byte == 0xC): print('INR    C')
    elif(byte == 0xD): print('DCR    C')
    elif(byte == 0xE): print(f'MVI    E,{single}'); oplen = 2
    elif(byte == 0xF): print('RRC')
    elif(byte == 0x10): print('NOP')
    elif(byte == 0x11): print(f'LXI    D,{double}'); oplen = 3
    elif(byte == 0x12): print('STAX   D')
    elif(byte == 0x13): print('INX    D')
    elif(byte == 0x14): print('INR    D')
    elif(byte == 0x15): print('DCR    D')
    elif(byte == 0x16): print(f'MVI    D,{single}'); oplen = 2
    elif(byte == 0x17): print('RAL')
    elif(byte == 0x18): print('NOP')
    elif(byte == 0x19): print('DAD    D')
    elif(byte == 0x1A): print('LDAX   D')
    elif(byte == 0x1B): print('DCX    D')
    elif(byte == 0x1C): print('INR    E')
    elif(byte == 0x1D): print('DCR    E')
    elif(byte == 0x1E): print(f'MVI    E,{single}'); oplen = 2
    elif(byte == 0x1F): print('RAR')
    elif(byte == 0x20): print('RIM')
    elif(byte == 0x21): print(f'LXI    H,{double}'); oplen = 3
    elif(byte == 0x22): print(f'SHLD   {double}'); oplen = 3
    elif(byte == 0x23): print('INX    H')
    elif(byte == 0x24): print('INR    H')
    elif(byte == 0x25): print('DCR    H')
    elif(byte == 0x26): print(f'MVI    H,{single}'); oplen = 2
    elif(byte == 0x27): print('DAA')
    elif(byte == 0x28): print('NOP')
    elif(byte == 0x29): print('DAD    H')
    elif(byte == 0x2A): print(f'LHLD   {double}'); oplen = 3
    elif(byte == 0x2B): print('DCX    H')
    elif(byte == 0x2C): print('INR    L')
    elif(byte == 0x2D): print('DCR    L')
    elif(byte == 0x2E): print(f'MVI    L,{single}'); oplen = 2
    elif(byte == 0x2F): print('CMA')
    elif(byte == 0x30): print('SIM')
    elif(byte == 0x31): print(f'LXI    SP,{double}'); oplen = 3
    elif(byte == 0x32): print(f'STA    {double}'); oplen = 3
    elif(byte == 0x33): print('INX    SP')
    elif(byte == 0x34): print('INR    M')
    elif(byte == 0x35): print('DCR    M')
    elif(byte == 0x36): print(f'MVI    M,{single}'); oplen = 2
    elif(byte == 0x37): print('STC')
    elif(byte == 0x38): print('NOP')
    elif(byte == 0x39): print('DAD    SP')
    elif(byte == 0x3A): print(f'LDA    {double}'); oplen = 3
    elif(byte == 0x3B): print('DCX    SP')
    elif(byte == 0x3C): print('INR    A')
    elif(byte == 0x3D): print('DCR    A')
    elif(byte == 0x3E): print(f'MVI    A,{single}'); oplen = 2
    elif(byte == 0x3F): print('CMC')
    elif(byte == 0x40): print('MOV    B,B')
    elif(byte == 0x41): print('MOV    B,C')
    elif(byte == 0x42): print('MOV    B,D')
    elif(byte == 0x43): print('MOV    B,E')
    elif(byte == 0x44): print('MOV    B,H')
    elif(byte == 0x45): print('MOV    B,L')
    elif(byte == 0x46): print('MOV    B,M')
    elif(byte == 0x47): print('MOV    B,A')
    elif(byte == 0x48): print('MOV    C,B')
    elif(byte == 0x49): print('MOV    C,C')
    elif(byte == 0x4A): print('MOV    C,D')
    elif(byte == 0x4B): print('MOV    C,E')
    elif(byte == 0x4C): print('MOV    C,H')
    elif(byte == 0x4D): print('MOV    C,L')
    elif(byte == 0x4E): print('MOV    C,M')
    elif(byte == 0x4F): print('MOV    C,A')
    elif(byte == 0x50): print('MOV    D,B')
    elif(byte == 0x51): print('MOV    D,C')
    elif(byte == 0x52): print('MOV    D,D')
    elif(byte == 0x53): print('MOV    D,E')
    elif(byte == 0x54): print('MOV    D,H')
    elif(byte == 0x55): print('MOV    D,L')
    elif(byte == 0x56): print('MOV    D,M')
    elif(byte == 0x57): print('MOV    D,A')
    elif(byte == 0x58): print('MOV    E,B')
    elif(byte == 0x59): print('MOV    E,C')
    elif(byte == 0x5A): print('MOV    E,D')
    elif(byte == 0x5B): print('MOV    E,E')
    elif(byte == 0x5C): print('MOV    E,H')
    elif(byte == 0x5D): print('MOV    E,L')
    elif(byte == 0x5E): print('MOV    E,M')
    elif(byte == 0x5F): print('MOV    E,A')
    elif(byte == 0x60): print('MOV    H,B')
    elif(byte == 0x61): print('MOV    H,C')
    elif(byte == 0x62): print('MOV    H,D')
    elif(byte == 0x63): print('MOV    H,E')
    elif(byte == 0x64): print('MOV    H,H')
    elif(byte == 0x65): print('MOV    H,L')
    elif(byte == 0x66): print('MOV    H,M')
    elif(byte == 0x67): print('MOV    H,A')
    elif(byte == 0x68): print('MOV    L,B')
    elif(byte == 0x69): print('MOV    L,C')
    elif(byte == 0x6A): print('MOV    L,D')
    elif(byte == 0x6B): print('MOV    L,E')
    elif(byte == 0x6C): print('MOV    L,H')
    elif(byte == 0x6D): print('MOV    L,L')
    elif(byte == 0x6E): print('MOV    L,M')
    elif(byte == 0x6F): print('MOV    L,A')
    elif(byte == 0x70): print('MOV    M,B')
    elif(byte == 0x71): print('MOV    M,C')
    elif(byte == 0x72): print('MOV    M,D')
    elif(byte == 0x73): print('MOV    M,E')
    elif(byte == 0x74): print('MOV    M,H')
    elif(byte == 0x75): print('MOV    M,L')
    elif(byte == 0x76): print('HLT')
    elif(byte == 0x77): print('MOV    M,A')
    elif(byte == 0x78): print('MOV    A,B')
    elif(byte == 0x79): print('MOV    A,C')
    elif(byte == 0x7A): print('MOV    A,D')
    elif(byte == 0x7B): print('MOV    A,E')
    elif(byte == 0x7C): print('MOV    A,H')
    elif(byte == 0x7D): print('MOV    A,L')
    elif(byte == 0x7E): print('MOV    A,M')
    elif(byte == 0x7F): print('MOV    A,A')
    elif(byte == 0x80): print('ADD    B')
    elif(byte == 0x81): print('ADD    C')
    elif(byte == 0x82): print('ADD    D')
    elif(byte == 0x83): print('ADD    E')
    elif(byte == 0x84): print('ADD    H')
    elif(byte == 0x85): print('ADD    L')
    elif(byte == 0x86): print('ADD    M')
    elif(byte == 0x87): print('ADD    A')
    elif(byte == 0x88): print('ADC    B')
    elif(byte == 0x89): print('ADC    C')
    elif(byte == 0x8A): print('ADC    D')
    elif(byte == 0x8B): print('ADC    E')
    elif(byte == 0x8C): print('ADC    H')
    elif(byte == 0x8D): print('ADC    L')
    elif(byte == 0x8E): print('ADC    M')
    elif(byte == 0x8F): print('ADC    A')
    elif(byte == 0x90): print('SUB    B')
    elif(byte == 0x91): print('SUB    C')
    elif(byte == 0x92): print('SUB    D')
    elif(byte == 0x93): print('SUB    E')
    elif(byte == 0x94): print('SUB    H')
    elif(byte == 0x95): print('SUB    L')
    elif(byte == 0x96): print('SUB    M')
    elif(byte == 0x97): print('SUB    A')
    elif(byte == 0x98): print('SBB    B')
    elif(byte == 0x99): print('SBB    C')
    elif(byte == 0x9A): print('SBB    D')
    elif(byte == 0x9B): print('SBB    E')
    elif(byte == 0x9C): print('SBB    H')
    elif(byte == 0x9D): print('SBB    L')
    elif(byte == 0x9E): print('SBB    M')
    elif(byte == 0x9F): print('SBB    A')
    elif(byte == 0xA0): print('ANA    B')
    elif(byte == 0xA1): print('ANA    C')
    elif(byte == 0xA2): print('ANA    D')
    elif(byte == 0xA3): print('ANA    E')
    elif(byte == 0xA4): print('ANA    H')
    elif(byte == 0xA5): print('ANA    L')
    elif(byte == 0xA6): print('ANA    M')
    elif(byte == 0xA7): print('ANA    A')
    elif(byte == 0xA8): print('XRA    B')
    elif(byte == 0xA9): print('XRA    C')
    elif(byte == 0xAA): print('XRA    D')
    elif(byte == 0xAB): print('XRA    E')
    elif(byte == 0xAC): print('XRA    H')
    elif(byte == 0xAD): print('XRA    L')
    elif(byte == 0xAE): print('XRA    M')
    elif(byte == 0xAF): print('XRA    A')
    elif(byte == 0xB0): print('ORA    B')
    elif(byte == 0xB1): print('ORA    C')
    elif(byte == 0xB2): print('ORA    D')
    elif(byte == 0xB3): print('ORA    E')
    elif(byte == 0xB4): print('ORA    H')
    elif(byte == 0xB5): print('ORA    L')
    elif(byte == 0xB6): print('ORA    M')
    elif(byte == 0xB7): print('ORA    A')
    elif(byte == 0xB8): print('CMP    B')
    elif(byte == 0xB9): print('CMP    C')
    elif(byte == 0xBA): print('CMP    D')
    elif(byte == 0xBB): print('CMP    E')
    elif(byte == 0xBC): print('CMP    H')
    elif(byte == 0xBD): print('CMP    L')
    elif(byte == 0xBE): print('CMP    M')
    elif(byte == 0xBF): print('CMP    A')
    elif(byte == 0xC0): print('RNZ')
    elif(byte == 0xC1): print('POP    B')
    elif(byte == 0xC2): print(f'JNZ    {double}'); oplen = 3
    elif(byte == 0xC3): print(f'JMP    {double}'); oplen = 3
    elif(byte == 0xC4): print(f'CNZ    {double}'); oplen = 3
    elif(byte == 0xC5): print('PUSH   B')
    elif(byte == 0xC6): print(f'ADI    {single}'); oplen = 2
    elif(byte == 0xC7): print('RST    0')
    elif(byte == 0xC8): print('RZ')
    elif(byte == 0xC9): print('RET')
    elif(byte == 0xCA): print(f'JZ     {double}'); oplen = 3
    elif(byte == 0xCB): print('NOP')
    elif(byte == 0xCC): print(f'CZ     {double}'); oplen = 3
    elif(byte == 0xCD): print(f'CALL   {double}'); oplen = 3
    elif(byte == 0xCE): print(f'ACI    {single}'); oplen = 2
    elif(byte == 0xCF): print('RST    1')
    elif(byte == 0xD0): print('RNC')
    elif(byte == 0xD1): print('POP    D')
    elif(byte == 0xD2): print(f'JNC    {double}'); oplen = 3
    elif(byte == 0xD3): print(f'OUT    {single}'); oplen = 2
    elif(byte == 0xD4): print(f'CNC    {double}'); oplen = 3
    elif(byte == 0xD5): print('PUSH   D')
    elif(byte == 0xD6): print(f'SUI    {single}'); oplen = 2
    elif(byte == 0xD7): print('RST    2')
    elif(byte == 0xD8): print('RC')
    elif(byte == 0xD9): print('NOP')
    elif(byte == 0xDA): print(f'JC     {double}'); oplen = 3
    elif(byte == 0xDB): print(f'IN     {single}'); oplen = 2
    elif(byte == 0xDC): print(f'CC     {double}'); oplen = 3
    elif(byte == 0xDD): print('NOP')
    elif(byte == 0xDE): print(f'SBI    {single}'); oplen = 2
    elif(byte == 0xDF): print('RST    3')
    elif(byte == 0xE0): print('RPO')
    elif(byte == 0xE1): print('POP    H')
    elif(byte == 0xE2): print(f'JPO    {double}'); oplen = 3
    elif(byte == 0xE3): print('XTHL')
    elif(byte == 0xE4): print(f'CPO    {double}'); oplen = 3
    elif(byte == 0xE5): print('PUSH   H')
    elif(byte == 0xE6): print(f'ANI    {single}'); oplen = 2
    elif(byte == 0xE7): print('RST    4')
    elif(byte == 0xE8): print('RPE')
    elif(byte == 0xE9): print('PCHL')
    elif(byte == 0xEA): print(f'JPE    {double}'); oplen = 3
    elif(byte == 0xEB): print('XCHG')
    elif(byte == 0xEC): print(f'CPE    {double}'); oplen = 3
    elif(byte == 0xED): print('NOP')
    elif(byte == 0xEE): print(f'XRI    {single}'); oplen = 2
    elif(byte == 0xEF): print('RST    5')
    elif(byte == 0xF0): print('RP')
    elif(byte == 0xF1): print('POP    PSW')
    elif(byte == 0xF2): print(f'JP     {double}'); oplen = 3
    elif(byte == 0xF3): print('DI')
    elif(byte == 0xF4): print(f'CP     {double}'); oplen = 3
    elif(byte == 0xF5): print('PUSH   PSW')
    elif(byte == 0xF6): print(f'ORI    {single}'); oplen = 2
    elif(byte == 0xF7): print('RST    6')
    elif(byte == 0xF8): print('RM')
    elif(byte == 0xF9): print('SPHL')
    elif(byte == 0xFA): print(f'JM     {double}'); oplen = 3
    elif(byte == 0xFB): print('EI')
    elif(byte == 0xFC): print(f'CM     {double}'); oplen = 3
    elif(byte == 0xFD): print('NOP')
    elif(byte == 0xFE): print(f'CPI    {single}'); oplen = 2
    elif(byte == 0xFF): print('RST    7')

    else: raise Exception('Something went REALLY wrong!')

    return oplen

with open('cpudiag.bin', 'rb') as rom:
    data = rom.read()
    pc = 0
    while(pc < len(data)):
        if(pc == len(data) - 1):
            codebuff = (data[pc], )
        elif(pc == len(data) - 2):
            codebuff = (data[pc], data[pc + 1])
        else:
            codebuff = (data[pc], data[pc + 1], data[pc + 2])
        oplen = Disassemble8080(codebuff)
        pc += oplen
    input('Press any key to exit...')
