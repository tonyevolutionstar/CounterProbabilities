
text_file = "books/text_test.txt"
books_dir = "books/"

def tests():
    pass

# receives a charecter and checks if we got accent and replace with a charecter without a accent, example À - A
def accents(c):
    # based on table http://accentcodes.com/

    # ord converts a char to ascii number 
    number_ascii = ord(c.lower())
    
    # A
    a_ascii = [192, 224, 193, 226, 195, 227, 196, 228]
    for letter_a in a_ascii:
        if letter_a == number_ascii:
            return "a"

    # E
    e_ascii = [200, 232, 201, 233, 202, 234, 203, 235]
    for letter_e in e_ascii:
        if letter_e == number_ascii:
            return "e"

    # I
    i_ascii = [204, 236, 205, 237, 206, 238, 207, 239]
    for letter_i in i_ascii: 
        if letter_i == number_ascii:
            return "i"

    # O
    o_ascii = [210, 242, 211, 243, 212, 244, 213, 245, 214, 246]
    for letter_o in o_ascii:
        if letter_o == number_ascii:
            return "o"

    # U
    u_ascii = [217, 249, 218, 250, 219, 251, 220, 252]
    for letter_u in u_ascii:
        if letter_u == number_ascii:
            return "u"

    # Y
    y_ascii = [221, 253, 159, 255]
    for letter_y in y_ascii:
        if letter_y == number_ascii:
            return "y"

    # Ç
    c_ascii = [199, 231]
    for letter_c in c_ascii:
        if letter_c == number_ascii:
            return "c"

    return c
    

def read_file():
    file = open(text_file, "r", encoding='utf-8')
    letter = {}
    for line in file:
        for character in line:
            # isalpha remove special charecters
            if character.isalpha() == True:
                #print(character)
                c = accents(character).upper()
                
                if c in letter:
                    letter[c] = letter[c] + 1
                else: 
                    letter[c] = 1
              
    file.close()
    return dict(sorted(letter.items(), key = lambda x:x[0]))

if __name__ == "__main__":
    letters = read_file()
