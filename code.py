
from os import system
from os import path as p
from os import makedirs

from sys import argv
from json import load, loads

from Generator.models import Models_Generator
from Generator.forms import Forms_Generator
from Generator.views import Views_Generator
from Generator.template_list import Lists_Generator as template_list_generator
from Generator.template_form import Forms_Generator as template_form_generator

from Generator.footer_layout import Footer_Generator as template_footer_generator
from Generator.nav_layout import Navs_Generator as template_nav_generator
from Generator.base_layout import Base_template_generator as template_base_generator


from Generator.url import Urls_Generator
from Generator.url_project import Urls_project_Generator

from Generator.settings import Settings


##################################################
#This tool was developed on python 3.7.4
#Dependencies
# -Django 3.0.5
# --asgiref-3.2.7 django-3.0.5 pytz-2019.3 sqlparse-0.3.1
# --django-crispy-forms
# --psycopg2 Modulo de Postgresql

class sites_generator():
    def __init__(self,app_json,out_path = './SitesGenerated'):
        self.project_name = app_json['name']
        app_json['name']='app'
        obj = app_json #pending convert json to object
        self.app_config = obj
        self.out_path = out_path
        
        print("output"+self.out_path)
        if not p.exists(out_path) :
            makedirs(out_path,0o777)
        
        pass
    
    def create(self):
        # Create Project and app
        try:
            print("Cooking project...")
            self._shell_creator()
            
            # Settings file
            Settings(self.app_config, self.project_name, self.out_path)
            
            # Create Models
            Models_Generator(self.app_config, self.project_name, self.out_path)
            
            # Hacer migraciones
            #self.__make_migrations()
            
            # Migrar
            #self.__migrate()
            
            # 3- Create Forms
            Forms_Generator(self.app_config, self.project_name, self.out_path)
            
            # 4- Create Views
            Views_Generator(self.app_config, self.project_name, self.out_path)
            
            print("Curing the templates files...")
            # 5- Create Templates
            template_list_generator(self.app_config, self.project_name,self.out_path)
            template_form_generator(self.app_config, self.project_name,self.out_path)
            template_nav_generator(self.app_config, self.project_name,self.out_path)
            template_base_generator(self.app_config, self.project_name, self.out_path)
            template_footer_generator(self.app_config, self.project_name, self.out_path)
            
            print("Melting the URLS files...")
            # 6- Set URLs
            Urls_Generator(self.app_config, self.project_name,self.out_path)
            Urls_project_Generator(self.app_config, self.project_name, self.out_path)
            
            print("Done...")
            """
            """
        except Exception as e:
            print(e)
            pass
        pass
    
    def _shell_creator(self):
        self.__start_project()
        self.__start_app()
        pass

    def __start_project(self):
        commands = "cd "+self.out_path+" && django-admin.py startproject "+self.project_name
        system(commands)
        pass
    
    def __start_app(self):
        commands = "cd "+self.out_path+"/"+self.project_name+" && py ./manage.py startapp "+self.app_config['name']
        system(commands)
        pass
    
    def __make_migrations(self):
        commands = "cd "+self.out_path+"/"+self.project_name+" && py ./manage.py makemigrations "+self.app_config['name']
        system(commands)
        
    def __migrate(self):
        commands = "cd "+self.out_path+"/"+self.project_name+" && py ./manage.py migrate "+self.app_config['name']
        system(commands)
    

if __name__ == "__main__":

    logPath = './log.txt'
    
    if not p.exists(logPath):
        logf = open(logPath,"x")
    else:
        logf = open(logPath,"a")
        pass
    
    #argv[1] JSON type
    #argv[2] JSON path | string
    #argv[3] out_path
    
    if len(argv) == 4:
        JSON_type = argv[1]
        input_json = argv[2] 
        out_path = argv[3]
        
        if JSON_type== 'json_path': app = load(open(input_json))
        
        elif JSON_type== 'json_string': app = loads(input_json)
        
        else: app = load(open('./JSON_Examples/admin_products.json'))
            
        
        print(out_path)
        try:
            project = sites_generator(app,out_path)
            project.create()
            
        except Exception as e:
            logf.write(str(e))
            pass
        
    else:
        print('################################')
        print('\tSome arguments are required:')
        print('\t\targv[1] "json_path"|"json_string"')
        print('\t\targv[2] JSON path "./<yourJSONfile>.json" | string Your Json as string ')
        print('\t\targv[3] out_path "<yourOutput Path>"')
        print('################################')
        