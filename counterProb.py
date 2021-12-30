__author__ = "António Ramos"

import random
import math
import matplotlib.pyplot as plt
import time
import sys


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

    # Ñ
    if number_ascii == 209:
        return "n"

    return c

# implementation of exact counter
def exact_counter(letter, c):
    if c in letter:
        letter[c] = letter[c] + 1
    else: 
        letter[c] = 1

    return letter

# implementation of fixed probability with 1/8
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

# implementation of floating point of csuros counter according to the slides 
def fp_increment(X, d, n_times):
    m = pow(2, d)
    t = X/m 
    
    while t > 0:
        for i in range(n_times):
            if random.randint(0, 1) == 1: 
                return X
            t = t - 1

    return X + 1

def csuros_counter(csurosCounter, c, n_times, m, d):
    start = time.time()
    x =  fp_increment(m, d, n_times)

    if c in csurosCounter:
        csurosCounter[c] = csurosCounter[c] + x
    else:
        csurosCounter[c] = x

    return csurosCounter
   

def create_file(): 
    file = open("results.csv", "w")
    file.write("Name:")
    file.write("counter\n")
    file.write("letter,exact_counts,fixed_counts,fixed_prob_small,fixed_prob_av,fixed_prob_larg,fixed_max_dev,fixed_mad,fixed_stdd_dev,csuros_counts,cs_small,cs_av,cs_larg,cs_max_dv,cs_mad,cs_stdd_dev \n")
    file.close()

#create a table with results
def write_file_results(name, counter, exct_counter, fix_counter, cs_counter):
    file = open("results.csv", "a")
    file.write("Name: " + str(name) + "\n")
    file.write(str(counter)+"\n")
    mean_fc, max_dev_fc, mad_fc, stdd_fc = statiscs(fix_counter)
    mean_c, max_dev_c, mad_c, stdd_c = statiscs(cs_counter)

    for char in exct_counter:
        fixed_prob_small = str(min(fix_counter, key=fix_counter.get)) + ":" + str(fix_counter.get(min(fix_counter, key=fix_counter.get)))
        fixed_prob_larg = str(max(fix_counter, key=fix_counter.get)) + ":" + str(fix_counter.get(max(fix_counter, key=fix_counter.get)))
        cs_small = str(min(cs_counter, key=cs_counter.get)) + ":" + str(cs_counter.get(min(cs_counter, key=cs_counter.get)))
        cs_larg = str(max(cs_counter, key=cs_counter.get)) + ":" + str(cs_counter.get(max(cs_counter, key=cs_counter.get)))
        file.write(str(char) + "," + str(exct_counter[char]) + "," + str(fix_counter[char])  + "," + str(fixed_prob_small) + "," + str(mean_fc) + "," + str(fixed_prob_larg) + "," + str(max_dev_fc) + "," + str(mad_fc) + "," + str(stdd_fc) + "," + str(cs_counter[char]) + "," + str(cs_small) + "," + str(mean_c) + "," + str(cs_larg) + "," + str(max_dev_c) + "," + str(mad_c) + "," + str(stdd_c) + "\n")
    
    file.close()

#analise time executation
def create_file_time():
    file = open("results_time.csv", "w")
    file.write("Counter,Exact,Fixed,Csuros\n")
    file.close()

def time_executation(counter, exact, fixed, csuros):
    file = open("results_time.csv", "a")
    file.write(f"{counter},{exact},{fixed},{csuros}\n")
    file.close()

#create a file to study the memory 
def create_file_memory():
    file = open("results_memory.txt", "w")
    file.write("")
    file.close()

#write information in file of memory of counters
def write_file_memory(book, count, exact, fixed, csuros):
    file = open("results_memory.txt", "a")
    file.write(f"Book: {book}\n")
    file.write(f"Memory of Exact Counter: {sys.getsizeof(exact)}\n")
    file.write(f"Counter: {count}\n")
    file.write(f"Memory of Fixed Counter: {sys.getsizeof(fixed)}\n")
    file.write(f"Memory of Csuros Counter: {sys.getsizeof(csuros)}\n")
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
def write_counter(book, ntimes, exct_counter, fixed_counter, csuros):
    file = open("results_counters.txt", "a")
    file.write(f"Ntimes: {ntimes}\n")
    file.write(f"Name of book: {book} - Total of letters: {sum(exct_counter.values())}\n")
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
    file.write(f"Csuros: {csuros}\n")
    file.write(f"Highest letter: {max(csuros, key=csuros.get)} value: {csuros.get(max(csuros, key=csuros.get))}\n")
    file.write(f"Lowest letter: {min(csuros, key=csuros.get)} value: {csuros.get(min(csuros, key=csuros.get))}\n")
    mean_c, max_dev_c, mad_c, stdd_c = statiscs(csuros)
    file.write(f"{mean_c}, {max_dev_c}, {mad_c}, {stdd_c}\n") 
    file.write("------------------------------\n")
    file.close()


