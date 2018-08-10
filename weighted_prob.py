import random
import exceptions
import numpy as np
def weighted_prob(dictionary, num_times = 1):

	for key, value in dictionary.items():
		if value <= 0:
			dictionary[key] = 0.00000001




	prev_keys = set()
	return_stuff = weighted_prob2(dictionary, num_times, prev_keys)

	if num_times == 1:
		return return_stuff

def weighted_prob2(dictionary, num_times = 1, prev_keys = set()):
	"""
	takes a dictionary of things
	key is whatever you want (like path or whatever)
	
	key has to be immutable
	value is weight
	"""

	#set all weights add up to 1
	original_dict = dict(dictionary)
	
	summation = 0
	key_type = None

	key_dict = {}

	count = 0
	for key,value in dictionary.items():
		key_dict[str(count)]= key
		count += 1

		key_type = type(key)
		if value < 0:
			dictionary[key] = 0
			value = 0
		summation += value


	keys = []
	probs = []
	for key,value in dictionary.items():
		dictionary[key] = value/summation
		keys.append(key)
		probs.append(value/summation)

	keys = list(key_dict.keys())

	if sum(probs) < 1:
		probs.append(1-sum(probs))
		keys.append('do nothing')



	choice_list = np.random.choice(keys, 1, replace=True, p=probs)

	choice = str(choice_list[0])


	return key_dict[choice]



def main():
	dictionary = {'hi': .125, 'hey': .375, 'hello': .4, 'u bad': .1}
	hey = {'hey':0, 'hi': 0, 'hello': 0, 'u bad': 0}
	#for i in range(1000):
		#hey[weighted_prob(dictionary)] += 1

	for i in range(500):
		for key in weighted_prob(dictionary, 2):
			hey[key] += 1
	print(hey)


if __name__ == '__main__':
	main()





