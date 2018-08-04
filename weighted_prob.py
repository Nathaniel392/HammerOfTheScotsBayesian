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
	for key in dictionary.items():
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
		if base_flt in rage:
			return key

	return dictionary[0]