# create a visualization of char of each count and each counter and each book
def export_image(dir, book, count, exact_counter, fixed_counter, csuros_counter):    
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
    plt.savefig(f"{dir}Fixed_probability of {book} generated in {count}")
    plt.close(fig2)

    cs_letter = list(csuros_counter.keys())
    cs_values = list(csuros_counter.values())
    
    fig3 = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(cs_letter, cs_values, color ='green', width = 0.4)
    plt.xlabel("Letter")
    plt.ylabel("Qtd")
    plt.title("Csuros Counts")
    plt.savefig(f"{dir}Csuros_count of {book} generated in {count}")
    plt.close(fig3)
        

# read a book file and calculate the counters
def read_file(text_file, n_times, m, d):
    file = open(text_file, "r", encoding='utf-8')
    exactCounter = {}
    fixedCounter = {}
    csurosCounter = {}
    list_file = []
    time_ex = 0
    time_fx = 0
    time_cs = 0
    start_ex = time.time()
    # first read of file to a list, and do exact counting
    for line in file:
        for character in line:
            # isalpha remove special charecters
            # https://www.w3schools.com/python/ref_string_isalpha.asp
            if character.isalpha() == True:
                c = accents(character).upper()
                if c != "Œ":
                    l = exact_counter(exactCounter, c)
                    time_ex = round(time.time() - start_ex, 3)
                    exct_counter = dict(sorted(l.items(), key = lambda x:x[0]))
        list_file.append(line)
    file.close()      

    start_fx = time.time()
    
    #second loop to calculate fixed
    for line2 in list_file:
        for character in line2:
            if character.isalpha() == True:
                c = accents(character).upper()
                if c != "Œ":
                    fc = fixed_counter(fixedCounter, c, n_times)
                    time_fx = round(time.time() - start_fx, 3)

    #third loop to calculate csuros              
    start_cs = time.time()
    for line2 in list_file:
        for character in line2:
            if character.isalpha() == True:
                c = accents(character).upper()
                if c != "Œ":
                    csuros = csuros_counter(csurosCounter, c, n_times, m, d)
                    time_cs = round(time.time() - start_cs, 3)
    

    time_executation(n_times, time_ex, time_fx, time_cs)
    return exct_counter, dict(sorted(fc.items(), key = lambda x:x[0])), dict(sorted(csuros.items(), key = lambda x:x[0]))   


def main(englishbook, frenchbook, spannishbook, portuguesebook):
    list_books = {englishbook:"english", frenchbook:"french", spannishbook:"spannish", portuguesebook:"portuguese"}
    
    n_times = [1000, 10000]
    m = 15
    d = 25
    for book in list_books:
        for i in n_times:
            print(f"Time {i}")
            print(f"Book {book}\n")
            ex_counter, fc_counter, cs_counter = read_file(book, i, m, d)
            write_counter(list_books[book], i, ex_counter, fc_counter, cs_counter)
            write_file_results(list_books[book], i, ex_counter, fc_counter, cs_counter)
            write_file_memory(list_books[book], i, ex_counter, fc_counter, cs_counter)
            export_image(dir, list_books[book], i, ex_counter, fc_counter, cs_counter)


if __name__ == "__main__":
    create_file()
    create_counter()
    create_file_memory()
    create_file_time()
    dir = "resultsImages/"
    
    # books available
    frenchbook = "books/francebook.txt" 
    portuguesebook = "books/portuguesebook.txt" 
    spannishbook = "books/spannishbook.txt" 
    englishbook = "books/bible.txt"
    main(englishbook, frenchbook, spannishbook, portuguesebook)