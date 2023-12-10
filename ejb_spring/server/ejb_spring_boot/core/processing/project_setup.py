from .directory import create_directory_if_not_exist
from decouple import config
import os
import json
from .file_writer import write_to_file
from ..gen_ai.generate_code import create_main_class_for_application
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("project_setup")


def create_spring_boot_project_in_given_directory(spring_boot_path, application_name, package_name, open_api_key, timestamp):
    print("creating project")
    directory = spring_boot_path

    #directory = os.getcwd()+"/"+application_name
    os.environ["PROJECT_DIRECTORY"] = directory
    create_directory_if_not_exist(directory)
    create_directory_if_not_exist(directory+"/src")
    create_directory_if_not_exist(directory+"/documentation")
    create_directory_if_not_exist(directory+"/src/main")
    create_directory_if_not_exist(directory+"/src/test")
    create_directory_if_not_exist(directory+"/src/main/java")
    create_directory_if_not_exist(directory+"/src/test/java")
    create_directory_if_not_exist(directory+"/src/main/resources")
    create_directory_if_not_exist(directory+"/src/main/resources/static")
    create_directory_if_not_exist(directory+"/src/main/resources/templates")
    package_folders = package_name.split(".")
    prev_package_folder = ""
    prev_test_package_folder = ""
    for index, package_folder in enumerate(package_folders):
        if index == 0:
            create_directory_if_not_exist(directory+"/src/main/java/"+package_folder)
            create_directory_if_not_exist(directory+"/src/test/java/"+package_folder)
            prev_package_folder = directory+"/src/main/java/"+package_folder
            prev_test_package_folder = directory+"/src/test/java/"+package_folder
        else:
            create_directory_if_not_exist(prev_package_folder+"/"+package_folder)
            prev_package_folder = prev_package_folder+"/"+package_folder
            prev_test_package_folder = prev_test_package_folder+"/"+package_folder

    os.environ["ROOT_PACKAGE"] = prev_package_folder
    os.environ["ROOT_TEST_PACKAGE"] = prev_test_package_folder
    create_directory_if_not_exist(prev_package_folder+"/controllers")
    create_directory_if_not_exist(prev_package_folder+"/services")
    create_directory_if_not_exist(prev_package_folder+"/config")
    create_directory_if_not_exist(prev_package_folder+"/models")
    create_directory_if_not_exist(prev_package_folder+"/entity")
    create_directory_if_not_exist(prev_package_folder+"/repository")
    create_directory_if_not_exist(prev_package_folder+"/constants")
    create_directory_if_not_exist(prev_package_folder+"/services/impl")
    create_directory_if_not_exist(prev_test_package_folder+"/controllers")
    create_directory_if_not_exist(prev_test_package_folder+"/services")
    create_directory_if_not_exist(prev_test_package_folder+"/config")
    create_directory_if_not_exist(prev_test_package_folder+"/models")
    create_directory_if_not_exist(prev_test_package_folder+"/entity")
    create_directory_if_not_exist(prev_test_package_folder+"/repository")
    create_directory_if_not_exist(prev_test_package_folder+"/constants")
    create_directory_if_not_exist(prev_test_package_folder+"/services/impl")
    os.environ["CONTROLLER_DIRECTORY"] = prev_package_folder+"/controllers/"
    os.environ["SERVICE_DIRECTORY"] = prev_package_folder+"/services/"
    os.environ["REPOSITORY_DIRECTORY"] = prev_package_folder+"/repository/"
    os.environ["ENTITY_DIRECTORY"] = prev_package_folder+"/entity/"
    os.environ["CONSTANTS_DIRECTORY"] = prev_package_folder+"/constants/"
    os.environ["CONFIG_DIRECTORY"] = prev_package_folder+"/config/"
    os.environ["MODELS_DIRECTORY"] = prev_package_folder+"/models/"
    os.environ["CONTROLLER_TEST_DIRECTORY"] = prev_test_package_folder+"/controllers/"
    os.environ["SERVICE_TEST_DIRECTORY"] = prev_test_package_folder+"/services/"
    os.environ["ENTITY_TEST_DIRECTORY"] = prev_test_package_folder+"/entity/"
    os.environ["JPA_REPOSITORY_TEST_DIRECTORY"] = prev_test_package_folder+"/repository/"
    os.environ["CONSTANTS_TEST_DIRECTORY"] = prev_test_package_folder+"/constants/"
    os.environ["POJO_MODEL_TEST_DIRECTORY"] = prev_test_package_folder+"/models/"


    os.environ["PACKAGE_NAME"] = package_name
    os.environ["RESOURCES_PACKAGE"] = directory+"/src/main/resources"
    os.environ["APPLICATION_NAME"] = application_name
    
    main_class_creation_prompt = "Create a spring boot main java class for application name "+application_name+" and include package "+package_name
    chat_response = create_main_class_for_application(main_class_creation_prompt, open_api_key)
    
    handle_function_class_for_main_class_creation(chat_response.json()['choices'][0]['message'])

    #os.environ["SERVICE_DIRECTORY"] = directory

def handle_function_class_for_main_class_creation(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "get_main_class_code": get_main_class_code
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments)

def get_main_class_code(content):
    directory = os.environ["ROOT_PACKAGE"]
    write_to_file(content['mainClassCode'],directory+"/"+content['filename'])



        




