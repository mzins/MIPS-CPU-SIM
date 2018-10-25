i_type_look_up = {
    "ADDI": {
        "OPCODE": "001000",
        "FUNCTION": ""

    }
}


r_type_look_up = {
    "ADD": {
        "OPCODE": "000000",
        "FUNCTION": "100000"

    }
}

j_type_look_up = {

}


def type_finder(opcode):
    if opcode in i_type_look_up.keys():
        return "I"
    if opcode in r_type_look_up.keys():
        return "R"
    if opcode in j_type_look_up.keys():
        return "J"
    return None

def to_binary(register):
    return bin(int(register.replace("$R",""))).replace("0b","").zfill(5)

def immediate_to_binary(value):
    return bin(int(value)).replace("0b","").zfill(16)