import numpy as np
import json


############################################################### Data Processing ############################################################### 

def toTensor(latent_json):
	latent_object = json.loads(latent_json)
	latent_list = latent_object["input"]
	return np.array(latent_list)

def toJson(latent_tensor):
	latent_list = [list(vec) for vec in latent_tensor]
	latent_object = {"input": latent_list}
	return json.dumps(latent_object)


############################################################### Tensor Manipulation ############################################################### 

#Input: 1D Tensor and int n number of samples
#Output: n random samples from the original tensor (equal probability with replacement)
def randomChoice(tensor, n):
	return np.random.choice(tensor, n, replace=True)
