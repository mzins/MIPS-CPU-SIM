from configurations.control_table import Control
from configurations.registers import Registers
from configurations.memory import Memory


from logs.logconfig import log_config

LOG = log_config()


class RegisterAccess:
    RegWrite = None
    RegDst = None
    ReadRegister1 = None
    ReadRegister2 = None
    WriteRegister = None
    WriteData = None
    ReadData1 = None
    ReadData2 = None

    def __init__(self, INST):
        self.RegWrite = Control.get(INST.opcode).get("RegWrite")
        LOG.info('<control line> SET REGWRITE TO {}'.format(self.RegWrite))

        self.RegDst = Control.get(INST.opcode).get("RegDst")
        LOG.info('<control line> SET REGDst TO {}'.format(self.RegDst))

        self.ReadRegister1 = INST.binary_instruction[6:11]
        LOG.info('<data change> SET READ REGISTER 1 TO {}'.format(self.ReadRegister1))

        self.ReadRegister2 = INST.binary_instruction[11:16]
        LOG.info('<data change> SET READ REGISTER 2 TO {}'.format(self.ReadRegister2))

        self.WriteRegister = Mux2i(control=self.RegDst,
                                   zero=INST.binary_instruction[11:16],
                                   one=INST.binary_instruction[16:21])
        LOG.info('<data change> CALLING MUX FOR WRITE REGISTER...SET WRITE REGISTER TO {}'.format(self.WriteRegister))

        self.ReadData1 = Registers.get(self.ReadRegister1)
        LOG.info('<data change> SET READ DATA 1 TO {}'.format(self.ReadData1))

        self.ReadData2 = Registers.get(self.ReadRegister2)
        LOG.info('<data change> SET READ DATA 2 TO {}\n'.format(self.ReadData2))

    def write_to_register(self):
        register_num = self.WriteRegister
        data = self.WriteData
        Registers[register_num] = data
        LOG.info('<writing notice> WROTE VALUE {} TO REGISTER NUMBER {}\n'.format(data, register_num))


class ALU:
    input1 = None
    input2 = None
    Zero = 0
    ALUResult = None

    def __init__(self, ru, inst):
        self.input1 = ru.ReadData1
        LOG.info('<data change> INPUT ONE IS {}'.format(self.input1))

        self.input2 = Mux2i(control=Control.get(inst.opcode).get('ALUSrc'), zero=ru.ReadData2,
                     one=sign_extend(inst.binary_instruction[16:32]))
        LOG.info('<data change>INPUT TWO IS {}\n'.format(self.input2))

        self.execute(ru, inst)

    def execute(self, ru, inst):
        execution_string = '{}{}{}'.format(self.input1, Control.get(inst.opcode).get("ALUOp"), self.input2)

        LOG.info('<processing> EXECUTING {}'.format(execution_string))
        self.ALUResult = eval(execution_string)

        if self.ALUResult < 0:
            self.Zero = 1
        LOG.info('<data change> ALU ZERO SET TO {}\n'.format(self.Zero))


class DataMem:
    Address = None
    WriteData = None
    ReadData = None
    MemWrite = None
    MemRead = None

    def __init__(self, alu, ru, inst):
        self.Address = alu.ALUResult
        LOG.info('<data change> SET DATA MEM ADDRESS TO {}'.format(self.Address))

        self.WriteData = ru.ReadData2
        LOG.info('<data change> SET WRITE DATA TO {}'.format(self.WriteData))

        self.MemRead = Control.get(inst.opcode).get('MemRead')
        LOG.info('<control line> SET DATA MEM READ TO {}'.format(self.MemRead))

        self.MemWrite = Control.get(inst.opcode).get('MemWrite')
        LOG.info('<control line> SET DATA MEM WRITE TO {}'.format(self.MemWrite))

        if self.MemRead:
            self.ReadData = self.grab_from_memory()
            LOG.info('<processing> READ DATA {} FROM MEMORY {}'.format(self.ReadData, self.Address))

        # Determine if dest register gets memory or alu result
        ru.WriteData = Mux2i(control=Control.get(inst.opcode).get("MemtoReg"), zero=alu.ALUResult, one=self.ReadData)
        LOG.info('<data change> CALLING MUX TO DETERMINE WRITE DATA SOURCE... REGISTER WRITE DATA IS {}\n'.format(ru.WriteData))


    def grab_from_memory(self):
        if not self.Address >= 0 and self.Address <= 40:
            raise Exception('Your address is out of scope: {}\n'.format(self.Address))
        return Memory.get(self.Address)

    def write_to_memory(self):
        if self.MemWrite:
            if not self.Address >= 0 and self.Address <= 40:
                raise Exception('Your address is out of scope: {}'.format(self.Address))
            Memory[self.Address] = self.WriteData
            LOG.info('<writing notice> WROTE DATA {} TO MEMORY ADDRESS {}\n'.format(self.WriteData, self.Address))



def Mux2i(control, zero, one):
    if control == 0:
        return zero
    elif control == 1:
        return one

def sign_extend(value):
    LOG.info('<processing> EXTENDING SIGN ON VALUE {}\n'.format(value))
    return int(value, 2)
