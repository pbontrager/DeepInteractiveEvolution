import os
import numpy as np
from PIL import Image

#Model server
class ModelServer:

	def __init__(self):
		self.latent_size = 20
		self.img_size = 128

		#Load trained models here (or a server/logic to manage which models are loaded)
		self.random_fc = np.random.beta(2,5,(latent_size, img_size**2))*10 - 5

	#generate images from latent variables return array/tensor
	def generate(self, model, latent_variables):
		#Call trained generator network here (specified by model)
		l1 = latent_variables.dot(self.random_fc)
		sig = 1/(1+np.exp(-l1))
		return np.reshape(sig, (-1, self.img_size, self.img_size))

	#tensor or array of image convert to image format
	def show(self, img_array):
		num = img_array.shape[0]
		imgs = []
		for i in range(num):
			scaled_array = (255*img_array[i]).astype(np.uint8)
			img = Image.fromarray(scaled_array)
			img = img.convert("L")
			imgs.append(img)
		return imgs

	#tensor or array of images converted and saved as .png
	def save(self, img_array, path):
		imgs = self.show(img_array)
		for idx,img in enumerate(imgs):
			img.save(os.path.join(path, "{}.png".format(idx)))
