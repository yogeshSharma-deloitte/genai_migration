from .source_file_loader import load_pom_file, load_all_java_file_paths, load_pom_file_struts, load_all_java_file_paths_struts, load_all_java_file_paths_mybatis
from ..gen_ai.generate_code import initiate_api,get_details_of_other_files,improve_build_result, initiate_api_struts, get_details_of_other_files_for_struts, get_details_of_other_files_for_mybatis
from .preprocessing import handle_method_calls_for_preprocessing, handle_method_calls_for_struts_preprocessing, handle_method_calls_for_mybatis_preprocessing
from .project_setup import create_spring_boot_project_in_given_directory
from .test_cases_creator import create_test_cases_for_migrated_code
from .properties_generator import create_application_properties_with_pom, create_documentation, \
    CREATE_DOCUMETATION_POJO, CREATE_TESTCASE_POJO, CREATE_JPA_REPOSITORY_POJO, CREATE_ENTITY_BY_SPECIFICATION, \
    CREATE_KITTY_FILE, create_data_migration_script_from_models, CREATE_DATA_MIGRATION_SCRIPT, CREATE_BATCH_SCRIPT, \
    CREATE_DATA_LAKE_SCRIPT, CREATE_SQL_SCRIPT, CREATE_UNIT_TESTS, CREATE_DOCS, CREATE_INFRA_CODE
from git import Repo, GitCommandError
from .report import report_generation
import os
import shutil
import subprocess
import logging
import datetime
import requests
from from_root import from_root



from ..build_manage.build_project import migration_report

logger = logging.getLogger("EJB to spring boot")

GENAI_UNIFIED_POST_PUT_HISTORY = f'{os.environ.get("BACKEND_BASE_URL")}/genai-unified/history?key={os.environ.get("API_GATEWAY_KEY")}'
GENAI_UNIFIED_HISTORY_BY_CREATEDBY_AND_PRODUCTID = f'{os.environ.get("BACKEND_BASE_URL")}/genai-unified/history/product?key={os.environ.get("API_GATEWAY_KEY")}'

def migrate_ejb_to_spring_boot(productId, ejb_file_path, spring_boot_repo_url, application_name, package_name, open_api_key, gitusername, gitEmail):
    logger.info("Started executing ")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    #try:
        #source_project = ejb_path.split("/")[-1].split(".")[0]
        #history_id = create_history(productId,spring_boot_repo_url,gitusername)
    #except Exception as ex:
    #    raise ex;   
    sprint_boot_app_file_path = str(from_root(timestamp,application_name, mkdirs=True))
    templates_path = str(from_root('ejb_spring','server','ejb_spring_boot','templates', mkdirs=True))
    
    logger.info(f"sprint_boot_app_file_path path: {sprint_boot_app_file_path}")

    try:
        create_spring_boot_project_in_given_directory(sprint_boot_app_file_path, application_name, package_name, open_api_key, timestamp)
        convert_pom(ejb_file_path, open_api_key)
        #increase_step_count(history_id)
        reportContent = get_other_file_details(ejb_file_path, open_api_key, templates_path, sprint_boot_app_file_path)
        #increase_step_count(history_id)
        create_test_cases_for_migrated_code(os.environ["ROOT_PACKAGE"], open_api_key)
        #increase_step_count(history_id)
        create_application_properties_with_pom(os.environ["PROJECT_DIRECTORY"], open_api_key)
        create_documentation(ejb_file_path, os.environ["PROJECT_DIRECTORY"],package_name, open_api_key)
        #increase_step_count(history_id)
        migration_report(templates_path, os.environ["PROJECT_DIRECTORY"], reportContent, sprint_boot_app_file_path)
        #increase_step_count(history_id)
        move_jsp_folder(ejb_file_path, sprint_boot_app_file_path)
        push_code_to_repository(sprint_boot_app_file_path, spring_boot_repo_url, gitusername, gitEmail)
        
    except Exception as e: 
        logger.info(f"Exception :: {str(e)}")
        #increase_step_count(history_id,failed_request=True)
        raise e
    finally:
        logger.info(f"For this execution.We have created project under : {str(from_root(timestamp))}")
        #deletetemp(str(from_root(timestamp)))

