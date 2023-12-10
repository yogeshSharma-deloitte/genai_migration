from langchain.document_loaders import DirectoryLoader,UnstructuredXMLLoader
from ..gen_ai.generate_code import generate_properties_for_application, create_documentation_for_application, \
    create_test_case_for_application, create_jpa_for_entity, create_entity_by_API_specification, \
    create_kitty_specification, create_data_migration_script, create_batch_script, create_infrastructure_code, \
    create_docs, create_unit_tests_for_code, create_sql_script, create_data_lake_script
import json
import os
from .file_writer import write_to_file, write_to_html_file
import logging
from decouple import config
import markdown

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("properties_generator")

def create_application_properties_with_pom(application_directory, open_api_key):
    try:
        loader = DirectoryLoader(application_directory, glob="**/pom.xml")
        docs = loader.load()
        logger.info(len(docs))
        # username='root'
        # password='Admin@123'
        # url='jdbc:mysql://localhost:3306/mydb'
    
        #TODO: create prompt for all java source code and generate JUNIT test cases    
        prompt = "Act as a Spring boot Java developer, based on the dependencies in the pom.xml, generate properties to include in spring boot application properties file.Here is pom.xml file content:\n"
        for doc in docs:
            # prompt = prompt + "\n" + doc.metadata['source']
            with open(doc.metadata['source']) as f:
                lines = f.readlines()
                for line in lines:
                    prompt = prompt + line
        generate_application_properties(prompt, open_api_key)
    except Exception as e:
        print("Unable to generate the properties file")

def create_documentation(source_file_path,application_directory, package_name, open_api_key):
    try:
        package_components = package_name.split('.')
        entity_path = os.path.join(source_file_path, 'src', 'main', 'java')

        loader = DirectoryLoader(entity_path, glob="**/*.java")
        docs = loader.load()
        
        for doc in docs:
            
            logger.info(doc.metadata['source'])
            with open(doc.metadata['source']) as f:
                entity_content = ""
                lines = f.readlines()
                # logger.info(lines)
                for line in lines:
                    entity_content = entity_content + line
            first_prompt = """User, you need to create a document in Markdown format and convert it to HTML. Please provide the following information:\n """
            second_prompt = """ \n1. **Document Content:** (Write the content of your document in Markdown format. Include headings, lists, links, and any other formatting you need.) Note: Ensure that your Markdown content adheres to the Markdown syntax. If you have specific requirements for the HTML output, please mention them. Once you provide the Markdown content, file name, and conversion options, I will assist you in generating the HTML document."""
            final_prompt=first_prompt+entity_content+second_prompt
            create_entity_documentation(application_directory,final_prompt, open_api_key)
    except Exception as e:
        print("Unable to generate the documents")

def CREATE_DOCUMETATION_POJO(source_file_path, open_api_key):
    try:
        with open(source_file_path,'r') as file:
            lines = file.read()
            first_prompt = """User, you need to create a document in Markdown format and convert it to HTML. Please provide the following information:\n """
            second_prompt = """ \n1. **Document Content:** (Write the content of your document in Markdown format. Include headings, lists, links, and any other formatting you need.) Note: Ensure that your Markdown content adheres to the Markdown syntax. If you have specific requirements for the HTML output, please mention them. Once you provide the Markdown content, file name, and conversion options, I will assist you in generating the HTML document."""
            final_prompt = first_prompt+lines+second_prompt
            directory_path = os.path.dirname(source_file_path)
            create_entity_documentation(directory_path, final_prompt, open_api_key)
    except Exception as e:
        print("Unable to generate the documents")

