from app import db

class NeuralNetwork(db.Model):
    __tablename__ = 'neuralnetworks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    Nusages = db.relationship('Generator', backref='Neural', lazy='dynamic')

    def __repr__(self):
        return '<Id {} Name {}>'.format(self.id, self.name)

class EvolAl(db.Model):
    __tablename__ = 'evolals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    Eusages = db.relationship('Generator', backref='EvolAl', lazy='dynamic')

    def __repr__(self):
        return '<Id {} Name {}>'.format(self.id, self.name)

class Generator(db.Model):
    __tablename__ = 'generators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    NN = db.Column(db.Integer, db.ForeignKey("neuralnetworks.id"))
    EA = db.Column(db.Integer, db.ForeignKey("evolals.id"))
    visible = db.Column(db.Boolean)
    histories = db.relationship('History', backref='Gen', lazy='dynamic')

    def __repr__(self):
        return '<Id {} Name {} NN {} EA {} visible {}>'.format(
            self.id, self.name, self.NN, self.EA, self.visible)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latentVariabls = db.Column(db.String(10000))
    GA = db.Column(db.Integer, db.ForeignKey('generators.id'))
    ParentHistory = db.Column(db.Integer)

    def __repr__(self):
        return '<Id {} LatentVariabls {} Generator {} Parent {}>'.format(self.id, self.latentVariabls, self.GA, self.ParentHistory)
