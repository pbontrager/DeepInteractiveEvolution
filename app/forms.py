from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, IntegerField, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from app import models
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

class RegisterGRForm(FlaskForm):
    id = IntegerField('Identifier', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_id(self, id):
        generator = Generator.query.filter_by(id=id.data).first()
        if generator is not None:
            raise ValidationError('Please use a different id.')

class RegisterESForm(FlaskForm):
    id = IntegerField('Identifier', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_id(self, id):
        evolutionarystrategy = EvolutionaryStrategy.query.filter_by(id=id.data).first()
        if evolutionarystrategy is not None:
            raise ValidationError('Please use a different id.')

class RegisterCATEForm(FlaskForm):
    id = IntegerField('Identifier', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    Gene = IntegerField('Generator', validators=[DataRequired()])
    ES = IntegerField('EvolutionaryStrategy', validators=[DataRequired()])
    visible = BooleanField('Visible', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_id(self, id):
        category = Category.query.filter_by(id=id.data).first()
        if category is not None:
            raise ValidationError('Please use a different id')

    def validate_Gene(self, Gene):
        generator = Generator.query.filter_by(id=NN.data).first()
        if generator is None:
            raise ValidationError('This Generator does not exist')

    def validate_ES(self, ES):
        evolutionarystrategy = EvolutionaryStrategy.query.filter_by(ES=EA.data).first()
        if evolutionarystrategy is None:
            raise ValidationError('This Evolution Algrithm does not exist')
