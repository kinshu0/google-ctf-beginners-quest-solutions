operands_and_results = [('0001000100010001000100010001000100010001000100010001000100010001', '0000000100000000000100000001000000000000000000010001000100010000')]

operand_string = '0001000100010001000100010001000100010001000100010001000100010001'
result_string = '0000000100000000000100000001000000000000000000010001000100010000'

def reverse_and(operand_string, result_string):
    x_arr = []

    ZERO = '0'
    QMARK = '?'
    ONE = '1'

    for operand, result in zip(operand_string, result_string):
        if operand == ZERO:
            x_arr.append(QMARK)
        elif operand == ONE:
            x_arr.append(result)

    return ''.join(x_arr)