from sys import argv
import csv
import sqlite3

def main():
    if len(argv) != 2:
        print("Usage: python import.py characters.csv")
        exit(1)

    db = sqlite3.connect("students.db")
    cur = db.cursor()

    csv_path = argv[1]
    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            names = name_split(row["name"])
            if len(names) >= 3:
                cur.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", 
                (names[0], names[1], names[2], row["house"], row["birth"]))
            else:
                cur.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", 
                (names[0], None, names[1], row["house"], row["birth"]))

        db.commit()
        db.close()

def name_split(name):
    names = name.split()
    return names if len(name) >= 3 else (names[0], None, names[1])
     
if __name__ == "__main__":
    main()
