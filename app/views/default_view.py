'''
########################################################
# Name Project: qrG1Code                               #
# Developer Name: Mário Wessen                         #
# Contact: mrfwn@cin.ufpe.br                           #
# Date last Modify:  25/06/2019                        #
# Description File: This is Controller ,               #
# for access pages                                     #
########################################################
'''
from app import app
from flask import Flask,render_template,flash
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField,PasswordField,Form, FieldList, FormField ,SelectField
from app.services.contact_service import Contact
from wtforms import validators

class LapForm(Form):
    url = StringField('URL:',[validators.Required()])


class MainForm(FlaskForm):
    laps = FieldList(
        FormField(LapForm),
        min_entries=1,
        max_entries=20
    )
    check = SelectField('Destino',choices=[('','Selecione o Destino'),('rec','Arte Recife'),('sp','Arte São Paulo'),('rj','Arte Rio de Janeiro')], default='',validators=[validators.Required(message=('Region is required'))])
    email = StringField('Email',[validators.Required()])
    password = PasswordField('Senha',[validators.Required()])
   

@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = MainForm()
    alert = None
    if form.validate_on_submit():
        instance = Contact()
        if instance.urlFormat(form.data['laps'],form.data['email'],form.data['password'],form.data['check']):
            alert=True
            return render_template('home_template.html',form=form,data=form.data,alert=alert) 
        else:
            alert=False
            return render_template('home_template.html',form=form,data=form.data,alert=alert)         
    return render_template('home_template.html', form=form,alert=alert)


    


