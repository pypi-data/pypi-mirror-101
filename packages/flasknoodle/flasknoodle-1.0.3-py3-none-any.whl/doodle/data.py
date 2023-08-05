data = {\
"inits": ["from flask import Flask{}{}\
from main.config import configure_app{}{}\
app = Flask(__name__){}{}\
app = Flask(__name__, instance_relative_config=True, static_folder='./static', template_folder='./templates'){}{}\
configure_app(app){}{}\
import main.view"\
],\
"dotEnvString": "SECRET_KEY=TemporaryString",\
"configString":\
"#import os and dotenv module{}\
import os{}\
from dotenv import load_dotenv{}\
#load environment variables into module{}\
load_dotenv(){}{}\
class BaseConfig(object):{}{}\
SQLALCHEMY_TRACK_MODIFICATIONS = False{}{}\
DEBUG = True{}{}\
TESTING = False{}{}\
class DevelopmentConfig(BaseConfig):{}{}\
DEBUG =  True{}{}\
TESTING = True{}{}\
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'{}{}\
class ProductionConfig(BaseConfig):{}{}\
DEBUG = False{}{}\
TESTING = True{}{}\
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL'){}{}\
config = {{{}{}\
'default': 'main.config.BaseConfig',{}{}\
'development': 'main.config.DevelopmentConfig',{}{}\
'production': 'main.config.ProductionConfig'\
}}{}{}\
def configure_app(app):{}{}\
config_name = os.getenv('FLASK_ENV'){}{}\
app.config.from_object(config['production']){}{}\
app.config.from_pyfile('application.cfg', silent=True)",\
"requirementString":\
"click==7.1.2{}\
Flask==1.1.2{}\
itsdangerous==1.1.0{}\
Jinja2==2.11.2{}\
MarkupSafe==1.1.1{}\
Werkzeug==1.0.1{}\
python-dotenv==0.17.0",\
"manageString": "from main import app{}{}\
if __name__ == '__main__':{}\
{}app.run()",\
"viewString": "#import module{}\
from flask import Flask, url_for, render_template, redirect, request{}\
import os{}\
from main import app{}{}\
#load environment variables into module{}\
from dotenv import load_dotenv{}\
load_dotenv(){}{}\
#get secret key from environment{}\
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY'){}{}\
@app.route('/'){}\
def index():{}{}\
return render_template ('index.html')",\
"indexString": "<!DOCTYPE html>{}\
<html lang='en'>{}\
<head>{}\
<meta charset='UTF-8'>{}{}\
<meta name='viewport' content='width=device-width, initial-scale=1.0'>{}{}\
<title>Flask | Noodle</title>{}{}\
<link rel='stylesheet' type='text/css' href='{}'>{}{}\
</head>{}\
<body>{}{}\
<main>{}{}{}\
<h1>Welcome to Flask Instant Noodle<h1>{}{}{}\
<p>&#169; <strong>Ayokunle Odutayo</strong></p>{}{}\
</main>{}\
</body>{}\
</html>",\
"styleString": "*{{{}\
margin: 0px;{}\
padding: 0px;{}\
}}{}{}\
body {{{}\
box-sizing: border-box;{}\
}}{}{}\
main {{{}\
text-align: center;{}\
width: 80%;{}\
height: 100vh;{}\
margin: auto;{}\
background: rgb(200, 200, 219);{}\
}}"}