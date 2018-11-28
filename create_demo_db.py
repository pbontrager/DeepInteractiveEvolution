
from app import db
db.create_all()
from app import NeuralNetwork
from app import EvolAl
from app import Generator

neural_network = NeuralNetwork(nama='demo')
#DB change -> NeuralNetwork = Generator
evolution_algorithm = EvolAl(name='spherical')
#DB change -> EvolAI = EvolutionaryStrategy
generator = Generator(name='Demo', NN=neural_network, EA=evolution_algorithm, visible=True)
#DB change -> Generator = Category
