ops = { 
    'ADD' : '0001',
    'SUB' : '0010',
    'JMP' : '0011',
    'AND' : '0100',
    'OR'  : '0101',
    'MUL' : '0110',
    'XOR' : '0111',
    'MOV' : '1000',
    'LOD' : '1001',
    'STR' : '1010',
    'HLT' : '1111',
    'NOP' : '0000',
    }

registers = {
    'R0' : '000',
    'R1' : '001',
    'R2' : '010',
    'R3' : '011',
    'R4' : '100',
    'R5' : '101'
}

def makeInstruction(line):
    op = line.split(',')[0].split()[0].upper()
        
    if op not in ops:
        raise Exception('Operation %s Not Found!' % op)
    
    if op == 'NOP':
        i = Instruction(op, False, None, None, None, line)
        
    elif op == 'JMP':
        if len(line.split(',')) > 1 or len(line.split()) != 2:
            raise Exception('Instruction Format is Wrong')
        op1 = line.split()[1]
        
        if op1.upper() in registers:
            i = Instruction(op, False, op1.upper(), None, None, line)
        elif op1[:2] == '0x' and len(op1) == 4:
            num = int(op1, 16)
            if (num > 255):
                raise Exception('Immediate Value too big!')
            imd = '{0:08b}'.format(num)
            i = Instruction(op, True, None, None, imd, line)
        else:
            raise Exception('Bad Operand')
        
    # elif op == 'NOT':
    #     if len(line.split(',')) > 1 or len(line.split()) != 2 or line.split()[1] not in registers:
    #         raise Exception('Instruction Format is Wrong')

        # op1 = line.split()[1]
        # i = Instruction(op, False, op1.upper(), None, None, line)


    elif op == 'HLT':
        if len(line.split(',')) > 1 or len(line.split()) != 1:
            raise Exception('Instruction Format is Wrong')
    
        i = Instruction(op, False, None, None, None, line)

    else:
        if len(line.split(',')) != 2 or len(line.split(',')[0].split()) != 2:
            print(len(line.split(',')))
            print(len(line.split(',')[1].split()))
            raise Exception('Instruction Format is Wrong')
        
        op2 = line.split(',')[1].strip()

        op1 = line.split(',')[0].split()[1].upper()

        if op1 not in registers:
            raise Exception('Bad Operand')
        
        if op2.upper() in registers:
            i = Instruction(op, False, op1.upper(), op2.upper(), None, line)
        elif op2[:2] == '0x' and len(op2) == 4:
            num = int(str(op2), 16)
            if (num > 255):
                raise Exception('Immediate Value too big!')
            imd = '{0:08b}'.format(num)
            print(imd)
            i = Instruction(op, True, op1.upper(), None, imd, line)
        else:
            raise Exception('Bad Operand')


    return i.strInstr()


class Instruction:
    indirect = bool()
    opcode = str()
    immediate = str()
    src = str()
    dest = str()
    comment = str()
    binaryInstr = list()
    hexInstr = list()

    def __init__(self, opr, indirect, src, dest, immediate, text):
        self.binaryInstr.clear()
        self.hexInstr.clear()
        if not opr in ops:
            raise Exception('Not a valid operation!')

        if not src and (opr != 'JMP' and opr != 'HLT' and opr != 'NOP'):
            raise Exception('Invalid Source')

        if src and not src in registers:
            raise Exception('Invalid Source')

        if not dest and not indirect and opr != 'JMP' and opr != 'HLT' and opr != 'NOP':
            raise Exception('Invalid Destination')

        if dest and not dest in registers:
            raise Exception('Invalid Destination')

        if indirect and (not immediate or len(immediate) != 8):
            raise Exception('Invalid Immediate Value')

        self.opcode = ops[opr]
        self.indirect = indirect
        if src:
            self.src = registers[src]
        if dest:
            self.dest = registers[dest]
        self.immediate = immediate
        self.comment = text

        if indirect:
            self.binaryInstr.append('1')
        else:
            self.binaryInstr.append('0')

        self.binaryInstr.extend(list(self.opcode))

        if opr == 'JMP' and indirect:
            self.binaryInstr.extend(list('000'))            
        elif opr != 'HLT' and opr != 'NOP':
            self.binaryInstr.extend(list(self.src))
        else:
            self.binaryInstr.extend(list('000'))

        if not indirect:
            self.binaryInstr.extend(list(self.dest))
            self.binaryInstr.extend(list('00000'))
        else:
            self.binaryInstr.extend(list(self.immediate))

        self.hexInstr.append( hex( int(''.join(self.binaryInstr[0:4]), 2) )[2:] )
        self.hexInstr.append( hex( int(''.join(self.binaryInstr[4:8]), 2) )[2:] )
        self.hexInstr.append( hex( int(''.join(self.binaryInstr[8:12]), 2) )[2:] )
        self.hexInstr.append( hex( int(''.join(self.binaryInstr[12:16]), 2) )[2:] )

    def strInstr(self):
        return ''.join(self.hexInstr) + '   # ' + self.comment
