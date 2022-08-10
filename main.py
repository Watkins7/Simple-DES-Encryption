import time

s1 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

s2 =[
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

input_intial_permutation = [
    1, 5, 2, 0,
    3, 7, 4, 6
]

output_permutation = [
    3, 0, 2, 4,
    6, 1, 7, 5
]

expanison_table = [
    3, 0, 1, 2,
    1, 2, 3, 0
]

four_bit_permute = [
    1, 3, 2, 0
]

permute_choice1 = [
    2, 4, 1, 6, 3,
    9, 0, 8, 7, 5
]

permute_choice2 = [
    5, 2, 6, 3,
    7, 4, 9, 8
]

shift_per_round = [
    1, 2, 2, 2
]

sub_key = []

# s1 lookup with four bits
def s1_look_up(four_bits):

    colum_num = (((four_bits >> 2) & 0b1)) * 2
    colum_num = colum_num + ((four_bits >> 1) & 0b1)

    row_num = ((four_bits >> 3) & 0b1)* 2
    row_num = row_num + (four_bits & 0b1)

    lower_bit = s1[row_num][colum_num]

    return lower_bit


# Calculate S
def combine_s(s1, s2):

    # Combine S's
    new_four_bit = s1 << 2
    new_four_bit += s2
    new_four_bit = new_four_bit & 0b1111

    return new_four_bit


# s2 lookup with four bits
def s2_look_up(four_bits):

    colum_num = ((four_bits >> 2) & 0b1) * 2
    colum_num = colum_num + (((four_bits >> 1) & 0b1))

    row_num = ((four_bits >> 3) & 0b1) * 2
    row_num = row_num + ((four_bits & 0b1))

    upper_bit = s2[row_num][colum_num]

    return upper_bit


# Change S lookup
def permute_4bits(four_bits):

    # convert decimal to binary list
    four_list = [int(i) for i in bin(four_bits)[2:]]

    # Fix List
    while len(four_list) < 4:
        four_list.insert(0, 0b0)

    # Blank list of new order
    new_order = []

    # Make new order
    for i in four_bit_permute:
        new_order.append(four_list[i])

    # Add all binary numbers up
    binary_num = 0
    for b in new_order:
        binary_num = 2 * binary_num + b

    return binary_num


# Text input permutation
def input_permutation(eight_bit_text):

    # convert decimal to binary list
    text_list = [int(i) for i in bin(eight_bit_text)[2:]]

    while len(text_list) < 8:
        text_list.insert(0, 0b0)

    new_order = []

    for i in input_intial_permutation:
        new_order.append(text_list[i])

    binary_num = 0
    for b in new_order:
        binary_num = 2 * binary_num + b

    return binary_num


# Exapnds rightside
def right_side_expand(right):

    # convert decimal to binary list
    right_list = [int(i) for i in bin(right)[2:]]

    # Fix List
    while len(right_list) < 4:
        right_list.insert(0, 0b0)

    # Blank list of new order
    new_order = []

    # Make new order
    for i in expanison_table:
        new_order.append(right_list[i])

    # Add all binary numbers up
    binary_num = 0
    for b in new_order:
        binary_num = 2 * binary_num + b

    return binary_num

def final_permutation(eight_bit_text):

    # convert decimal to binary list
    text_list = [int(i) for i in bin(eight_bit_text)[2:]]

    # Make list at least 8 bits by padding
    while len(text_list) < 8:
        text_list.insert(0, 0b0)

    new_order = []

    for i in output_permutation:
        new_order.append(text_list[i])

    binary_num = 0
    for b in new_order:
        binary_num = 2 * binary_num + b

    return binary_num


# Initial Ciphertext Permutation
def initial_ciphertext_permutation(left_and_right):

    # convert decimal to binary list
    left_and_right = [int(i) for i in bin(left_and_right)[2:]]

    # Make Binary into List
    while len(left_and_right) < 10:
        left_and_right.insert(0, 0b0)

    # Blank list of new order
    new_order = []

    # Make new order
    for i in permute_choice1:
        new_order.append(left_and_right[i])

    # Add all binary numbers up
    binary_num = 0
    for b in new_order:
        binary_num = 2 * binary_num + b

    binary_num = bin(binary_num)
    binary_num = int(binary_num, 2)

    return binary_num

def second_permutation_cipher_function(sub_key):

    # convert decimal to binary list
    sub_key = [int(i) for i in bin(sub_key)[2:]]

    # Make list at least 28 bits by padding
    while len(sub_key) < 10:
        sub_key.insert(0, 0b0)

    new_order = []

    for i in permute_choice2:
        new_order.append(sub_key[i])

    binary_num = 0
    for b in new_order:
        binary_num = 2 * binary_num + b

    return binary_num


def swap(left_and_right):
    new_8bits = (left_and_right << 4 | left_and_right >> 4)
    new_8bits = new_8bits & 0b11111111
    return new_8bits


def function_f(key, data):

    # Seperate orginal left and right
    left = data & 0b11110000
    right = data & 0b00001111

    # Expand right, preform xor on key
    key_xor_right = key ^ right_side_expand(right)

    # Seperate xor result
    left_s1 = (key_xor_right & 0b11110000) >> 4
    right_s2 = key_xor_right & 0b00001111

    # preform s box look up
    left_s1 = s1_look_up(left_s1)
    right_s2 = s2_look_up(right_s2)

    # combine new S
    left_and_right = combine_s(left_s1, right_s2)

    # permutation
    permute = permute_4bits(left_and_right)
    permute = permute << 4

    # XOR permutation with left
    wrong_left = left ^ permute

    # combine left and right
    left_and_right = wrong_left | right

    return left_and_right

# Makes actual keys
def make_sub_keys(key):
    i = 0

    key = initial_ciphertext_permutation(key)

    # Make new LEFT & RIGHT keys
    right = key & 0b11111
    left = (key >> 5) & 0b11111

    # 4 sub keys
    while i < 4:

        # Shift round key at appropriate length
        left = (left << shift_per_round[i]) | (left >> (5 - shift_per_round[i]))
        right = (right << shift_per_round[i]) | (right >> (5 - shift_per_round[i]))
        left = left & 0b11111
        right = right & 0b11111

        # Combine Keys
        new_key = left << 5
        new_key = new_key + right

        # Have left and right do sub_permutation
        new_key = second_permutation_cipher_function(new_key)

        i += 1

        sub_key.append(new_key)

    return

def encrypt(key, plaintext):

    # make subkeys
    make_sub_keys(key)

    # permute
    data = input_permutation(plaintext)

    # Function f
    data = function_f(sub_key[0], data)
    # Swap left and right
    data = swap(data)
    data = function_f(sub_key[1], data)
    data = swap(data)
    data = function_f(sub_key[2], data)
    data = swap(data)
    data = function_f(sub_key[3], data)

    # Final permutation
    data = final_permutation(data)

    # clear keys
    sub_key.clear()

    return data


def decrypt(key, ciphertext):

    # make subkeys
    make_sub_keys(key)

    # input permutation
    data = input_permutation(ciphertext)

    # cipher function f
    data = function_f(sub_key[3], data)
    # Swap left and right
    data = swap(data)
    data = function_f(sub_key[2], data)
    data = swap(data)
    data = function_f(sub_key[1], data)
    data = swap(data)
    data = function_f(sub_key[0], data)
    data = final_permutation(data)

    sub_key.clear()

    return data

hex_text = [
0x58,0x65,0x19,0xb0,0x31,0xaa,0xee,0x9a,0x23,0x52,
0x47,0x60,0x1f,0xb3,0x7b,0xae,0xfb,0xcd,0x54,0xd8,
0xc3,0x76,0x3f,0x85,0x23,0xd2,0xa1,0x31,0x5e,0xd8,
0xbd,0xcc
]

variable_keys = [
    0b1000000000,
    0b0100000000,
    0b0010000000,
    0b0001000000,
    0b0000100000,
    0b0000010000,
    0b0000001000,
    0b0000000100,
    0b0000000010,
    0b0000000001
]

key_answers = [
    0b01100001,
    0b00010011,
    0b01001111,
    0b11100101,
    0b01100101,
    0b01011100,
    0b10101110,
    0b11011001,
    0b10101010,
    0b01001110
]

variable_plain = [
    0b10000000,
    0b01000000,
    0b00100000,
    0b00010000,
    0b00001000,
    0b00000100,
    0b00000010,
    0b00000001
]

plain_answers = [
    0b10101000,
    0b10111110,
    0b00010110,
    0b01001010,
    0b01001001,
    0b01001110,
    0b00010101,
    0b01101000
]

permutation_known = [
    0b11,
    0b0011001010,
    0b0001011001,
    0b1011001111
]
permutation_answers = [
    0b11,
    0b100010,
    0b1000000,
    0b1100000
]

subsitution_known = [
    0b1101101,
    0b1101110,
    0b1110000,
    0b1110001,
    0b1110110,
    0b1111000,
    0b1111001
]

subsitution_answers = [
    0b10000111,
    0b10110110,
    0b10110100,
    0b00110011,
    0b11011001,
    0b10001101,
    0b00010001
]

def test_of_PLAINTEXT():
    for i in range(len(variable_plain)):

        if encrypt(0b0, variable_plain[i]) == plain_answers[i]:
            print("Plaintext Test SUCCESS!")

        else:
            print("Plaintext Test FAILED!")


def test_of_KEYS():
    for i in range(len(variable_keys)):

        if encrypt(variable_keys[i], 0b0) == key_answers[i]:
            print("Variable Key Test SUCCESS!")

        else:
            print("Variable Key Test FAILED!")


def test_of_PERMUTATION():
    for i in range(len(permutation_known)):

        if encrypt(permutation_known[i], 0b0) == permutation_answers[i]:
            print("Permutation Test SUCCESS!")

        else:
            print("Permutation Test FAILED!")


def test_of_SUBSITUTION():
    for i in range(len(subsitution_known)):

        if encrypt(subsitution_known[i], 0b0) == subsitution_answers[i]:
            print("Substitution Test SUCCESS!")

        else:
            print("Substitution Test FAILED!")


def double_des_break():
    i_1, i_0, j_1, j_0 = [], [], [], []

    print("PLEASE WAIT! Attempting meet-in-middle attack...")

    begin = time.time()

    #dictonary1 = defaultdict(list)
    dictonary1 = {}
    key_pairs = []

    for z in range(1024):
        plain = encrypt(int(z), 0x42)
        dictonary1[plain] = []

    for z in range(1024):
        plain = encrypt(int(z), 0x42)
        dictonary1[plain].append(z)

    #dictonary1.clear()
    for y in range(1024):

        cipher = decrypt(y, 0x52)

        if cipher in dictonary1.keys():
            for key in dictonary1[cipher]:
                key_pairs.append((y, key))

    print("Finished with 0x42 and 0x52")
    print("Number of i: ", len(key_pairs))
    print("Number of j: ", len(key_pairs))
    print()

    for i in range(len(key_pairs)):

        plain = encrypt(key_pairs[i][1], 0x72)
        cipher = decrypt(key_pairs[i][0], 0xf0)

        if plain == cipher:
            i_0.append(key_pairs[i][1])
            j_0.append(key_pairs[i][0])

    print("Finished with 0x72 and 0xf0")
    print("Number of i: ", len(i_0))
    print("Number of j: ", len(j_0))
    print()
    j_1.clear()
    i_1.clear()

    for i in range(len(i_0)):

        plain = encrypt(int(i_0[i]), 0x75)
        cipher = decrypt(int(j_0[i]), 0xbe)

        if plain == cipher:
            j_1.append(j_0[i])
            i_1.append(i_0[i])

    print("Finished wih 0x75 and 0xbe")
    print("Number of i: ", len(i_1))
    print("Number of j: ", len(j_1))
    print()
    j_0.clear()
    i_0.clear()

    for i in range(len(i_1)):

        plain = encrypt(int(i_1[i]), 0x74)
        cipher = decrypt(int(j_1[i]), 0x69)

        if plain == cipher:
            j_0.append(j_1[i])
            i_0.append(i_1[i])

    print("Finished with 0x74 and 0x69")
    print("Number of i: ", len(i_0))
    print("Number of j: ", len(j_0))
    print()
    j_1.clear()
    i_1.clear()

    for i in range(len(i_0)):

        plain = encrypt(int(i_0[i]), 0x65)
        cipher = decrypt(int(j_0[i]), 0x8a)

        if plain == cipher:
            j_1.append(j_0[i])
            i_1.append(i_0[i])

    end = time.time()
    print("Finished with 0x65 and 0x8a")
    print("Number of i: ", len(i_0))
    print("Number of j: ", len(j_0))
    print()

    print("Finished!")
    print("The i keys were found to be", i_1)
    print("The j keys were found to be", j_1)
    print("Total time in seconds:", end-begin)


def brute_force():
    i_1, i_0, j_1, j_0 = [], [], [], []

    print("PLEASE WAIT! Attempting brute force attack...")

    begin = time.time()

    for i in range(1024):

        plain = encrypt(int(i), 0x42)

        for j in range(1024):
            if decrypt(int(j), 0x52) == plain:
                i_1.append(i)
                j_1.append(j)

    print("Finished with 0x42, and 0x52")
    print("Number of i: ", len(i_1))
    print("Number of j: ", len(j_1))
    print()

    for i in range(len(i_1)):

        plain = encrypt(int(i_1[i]), 0x72)
        cipher = decrypt(int(j_1[i]), 0xf0)

        if plain == cipher:
            j_0.append(j_1[i])
            i_0.append(i_1[i])

    print("Finished with 0x72 and 0xf0")
    print("Number of i: ", len(i_0))
    print("Number of j: ", len(j_0))
    print()
    j_1.clear()
    i_1.clear()

    for i in range(len(i_0)):

        plain = encrypt(int(i_0[i]), 0x75)
        cipher = decrypt(int(j_0[i]), 0xbe)

        if plain == cipher:
            j_1.append(j_0[i])
            i_1.append(i_0[i])

    print("Finished wih 0x75 and 0xbe")
    print("Number of i: ", len(i_1))
    print("Number of j: ", len(j_1))
    print()
    j_0.clear()
    i_0.clear()

    for i in range(len(i_1)):

        plain = encrypt(int(i_1[i]), 0x74)
        cipher = decrypt(int(j_1[i]), 0x69)

        if plain == cipher:
            j_0.append(j_1[i])
            i_0.append(i_1[i])

    print("Finished with 0x74 and 0x69")
    print("Number of i: ", len(i_0))
    print("Number of j: ", len(j_0))
    print()
    j_1.clear()
    i_1.clear()

    for i in range(len(i_0)):

        plain = encrypt(int(i_0[i]), 0x65)
        cipher = decrypt(int(j_0[i]), 0x8a)

        if plain == cipher:
            j_1.append(j_0[i])
            i_1.append(i_0[i])

    end = time.time()
    print("Finished with 0x65 and 0x8a")
    print("Number of i: ", len(i_0))
    print("Number of j: ", len(j_0))
    print()

    print("Finished!")
    print("The i keys were found to be", i_1)
    print("The j keys were found to be", j_1)
    print("Total time in seconds:", end - begin)

def ecb_mode():

    print("PLEASE WAIT! Attempting CBC mode...")

    sub_key.clear()
    mod_bit = 0x9c
    key1 = 831
    key2 = 339

    for i in range(len(hex_text)):

        plain_text = decrypt(key2, int(hex_text[i]))
        plain_text = decrypt(key1, plain_text)
        plain_text = plain_text ^ mod_bit
        print(chr(plain_text), end ='')
        mod_bit = hex_text[i]




if __name__ == '__main__':
    test_of_PLAINTEXT()
    print("-------------------------\n")
    test_of_KEYS()
    print("-------------------------\n")
    test_of_PERMUTATION()
    print("-------------------------\n")
    test_of_SUBSITUTION()
    print("-------------------------\n")
    double_des_break()
    print("-------------------------\n")
    brute_force()
    print("-------------------------\n")
    ecb_mode()

