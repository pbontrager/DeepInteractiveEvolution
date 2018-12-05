
from app import db

db.drop_all()
db.create_all()

from app.models import Generator
from app.models import EvolutionaryStrategy
from app.models import Category

generator = Generator(name='demo')
#DB change -> NeuralNetwork = Generator
evolution_strategy = EvolutionaryStrategy(name='spherical')
#DB change -> EvolAI = EvolutionaryStrategy

db.session.add(generator)
db.session.add(evolution_strategy)

db.session.commit()

category = Category(name='Demo', Gene=1, ES=1, visible=True)
# #DB change -> Generator = Category
db.session.add(category)
db.session.commit()