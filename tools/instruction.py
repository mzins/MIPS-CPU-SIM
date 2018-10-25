from tools import instruction_helpers
from tools.errors import InstructionNotFound
from logs.logconfig import log_config

LOG = log_config()


class Instruction:
    binary_instruction = ""

    def __init__(self):
        inst = raw_input("Please type a single command\n")
        self.opcode = None
        self.binary_instruction = self.parse_instruction(inst)

    def parse_instruction(self, instruction=""):

        instruction = instruction.replace(",","")
        instruction = instruction.upper()
        instruction_parts = instruction.split(" ")
        LOG.info('<note> INSTRUCTION UNITS ARE  {}'.format(instruction_parts))

        self.opcode = instruction_parts[0]

        type = instruction_helpers.type_finder(opcode=self.opcode)
        if type == "I":
            LOG.info('<note> FOUND I TYPE INSTRUCTION')
            opcode = instruction_helpers.i_type_look_up.get(instruction_parts[0]).get('OPCODE')
            rs = instruction_helpers.to_binary(instruction_parts[2])
            rt = instruction_helpers.to_binary(instruction_parts[1])
            imm = instruction_helpers.immediate_to_binary(instruction_parts[3])
            binary_instruction = "{}{}{}{}".format(opcode, rs, rt, imm)


        elif type == "R":
            LOG.info('<note> FOUND R TYPE INSTRUCTION')
            opcode = instruction_helpers.r_type_look_up.get(instruction_parts[0]).get('OPCODE')

            rs = instruction_helpers.to_binary(instruction_parts[2])
            rt = instruction_helpers.to_binary(instruction_parts[3])
            rd = instruction_helpers.to_binary(instruction_parts[1])
            func_code = instruction_helpers.r_type_look_up.get(instruction_parts[0]).get('FUNCTION')
            binary_instruction = "{}{}{}{}{}{}".format(opcode,rs, rt, rd, "00000", func_code)


        elif type == "J":
            LOG.info('<note>FOUND J TYPE INSTRUCTION')

        else:
            raise InstructionNotFound

        LOG.info('<note> BINARY INSTRUCTION {}\n'.format(binary_instruction))
        return binary_instruction