def GENERATE_DOCUMENTS(struts_filepath, open_api_key):
    try:
        CREATE_DOCUMETATION_POJO(struts_filepath, open_api_key)       
        
    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_TESTCASE(struts_filepath, open_api_key):
    try:
        CREATE_TESTCASE_POJO(struts_filepath, open_api_key)       
        
    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_JPA_REPOSITORY(struts_filepath, open_api_key):
    try:
        CREATE_JPA_REPOSITORY_POJO(struts_filepath, open_api_key)       
        
    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

#=============================VG BRUSHES END=============================

def GENERATE_ENTITY_BY_SPECIFICATION(struts_filepath, open_api_key):
    try:
        CREATE_ENTITY_BY_SPECIFICATION(struts_filepath, open_api_key)       
        
    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_DATA_MIGRATION_SCRIPT(struts_filepath, open_api_key):
    try:
        CREATE_DATA_MIGRATION_SCRIPT(struts_filepath, open_api_key)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_BATCH_SCRIPT(struts_filepath, open_api_key):
    try:
        CREATE_BATCH_SCRIPT(struts_filepath, open_api_key)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_DATA_LAKE_SCRIPT(struts_filepath, open_api_key):
    try:
        CREATE_DATA_LAKE_SCRIPT(struts_filepath, open_api_key)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_SQL_SCRIPT(struts_filepath, open_api_key):
    try:
        CREATE_SQL_SCRIPT(struts_filepath, open_api_key)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_UNIT_TESTS(struts_filepath, open_api_key):
    try:
        CREATE_UNIT_TESTS(struts_filepath, open_api_key)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_DOCS(struts_filepath, open_api_key):
    try:
        CREATE_DOCS(struts_filepath, open_api_key)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

def GENERATE_INFRA_CODE(struts_filepath, open_api_key):
    try:
        CREATE_INFRA_CODE(struts_filepath, open_api_key)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e

#=============================VG BRUSHES END=============================

def GENERATE_KITTY_FILE(struts_filepath, open_api_key):
    try:
        CREATE_KITTY_FILE(struts_filepath, open_api_key)       
        
    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e



def migrate_mybatis_to_spring_boot(struts_filepath, spring_boot_repo_url, application_name, package_name, open_api_key, gitusername, gitEmail):
    logger.info("Started executing ")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sprint_boot_app_file_path = str(from_root(timestamp,application_name, mkdirs=True))

    logger.info(f"EJB path: {struts_filepath}")
    logger.info(f"sprint_boot_app_file_path path: {sprint_boot_app_file_path}")
    templates_path = str(from_root('ejb_spring','server','ejb_spring_boot','templates', mkdirs=True))
    try:
        create_spring_boot_project_in_given_directory(sprint_boot_app_file_path, application_name, package_name, open_api_key, timestamp)
        convert_pom_struts(struts_filepath, open_api_key)
        reportContent = get_other_file_details_for_struts(struts_filepath, open_api_key, templates_path, sprint_boot_app_file_path)
        get_other_file_details_for_mybatis(struts_filepath, open_api_key) 
        create_test_cases_for_migrated_code(os.environ["ROOT_PACKAGE"], open_api_key)
        create_application_properties_with_pom(os.environ["PROJECT_DIRECTORY"], open_api_key)
        create_documentation(struts_filepath, os.environ["PROJECT_DIRECTORY"],package_name, open_api_key)       
        migration_report(templates_path, os.environ["PROJECT_DIRECTORY"],reportContent, sprint_boot_app_file_path)
        move_jsp_folder(struts_filepath, sprint_boot_app_file_path)
        push_spring_boot_code_to_repository(sprint_boot_app_file_path, spring_boot_repo_url, gitusername, gitEmail)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e
    finally:
        logger.info(f"For this execution.We have created project under : {str(from_root(timestamp))}")
        #deletetemp(str(from_root(timestamp)))



