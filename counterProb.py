__author__ = "António Ramos"

import random
import math
import matplotlib.pyplot as plt
import time


# receives a charecter and checks if we got accent and replace with a charecter without a accent, example À - A
def accents(c):
    # based on table http://accentcodes.com/
    # http://accentcodes.com/cutout_chart.html

    # ord converts a char to ascii number 
    number_ascii = ord(c.upper())

    ## A  
    a_ascii = [192, 193, 194, 195, 224, 196, 197, 198]
    for letter_a in a_ascii:
        if letter_a == number_ascii:
            return "a"

    # E
    e_ascii = [200, 201, 202, 203]
    for letter_e in e_ascii:
        if letter_e == number_ascii:
            return "e"

    # I
    i_ascii = [204, 205, 206, 207]
    for letter_i in i_ascii: 
        if letter_i == number_ascii:
            return "i"

    # O
    o_ascii = [210, 211, 212, 213, 214]
    for letter_o in o_ascii:
        if letter_o == number_ascii:
            return "o"

    # U
    u_ascii = [217, 218, 219, 220]
    for letter_u in u_ascii:
        if letter_u == number_ascii:
            return "u"

    # Y
    y_ascii = [221, 253, 159]
    for letter_y in y_ascii:
        if letter_y == number_ascii:
            return "y"

    # Ç
    c_ascii = [140, 199]
    for letter_c in c_ascii:
        if letter_c == number_ascii:
            return "c"

    return c


def exact_counter(letter, c):
    if c in letter:
        letter[c] = letter[c] + 1
    else: 
        letter[c] = 1

    return letter


def fixed_counter(fixedCounter, c, n_times):
    p = 1/8
    for i in range(n_times):
        number_rand = random.random() # generates a number random between 0, 1 only counts if the number generated is less than the p 
        if number_rand < p: 
            if c in fixedCounter:
                fixedCounter[c] = fixedCounter[c] + 1
            else:
                fixedCounter[c] = 1

    return fixedCounter

# implementation of floating point of csursos counter according to the slides 
def fp_increment(X, d, n_times):
    m = pow(2, d)
    t = X/m 
    
    while t > 0:
        for i in range(n_times):
            if random.randint(0, 1) == 1: 
                return X
            t = t - 1

    return X + 1

def csursos_counter(csursoCounter, c, n_times):
    x =  fp_increment(1, 20, n_times)

    if c in csursoCounter:
        csursoCounter[c] = csursoCounter[c] + x
    else:
        csursoCounter[c] = x

    return csursoCounter
   

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

# create file counter results
def create_counter():
    file = open("results_counters.txt", "w")
    file.write("Layout of file\n")
    file.write("------------------------------\n")
    file.write("Ntimes: X \n")
    file.write("Name of book: X - Total of letters: X \n")
    file.write("Exact Counter: \n")
    file.write("Highest letter: X value: X\n")
    file.write("Lowest letter: X value: X\n")
    file.write("MEAN, MAX_DEV, MAD, STDD_DEV\n")
    file.write("Fixed probability with 1/8: \n")
    file.write("Highest letter: X value: X\n")
    file.write("Lowest letter: X value: X\n")
    file.write("MEAN, MAX_DEV, MAD, STDD_DEV\n")
    file.write("Csuros: \n")
    file.write("Highest letter: X value: X\n")
    file.write("Lowest letter: X value: X\n")
    file.write("MEAN, MAX_DEV, MAD, STDD_DEV\n")
    file.write("------------------------------\n")
    file.close()

# write information about counters and statics 
def write_counter(book, ntimes, exct_counter, fixed_counter, csursos, exc):
    file = open("results_counters.txt", "a")
    file.write(f"Ntimes: {ntimes}\n")
    file.write(f"Name of book: {book} - Total of letters: {sum(exct_counter.values())} - Execution time: {exc}\n")
    file.write(f"Exact Counter: {exct_counter}\n")
    file.write(f"Highest letter: {max(exct_counter, key=exct_counter.get)} value: {exct_counter.get(max(exct_counter, key=exct_counter.get))}\n")
    file.write(f"Lowest letter: {min(exct_counter, key=exct_counter.get)} value: {exct_counter.get(min(exct_counter, key=exct_counter.get))}\n")
    mean_ex, max_dev_ex, mad_ex, stdd_ex = statiscs(exct_counter)
    file.write(f"{mean_ex}, {max_dev_ex}, {mad_ex}, {stdd_ex}\n")
    file.write(f"Fixed probability with 1/8: {fixed_counter}\n")
    file.write(f"Highest letter: {max(fixed_counter, key=fixed_counter.get)} value: {fixed_counter.get(max(fixed_counter, key=fixed_counter.get))}\n")
    file.write(f"Lowest letter: {min(fixed_counter, key=fixed_counter.get)} value: {fixed_counter.get(min(fixed_counter, key=fixed_counter.get))}\n")
    mean_fc, max_dev_fc, mad_fc, stdd_fc = statiscs(fixed_counter)
    file.write(f"{mean_fc}, {max_dev_fc}, {mad_fc}, {stdd_fc}\n")    
    file.write(f"Csuros: {csursos}\n")
    file.write(f"Highest letter: {max(csursos, key=csursos.get)} value: {csursos.get(max(csursos, key=csursos.get))}\n")
    file.write(f"Lowest letter: {min(csursos, key=csursos.get)} value: {csursos.get(min(csursos, key=csursos.get))}\n")
    mean_c, max_dev_c, mad_c, stdd_c = statiscs(csursos)
    file.write(f"{mean_c}, {max_dev_c}, {mad_c}, {stdd_c}\n") 
    file.write("------------------------------\n")
    file.close()


