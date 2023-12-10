import json
import os
from .file_writer import write_to_file
from .directory import create_directory_if_not_exist
from ..constants import controller,service,entity,dao,repository,jpaRepository
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("component_migration")

def handle_method_calls_for_component_migration(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "get_migrated_code": get_migrated_code
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments)

def handle_method_calls_for_myBatis_component_migration(code, component, filename):
    get_spring_boot_migrated_code_from_Mybatis(code, component, filename)

def handle_method_calls_for_struts_component_migration(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "get_spring_boot_migrated_code": get_spring_boot_migrated_code
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments)


def handle_method_calls_for_spring_boot_component_migration(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "get_spring_boot_code": get_spring_boot_code
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments)


def get_spring_boot_code(content):
    directory = ""
    if content['component'] == controller:
        directory = os.environ["CONTROLLER_DIRECTORY"]
    elif content['component'] == entity:
        directory = os.environ["ENTITY_DIRECTORY"]
    print(directory+" -- writing code to here")
    create_directory_if_not_exist(directory)
    write_to_file(content['springBootCode'],directory+content['filename'])
    return content


def get_migrated_code(content):
    directory = ""
    if content['component'] == controller:
        directory = os.environ["CONTROLLER_DIRECTORY"]
    elif content['component'] == service:
        directory = os.environ["SERVICE_DIRECTORY"]
    elif content['component'] == entity:
        directory = os.environ["ENTITY_DIRECTORY"]
    elif content['component'] == dao or content['component'] == repository or content['component'] == jpaRepository:
        directory = os.environ["REPOSITORY_DIRECTORY"]
    elif content['component'] == 'Constants':
        directory = os.environ["CONSTANTS_DIRECTORY"]
    elif content['component'] == 'Config':
        directory = os.environ["CONFIG_DIRECTORY"]
    elif content['component'] == 'POJO model':
        directory = os.environ["MODELS_DIRECTORY"]



    print(directory+" -- writing code to here")
    create_directory_if_not_exist(directory)
    write_to_file(content['springBootCode'],directory+content['filename'])
    return content

def get_spring_boot_migrated_code_from_Mybatis(content, component, filename):
    
    directory = ""
    if component == service:
        directory = os.environ["SERVICE_DIRECTORY"]
    elif component == entity:
        directory = os.environ["ENTITY_DIRECTORY"]
    elif component == repository:
        directory = os.environ["REPOSITORY_DIRECTORY"]
    
    print(directory+" -- writing code to here")
    create_directory_if_not_exist(directory)
    write_to_file(content,directory+filename)
    return content


def get_spring_boot_migrated_code(content):
    directory = ""
    if content['component'] == controller:
        directory = os.environ["CONTROLLER_DIRECTORY"]
    elif content['component'] == service:
        directory = os.environ["SERVICE_DIRECTORY"]
    elif content['component'] == entity:
        directory = os.environ["ENTITY_DIRECTORY"]
    elif content['component'] == dao or content['component'] == repository or content['component'] == jpaRepository:
        directory = os.environ["REPOSITORY_DIRECTORY"]
    elif content['component'] == 'Constants':
        directory = os.environ["CONSTANTS_DIRECTORY"]
    elif content['component'] == 'Config':
        directory = os.environ["CONFIG_DIRECTORY"]
    elif content['component'] == 'POJO model':
        directory = os.environ["MODELS_DIRECTORY"]



    print(directory+" -- writing code to here")
    create_directory_if_not_exist(directory)
    write_to_file(content['springBootCode'],directory+content['filename'])
    return content

def get_partial_migrated_code(finalCode, component, filename):
    directory = ""
    if component == controller:
        directory = os.environ["CONTROLLER_DIRECTORY"]
    elif component == service:
        directory = os.environ["SERVICE_DIRECTORY"]
    elif component == entity:
        directory = os.environ["ENTITY_DIRECTORY"]
    elif component == dao or component == repository or component == jpaRepository:
        directory = os.environ["REPOSITORY_DIRECTORY"]
    elif component == 'Constants':
        directory = os.environ["CONSTANTS_DIRECTORY"]
    elif component == 'Config':
        directory = os.environ["CONFIG_DIRECTORY"]
    elif component == 'POJO model':
        directory = os.environ["MODELS_DIRECTORY"]



    print(directory+" -- writing code to here")
    create_directory_if_not_exist(directory)
    write_to_file(finalCode,directory+filename)
