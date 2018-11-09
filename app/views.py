from app import app
from flask import Response, render_template, flash, redirect, url_for, request
import app.forms as forms
import app.models as models
from app import db
from flask import jsonify, send_file, session, send_from_directory
import base64
import requests, json, numpy as np
import os
import re
from io import BytesIO
from flask import Flask, abort, send_file
#from PIL import Image, ImageDraw
import ast

import generator.demo as modelserver	#where do I initialize modelserver so it persists?
#All the Clipper specific code can be added to a generator file like Demo so it is not lost.
#We don't want any PyTorch Requirements
import evolution as evo

ms = modelserver.ModelServer()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    results = models.Generator.query.filter_by(visible=True).all()
    return render_template('index.html',
        title='Deep IE', results=results)

@app.route('/start', methods=['GET', 'POST'])
def start():
    results = models.Generator.query.filter_by(visible=True).all()
    choice = request.args.get('values')
    latentVar = json.loads(evo.spherical.init(20, 20))["input"]			#init needs to come from db as well as spherical
    newHis = History(latentVariabls=str(latentVar), GA=str(choice))
    db.session.add(newHis)
    db.session.commit()
    his_ID=newHis.id
    directory = "./app/static/tmp/{}".format(his_ID)
    if os.path.exists(directory):
        return redirect(url_for('{}'.format(his_ID)))
    os.makedirs(directory)

    #headers = {"Content-type": "application/json"}
    #x = requests.post("http://localhost:1337/" + choice + "/predict", headers=headers, data=json.dumps({"input_batch": latentVar})).json()
    #batchString = x['batch_predictions']
    #resString = [ast.literal_eval(b['output']) for b in batchString]

    #res_tensor = np.array(resString, dtype='float64')
    #res_tensor = Tensor(res_list)
    #for i in range(0,20):
        #img = Image.fromarray(res_tensor[i])
        #img.save("./app/static/tmp/{}/{}.png".format(his_ID, i))
        #torchvision.utils.save_image(res_tensor[i], "./app/static/tmp/{}/{}.png".format(his_ID, i), normalize=True)

    imgs = ms.generate("demo_noise", latentVar)
    ms.save(imgs, directory)

    return redirect(url_for('show', id = his_ID))


@app.route('/prepare',methods=['GET', 'POST'])
def prepare():
    data = json.loads(request.data)
    preference = float(data['p'])
    cho = data["c"]
    choices = []
    for c in cho:
        choices.append(int(c))
    lastid = int(data["id"])
    curlatentVar = History.query.filter_by(id = lastid).first().latentVariabls
    curlatentVar = ast.literal_eval(curlatentVar)
    curlatentVar = json.dumps({"input":curlatentVar})
    noise = preference
    para = json.dumps({"foreign":2, "mutation":0.5})
    nextLatentVar = evo.spherical.next(curlatentVar, choices, noise, para)
    nextLatentVar = json.loads(nextLatentVar)["input"]
    Gene = History.query.filter_by(id=lastid).first().GA;
    newHis = History(latentVariabls=str(nextLatentVar), GA=str(Gene), ParentHistory=lastid)
    db.session.add(newHis)
    db.session.commit()
    his_ID=newHis.id
    directory = "./app/static/tmp/{}".format(his_ID)
    if os.path.exists(directory):
        return redirect(url_for('{}'.format(his_ID)))
    os.makedirs(directory)

    #headers = {"Content-type": "application/json"}
    #x = requests.post("http://localhost:1337/" + Gene + "/predict", headers=headers, data=json.dumps({"input_batch": nextLatentVar })).json()
    #batchString = x['batch_predictions']
    #resString = [ast.literal_eval(b['output']) for b in batchString]

    #res_list = np.array(resString, dtype='float64')
    #res_tensor = Tensor(res_list)
    #for i in range(0,20):
    #    torchvision.utils.save_image(res_tensor[i], "./app/static/tmp/{}/{}.png".format(his_ID, i), normalize=True)

    imgs = ms.generate("demo_noise", nextLatentVar)
    ms.save(imgs, directory)

    nextUrl = "/" + str(his_ID)
    return nextUrl