# create a visualization of char of each count and each counter and each book
def export_image(dir, book, count, exact_counter, fixed_counter, csursos_counter):    
    ex_letter = list(exact_counter.keys())
    ex_values = list(exact_counter.values())
    
    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(ex_letter, ex_values, color ='green', width = 0.4)
    plt.xlabel("Letter")
    plt.ylabel("Qtd")
    plt.title("Exact Counts")
    plt.savefig(f"{dir}Exact_count of {book} generated in {count}")
    plt.close(fig)
    
    fx_letter = list(fixed_counter.keys())
    fx_values = list(fixed_counter.values())
    
    fig2 = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(fx_letter, fx_values, color ='green', width = 0.4)
    plt.xlabel("Letter")
    plt.ylabel("Qtd")
    plt.title("Fixed probability with 1/8")
    plt.savefig(f"{dir}Fixed_probability_ of {book} generated in {count}")
    plt.close(fig2)


    cs_letter = list(csursos_counter.keys())
    cs_values = list(csursos_counter.values())
    
    fig3 = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(cs_letter, cs_values, color ='green', width = 0.4)
    
    plt.xlabel("Letter")
    plt.ylabel("Qtd")
    plt.title("Csursos Counts")
    plt.savefig(f"{dir}Csursos_count of {book} generated in {count}")
    plt.close(fig3)
        

# read a book file and calculate the counters
def read_file(text_file, n_times):
    file = open(text_file, "r", encoding='utf-8')
    exactCounter = {}
    fixedCounter = {}
    csursoCounter = {}
    list_file = []

    for line in file:
        for character in line:
            # isalpha remove special charecters
            # https://www.w3schools.com/python/ref_string_isalpha.asp
            if character.isalpha() == True:
                c = accents(character).upper()
                if c != "Œ":
                    l = exact_counter(exactCounter, c)
                    exct_counter = dict(sorted(l.items(), key = lambda x:x[0]))
        list_file.append(line)
    file.close()      

    
    for line2 in list_file:
        for character in line2:
            # isalpha remove special charecters
            # https://www.w3schools.com/python/ref_string_isalpha.asp
            if character.isalpha() == True:
                c = accents(character).upper()
                if c != "Œ":
                    fc = fixed_counter(fixedCounter, c, n_times)
                    csurso = csursos_counter(csursoCounter, c, n_times)

 
    return exct_counter, dict(sorted(fc.items(), key = lambda x:x[0])), dict(sorted(csurso.items(), key = lambda x:x[0]))   

def test():
    test = "books/test.txt"


    n_times = [1000, 10000]
    for i in n_times:
        start = time.time()

        print(f"Book {test}\n")
        ex_counter, fc_counter, csurso_counter = read_file(test, i)

        # set counts in exact count - multiply all counts with the number of times
        for c in ex_counter:
            ex_counter[c] = ex_counter[c]*i

        write_counter("test", i, ex_counter, fc_counter, csurso_counter)
        export_image(dir, "test", i, ex_counter, fc_counter, csurso_counter)

        stop = time.time() - start
        print(f"Book test finish in {round(stop, 3)} seconds\n")


def books_english():
    # books available
    bible_file = "books/bible.txt" # https://www.gutenberg.org/files/10/10-0.txt
    war_peace_file = "books/war_and_peace.txt" #https://www.gutenberg.org/files/2600/2600-0.txt
    david_copperfield = "books/david_copperfield.txt" #https://www.gutenberg.org/files/766/766-0.txt
    anna_karenina = "books/anna_karenina.txt" #https://www.gutenberg.org/files/1399/1399-0.txt
 
    list_books = {anna_karenina:"anna_karenina", bible_file:"bible", war_peace_file:"war_and_peace", david_copperfield:"david_copperfield"}
    


if __name__ == "__main__":
    create_file()
    create_counter()
    dir = "resultsImages/"
    
     # books available
    frenchbook = "books/francebook.txt" 
    germanbook = "books/germanbook.txt"
    portuguesebook = "books/portuguesebook.txt" 
    spannishbook = "books/spannishbook.txt" 
    englishbook = "books/anna_karenina.txt"

    list_books = {englishbook:"english", frenchbook:"french", spannishbook:"spannish", portuguesebook:"book"}
    
   
    n_times = [1000, 10000]

    for book in list_books:
        for i in n_times:
            print(f"Time {i}")
            start = time.time()
            print(f"Book {book}\n")
            ex_counter, fc_counter, csurso_counter = read_file(book, i)

            # set counts in exact count - multiply all counts with the number of times
            for c in ex_counter:
                ex_counter[c] = ex_counter[c]*i

            stop = time.time() - start

            write_counter(list_books[book], i, ex_counter, fc_counter, csurso_counter, round(stop, 3))
            export_image(dir, list_books[book], i, ex_counter, fc_counter, csurso_counter)

            print(f"Book {book} finish in {round(stop, 3)} seconds\n")