def CREATE_TESTCASE_POJO(source_file_path, open_api_key):
    try:
        with open(source_file_path,'r') as file:
            lines = file.read()
            prompt = "Act as Spring Boot Java developer, write the Junit test cases for the following java code. Generate the test-case in such a way which can execute in included version of junit and at the end when validating test result do prepare with assert,assertNotNull,assertEquals and other function as well and add import static org.junit.jupiter.api.Assertions.*; where ever you are using assert functions do not use Verify functions. Use Verify only in case assert do not have right function. This test case class name should append Test at the end to the actual class and where-ever for the new line adding \n add like \\n and same in all the places. Here is input java class for you to generate test cases.\n"
            final_prompt = prompt+lines
            directory_path = os.path.dirname(source_file_path)
            print("New file",directory_path)
            test_source_directory = directory_path.replace("main", "test")
            print("Test New file",directory_path)
            os.makedirs(test_source_directory, exist_ok=True)
            create_entity_test_case(test_source_directory, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to generate the documents")

def CREATE_JPA_REPOSITORY_POJO(source_file_path, open_api_key):
    try:
        with open(source_file_path,'r') as file:
            lines = file.read()
            prompt = "Act as Spring Boot Java developer, write the JPA interface for the entity class. Analyse the Entity code properly and Generate the basic Queries inside the JPA repository. Below are the entity code: \n"
            final_prompt = prompt+lines
            directory_path = os.path.dirname(source_file_path)
            jpa_source_directory = directory_path.replace("entity", "repository")
            print("final prompt",final_prompt)
            create_entity_jpa_repository(jpa_source_directory, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to generate the documents")

#=============================VG BRUSHES END=============================
def CREATE_ENTITY_BY_SPECIFICATION(source_file_path, open_api_key):
    try:
        with open(source_file_path,'r') as file:
            lines = file.read()
            prompt = (" As a Next generation Java developer, your role involves a thorough analysis of API "
                      "specifications, followed by the generation of  while generating the code follow the  "
                      "best practices of Spring Boot. Even follow the below Instructions\n : "
                      "1. code should be complete code.\n 2. Do not add extra validation which are "
                      "not present into API specification.\n 3. Generating entity code follow javax.persistance "
                      "package standards and entity should be standard entity class with column related annotations.\n")
            final_prompt = prompt+lines
            directory_path = os.path.dirname(source_file_path)
            destination_dir = os.path.join(directory_path, 'src','main','java','com','vanguard','core')
            create_entity_by_specification(destination_dir, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to specification")

def CREATE_BATCH_SCRIPT(source_file_path, open_api_key):
    source_data_model = source_file_path + '/rules.txt'
    try:
        with open(source_data_model,'r') as source_file:
            source_lines = source_file.read()
            prompt = (" As an expert data engineer, write a detailed pyspark script to process data "
                      "based on the rules provided. Rules = ")
            final_prompt = prompt + source_lines

            directory_path = os.path.dirname(source_file_path)
            destination_dir = os.path.join(directory_path)
            #destination_dir = os.path.join(directory_path, 'src','main','java','com','vanguard','core')
            '''
            change the directory
            '''

            create_batch_script_from_rules(destination_dir, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to specification")

def CREATE_DATA_MIGRATION_SCRIPT(source_file_path, open_api_key):
    source_data_model = source_file_path + '/source-data-model.txt'
    target_data_model = source_file_path + '/target-data-model.txt'
    try:
        with open(source_data_model,'r') as source_file, open(target_data_model,'r') as target_file:
            source_lines = source_file.read()
            target_lines = target_file.read()
            prompt = (" As a expert data engineer, write a detailed pyspark script to migrate data "
                      "from source database(DB2) to target database(postgres) based on the data model "
                      "mentioned below. Also, consider pyspark best practices like but not limited to batch "
                      "operations, retries, error handling, maintaining constants while implementing the script. "
                      "Also, the secrets for database connections are fetched from secrets manager "
                      "and decrypted through kms. "
                      "Also, make the python scripts modular with distinct functions. "
                      "Source data model=")
            final_prompt = prompt + source_lines + " Target data model= " + target_lines

            directory_path = os.path.dirname(source_file_path)
            destination_dir = os.path.join(directory_path)
            #destination_dir = os.path.join(directory_path, 'src','main','java','com','vanguard','core')
            '''
            change the directory
            '''
            create_data_migration_script_from_models(destination_dir, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to specification")

def CREATE_DATA_LAKE_SCRIPT(source_file_path, open_api_key):
    data_lake_ingestion_params = source_file_path + '/data-lake-ingestion-params.txt'
    try:
        with open(data_lake_ingestion_params, 'r') as data_lake_ingestion_params_file:
            data_lake_params = data_lake_ingestion_params_file.read()
            prompt = (" Write a detailed pyspark script to process the data for data lake ingestion "
                      "based on following instructions delimited by triple * \n"
                      "*** \n"
                      "1. Read data from the given path from S3 bucket. Leverage KMS while reading data from S3.\n"
                      #"2. Decompress all files present in the S3 location within the path from '.gz' for to json files. \n"
                      "2. Read all data from all the files in a single spark dataframe. \n"
                      "3. Add audit columns like createdBy, createdDate in the dataframe with values 'data-lake-ingestion' for createdBy column and current data for createdDate column. \n"
                      "4. Load the data in the staging path in S3. \n"
                      "5. Recursively, flatten out the nested data within the same dataframe and capture results in a new dataframe. Assume there can be multiple layers of nesting within the data objects. \n"
                      "6. Drop the columns/attributes(mentioned below) and data related to it from the dataframe. \n"
                      "7. Load the new flattened dataframe into S3 in master data location. The data must be date partitioned first followed by the partition column(mentioned below) to contruct the individual object path. \n"
                      "*** \n"
                      "\n "
                      "Consider the following details while generating the pyspark script: \n"
                    )

            # data lake params should include : source_data_path, stage_data_path,master_data_path,columns_to_omit,partition_column.
            final_prompt = prompt + "\n" + data_lake_params

            print(final_prompt)

            directory_path = os.path.dirname(source_file_path)
            destination_dir = os.path.join(directory_path, 'data-lake')
            #destination_dir = os.path.join(directory_path, 'src','main','java','com','vanguard','core')
            '''
            change the directory
            '''
            create_data_lake_script_from_models(destination_dir, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to specification")

def CREATE_SQL_SCRIPT(source_file_path, open_api_key):
    sql_requirements = source_file_path + '/sql-requirements.json'
    try:
        with (open(sql_requirements,'r') as source_file):
            sql_params = source_file.read()
            print("reading json")
            sql_params_dict = json.loads(sql_params)
            print("json loaded")
            db_model = sql_params_dict['db_model']
            print(db_model)
            functional_requirements = sql_params_dict['query']
            print(functional_requirements)
            prompt = ("Write a SQL query for the functional specifications delimited by triple *. "
                      "Use the schema details delimited by triple # to generate an accurate SQL query as "
                      "it is highly crucial to get an accurate output. \n"
                      "Make sure to follow the below mentioned action items while writing the SQL query: \n"
                      "1. Make sure to follow the below mentioned action items while writing the SQL query: \n"
                      "2. Refer to the database schema delimited by triple ` to identify the tables and columns necessary to write the SQL query. \n"
                      "3. Make sure to consider all the filter conditions requested in the functional specifications. \n"
                      "4. Figure out the accurate joins between the tables that would be used to write the SQL query. \n"
                      "5. Write the output SQL queries, ensure the query is accurate as it is highly crucial for the business requirement. \n"
                      "Output should be SQL queries enclosed within ```sql {SQL query} ``` \n")
            print(prompt)
            final_prompt = prompt + "*** \n" + json.dumps(functional_requirements) + "\n" + "*** \n" + "### \n" + json.dumps(db_model) + "\n" + "### \n"
            print(final_prompt)
            directory_path = os.path.dirname(source_file_path)
            destination_dir = os.path.join(directory_path, 'sql-implementation')
            #destination_dir = os.path.join(directory_path, 'src','main','java','com','vanguard','core')
            '''
            change the directory
            '''
            create_sql_from_models(destination_dir, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to specification")

def CREATE_UNIT_TESTS(source_file_path, open_api_key):
    source_data_model = source_file_path + '/source-data-model.txt'
    target_data_model = source_file_path + '/target-data-model.txt'
    try:
        with open(source_data_model,'r') as source_file, open(target_data_model,'r') as target_file:
            source_lines = source_file.read()
            target_lines = target_file.read()
            prompt = (" As a expert data engineer, write a detailed pyspark script to migrate data "
                      "from source database(DB2) to target database(postgres) based on the data model "
                      "mentioned below. Also, consider pyspark best practices like but not limited to batch "
                      "operations, retries, error handling, maintaining constants while implementing the script. "
                      "Also, the secrets for database connections are fetched from secrets manager "
                      "and decrypted through kms. "
                      "Also, make the python scripts modular with distinct functions. "
                      "Source data model=")
            final_prompt = prompt + source_lines + " Target data model= " + target_lines

            directory_path = os.path.dirname(source_file_path)
            destination_dir = os.path.join(directory_path)
            #destination_dir = os.path.join(directory_path, 'src','main','java','com','vanguard','core')
            '''
            change the directory
            '''
            create_unit_tests(destination_dir, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to specification")

def CREATE_DOCS(source_file_path, open_api_key):
    source_data_model = source_file_path + '/source-data-model.txt'
    target_data_model = source_file_path + '/target-data-model.txt'
    try:
        with open(source_data_model,'r') as source_file, open(target_data_model,'r') as target_file:
            source_lines = source_file.read()
            target_lines = target_file.read()
            prompt = (" As a expert data engineer, write a detailed pyspark script to migrate data "
                      "from source database(DB2) to target database(postgres) based on the data model "
                      "mentioned below. Also, consider pyspark best practices like but not limited to batch "
                      "operations, retries, error handling, maintaining constants while implementing the script. "
                      "Also, the secrets for database connections are fetched from secrets manager "
                      "and decrypted through kms. "
                      "Also, make the python scripts modular with distinct functions. "
                      "Source data model=")
            final_prompt = prompt + source_lines + " Target data model= " + target_lines

            directory_path = os.path.dirname(source_file_path)
            destination_dir = os.path.join(directory_path)
            #destination_dir = os.path.join(directory_path, 'src','main','java','com','vanguard','core')
            '''
            change the directory
            '''
            create_docs_for_code(destination_dir, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to specification")


def CREATE_INFRA_CODE(source_file_path, open_api_key):
    infra_param_file = source_file_path + '/infra-params.txt'
    try:
        with open(infra_param_file, 'r') as infra_file:
            infra_params = infra_file.read()
            prompt = ("Write a detailed cloudformation template for the AWS resources mentioned. "
                      "Also, follow the instructions delimited by triple * \n"
                      "*** \n"
                      "1. Generate cloudformation template for the mentioned AWS resources in JSON format. \n"
                      "2. Consider configuring all the options mentioned for the given AWS resources. \n"
                      "3. Consider the properties while defining the AWS resources. \n"
                      "4. Parameterize all possible variables within the cloudformation template. \n"
                      "*** \n"
                      "Consider the following details while generating the cloudformation template: \n"
                      )
            final_prompt = prompt + infra_params

            directory_path = os.path.dirname(source_file_path)
            destination_dir = os.path.join(directory_path, 'infrastructure')
            '''
            change the directory
            '''
            create_infra_code(destination_dir, final_prompt, open_api_key)

    except Exception as e:
        print("Unable to specification")

#=============================VG BRUSHES END=============================

def CREATE_KITTY_FILE(source_file_path, open_api_key):
    try:
            prompt = " As a Next generation Dev-Ops Engineer, your role involves a thorough analyse the example file of wcnp , generate the similar file with the name of kitty.yml file. Walmart will use the same file for the deployment purpose.\n"
            create_kitt_specification(source_file_path, prompt, open_api_key)

    except Exception as e:
        print("Unable to kitty file")



def create_entity_test_case(application_directory, prompt, open_api_key):
    try:
        chat_response = create_test_case_for_application(prompt, open_api_key)
        handle_function_call_for_test_case(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to generate the documents for the entity")

def create_entity_jpa_repository(application_directory, prompt, open_api_key):
    try:
        chat_response = create_jpa_for_entity(prompt, open_api_key)
        handle_function_call_for_jpa_respository(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to generate the documents for the entity")

#=============================VG BRUSHES END=============================
def create_entity_by_specification(application_directory, prompt, open_api_key):
    try:
        chat_response = create_entity_by_API_specification(prompt, open_api_key)
        handle_function_call_for_entity_specification(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to spring boot APIs ")

def create_batch_script_from_rules(application_directory, prompt, open_api_key):
    try:
        chat_response = create_batch_script(prompt, open_api_key)
        print(chat_response)
        handle_function_call_for_batch(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to spring boot APIs ")

def create_data_migration_script_from_models(application_directory, prompt, open_api_key):
    try:
        chat_response = create_data_migration_script(prompt, open_api_key)
        handle_function_call_for_data_migration(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to spring boot APIs ")

def create_data_lake_script_from_models(application_directory, prompt, open_api_key):
    try:
        chat_response = create_data_lake_script(prompt, open_api_key)
        handle_function_call_for_data_lake(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to spring boot APIs ")

def create_sql_from_models(application_directory, prompt, open_api_key):
    try:
        chat_response = create_sql_script(prompt, open_api_key)
        handle_function_call_for_sql(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to spring boot APIs ")

def create_unit_tests(application_directory, prompt, open_api_key):
    try:
        chat_response = create_unit_tests_for_code(prompt, open_api_key)
        handle_function_call_for_unit_tests(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to spring boot APIs ")

def create_docs_for_code(application_directory, prompt, open_api_key):
    try:
        chat_response = create_docs(prompt, open_api_key)
        handle_function_call_for_docs(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to spring boot APIs ")

def create_infra_code(application_directory, prompt, open_api_key):
    try:
        chat_response = create_infrastructure_code(prompt, open_api_key)
        handle_function_call_for_infrastructure(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to spring boot APIs ")

#=============================VG BRUSHES END=============================

def create_kitt_specification(application_directory, prompt, open_api_key):
    try:
        chat_response = create_kitty_specification(prompt, open_api_key)
        handle_function_call_for_kitt_specification(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to generate the documents for the entity")



def create_entity_documentation(application_directory, prompt, open_api_key):
    try:
        chat_response = create_documentation_for_application(prompt, open_api_key)
        handle_function_call_for_documentation(application_directory, chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to generate the documents for the entity")


def generate_application_properties(prompt, open_api_key):
    try:
        print(prompt)
        chat_response = generate_properties_for_application(prompt, open_api_key)
        handle_function_call_for_application_properties(chat_response.json()['choices'][0]['message'])
    except Exception as e:
        print("Unable to generate the properties file")

def handle_function_call_for_application_properties(assistant_response):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "create_application_properties": create_application_properties
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments)

def handle_function_call_for_documentation(file_path, assistant_response):
    try: 
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "documentation_generation": documentation_generation
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to generate the documents") 

def handle_function_call_for_test_case(file_path, assistant_response):
    try: 
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "write_test_cases": write_test_cases
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to generate the documents") 

def handle_function_call_for_jpa_respository(file_path, assistant_response):
    try: 
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "get_jpa_repository_code": get_jpa_repository_code
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to generate the documents") 

def handle_function_call_for_entity_specification(file_path, assistant_response):
    try: 
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "get_spring_boot_code_by_API_specification": get_spring_boot_code_by_API_specification
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to extract the repsonse")


def handle_function_call_for_data_migration(file_path, assistant_response):
    try:
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "get_data_migration_code_in_pyspark": get_data_migration_code_in_pyspark
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to extract the repsonse")

def handle_function_call_for_batch(file_path, assistant_response):
    try:
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "get_batch_code_in_pyspark": get_batch_code_in_pyspark
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to extract the repsonse")

def handle_function_call_for_data_lake(file_path, assistant_response):
    try:
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print("function args = ")
        print(function_arguments)
        available_functions = {
            "get_data_lake_code_in_pyspark": get_data_lake_code_in_pyspark
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to extract the repsonse")

def handle_function_call_for_sql(file_path, assistant_response):
    try:
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "get_db_queries_in_sql": get_db_queries_in_sql
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to extract the repsonse")

def handle_function_call_for_unit_tests(file_path, assistant_response):
    try:
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "get_data_migration_code_in_pyspark": get_data_migration_code_in_pyspark
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to extract the repsonse")

def handle_function_call_for_docs(file_path, assistant_response):
    try:
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "get_data_migration_code_in_pyspark": get_data_migration_code_in_pyspark
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to extract the repsonse")

def handle_function_call_for_infrastructure(file_path, assistant_response):
    try:
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print("calling function")
        print(function_call)
        print(assistant_response)
        print(assistant_response["function_call"]["arguments"])
        #print("unescaped string")
        #print(assistant_response["function_call"]["arguments"].decode('string_escape'))
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print("function args = ")
        print(function_arguments)
        available_functions = {
            "get_cloudformation_code_for_infra": get_cloudformation_code_for_infra
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to extract the repsonse")

def handle_function_call_for_kitt_specification(file_path, assistant_response):
    try: 
        print("Here we are saving the file", file_path)
        function_call = assistant_response["function_call"]["name"]
        print(function_call)
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        print(function_arguments)
        available_functions = {
            "get_kitty_file": get_kitty_file
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(file_path, function_arguments)
    except Exception as e:
        print("Unable to generate the documents") 



def write_test_cases(directory, content):
     write_to_file(content['generatedTestCode'],directory+"/"+content['filename'])

def get_data_migration_code_in_pyspark(directory, content):

    write_to_file(content['pysparkcode'], directory+"/"+'data_migration.py')

def get_batch_code_in_pyspark(directory, content):

    write_to_file(content['batchcode'], directory+"/"+'batch_application.py')

def get_data_lake_code_in_pyspark(directory, content):

    write_to_file(content['datalakecode'], directory+"/"+'data_lake_ingestion.py')

def get_db_queries_in_sql(directory, content):

    write_to_file(content['sqlcode'], directory+"/"+'queries.sql')

def get_cloudformation_code_for_infra(directory, content):
    print('writing file in target folder')
    write_to_file(content['infracode'], directory+"/"+'cloudformation.json')

def get_spring_boot_code_by_API_specification(directory, content):
    
    for data in content['details']:
        
        destination_dir_entity = os.path.join(directory,'entity')
        print("Entity :",data['entityCode'])
        print("Path:",destination_dir_entity)
        if data['entityCode'] is not None and data['entityCode']:
            write_to_file(data['entityCode'],destination_dir_entity+"/"+data['entityFilename'])

        destination_dir = os.path.join(directory,'repository')
        
        print("Repository :",destination_dir)
        print("Code", data['repositoryCode'])
        if data['repositoryCode'] is not None and data['repositoryCode']:
            write_to_file(data['repositoryCode'],destination_dir+"/"+data['repositoryFilename'])
        
        destination_dir_s = os.path.join(directory,'service')
        print("Service :",destination_dir_s)
        if data['serviceCode'] is not None and data['serviceCode']:
            write_to_file(data['serviceCode'],destination_dir_s+"/"+data['serviceFilename'])
        
        destination_dir_r = os.path.join(directory,'model')
        print("Model :",data['dtoCode'])
        if data['dtoCode'] is not None and data['dtoCode']:
            write_to_file(data['dtoCode'],destination_dir_r+"/"+data['dtoFilename'])
        
        destination_dir_service = os.path.join(directory,'controller')
        print("Controller :",data['controllerCode'])
        if data['controllerCode'] is not None and data['controllerCode']:
            write_to_file(data['controllerCode'],destination_dir_service+"/"+data['controllerFilename'])
        
    


def get_kitty_file(directory, content):
    print("coming", content)
    print("Entity code", content['kittyCode'])
    print("directory path:", directory)
    write_to_file(content['kittyCode'],directory+"/"+content['filename'])


def get_jpa_repository_code(directory, content):
    print("New JPA repository", content['jpaRepositoryCode'])
    write_to_file(content['jpaRepositoryCode'],directory+"/"+content['filename'])


def documentation_generation(directory, content):
    if(len(str(content['markdownDocumetation'])) == 0):
          print("Mark down content is empty for the file name:",content['EntityName'])    
    else:
        try:
            filename = content['EntityName']
            os.path.join(directory,)
            out_md = filename+'.md'
            md_file_location = os.path.join(directory,out_md)
            with open(md_file_location, 'w') as f:
                f.write(content['markdownDocumetation'])
                
            with open(md_file_location, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()
                html_content = markdown.markdown(md_content)
                
            write_to_html_file(html_content,directory+"/"+filename+".html")

        except Exception as e :
                logger.info(f"Exception :: {str(e)}")
def create_application_properties(content):
    
    directory = os.environ["RESOURCES_PACKAGE"]

    # directory = os.environ["ROOT_PACKAGE"]
    print(content)
    write_to_file(content['generatedProperties'],directory+"/application.properties")

    # Specify the path to the text file
    file_path = directory+"/application.properties"

    # Define the placeholders and corresponding values
    placeholders = {
        '{username}': 'root',
        '{password}': 'Admin@123',
        '{db_url}': 'jdbc:mysql://localhost:3306/mydb'
    }

    # Replace placeholders with actual values
    replace_placeholders(file_path, placeholders)

def replace_placeholders(file_path, placeholders):
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        for placeholder, value in placeholders.items():
            content = content.replace(placeholder, value)

        with open(file_path, 'w') as f:
            f.write(content)
    except Exception as e:
        print("Unable to generate the properties file")        