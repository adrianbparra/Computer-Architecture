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
        # self.SP = 0xF4
        self.reg[7] = 0xF4
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.ADD = 0b10100000
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.branchtable = {}
        self.branchtable[self.LDI] = self.handle_LDI
        self.branchtable[self.PRN] = self.handle_PRN
        self.branchtable[self.HLT] = self.handle_HLT
        self.branchtable[self.MUL] = self.handle_MUL
        self.branchtable[self.ADD] = self.handle_ADD
        self.branchtable[self.PUSH] = self.handle_PUSH
        self.branchtable[self.POP] = self.handle_POP
        self.branchtable[self.CALL] = self.handle_CALL
        self.branchtable[self.RET] = self.handle_RET

    def load(self):
        """Load a program into memory."""


        # For now, we've just hardcoded a program:

        try:
            if len(sys.argv) < 2:
                print(f'Usage: python3 {sys.argv[0]} <filename>')
                print("Exiting Program")
                sys.exit(1)
            
            address = 0

            with open(f"C:\\Users\\PC1\\Documents\\Lambda_School\\Computer_Architecture\\Computer-Architecture\\ls8\\examples\\{sys.argv[1]}.ls8") as f:
                print(f"Running file '{sys.argv[1]}.ls8'")
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
        
        self.ram[address] = value

    def handle_LDI(self):
        
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        # print("LDI: ",int(value))

        self.reg[address] = value

        self.pc += 2

    def handle_PRN(self):

        address = self.ram_read(self.pc + 1)

        print("PRINTING: ",self.reg[address])

        self.pc += 1

    def handle_MUL(self):
        
        registerA = self.ram_read(self.pc + 1)
        registerB = self.ram_read(self.pc + 2)

        self.alu("MUL", registerA, registerB)

        self.pc += 2

    def handle_ADD(self):

        registerA = self.ram_read(self.pc + 1)
        registerB = self.ram_read(self.pc + 2)

        self.alu("ADD", registerA, registerB)
        
        self.pc += 2
        
    def handle_PUSH(self):
        self.reg[7] -= 1

        address = self.ram_read(self.pc+1)

        value = self.reg[address]

        self.ram_write(value, self.reg[7])

        self.pc += 1

    def handle_POP(self):

        value = self.ram_read(self.reg[7])


        address = self.ram_read(self.pc + 1)

        self.reg[address] = value
        
        self.reg[7] += 1
        self.pc += 1
    def handle_CALL(self):
    # calls a subroutine at address stored in register
        # save next address to stack
        next_command = self.pc + 2

        self.reg[7] -= 1

        self.ram_write(next_command, self.reg[7])
        # print(f"save: {self.pc+2} to ram: {stack_address}")
        # print(self.ram)

        # address to save
        register_number = self.ram_read(self.pc + 1)

        address_jump = self.reg[register_number]
        # print("Address :", address_jump)

        # pc is set to address stored in register
        self.pc = address_jump - 1
        # print(f"save pc to {self.reg[address]}")
 
    def handle_RET(self):
        # get saved pc in reg
        stack_pointer = self.reg[7]
        saved_pc =  self.ram_read(stack_pointer)
        # print("Return: ", int(saved_pc))
        
        # increment stack
        self.reg[7] += 1
        # save address to pc
        self.pc = saved_pc - 1

    def handle_HLT(self):

        self.running = False

    def run(self):
        """Run the CPU."""
        
        while self.running:
            # self.trace()
            # print("Command I: ",int(self.pc))
            
            command = self.ram[self.pc]
            
            if command in self.branchtable:


                self.branchtable[command]()
            else:
                print(f"Error:{command} not Found at PC:{self.pc}")
            

            self.pc += 1