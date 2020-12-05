"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = True
        self.pc = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.branchtable = {}
        self.branchtable[self.LDI] = self.handle_LDI
        self.branchtable[self.PRN] = self.handle_PRN
        self.branchtable[self.HLT] = self.handle_HLT
        self.branchtable[self.MUL] = self.handle_MUL

    def load(self):
        """Load a program into memory."""


        # For now, we've just hardcoded a program:

        try:
            if len(sys.argv) < 2:
                print(f'Usage: python3 {sys.argv[0]} <filename>')
                print("Exiting Program")
                sys.exit(1)
            
            address = 0

            with open(f"C:\\Users\\PC1\\Documents\\Lambda_School\\Computer_Architecture\\Computer-Architecture\\ls8\\examples\\{sys.argv[1]}") as f:
                print(f"Running file '{sys.argv[1]}'")
                print("--------------------------------")

                for line in f:
                    split_line = line.split("#")[0]
                    stripped_line = split_line.strip()
                    if stripped_line != "":
                        command = int(stripped_line, 2)

                        # print(command)

                        self.ram[address] = command
                        address += 1

        except FileNotFoundError:

            print(f"Error file '{sys.argv[1]}' not found")
            print("Exiting Program")
            sys.exit(1)
            

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | RAM: %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='REG:')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self,address):
        
        return self.ram[address]

    def ram_write(self,value,address):
        
        self.reg[address] =  value

    def handle_LDI(self):
        
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)

        self.ram_write(value,address)

        self.pc += 2

    def handle_PRN(self):

        address = self.ram_read(self.pc + 1)

        print(self.reg[address])

        self.pc += 1

    def handle_MUL(self):
        
        registerA = self.ram_read(self.pc + 1)
        registerB = self.ram_read(self.pc + 2)

        value = self.alu("MUL", registerA, registerB)

        self.pc += 2
        
    def handle_HLT(self):

        self.running = False

    def run(self):
        """Run the CPU."""
        
        while self.running:
            # self.trace()
            
            command = self.ram[self.pc]

            if command in self.branchtable:

                self.branchtable[command]()
            else:
                print(f"Error {bin(command)} not Found")
            

            self.pc += 1
