import random
def weighted_prob(dictionary):
	"""
	takes a dictionary of things
	key is whatever you want (like path or whatever)
	value is weight
	"""

	#set all weights add up to 1
	weight_sum = 0
	for key, item in dictionary.items():
		weight_sum += item
	for key in dictionary:
		dictionary[key] /= float(weight_sum)


	#set range dictionaries
	#keys are same as in dictionary
	#value is a tuple (a range)
	range_dict = dict()
	prev_top_range = 0
	for key, item in dictionary.items():
		range_dict[key] = (prev_top_range, prev_top_range + item)
		prev_top_range += item

	#select key
	base_flt = random.uniform(0.0, 1.0)

	for key, rage in range_dict.items():

		if base_flt <= rage[1] and base_flt > rage[0]:
			return key

	

def main():
	dictionary = {'hi': .25, 'hey': .75}
	hey = {'hey':0, 'hi': 0}
	for i in range(1000):
		hey[weighted_prob(dictionary)] += 1
	print(hey)


if __name__ == '__main__':
	main()





