class Stupid(object):
	def __init__Stupid(self):
		self.hi = 'hi'

def main():
	hey = Stupid()
	if False:
		hey.a = True
	try:
		if hey.a:
			print('hi')
	except AttributeError:
		pass
main()