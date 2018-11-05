from instructions import makeInstruction

address = 0

print(
    '''
    This program assembles a 8-bit assembly program using mneunomics.
    The assembler is non-case sensitive and White Space is ignored.
    Registers Available :- (R0-R6), Register number should be prefixed with 'R' or 'r'.
    Immediate value should be two digit hexadecimal and prefixed with 0x.
    The Legal instructions available are:\n\n
    ADD RegSrcA, RegSrcB\n
    SUB RegSrcA, RegSrcB\n
    JMP JMP 0xF1 \n
    AND RegSrcA, RegSrcB\n    
    OR RegSrcA, RegSrcB\n    
    MUL RegSrcA, RegSrcB \n
    XOR RegSrcA, RegSrcB\n    
    MOV RegSrcA, RegSrcB or MOV RegSrcA, 0xF1 \n
    LOD RegSrcA, 0xF1 \n
    STR RegSrcA, 0xF1 \n
    HLT \n\n

    Enter your program one instruction per line.\n\n
    '''
)

machineCode = 'v2.0 raw'
instrList = []
while True:
    line = str(input('0x%02d : ' % address))
    address = address + 2

    try:
        if line.strip()[:3].upper() == 'END':
            break
        instr = makeInstruction(line)
        instrList.append(instr)
    except Exception as e:
        # print('Bad Instruction: ', e)
        raise Exception()
    

if len(instrList) > 0:
    filename = str(input('File Name: '))
    with open(filename, 'w') as f:
        f.write('v2.0 raw\n')
        for line in instrList:
            f.write(line[:2] + '\n')
            f.write(line[2:] + '\n')
