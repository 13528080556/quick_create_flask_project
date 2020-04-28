import os

application = """
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager


class Application(Flask):

    def __init__(self,
                 import_name,
                 static_url_path=None,
                 static_folder='static',
                 static_host=None,
                 host_matching=False,
                 subdomain_matching=False,
                 template_folder="templates",
                 instance_path=None,
                 instance_relative_config=False,
                 root_path=None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching,
                         subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)
        self.config.from_pyfile('config/base_setting.py')
        if 'ops_config' in os.environ:
            self.config.from_pyfile('config/{}'.format(os.environ['ops_config']))
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__)
manager = Manager(app)
"""

manager = """
from flask_script import Server

from application import manager, app
import www

manager.add_command('runserver', Server(host='0.0.0.0', port=app.config['PORT']))


def main():
    manager.run()


if __name__ == '__main__':
    main()
"""

index = """
from flask import Blueprint

route_index = Blueprint('index_page', __name__)


@route_index.route('/')
def index():
    return 'Hello World!'


"""

www = """
from application import app
from web.controllers.index import route_index

app.register_blueprint(route_index, url_prefix='/')
"""

requirements = """
Flask_Script==2.0.6
Flask==1.1.2
Flask_SQLAlchemy==2.4.1
"""

base_setting = """
import os

PORT = 5000
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
                            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
"""


class CreateProject:
    current_path = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def create_project(cls, project_name):
        project_dir = os.path.join(cls.current_path, project_name)
        if cls.check_project_dir_exists(project_dir):
            print('该目录已存在')
            return
        os.mkdir(project_dir)
        common_dir = os.path.join(project_dir, 'common')
        libs = os.path.join(common_dir, 'libs')
        models = os.path.join(common_dir, 'models')
        config_dir = os.path.join(project_dir, 'config')
        docs_dir = os.path.join(project_dir, 'docs')
        jobs_dir = os.path.join(project_dir, 'jobs')
        web_dir = os.path.join(project_dir, 'web')
        controllers_dir = os.path.join(web_dir, 'controllers')
        cls.mkdir_package(common_dir)
        cls.mkdir_package(libs)
        cls.mkdir_package(models)
        cls.mkdir_package(config_dir)
        os.mkdir(docs_dir)
        cls.mkdir_package(jobs_dir)
        cls.mkdir_package(web_dir)
        cls.mkdir_package(controllers_dir)
        cls.create_file(os.path.join(config_dir, 'base_setting.py'), base_setting)
        cls.create_file(os.path.join(project_dir, 'application.py'), application)
        cls.create_file(os.path.join(project_dir, 'manager.py'), manager)
        cls.create_file(os.path.join(controllers_dir, 'index.py'), index)
        cls.create_file(os.path.join(project_dir, 'www.py'), www)
        cls.create_file(os.path.join(project_dir, 'requirements.txt'), requirements)
        print('创建项目结构 done')
        os.chdir(project_dir)
        print('创建虚拟环境 ...')
        os.system('python -m venv env')
        print('创建虚拟环境 done')
        os.system(r'env\Scripts\pip.exe install -r requirements.txt')
        os.system(r'env\Scripts\python.exe -m pip install --upgrade pip')
        print('创建项目 done')
        print('即将为你启动项目 ...')
        os.system(r'env\Scripts\python.exe manager.py runserver')

    @classmethod
    def check_project_dir_exists(cls, project_dir):
        return os.path.exists(project_dir)
    
    @classmethod
    def mkdir_package(cls, package_path):
        os.mkdir(package_path)
        f = open(os.path.join(package_path, '__init__.py'), encoding='utf-8', mode='w')
        f.close()
    
    @classmethod
    def create_file(cls, path, content):
        with open(path, encoding='utf-8', mode='w') as f:
            f.write(content)
    
    

if __name__ == "__main__":
    name = input('请输入你想创建的项目名称:\n')
    CreateProject.create_project(name)