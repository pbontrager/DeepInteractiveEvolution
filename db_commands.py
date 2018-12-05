import json
import ast
from app import db
import app.models as models
import evolution as evo

def getVisibleModel():
    return models.Category.query.filter_by(visible=True).all()

def createNewLatent():
    # evolution_algrith = Evol.query.filter_by(id = 1).first()
    # evo.evolution_algrith.
    # eval("evo.{}.init({},{})".format(a,b,c)) )
    return json.loads(evo.spherical.init(20, 20))["input"]

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
