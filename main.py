import argparse


class Sigma16Disassembler:
    def __init__(self):
        self.obj_code = {"module": [],
                         "data": [],
                         "relocate": []}
        self.ip = 0
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

    def disassemble(self):
        while self.ip != len(self.obj_code["data"]):
            current_instruction = self.obj_code["data"][self.ip]
            instr_type = self.__check_instruction_type(current_instruction)
            if instr_type == "RRR":
                assembly_instr, operation = self.__disassemble_RRR(current_instruction)
                self.assembly_instructions.append(assembly_instr)
                self.ip += 1
                if operation == "trap":
                    # If the last RRR was trap, then move onto iterating over variable declaration
                    break
            elif instr_type == "RX":
                # Currently skip forward by 2 instructions
                self.ip += 2
                continue
            elif instr_type == "EXP":
                self.ip += 2
                continue

        # Iterate over the 'variables' declared at the end of the data section
        var_counter = 0
        while self.ip != len(self.obj_code["data"]):
            # Convert string representation to hex to get the hex value
            hex_str = self.obj_code["data"][self.ip]
            var_value = int(hex_str, base=16)
            self.variables.append(var_value)
            self.ip += 1

        return self.assembly_instructions, self.variables


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs=1,
                        help="The filename of the object file to be disassembled")
    return parser.parse_args()


if __name__ == "__main__":
    disassembler = Sigma16Disassembler()
    args = parse_args()
    disassembler.load(args.file[0])
    assembly_instructions, variables = disassembler.disassemble()
    print("\n".join(assembly_instructions))
    print(variables)
