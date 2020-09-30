while True:
	try:
		n = int(input("Enter number(1-8): "))
	except:
		print("Input is not a number!")
		continue

	if n < 1 or n > 8:
		print("Number out of range!")
		continue	

	for i in range(n):
		print((n - 1 - i) * " "+ (i + 1) * "#")
	break
