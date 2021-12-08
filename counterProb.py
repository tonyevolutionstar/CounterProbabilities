__author__ = "António Ramos"

import random
import math

# receives a charecter and checks if we got accent and replace with a charecter without a accent, example À - A
def accents(c):
    # based on table http://accentcodes.com/
    # http://accentcodes.com/cutout_chart.html

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
    
def exact_counter(letter, c):
    if c != 'Æ':
        if c in letter:
            letter[c] = letter[c] + 1
        else: 
            letter[c] = 1

    return letter


def fixed_counter(fixedCounter, c):
    p = 1/8
    number_rand = random.random() # generates a number random between 0, 1 only counts if the number generated is less than the p 
    if number_rand < p: 
        exact_counter(fixedCounter, c)

    return fixedCounter

def csursos_counter(csursoCounter, c):
    pass

def create_file(): 
    file = open("results.csv", "w")
    file.write("exact_counter, fixed_prob, csurso_prob\n")
    file.close()


# maybe change this 
def write_file(exact, fixed_prob, decrease_prob):
    file = open("results.csv", "a")
    file.write(f"{exact}, {fixed_prob}, {decrease_prob}\n")
    file.close()

# function for statiscs of each counter to write on a file
def statiscs(counter):
    mean = sum(counter.values())/len(counter)
    max_dev = 0 # maximal deviation
    mad = 0 # mean absolute deviation
    stdd_dev = 0 #standard deviation

    for i in counter:
        max_dev_ = abs(counter[i] - mean)
        if max_dev_ > max_dev: 
            max_dev = max_dev_

        mad += abs(counter[i] - mean)
        stdd_dev += pow((counter[i] - mean), 2)

    return (round(mean, 3), round(max_dev, 3), round((1/len(counter) * mad), 3), round(math.sqrt(1/len(counter)*stdd_dev), 3))

def create_counter():
    file = open("results_counters.txt", "w")
    file.write("Layout of file\n")
    file.write("------------------------------\n")
    file.write("Ntimes: X \n")
    file.write("Name of book: X - Total of letters: X \n")
    file.write("Exact Counter: \n")
    file.write("MEAN, MAX_DEV, MAD, STDD_DEV\n")
    file.write("Fixed probability with 1/8: \n")
    file.write("MEAN, MAX_DEV, MAD, STDD_DEV\n")
    file.write("Csuros: \n")
    file.write("MEAN, MAX_DEV, MAD, STDD_DEV\n")
    file.write("------------------------------\n")
    file.close()

def write_counter(book, ntimes, exct_counter, fixed_counter, csursos):
    file = open("results_counters.txt", "a")
    file.write(f"Ntimes: {ntimes}\n")
    file.write(f"Name of book: {book} - Total of letters: {sum(exct_counter.values())}\n")
    file.write(f"Exact Counter: {exct_counter}\n")
    mean_ex, max_dev_ex, mad_ex, stdd_ex = statiscs(exct_counter)
    file.write(f"{mean_ex}, {max_dev_ex}, {mad_ex}, {stdd_ex}\n")
    file.write(f"Fixed probability with 1/8: {fixed_counter}\n")
    mean_fc, max_dev_fc, mad_fc, stdd_fc = statiscs(fixed_counter)
    file.write(f"{mean_fc}, {max_dev_fc}, {mad_fc}, {stdd_fc}\n")
    """
    file.write(f"Csuros: {csursos}")
    mean_c, max_dev_c, mad_c, stdd_c = statiscs(csursos)
    file.write(f"{mean_c}, {max_dev_c}, {mad_c}, {stdd_c}\n") 
    """
    file.write("------------------------------\n")
    file.close()



def read_file(text_file, n_times):
    file = open(text_file, "r", encoding='utf-8')
    exactCounter = {}
    fixedCounter = {}
    csursoCounter = {}

    
    for ntime in range(n_times):
        print(f"I'm doing the counter {ntime} \n")
        for line in file:
            for character in line:
                # isalpha remove special charecters
                # https://www.w3schools.com/python/ref_string_isalpha.asp
                if character.isalpha() == True:
                    #print(character)
                    c = accents(character).upper()
                    l = exact_counter(exactCounter, c)
                    exct_counter = dict(sorted(l.items(), key = lambda x:x[0]))
                    
                    fc = fixed_counter(fixedCounter, c)
                    fc_counter = dict(sorted(fc.items(), key = lambda x:x[0]))
              
    file.close()
    return exct_counter, fc_counter, csursoCounter

if __name__ == "__main__":
    create_file()
    create_counter()

    # books available
    text_file = "books/text_test.txt" # for testing
    frank_file = "books/frankenstein.txt" # https://www.gutenberg.org/cache/epub/42324/pg42324.txt # it was removed the header and the footer
    
    # the counters are implemented in a function read_file 
    n_times = 1
    ex_coutner, fc_counter, csurso_counter = read_file(text_file, n_times) # this is a exact counter
    write_counter("text_test", n_times, ex_coutner, fc_counter, csurso_counter)
 
    n_times = 1000
    ex_coutner, fc_counter, csurso_counter = read_file(text_file, n_times) # this is a exact counter
    write_counter("text_test", n_times, ex_coutner, fc_counter, csurso_counter)