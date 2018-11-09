from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, IntegerField, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from app.models import NeuralNetwork, EvolAl, Generator
from wtforms.fields.html5 import DecimalRangeField, IntegerRangeField
from wtforms import Form

# class PreferrenceForm(Form):
#     Preferrence = IntegerRangeField('Preferrence', default=0.0)

class LanguageForm(Form):
    language = SelectMultipleField('Programming Language', choices=[('c++', 'C++'), ('py', 'Python'), ('plain', 'Plain Text')])


class testForm(FlaskForm):
    selection = SelectMultipleField('Choices', choices=[('1','1'),('2','2')], validators=[DataRequired()])
    submit = SubmitField("Next")

class SelectForm(FlaskForm):
    Preferrence = IntegerRangeField('Preferrence', default=0.0)
    selection = SelectMultipleField('Choices', choices=[])
    submit = SubmitField("Next")

class RegisterNNForm(FlaskForm):
    id = IntegerField('Identifier', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_id(self, id):
        neural = NeuralNetwork.query.filter_by(id=id.data).first()
        if neural is not None:
            raise ValidationError('Please use a different id.')

class RegisterEAForm(FlaskForm):
    id = IntegerField('Identifier', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_id(self, id):
        evolal = EvolAl.query.filter_by(id=id.data).first()
        if evolal is not None:
            raise ValidationError('Please use a different id.')

class RegisterGRForm(FlaskForm):
    id = IntegerField('Identifier', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    NN = IntegerField('NeuralNetwork', validators=[DataRequired()])
    EA = IntegerField('EvolotionAlgorithm', validators=[DataRequired()])
    visible = BooleanField('Visible', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_id(self, id):
        gr = Generator.query.filter_by(id=id.data).first()
        if gr is not None:
            raise ValidationError('Please use a different id')

    def validate_NN(self, NN):
        neural = NeuralNetwork.query.filter_by(id=NN.data).first()
        if neural is None:
            raise ValidationError('This NeuralNetwork does not exist')

    def validate_EA(self, EA):
        ea = EvolAl.query.filter_by(id=EA.data).first()
        if ea is None:
            raise ValidationError('This Evolution Algrithm does not exist')
