import numpy as np
import json
import math
import evolution._common as c


def init(population, latent):
	pop = np.random.normal(loc=0, scale=1, size=(population, latent))
	return c.toJson(pop)

#latentVariables: latent variables json string
#indices: list of selected indices of the images
#noise: float of std value
#parameters: json string of values used for evolution
	#foreign - number of foreign memebers to add each round
	#mutation - probability that a mutation will occur
def next(latent_variables, indices, noise, parameters):
	p = json.loads(parameters)
	variables = c.toTensor(latent_variables)
	selected = np.array(indices)
	pop_size, latent_size = variables.shape
	select_size = selected.shape[0]
	crossover_size = int(max(pop_size - select_size - p["foreign"], 0))
	foreign_size = int(min(pop_size - select_size, p["foreign"]))

	#Crossover
	A = variables[c.randomChoice(selected, crossover_size)]
	B = variables[c.randomChoice(selected, crossover_size)]
	T = np.random.uniform(low=0, high=1, size=crossover_size)
	crossover = _slerp(T, A, B)

	#New random members
	new = np.random.normal(loc=0, scale=1, size=(foreign_size, latent_size))

	#Mutate
	next_pop = np.concatenate((variables[selected], crossover))
	next_pop = _mutate(next_pop, noise, p["mutation"])
	next_pop = np.concatenate((next_pop, new))

	return c.toJson(next_pop)

def _slerp(t, a, b):
	unit_a = a / np.transpose([np.linalg.norm(a, 2, 1)])
	unit_b = b / np.transpose([np.linalg.norm(b, 2, 1)])

	omega = np.sum(unit_a*unit_b, 1)
	omega = np.arccos(np.clip(omega, -1, 1)) + 1e-8

	weighted_a = np.transpose(np.sin(omega*(1-t))/np.sin(omega)*np.transpose(a))
	weighted_b = np.transpose(np.sin(omega*t)/np.sin(omega)*np.transpose(b))
	return weighted_a + weighted_b

def _mutate(a, noise, prob):
	size = a.shape[0]
	mask = np.random.binomial(1, prob, size)
	t = -math.log(1-.9*noise, 10)*mask
	b = np.random.uniform(low=0, high=1, size=a.shape)
	return _slerp(t, a, b)

############### Test ###############
# import math

# #Fast approximation of slerp
# #Need batch lerp
# #def _fastSlerp(t, a, b):
# #	x = torch.lerp(t, a, b)
# #	x = torch.renorm(x, 2, 0, 1)
# #	return x

# pop = init(5,5)
# print(pop)
# latents = c.toTensor(pop)
# print(_mutate(latents, .2, .5))
# A = latents[c.randomChoice(np.array([0,1,2,3]), 4)]
# B = latents[c.randomChoice(np.array([0,1,2,3]), 4)]
# print(_slerp(.5, A, B))
# params = json.dumps({"mutation": 0.5, "foreign": 0.2})
# print(next(pop, np.array([0,1,2,3]), .2, params))
