
def test(un_ordered_list, character):
    return "-".join([i*character for i in un_ordered_list])

def print_rangoli(size):
    max_char = 97 + size -1
    total = list(range(size))+list(range(size))[::-1][1:]
    result = []
    for i in (total):
        row_char = chr(max_char-i)
        char_list = [chr(letter) for letter in range(max_char-i+1, max_char+1)]       
        centered_str = "-".join(char_list[::-1]+[row_char]+char_list)
        result.append(centered_str.center((size-1)*4+1, "-"))
    return "\n".join(result)