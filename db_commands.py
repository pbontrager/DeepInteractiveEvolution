import json
import ast
from app import db
import app.models as models
import evolution as evo

def getVisibleModel():
    return models.Category.query.filter_by(visible=True).all()

def initPopulation(category):
    # evolution_algrith = Evol.query.filter_by(id = 1).first()
    # evo.evolution_algrith.
    # eval("evo.{}.init({},{})".format(a,b,c)) )
    es_index =  models.Category.query.filter_by(name=category).first().ES
    evolutionarystrategy = models.EvolutionaryStrategy.query.filter_by(id=es_index).first()
    es_name = evolutionarystrategy.name
    es_population = evolutionarystrategy.population_size
    es_latentsize = evolutionarystrategy.latent_size
    return json.loads(eval("evo.{}.init({},{})".format(es_name,es_population,es_latentsize)))["input"]

def getCurLatentVar(lastid):
    curlatentVar = models.History.query.filter_by(id = lastid).first().latentVariabls
    curlatentVar = ast.literal_eval(curlatentVar)
    curlatentVar = json.dumps({"input":curlatentVar})
    return curlatentVar

def createNextLatentVar(curlatentVar, choices, noise, para):
    nextLatentVar = evo.spherical.next(curlatentVar, choices, noise, para)          #Database: eval type
    nextLatentVar = json.loads(nextLatentVar)["input"]
    return nextLatentVar

def createNewHistory(latentVar, choice):
    newHis = models.History(latentVariabls=str(latentVar), Cate=str(choice))     #This to makedirctory, maybe make a function
    db.session.add(newHis)
    db.session.commit()
    return newHis.id

def getCategory(lastid):
    Category = models.History.query.filter_by(id=lastid).first().Cate
    return Category
