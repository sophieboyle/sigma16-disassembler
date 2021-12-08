import argparse


class Sigma16Disassembler:
    def __init__(self):
        self.obj_code = {"module": [],
                         "data": [],
                         "relocate": []}
        self.ip = 0
        self.mem_count = 0x0000
        self.assembly = {}
        self.assembly_instructions = []
        self.variables = []

    def load(self, filename):
        """
        Load the given object file to disassemble into the obj_code dictionary
        :param filename: The path of the object file, usually format 'example.obj.txt'
        :return: None
        """
        with open(filename, 'r') as f:
            for line in f:
                section, instr_blocks = line.split()
                self.obj_code[section].extend(instr_blocks.split(','))

    def construct_assembly_output(self):
        output = ""
        tab = "\t"
        for memaddr, instruction in self.assembly.items():
            output += f"{'{:04x}'.format(memaddr)}{tab}{instruction}\n"
        return output

    def __check_instruction_type(self, instr):
        """
        Checks the first hex digit to determine the type of instruction
        :param instr: The hex string representing the machine code instruction
        :return: str instruction-type, either 'RRR', 'RX', or 'EXP'
        """
        if instr[0] == 'f':
            return "RX"
        elif instr[0] == 'e':
            return "EXP"
        else:
            return "RRR"
        pass

    def __disassemble_RRR(self, instr):
        """
        Disassemble an RRR function
        :param instr: (str) A string of 4 hex digits representing the machine code instruction
        :return: (str) The assembly instruction result of the disassembly
        """
        tab = '\t'
        opcode_mapping = {'0': "add", '1': "sub", '2': "mul", '3': "div", '4': "addc",
                          '5': "muln", '6': "divn", '7': "cmp", '8': "push", '9': "pop",
                          'a': "top", 'b': "trap", 'c': "trap"}
        operation = opcode_mapping[instr[0]]
        return f"{operation}{tab}R{instr[1]},R{instr[2]},R{instr[3]}", operation

    def __disassemble_RX(self, instr, displacement):
        """
        Disassemble an RX instruction
        :param instr: The hex string representing the first 16 bytes of the instruction
        :param displacement: A memory address which is used as a displacement in the RX instruction
        :return: (str) The assembly instruction result of the disassembly
        """
        tab = '\t'
        opcode_mapping = {"0": "lea", "1": "load", "2": "store", "3": "jump", "4": "jal",
                          "5": "jumpc0", "6": "jumpc1", "7": "jumpn", "8": "jumpz", "9": "jumpnz",
                          "a": "jumpp", "b": "testset"}
        operation = opcode_mapping[instr[3]]
        return f"{operation}{tab}R{instr[1]},{displacement}[{instr[2]}]", operation

    def __increment_pointers(self, n):
        """
        Increment both the instruction pointer and the memory counter
        :param n: The number of instructions which were disassembled and must now be incremented
        :return: None
        """
        self.ip += n
        self.mem_count += n

    def disassemble(self):
        tab = "\t"
        while self.ip != len(self.obj_code["data"]):
            current_instruction = self.obj_code["data"][self.ip]
            instr_type = self.__check_instruction_type(current_instruction)

            if instr_type == "RRR":
                assembly_instr, operation = self.__disassemble_RRR(current_instruction)
                self.assembly[self.mem_count] = assembly_instr
                self.assembly_instructions.append(assembly_instr)
                self.__increment_pointers(1)

                if operation == "trap":
                    # If the last RRR was trap, then move onto iterating over variable declaration
                    break

            elif instr_type == "RX":
                displacement = self.obj_code["data"][self.ip+1]
                assembly_instr, operation = self.__disassemble_RX(current_instruction, displacement)
                self.assembly[self.mem_count] = assembly_instr
                self.assembly_instructions.append(assembly_instr)
                self.__increment_pointers(2)
                continue

            elif instr_type == "EXP":
                self.__increment_pointers(2)
                continue

        # Iterate over the 'variables' declared at the end of the data section
        var_counter = 0
        while self.ip != len(self.obj_code["data"]):
            # Convert string representation to hex to get the hex value
            hex_str = self.obj_code["data"][self.ip]
            var_value = int(hex_str, base=16)
            self.variables.append(var_value)
            self.assembly[self.mem_count] = f"Var{var_counter}{tab}data{tab}{var_value}"
            self.__increment_pointers(1)
            var_counter += 1

        return self.construct_assembly_output()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs=1,
                        help="The filename of the object file to be disassembled")
    return parser.parse_args()


if __name__ == "__main__":
    disassembler = Sigma16Disassembler()
    args = parse_args()
    disassembler.load(args.file[0])
    assembly = disassembler.disassemble()
    print(assembly)
