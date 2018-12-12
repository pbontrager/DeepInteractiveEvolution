
from app import db

db.drop_all()

import os, shutil
folder = './app/static/tmp'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

db.create_all()


from app.models import Generator
from app.models import EvolutionaryStrategy
from app.models import Category

generator = Generator(name='demo')
#DB change -> NeuralNetwork = Generator
evolution_strategy = EvolutionaryStrategy(name='spherical',population_size=20, latent_size=20)
#DB change -> EvolAI = EvolutionaryStrategy

db.session.add(generator)
db.session.add(evolution_strategy)

db.session.commit()

category = Category(name='Demo', Gene=1, ES=1, visible=True)
# #DB change -> Generator = Category
db.session.add(category)
db.session.commit()
