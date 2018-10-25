from tools.instruction import Instruction
from tools.components import RegisterAccess
from tools.components import ALU
from tools.components import DataMem

Instruction = Instruction()
RegisterUnit = RegisterAccess(INST=Instruction)
ALU = ALU(ru=RegisterUnit, inst=Instruction)
DataMemory = DataMem(ALU, RegisterUnit, Instruction)

RegisterUnit.write_to_register()
DataMemory.write_to_memory()
