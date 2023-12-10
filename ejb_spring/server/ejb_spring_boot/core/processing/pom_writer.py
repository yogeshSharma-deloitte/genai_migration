from ..processing.file_writer import write_to_file
from ..processing.directory import create_directory_if_not_exist
from decouple import config
import json
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("pom_writer")

def handle_function_call(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "get_complete_pom_code": get_complete_pom_code
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments)


def handle_struts_function_call(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "convert_struts_pom_to_spring_boot_pom": convert_struts_pom_to_spring_boot_pom
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments)


def handle_function_call_build_result(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    return function_arguments


def get_complete_pom_code(content):
    directory = os.environ["PROJECT_DIRECTORY"]
    print(directory+" -- writing pom to here")
    create_directory_if_not_exist(directory)
    write_to_file(content['code'],directory+"/pom.xml")
    return content

def convert_struts_pom_to_spring_boot_pom(content):
    directory = os.environ["PROJECT_DIRECTORY"]
    print(directory+" -- writing pom to here")
    create_directory_if_not_exist(directory)
    write_to_file(content['spring_boot_pom_code'],directory+"/pom.xml")
    return content