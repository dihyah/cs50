from sys import argv
import csv

#opens files to read, compare and display the matching person's name.
def main():
    if len(argv) != 3:
        print("Usage: python dna.py databases/small.csv sequences/4.txt")
        exit(1)
    else:
        csv_path = argv[1]
        csv_file = open(csv_path)
        database = csv.reader(csv_file)
        #for data in database:
           # print(data)
        str_header = next(database)[1:] #collects all the STR
        
        txt_path = argv[2]
        with open(txt_path) as txt_file:
            dna = txt_file.read()
            #for sequences in dna:
               #print(sequences, end='')
            str_pattern = [str_counts(dna, STR) for STR in str_header]  

        #compares number pattern and STR pattern
        for cells in database:
            name = cells[0]
            num_pattern = [ int(number) for number in cells[1:] ]
            if num_pattern == str_pattern:
                print(name)
                exit(0)
        print("No match.")

#calculates individual STR & keeps the longest sequence of STR
def str_counts(dna, sequence):
    repeats = [0] * len(dna)
    for i in range(len(dna) - len(sequence), -1, -1):
        if dna[i: i + len(sequence)] == sequence:
            if (i + len(sequence) > len(dna) -1):
                repeats[i] = 1
            else:
                repeats[i] = 1 + repeats[i + len(sequence)]
    return max(repeats) 

if __name__ == "__main__":
    main()
