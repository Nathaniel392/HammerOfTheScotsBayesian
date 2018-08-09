import random
import exceptions
def weighted_prob(dictionary, num_times = 1):

	for key, value in dictionary.items():
		if value <= 0:
			dictionary[key] = 0.00000001


	print('weighted_prob: ' + str(dictionary))
	if num_times <= 0:
		raise Exception('cannot return ' + str(num_times) + ' number of keys')
	if len(dictionary) < num_times:
		raise Exception("asking for more keys than you have in your dictionary")
	
	prev_keys = set()
	return_stuff = weighted_prob2(dictionary, num_times, prev_keys)

	if num_times == 1:
		return return_stuff
	else:
		return prev_keys
def weighted_prob2(dictionary, num_times = 1, prev_keys = set()):
	"""
	takes a dictionary of things
	key is whatever you want (like path or whatever)
	
	key has to be immutable
	value is weight
	"""

	#set all weights add up to 1
	
	

	while True:
		try:
			weight_sum = 0
			for key, item in dictionary.items():
				if item < 0:
					raise Exception('you got negative weight, fool')
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
					
					if num_times == 1:
						
						if key not in prev_keys:
							prev_keys.add(key)

							return key
						else:
							raise exceptions.BreakOutOfLoopException()
					else:
						if key not in prev_keys:
							prev_keys.add(key)
							
							return weighted_prob2(dictionary, num_times - 1, prev_keys)
						else:
							raise exceptions.BreakOutOfLoopException()



			#if for some reason the float rounding makes it not work
			#pick arbitrary key
			for key in dictionary:
				
				if num_times == 1:

					if key not in prev_keys:

						prev_keys.add(key)
						
						return key
					else:
						raise exceptions.BreakOutOfLoopException()
				else:
					if key not in prev_keys:
						prev_keys.add(key)
						return weighted_prob2(dictionary, num_times - 1, prev_keys)
					else:
						raise exceptions.BreakOutOfLoopException()

		except exceptions.BreakOutOfLoopException:
			pass

	

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





