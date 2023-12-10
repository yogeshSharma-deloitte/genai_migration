from langchain.document_loaders import DirectoryLoader,UnstructuredXMLLoader
from ..gen_ai.generate_code import generate_test_cases_for_given_java_code
import json
import os
from .file_writer import write_to_file
from ..constants import controller_test, service_test,main_class_test,entity_test,jpa_repository_test,constants_test,pojo_model_test
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("test_cases_creator")


def create_test_cases_for_migrated_code(application_directory, open_api_key):
    loader = DirectoryLoader(application_directory, glob="**/*.java")
    docs = loader.load()
    logger.info(len(docs))
    #TODO: create prompt for all java source code and generate JUNIT test cases    
    for doc in docs:
        prompt = "Act as Spring Boot Java developer, write the Junit test cases for the following java code. Generate the test-case in such a way which can execute in included version of junit and at the end when validating test result do prepare with assert,assertNotNull,assertEquals and other function as well and add import static org.junit.jupiter.api.Assertions.*; where ever you are using assert functions do not use Verify functions. Use Verify only in case assert do not have right function. This test case class name should append Test at the end to the actual class and where-ever for the new line adding \n add like \\n and same in all the places. Here is input java class for you to generate test cases.\n"
        logger.info(doc.metadata['source'])
        if doc.metadata['source'].__contains__('Constants') or doc.metadata['source'].__contains__('Config') or doc.metadata['source'].__contains__('Repository') or doc.metadata['source'].__contains__('Model'):
            continue
        else:
            # prompt = prompt + "\n" + doc.metadata['source']
            with open(doc.metadata['source']) as f:
                lines = f.readlines()
                # logger.info(lines)
                for line in lines:
                    prompt = prompt + line
                generate_test_cases(prompt, open_api_key)

def generate_test_cases(prompt, open_api_key):
    try:
        chat_response = generate_test_cases_for_given_java_code(prompt, open_api_key)
        handle_function_call_for_test_cases(chat_response.json()['choices'][0]['message'])
    except:
        logger.info("Unable to generate the test case")

def handle_function_call_for_test_cases(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    logger.info(function_call)
    try:
            function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    except:
        function_arguments = assistant_response["function_call"]["arguments"]
    logger.info(function_arguments)
    available_functions = {
        "write_test_cases": write_test_cases
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments)

def write_test_cases(content):
    directory = ""
    if content['component'] == controller_test:
        directory = os.environ["CONTROLLER_TEST_DIRECTORY"]
    elif content['component'] == service_test:
        directory = os.environ["SERVICE_TEST_DIRECTORY"]
    elif content['component'] == main_class_test:
        directory = os.environ["ROOT_TEST_PACKAGE"]
    elif content['component'] == entity_test:
        directory = os.environ["ENTITY_TEST_DIRECTORY"]
    elif content['component'] == jpa_repository_test:
        directory = os.environ["JPA_REPOSITORY_TEST_DIRECTORY"]
    elif content['component'] == constants_test:
        directory = os.environ["CONSTANTS_TEST_DIRECTORY"]
    elif content['component'] == pojo_model_test:
        directory = os.environ["POJO_MODEL_TEST_DIRECTORY"]


    # directory = os.environ["ROOT_PACKAGE"]
    write_to_file(content['generatedTestCode'],directory+"/"+content['filename'])
