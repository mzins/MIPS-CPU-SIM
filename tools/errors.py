class InstructionNotFound(Exception):
    def __init__(self):
        print("Sorry your instruction does not exist yet in this system")