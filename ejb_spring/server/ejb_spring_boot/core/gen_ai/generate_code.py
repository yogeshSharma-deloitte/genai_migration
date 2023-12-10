import openai
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import requests
from .functions import get_functions_for_pom_generation, get_functions_for_code_identification, \
    get_functions_for_code_migration, get_functions_for_main_class_creation, get_functions_for_test_cases_generation, \
    get_functions_for_application_properties_generation, get_functions_for_build_improvements, \
    get_functions_for_documentation_generation, get_functions_for_struts_pom_generation, \
    get_functions_for_code_struts_identification, get_functions_for_struts_code_migration, \
    get_functions_for_mybatis_code_migration, get_functions_for_jpa_repository, \
    get_function_for_spring_boot_api_code_by_specification, get_function_for_kitty_specification, \
    get_functions_for_data_migration_code, get_functions_for_batch_code, get_functions_for_data_lake_code, \
    get_functions_for_sql, get_functions_for_unit_tests, get_functions_for_docs, get_functions_for_infra_code
from .conversation import Conversation
from ..processing.pom_writer import handle_function_call, handle_function_call_build_result, handle_struts_function_call
from ..gen_ai.prompts import system_prompt_other_file_description_template,system_prompt_convert_code_template,system_prompt_generate_test_cases_template, system_prompt_generate_application_properties_template, mainclassPrompt, system_prompt_convert_partial_code_template, system_prompt_other_file_description_template_struts, system_prompt_convert_struts_code_template, system_prompt_struts_pom, systemPrompt_mybatis, system_prompt_generate_kitty_file
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("generate_code")

# GPT_MODEL = "gpt-3.5-turbo-0613"
# GPT_MODEL = "gpt-3.5-turbo-16k"
GPT_MODEL = "gpt-4-32k"


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, model=GPT_MODEL, open_api_key=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + open_api_key,
    }
    json_data = {"model": model, "messages": messages,"temperature": 0.01}
    if functions is not None:
        json_data.update({"functions": functions})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        logger.info("Unable to generate ChatCompletion response")
        logger.info(f"Exception: {e}")
        return e
    

def improve_build_result(prompt):
    conversation = Conversation()
    conversation.add_message("user", prompt)
    functions = get_functions_for_build_improvements()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions
    )
    return handle_function_call_build_result(chat_response.json()['choices'][0]['message'])


def initiate_api(prompt, open_api_key):
    conversation = Conversation()
    conversation.add_message("user", prompt)
    functions = get_functions_for_pom_generation()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    handle_function_call(chat_response.json()['choices'][0]['message'])

def initiate_api_struts(prompt, open_api_key):
    conversation = Conversation()
    conversation.add_message("system", system_prompt_struts_pom)
    conversation.add_message("user", prompt)
    functions = get_functions_for_struts_pom_generation()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    handle_struts_function_call(chat_response.json()['choices'][0]['message'])



def get_details_of_other_files(prompt, open_api_key):
    print(prompt)
    conversation = Conversation()
    conversation.add_message("system", system_prompt_other_file_description_template)
    conversation.add_message("user", prompt)
    functions = get_functions_for_code_identification()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )

    return chat_response


def get_details_of_other_files_for_struts(prompt, open_api_key):
    print(prompt)
    conversation = Conversation()
    conversation.add_message("system", system_prompt_other_file_description_template_struts)
    conversation.add_message("user", prompt)
    functions = get_functions_for_code_struts_identification()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )

    return chat_response

def get_details_of_other_files_for_mybatis(prompt, open_api_key):
    print(prompt)
    conversation = Conversation()
    conversation.add_message("system", systemPrompt_mybatis)
    conversation.add_message("user", prompt)
    functions = get_functions_for_mybatis_code_migration()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )

    return chat_response




# handle_method_calls_for_preprocessing(chat_response.json()['choices'][0]['message'])

def migrate_all_java_code(prompt, open_api_key):
    print(prompt)
    conversation = Conversation()
    conversation.add_message("system", system_prompt_convert_code_template)
    conversation.add_message("user", prompt)
    functions = get_functions_for_code_migration()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )

    return chat_response


def migrate_all_struts_code(prompt, open_api_key):
    print(prompt)
    conversation = Conversation()
    conversation.add_message("system", system_prompt_convert_struts_code_template)
    conversation.add_message("user", prompt)
    functions = get_functions_for_struts_code_migration()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )

    return chat_response


def create_main_class_for_application(prompt, open_api_key):
    print(prompt)
    conversation = Conversation()
    conversation.add_message("system", mainclassPrompt)
    conversation.add_message("user", prompt)
    functions = get_functions_for_main_class_creation()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    return chat_response

