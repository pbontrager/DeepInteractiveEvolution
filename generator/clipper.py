#Need Clipper Server Setup to use this

import os
import numpy as np
from PIL import Image

from clipper_admin import ClipperConnection, DockerContainerManager

import shoe2
import numpy as np
from torch import nn
from clipper_admin.deployers.pytorch import deploy_pytorch_model


from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())
clipper_conn.start_clipper()

clipper_conn.register_application(name="Shoe", input_type="doubles", default_output="-1.0", slo_micros=30000000)

import os
#import random

import torch
import torch.nn as nn
#import torch.nn.parallel
#import torch.backends.cudnn as cudnn
#import torch.optim as optim
import torchvision.utils as vutils
from torch.autograd import Variable

#Model server
class ModelServer:

	def __init__(self):
		self.latent_size = 20
		self.img_size = 128

		model = loadModel()
		deploy_pytorch_model(
		    clipper_conn,
		    name="example",
		    version = 1,
		    input_type="doubles",
		    func=predict,
		    pytorch_model=model
	    )

		clipper_conn.link_model_to_app(app_name="Shoe", model_name="example")


	#generate images from latent variables return array/tensor
	def generate(self, model, latent_variables):
		trans = shift(inputs)
    	pred = model(trans)
	    pred = pred.data.numpy()
	    #Fix bug, append str(pred.shape) tuple as string, and append dtype
	    return pred.astype(np.str).tolist()


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

	def __del__(self):
		clipper_conn = ClipperConnection(DockerContainerManager())
		clipper_conn.stop_all()

class Generator(nn.Module):
    def __init__(self, img_dim, noise_dim):
        super(Generator, self).__init__()
        DIM = 128

        preprocess = nn.Sequential(
            nn.Linear(noise_dim, 4 * 4 * 8 * DIM),
            nn.BatchNorm2d(4 * 4 * 8 * DIM),
            nn.ReLU(True)
        )

        block1 = nn.Sequential(
            nn.ConvTranspose2d(8 * DIM, 8 * DIM, 2, stride=2, padding=0),
            nn.BatchNorm2d(8 * DIM),
            nn.ReLU(True),
        )
        block2 = nn.Sequential(
            nn.ConvTranspose2d(8 * DIM, 4 * DIM, 2, stride=2, padding=0),
            nn.BatchNorm2d(4*DIM),
            nn.ReLU(True),
        )
        block3 = nn.Sequential(
            nn.ConvTranspose2d(4 * DIM, 2 * DIM, 2, stride=2, padding=0),
            nn.BatchNorm2d(2*DIM),
            nn.ReLU(True),
        )
        block4 = nn.Sequential(
            nn.ConvTranspose2d(2 * DIM, DIM, 2, stride=2, padding=0),
            nn.BatchNorm2d(DIM),
            nn.ReLU(True),
        )
        deconv_out = nn.ConvTranspose2d(DIM, 3, 2, stride=2, padding=0)

        self.dim = DIM
        self.noise = noise_dim
        self.size = img_dim
        self.preprocess = preprocess
        self.block1 = block1
        self.block2 = block2
        self.block3 = block3
        self.block4 = block4
        self.deconv_out = deconv_out
        self.tanh = nn.Tanh()

    def forward(self, input):
        output = input.view(-1, self.noise)
        output = self.preprocess(output)
        output = output.view(-1, 8 * self.dim, 4, 4)
        output = self.block1(output)
        output = self.block2(output)
        output = self.block3(output)
        output = self.block4(output)
        output = self.deconv_out(output)
        output = self.tanh(output)
        return output.view(-1, 3, self.size, self.size)

def loadModel():
	netG = Generator(128,20)
	#netG.cuda()
	netG.load_state_dict(torch.load("./shoe2", map_location=lambda storage, loc: storage))
	netG.eval()
	return netG

def shift(inputs):
    output = Variable(torch.Tensor(inputs))
    return output
