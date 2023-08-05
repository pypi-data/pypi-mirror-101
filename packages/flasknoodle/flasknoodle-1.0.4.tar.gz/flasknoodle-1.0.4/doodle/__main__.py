# import data
from doodle.data import data

# import the os module
import os

def main():
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