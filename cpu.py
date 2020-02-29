"""CPU functionality."""

"""
Sprint Requirement
[ ] Add the `CMP` instruction and `equal` flag to your LS-8.

- [ ] Add the `JMP` instruction.

- [ ] Add the `JEQ` and `JNE` instructions.

--> CMP is handled by ALU (see LS8-spec)
--> Not necessary to put JMP/JEQ/JNE in ALU?
--> Need to create a flag 


"""


import sys
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
AND = 0b10101000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Create Memory
        self.ram = [0] * 256
        # Create Register
        self.reg = [0] * 8

        # Create program counter
        self.pc = 0

        # Create stack pointer
        self.sp = 0

        # Create flag
        self.flag = 0

        # Running CPU is true
        self.running = True
        # self.PC = self.reg[0]
        # self.IM = self.reg[5]
        # self.IS = self

    def LDI_function(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def PRN_function(self, a):
        print(f'{self.reg[a]}')
        self.pc += 2

    def HLT_function(self):
        self.running = False
        self.pc += 1

    def JMP_function(self, a):
        # On Jump
        # Set PC to the current register indicated by a
        self.pc = self.reg[a]

    def JEQ_function(self, a):
        # if reg a == reg b, which means flag hash E=1
        if self.flag == 0b00000001:
            # Set PC to current register
            self.pc = self.reg[a]
        else:
            # Catch case to move PC, since JNE should catch this alternative
            self.pc += 2

    def JNE_function(self, a):
        # reg a != reg b, which means flag hash E !=1
        if self.flag != 0b00000001:
            self.pc = self.reg[a]
        else:
            self.pc += 2

    def load(self, file_name):
        """Load a program into memory."""
        # Add all data in file into ram
        try:
            address = 0
            # Open the file
            with open(file_name) as f:
                # Reading all the lines in file
                for line in f:
                    # Parse out comment/Clean up code to be readable
                    # Clean white space and ignore #
                    comment_split = line.strip().split("#")

                    # Cast the values from str -> int
                    value = comment_split[0].strip()

                    # Ignore blank lines
                    if value == '':
                        continue

                    convert_to_binary = '0b' + value
                    num = int(convert_to_binary, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print('File not found')
            sys.exit(2)

        # Checks to see if command was typed correctly
        if len(sys.argv) != 2:
            print('ERROR: Must have file name')
            sys.exit(1)

    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "SUB":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == "PUSH":
            # Decrement stack pointer
            self.sp -= 1
            # Set reg value in ram at stack pointer
            self.ram[self.sp] = self.reg[reg_a]
            # Increment pc
            self.pc += 2
        elif op == "POP":
            # Increment stack pointer
            # Set reg to popped value
            self.reg[reg_a] = self.ram[self.sp]
            # Increment pc
            self.sp += 1
            self.pc += 2
        elif op == "CMP":
            self.flag = 0b00000000
            # self.pc +=3 because an extra register is created during the comparison
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
                self.pc += 3
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
                self.pc += 3
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
                self.pc += 3
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]
            # or should it be self.pc +=3?
            self.pc += 2
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    # byte refers to the address

    def ram_read(self, byte):
        return self.ram[byte]

    # byte refers to the address
    # change refers to the new item to be added

    def ram_write(self, byte, change):
        self.ram[byte] = change
        return self.ram[byte]

    def run(self):
        """Run the CPU."""
        while self.running:
            # self.trace()
            # print('--------')
            # Setting current to IR
            ir = self.ram_read(self.pc)

            # Get PC+1
            operand_a = self.ram_read(self.pc+1)
            # Get PC+2
            operand_b = self.ram_read(self.pc+2)

            if ir == LDI:
                self.LDI_function(operand_a, operand_b)
            elif ir == PRN:
                self.PRN_function(operand_a)
            elif ir == HLT:
                # print(self.ram)
                self.running = False
            elif ir == ADD:
                self.alu('ADD', operand_a, operand_b)
            elif ir == SUB:
                self.alu('SUB', operand_a, operand_b)
            elif ir == MUL:
                self.alu('MUL', operand_a, operand_b)
            elif ir == PUSH:
                self.alu('PUSH', operand_a)
            elif ir == POP:
                self.alu('POP', operand_a)
            elif ir == CMP:
                self.alu('CMP', operand_a, operand_b)
            elif ir == JMP:
                self.JMP_function(operand_a)
            elif ir == JEQ:
                self.JEQ_function(operand_a)
            elif ir == JNE:
                self.JNE_function(operand_a)
            elif ir == AND:
                self.alu("AND", operand_a, operand_b)
            else:
                self.running = False
                print(f"I did not understand that ir: {ir}")
                sys.exit(1)
