while True:
	try:
		change = float(input("How much change is owed? "))
	except:
		print("Invalid input.")
		continue

	cash = round(change * 100)
	cents = [25, 10, 5, 1]
	coins = 0

	for cent in cents:
		coins += cash // cent
		cash %= cent
	print(coins)
	break