def migrate_struts_to_spring_boot(struts_filepath, spring_boot_repo_url, application_name, package_name, open_api_key, gitusername, gitEmail):
    logger.info("Started executing ")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sprint_boot_app_file_path = str(from_root(timestamp,application_name, mkdirs=True))

    logger.info(f"EJB path: {struts_filepath}")
    logger.info(f"sprint_boot_app_file_path path: {sprint_boot_app_file_path}")
    templates_path = str(from_root('ejb_spring','server','ejb_spring_boot','templates', mkdirs=True))
    try:
        create_spring_boot_project_in_given_directory(sprint_boot_app_file_path, application_name, package_name, open_api_key, timestamp)
        convert_pom_struts(struts_filepath, open_api_key)
        reportContent = get_other_file_details_for_struts(struts_filepath, open_api_key, templates_path, sprint_boot_app_file_path)
        create_test_cases_for_migrated_code(os.environ["ROOT_PACKAGE"], open_api_key)
        create_application_properties_with_pom(os.environ["PROJECT_DIRECTORY"], open_api_key)
        create_documentation(struts_filepath, os.environ["PROJECT_DIRECTORY"],package_name, open_api_key)       
        migration_report(templates_path, os.environ["PROJECT_DIRECTORY"],reportContent, sprint_boot_app_file_path)
        move_jsp_folder(struts_filepath, sprint_boot_app_file_path)
        push_spring_boot_code_to_repository(sprint_boot_app_file_path, spring_boot_repo_url, gitusername, gitEmail)

    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        raise e
    finally:
        logger.info(f"For this execution.We have created project under : {str(from_root(timestamp))}")
        #deletetemp(str(from_root(timestamp)))

def move_jsp_folder(struts_jsp_folder_path, springboot_jsp_folder_path):

    try:
        source_path = os.path.join(struts_jsp_folder_path,'src','main','webapp')
        destination_folder = os.path.join(springboot_jsp_folder_path, 'src', 'main','webapp')
        # Use shutil.move to move the source folder to the destination folder
        shutil.copytree(source_path, destination_folder)
        logger.info("Successfully migrated JSP folder")
    except Exception as e:
        print("Unable to copy the JSP folder to the new spring boot project")


def increase_step_count(history_id: int, request_completed: bool = False,
                        failed_request: bool = False) -> None:
    data = {
        'historyId': history_id,
    }

    # Update the data based on the request status
    if request_completed:
        data['status'] = 'Completed'
    
    if failed_request:
        data['status'] = 'Failed'

    # Make a POST request to the update_history API endpoint
    endpoint = GENAI_UNIFIED_POST_PUT_HISTORY
    param_data={
        "key":os.environ.get("API_GATEWAY_KEY")
    }
    response = requests.put(endpoint, json=data, params=param_data)
    if response.status_code != 200:
        print('Error updating step count:', response.json())


def create_history(product: int, repo_url: str, username: str) -> int:
    
    logging.info(f"Creating history at endpoint {GENAI_UNIFIED_POST_PUT_HISTORY}")
    repo_name = repo_url.split("/")[-1].split(".")[0]
    endpoint = GENAI_UNIFIED_POST_PUT_HISTORY
    data = {
        "product": int(product),
        "branch_name": repo_name,
        "source_url": repo_url,
        "github_username": username,
        "repo_name": repo_name,
        "status": 'Initiated'
    }

    param_data={
        "key":os.environ.get("API_GATEWAY_KEY")
    }
    response = requests.post(endpoint, json=data, params=param_data)
    if response.status_code != 201:
        raise Exception(response.json()["message"])
    response = response.json()

    logging.info(f"History created :: {response}")

    return response['id']

def deletetemp(file_complete_path):
    try:
        
        shutil.rmtree(file_complete_path)
        logger.info(f"Successfully deleted folder: {file_complete_path}")
    except Exception as e:
        logger.info(f"Exception :: {str(e)}")
        return e

def get_git_repo(repo_url, destination_dir, branch_name):
    logger.info(f"while clonning directory url is : {destination_dir}")
    try: 
        Repo.clone_from(repo_url, destination_dir, branch=branch_name)
        logger.info(f"EJB Repo clonned successfully {destination_dir}") 
    except GitCommandError as git_error:
        logger.info(f"Git command error: {git_error}")
        pull_repository(repo_url, destination_dir)
    except Exception as err:
        logger.info(f"Exception in repo {err}")
        pull_repository(repo_url, destination_dir)