#What is this for, there are no user logins?
@app.route('/signUpUser', methods=['GET', 'POST'])
def signUpUser():
    data = request.data;
    data = json.loads(data)
    preference = float(data['p'])
    cho = data["c"]
    choice = []
    for c in cho:
        choice.append(int(c))
    print(preference)
    print(type(preference))
    print(choice)
    print(type(choice))

    return "/15"

#?
@app.route('/test1', methods=['GET', 'POST'])
def test1():
    username = "user"
    password = "123"
    return render_template("test1.html", username=username, password=password)

#Is there a button for this?
@app.route('/tmp/<id>/<filename>')
def download_file(id, filename):
    pilImage = open('./app/static/tmp/{}/'.format(id)+filename,'rb')
    response = send_file(pilImage, mimetype='image/png')
    return response


@app.route('/<int:id>', methods=['GET', 'POST'])
def show(id):
    results = modelsGenerator.query.filter_by(visible=True).all()
    forms.Selectform = SelectForm()
    #Choices = [('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10'), ('11','11'), ('12','12'), ('13','13'), ('14','14'), ('15','15'), ('16','16'), ('17','17'), ('18','18'), ('19','19'), ('20','20')]
    Choices = [(str(i),str(i)) for i in range(20)] #This 20 should come from the population size
    forms.Selectform.selection.choices = Choices
    tmps = os.listdir('./app/static/tmp/{}'.format(id))
    paths=[]
    for tmp in tmps:
        if '.png' in tmp:
            paths.append('/tmp/{}/'.format(id) + tmp)
        else:
            continue
    dataset=zip(paths,Selectform.selection)

    return render_template('show.html', generationid=id, select=Selectform, results=results, dataset=dataset)

#We need to come up with a better naming convention for all of these: 
#Evol -> EvolutionaryStrategy (ES)
#Gen vs Neural? -> Generator
#Ele, history, develop?
@app.route('/develop', methods=['GET', 'POST'])
def develop():
    neural = NeuralNetwork.query.all()
    evolal = EvolAl.query.all()
    gene = Generator.query.all()
    return render_template('develop.html', neuraldata =  neural, evolaldata = evolal, genedata = gene)

@app.route('/history', methods=['GET', 'POST'])
def history():
    history = History.query.all()
    return render_template('history.html', historydata =  history)

@app.route('/addNeural', methods=['GET', 'POST'])
def addNeural():
    form = RegisterNNForm();
    if form.validate_on_submit():
        neuralnetwork = NeuralNetwork(id=form.id.data, name=form.name.data)
        db.session.add(neuralnetwork)
        db.session.commit()
        flash('Congratulations, you are now a registered Neural Network!')
        return redirect(url_for('develop'))
    return render_template('addNeural.html', title='Deep IE', form=form)

@app.route('/addEvol', methods=['GET', 'POST'])
def addEvol():
    form = RegisterEAForm();
    if form.validate_on_submit():
        evolutionAl = EvolAl(id=form.id.data, name=form.name.data)
        db.session.add(evolutionAl)
        db.session.commit()
        flash('Congratulations, you are now a registered Evolution Algorithm!')
        return redirect(url_for('develop'))
    return render_template('addEvol.html', title='Deep IE', form=form)

@app.route('/addGen', methods=['GET', 'POST'])
def addGen():
    form = RegisterGRForm()
    if form.validate_on_submit():
        generator = Generator(id=form.id.data, name=form.name.data,NN=form.NN.data, EA=form.EA.data, visible=form.visible.data)
        db.session.add(generator)
        db.session.commit()
        flash('Congratulations, you are now a registered Generator!')
        return redirect(url_for('develop'))
    return render_template('addGen.html', title='Deep IE', form=form)

@app.route('/DeleteEle', methods=['GET', 'POST'])
def deleteEle():
    NN = NeuralNetwork.query.all()
    EA = EvolAl.query.all()
    Gen = Generator.query.all()
    return render_template('deleteEle.html', title='Deep IE', NN=NN, EA=EA, GE=Gen)
