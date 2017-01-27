from helloWorld import app
from flask_script import Manager

# print app.url_map

manager = Manager(app)


if __name__ == '__main__':
    manager.run()



