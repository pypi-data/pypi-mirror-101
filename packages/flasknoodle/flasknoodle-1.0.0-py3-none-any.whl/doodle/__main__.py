# Import Regex
import re

# import the os module
import os

def main():
    """
    Data Section of Code
    """

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

    """
    Main Code
    """

    # detect the current working directory and print it
    parentDirectory = os.getcwd()

    #server directory name
    serverDirectory = "server"

    #main directory name
    mainDirectory = "main"

    # join server path
    serverPath = os.path.join(parentDirectory, serverDirectory)

    # join main path
    mainPath = os.path.join(serverPath, mainDirectory)

    # join templates path
    templatePath = os.path.join(mainPath, 'templates')

    # join static path
    staticPath = os.path.join(mainPath, 'static')

    # join instance path
    instancePath = os.path.join(mainPath, 'instance')

    """
    Create populate files
    """
    # populate data for .env
    dotEnvString = data["dotEnvString"]

    # populate data for manage.py
    manageString = data["manageString"].format('\n', '\n', '\n', '\t')

    # populate data for requirement
    requirementString = data["requirementString"].format('\n', '\n', '\n', '\n', '\n', '\n')

    # populate data for init file
    initString = data["inits"][0].format('\n', '\n','\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n')

    # populate data for view file
    viewString = data["viewString"].format('\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n',\
    '\n', '\n', '\n', '\n', '\n', '\t')

    # populate data for config file
    configString = data["configString"].format('\n', '\n', '\n', '\n', '\n', '\n',\
    '\n', '\t', '\n', '\t', '\n', '\t', '\n', '\n', '\n', '\t', '\n', '\t',\
    '\n', '\t', '\n', '\n', '\n', '\t', '\n', '\t', '\n', '\t', '\n',\
    '\n', '\n', '\t', '\n', '\t', '\n', '\t', '\n', '\n', '\n', '\t',\
    '\n', '\t', '\n', '\t')

    # populate data for index.html file
    indexString = data["indexString"].format('\n', '\n', '\n', '\n', '\t', '\n',\
    '\t', '\n', '\t', '{{ url_for("static", filename="style.css") }}', '\n', '\t', '\n', '\n', '\t', '\n', '\t',\
    '\t', '\n', '\t', '\t', '\n', '\t', '\n', '\n')

    # populate data for style.css file
    styleString = data["styleString"].format('\n', '\n', '\n', '\n', '\n', '\n', '\n',\
        '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n')

    """
    Create Folder Paths
    """
    # Create the Server directory
    os.makedirs(serverPath) 

    # Create the main directory
    os.makedirs(mainPath) 

    # Create the templates directory
    os.makedirs(templatePath) 

    # Create the static directory
    os.makedirs(staticPath)

    # Create the instance directory
    os.makedirs(instancePath)

    """
    Create Files
    """
    # Create Manage.py file
    with open(serverPath + '/manage.py', 'a') as a_writer:
        a_writer.write(manageString)

    # Create .env file
    with open(serverPath + '/.env', 'a') as a_writer:
        a_writer.write(dotEnvString)

    # Create requirement file
    with open(serverPath + '/requirements.txt', 'a') as a_writer:
        a_writer.write(requirementString)

    # Create init file
    with open(mainPath + '/__init__.py', 'a') as a_writer:
        a_writer.write(initString)

    # Create config file
    with open(mainPath + '/config.py', 'a') as a_writer:
        a_writer.write(configString)

    # Create view file
    with open(mainPath + '/view.py', 'a') as a_writer:
        a_writer.write(viewString)

    # Create application.cfg file
    with open(instancePath + '/application.cfg', 'a') as a_writer:
        a_writer.write("")

    # Create scripts.js file
    with open(staticPath + '/scripts.js', 'a') as a_writer:
        a_writer.write("")

    # Create style.css file
    with open(staticPath + '/style.css', 'a') as a_writer:
        a_writer.write(styleString)
    
    # Create index.html file
    with open(templatePath + '/index.html', 'a') as a_writer:
        a_writer.write(indexString)
    
    return

if __name__ == '__main__':
    main()