def generate_test_cases_for_given_java_code(prompt, open_api_key):
    print(prompt)
    conversation = Conversation()
    conversation.add_message("system", system_prompt_generate_test_cases_template)
    conversation.add_message("user", prompt)
    functions = get_functions_for_test_cases_generation()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    return chat_response

def generate_properties_for_application(prompt, open_api_key):
    print(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system", system_prompt_generate_application_properties_template)
    functions = get_functions_for_application_properties_generation()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response


def create_documentation_for_application(prompt, open_api_key):
    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    functions = get_functions_for_documentation_generation()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response


def create_test_case_for_application(prompt, open_api_key):
    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    functions = get_functions_for_test_cases_generation()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response


def create_jpa_for_entity(prompt, open_api_key):
    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system", "Always Generate the complete JPA repository code by analysing Provide code.")
    functions = get_functions_for_jpa_repository()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response


def create_entity_by_API_specification(prompt, open_api_key):
    
    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system","As a Spring Boot Java developer, your task is to create a "
                                      "complete set of Spring Boot code based on a given API specification. "
                                      "Follow the specified order by generating the entity first, then importing "
                                      "it into the repository. Subsequently, import the repository into the service "
                                      "layer, and finally, import the service into the controller. If there are "
                                      "multiple entities or reference entities, generate secondary entities and "
                                      "reference entities accordingly. Ensure a seamless flow of dependencies "
                                      "across the entity, repository, service, and controller layers.")
    functions = get_function_for_spring_boot_api_code_by_specification()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response

def create_data_migration_script(prompt, open_api_key):

    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system","As a expert data engineer, "
                                      "your task is to create a high quality data migration script in pyspark "
                                      "considering the data models provided for source and target databases. "
                                      "Consider all the best practices of pyspark and implement batching, retries, "
                                      "exception handling, etc wherever necessary. Also, use aws libraries ")

    '''
    update the system context
    '''
    functions = get_functions_for_data_migration_code()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response

def create_batch_script(prompt, open_api_key):

    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system"," As an expert data engineer, write a detailed pyspark script to process data "
                                      "based on the rules provided. Read and write the data from/to database or files and also "
                                      "transform and process the data wherever required. "
                                      "Consider pyspark best practices like but not limited to batch "
                                      "operations, retries, error handling while implementing the script. "
                                      "Also, the secrets for database connections are fetched from secrets manager "
                                      "and decrypted through kms. "
                                      "Also, make the pyspark script modular with distinct functions. ")
    '''
    update the system context
    '''
    functions = get_functions_for_batch_code()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response

def create_data_lake_script(prompt, open_api_key):

    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system", "As an expert pyspark developer and an experienced data engineer, "
                                      "consider all the best practices of pyspark and implement batching, retries, "
                                      "exception handling, etc wherever necessary.")

    '''
    update the system context
    '''
    functions = get_functions_for_data_lake_code()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response

def create_sql_script(prompt, open_api_key):

    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system","You are an experienced Data engineer with expertise in writing "
                                      "accurate and optimised SQL query.")

    '''
    update the system context
    '''
    functions = get_functions_for_sql()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response

def create_unit_tests_for_code(prompt, open_api_key):

    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system","As a expert data engineer, "
                                      "your task is to create a high quality data migration script in pyspark "
                                      "considering the data models provided for source and target databases. "
                                      "Consider all the best practices of pyspark and implement batching, retries, "
                                      "exception handling, etc wherever necessary. Also, use aws libraries ")

    '''
    update the system context
    '''
    functions = get_functions_for_unit_tests()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response

def create_docs(prompt, open_api_key):

    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system","As a expert data engineer, "
                                      "your task is to create a high quality data migration script in pyspark "
                                      "considering the data models provided for source and target databases. "
                                      "Consider all the best practices of pyspark and implement batching, retries, "
                                      "exception handling, etc wherever necessary. Also, use aws libraries ")

    '''
    update the system context
    '''
    functions = get_functions_for_docs()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response

def create_infrastructure_code(prompt, open_api_key):

    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system","As a expert Devops engineer, "
                                      "your task is to create a high quality cloudformation templates for the "
                                      "given AWS resource/infrastructure. Consider following all the best practices "
                                      "for writing cloudformation templates.")

    '''
    update the system context
    '''
    functions = get_functions_for_infra_code()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response

def create_kitty_specification(prompt, open_api_key):
    logger.info(prompt)
    conversation = Conversation()
    conversation.add_message("user", prompt)
    conversation.add_message("system", system_prompt_generate_kitty_file)
    functions = get_function_for_kitty_specification()

    chat_response = chat_completion_request(
        conversation.conversation_history,
        functions = functions,
        open_api_key = open_api_key
    )
    print(chat_response)
    return chat_response



    
