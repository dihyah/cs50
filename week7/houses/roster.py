from sys import argv
import sqlite3

if len(argv) != 2:
    print("Usage: python roster.py house(Gryffindor, Slytherin, Ravenclaw or Hufflepuffs)")
    exit(1)

house = argv[1]

conn = sqlite3.connect("students.db")
cur = conn.cursor()

exe = cur.execute("SELECT * FROM students WHERE house LIKE ? ORDER BY last, first;", [house])

for row in exe:
    first, middle, last, birth = row[1], row[2], row[3], row[5]
    if middle == None:
        print(f"{first} {last}, born {birth}")
    else:
        print(f"{first} {middle} {last}, born {birth}")

conn.close()
