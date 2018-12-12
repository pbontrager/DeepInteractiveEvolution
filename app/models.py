from app import db

class Generator(db.Model):
    __tablename__ = 'generators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    Gusages = db.relationship('Category', backref='Generator', lazy='dynamic')

    def __repr__(self):
        return '<Id {} Name {}>'.format(self.id, self.name)

class EvolutionaryStrategy(db.Model):
    __tablename__ = 'evolutionarystrategies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    population_size = db.Column(db.Integer)
    latent_size = db.Column(db.Integer)
    Eusages = db.relationship('Category', backref='EvolutionaryStrategy', lazy='dynamic')

    def __repr__(self):
        return '<Id {} Name {}>'.format(self.id, self.name)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    Gene = db.Column(db.Integer, db.ForeignKey("generators.id"))
    ES = db.Column(db.Integer, db.ForeignKey("evolutionarystrategies.id"))
    visible = db.Column(db.Boolean)
    histories = db.relationship('History', backref='Category', lazy='dynamic')

    def __repr__(self):
        return '<Id {} Name {} Gene {} ES {} visible {}>'.format(
            self.id, self.name, self.Generator, self.ES, self.visible)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latentVariabls = db.Column(db.String(10000))
    Cate = db.Column(db.Integer, db.ForeignKey('categories.id'))
    ParentHistory = db.Column(db.Integer)

    def __repr__(self):
        return '<Id {} LatentVariabls {} Category {} Parent {}>'.format(self.id, self.latentVariabls, self.GA, self.ParentHistory)
