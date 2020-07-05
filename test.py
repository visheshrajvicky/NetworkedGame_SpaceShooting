xyz = True

def abc():
	print("print")
	global xyz
	xyz = False

abc()
print(xyz)
