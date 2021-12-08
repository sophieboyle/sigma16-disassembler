import argparse


class Sigma16Disassembler:
    def __init__(self):
        self.obj_code = {"module": [],
                         "data": [],
                         "relocate": []}
        pass

    def load(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                section, instr_blocks = line.split()
                self.obj_code[section].extend(instr_blocks.split(','))

    def check_instruction_type(self):
        pass

    def disassemble(self):
        self.ip = 0
        for instr in self.obj_code['data']:
            pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs=1,
                        help="The filename of the object file to be disassembled")
    return parser.parse_args()


if __name__ == "__main__":
    disassembler = Sigma16Disassembler()
    args = parse_args()
    disassembler.load(args.file[0])
    disassembler.disassemble()