def pull_repository(repo_url, destination_dir):
    logger.info("Clonning attempted second time")
    try:
        result = subprocess.run(['git', 'clone', repo_url, destination_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logger.info(f"Repository cloned successfully into {destination_dir}")
        else:
            raise Exception(f"An error occurred while cloning the repository.")
    except Exception as e:
        raise e
    
def push_code_to_repository(sprint_boot_app_file_path, spring_boot_repo_url, gitusername, git_email):
    file_complete_path = sprint_boot_app_file_path
    try:
        subprocess.run(["git", "init"], cwd=file_complete_path)
        subprocess.run(["git", "config", "--global", "user.name", gitusername])
        subprocess.run(["git", "config", "--global", "user.email", git_email])
        subprocess.run(["git", "checkout", "-b", "main"], cwd=file_complete_path)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=file_complete_path)
        subprocess.run(["git", "add", "."], cwd=file_complete_path)
        subprocess.run(["git", "commit", "-m", "Pushed spring boot code converted from EJB"], cwd=file_complete_path)
        subprocess.run(["git", "remote", "add", "origin", spring_boot_repo_url], cwd=file_complete_path)
        result = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=file_complete_path)
        if result.returncode != 0:
            raise Exception(f"Unable to Push Code into spring boot repo URL {spring_boot_repo_url}. Verify the url and re-triggered the process")
        #increase_step_count(history_id,request_completed=True)
        print("Code pushed successfully to the springboot repo")
        logger.info(f"Code pushed successfully to {spring_boot_repo_url}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def push_spring_boot_code_to_repository(sprint_boot_app_file_path, spring_boot_repo_url, gitusername, git_email):
    file_complete_path = sprint_boot_app_file_path
    try:
        subprocess.run(["git", "init"], cwd=file_complete_path)
        subprocess.run(["git", "config", "--global", "user.name", gitusername])
        subprocess.run(["git", "config", "--global", "user.email", git_email])
        subprocess.run(["git", "checkout", "-b", "main"], cwd=file_complete_path)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=file_complete_path)
        subprocess.run(["git", "add", "."], cwd=file_complete_path)
        subprocess.run(["git", "commit", "-m", "Pushed converted spring boot code"], cwd=file_complete_path)
        subprocess.run(["git", "remote", "add", "origin", spring_boot_repo_url], cwd=file_complete_path)
        result = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=file_complete_path)
        if result.returncode != 0:
            raise Exception(f"Unable to Push Code into spring boot repo URL {spring_boot_repo_url}. Verify the url and re-triggered the process")
        print("Code pushed successfully")
        logger.info(f"Code pushed successfully to {spring_boot_repo_url}")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def improve_build(buildResult):
    prompt_content = "Below are the spring boot failed result. Provide the steps to fix in numerical format.\n"+buildResult
    return improve_build_result(prompt_content)


def get_current_activity(productId, createdBy):
    
    endpoint = GENAI_UNIFIED_HISTORY_BY_CREATEDBY_AND_PRODUCTID
    print()
    param_data={
        "productId" : productId,
        "createdBy": createdBy,
        "key":os.environ.get("API_GATEWAY_KEY")
    }
    print("final request",param_data)
    response= requests.get(endpoint,params=param_data)
    response=response.json()
    print("final response",response)
    return response[0]
   
   

def convert_pom(ejb_app_path, open_api_key):
    try:
        prompt_content = load_pom_file(ejb_app_path)
        initiate_api(prompt_content, open_api_key)
    except Exception as e:
        print("Unable to generate the pom file")

def convert_pom_struts(struts_path, open_api_key):
    try:
        prompt_content = load_pom_file_struts(struts_path)
        initiate_api_struts(prompt_content, open_api_key)
    except Exception as e:
        print("Unable to convert pom")

def get_other_file_details(ejb_app_path, open_api_key, templates_path, sprint_boot_app_file_path):
    prompt_content = load_all_java_file_paths(ejb_app_path)
    chat_response = get_details_of_other_files(prompt_content, open_api_key)
    reportContent = handle_method_calls_for_preprocessing(chat_response.json()['choices'][0]['message'], open_api_key, templates_path, sprint_boot_app_file_path)
    return reportContent

def get_other_file_details_for_struts(struts_filepath, open_api_key,templates_path, sprint_boot_app_file_path):
    prompt_content = load_all_java_file_paths_struts(struts_filepath)
    chat_response = get_details_of_other_files_for_struts(prompt_content, open_api_key)
    return handle_method_calls_for_struts_preprocessing(chat_response.json()['choices'][0]['message'], open_api_key, struts_filepath, templates_path, sprint_boot_app_file_path)


def get_other_file_details_for_mybatis(struts_filepath, open_api_key):
    prompt_list = load_all_java_file_paths_mybatis(struts_filepath)
    try:
        for prompt in prompt_list:
            chat_response = get_details_of_other_files_for_mybatis(prompt, open_api_key)
            handle_method_calls_for_mybatis_preprocessing(chat_response.json()['choices'][0]['message'])
            print("Mybatis files scanned and generated spring boot code")
    except Exception as e:
        print("Unable to generate the code for the mybatis file")        