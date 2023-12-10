from django.http import JsonResponse
from rest_framework import status
from .git_manage.source import pull_repository, push_code_to_repository
from decouple import config
from .processing.ejb_springboot import convert_pom, migrate_ejb_to_spring_boot, improve_build, get_current_activity, migrate_struts_to_spring_boot
import json
import os
import logging
from django.views.decorators.csrf import csrf_exempt
from .processing.report import report_generation_build
logger = logging.getLogger(" View of EJB to spring boot")

def hello_world(request):
    """
        API endpoint to test http layer.

        Methods:
        - GET: Returns static response.
        - Example url: /hello-world
    """
    return JsonResponse({"message": "hello world! I am ready"}, status=status.HTTP_200_OK)
@csrf_exempt
def setup_source_code(request):
    """
        API endpoint to setup the source code.

        Methods:
        - GET: Returns static response.
        - Example url: /hello-world
    """

    gitURL = json.loads(request.body).get("gitURL")
    source_project = json.loads(request.body).get("source_project")
    
    source_directory = os.getcwd()
    pull_repository(gitURL,source_directory, source_project)
    return JsonResponse({"message": "directory is created successfully"}, status=status.HTTP_200_OK)

@csrf_exempt
def push_source_code(request):
    """
        API endpoint to setup the source code.

        Methods:
        - GET: Returns static response.
        - Example url: /hello-world
    """

    destination_repo_url = json.loads(request.body).get("destination_repo_url")
    source_dir = json.loads(request.body).get("source_dir")
    branch_name = json.loads(request.body).get("branch_name")
    push_code_to_repository(source_dir, destination_repo_url, branch_name)
    logger.info("Spring boot code is pushed successfully")
    return JsonResponse({"message": " Spring boot code is pushed successfully"}, status=status.HTTP_200_OK)



@csrf_exempt
def create_spring_boot_project(request):
    """
        API endpoint to setup the source code.

        Methods:
        - GET: Returns static response.
        - Example url: /hello-world
    """
    try:
        application_name = json.loads(request.body).get("applicationName")
        open_ai_key = json.loads(request.body).get("X-GEN-API-KEY")
        package_name = json.loads(request.body).get("packageName")
        #source_project = json.loads(request.body).get("source_project")
        ejb_file_path = json.loads(request.body).get("ejbFilePath")
        spring_boot_repo_url = json.loads(request.body).get("springBootRepoUrl")
        git_user_name = json.loads(request.body).get("gitUserName")
        git_email = json.loads(request.body).get("gitEmail")
        productId = json.loads(request.body).get("productId")
        
        # create_spring_boot_project_in_given_directory(application_name, package_name)
        # convert_pom()
        # get_other_file_details()
        migrate_ejb_to_spring_boot(productId, ejb_file_path, spring_boot_repo_url, application_name, package_name, open_ai_key, git_user_name, git_email)
        logger.info("App created and Code pushed")
        return JsonResponse({"message": "Spring boot application is created successfully and pushed to given spring boot repo url"}, status=status.HTTP_200_OK) 
    except Exception as e:
        return JsonResponse({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def create_struts_project(request):
    """
        API endpoint to setup the source code.

        Methods:
        - GET: Returns static response.
        - Example url: /hello-world
    """
    try:
        application_name = json.loads(request.body).get("applicationName")
        open_ai_key = json.loads(request.body).get("X-GEN-API-KEY")
        package_name = json.loads(request.body).get("packageName")
        spring_boot_repo_url = json.loads(request.body).get("springBootRepoUrl")
        git_user_name = json.loads(request.body).get("gitUserName")
        git_email = json.loads(request.body).get("gitEmail")
        struts_path = json.loads(request.body).get("struts_path")

        # create_spring_boot_project_in_given_directory(application_name, package_name)
        # convert_pom()
        # get_other_file_details()
        migrate_struts_to_spring_boot(struts_path, spring_boot_repo_url, application_name, package_name, open_ai_key, git_user_name, git_email)
        logger.info("App created and Code pushed")
        return JsonResponse({"message": "Spring boot application is created successfully and pushed to given spring boot repo url"}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def ask_suggestion(request):
    """
        API endpoint to setup the source code.

        Methods:
        - GET: Returns static response.
        - Example url: /hello-world
    """
    build_result = json.loads(request.body).get("build_result")
    # create_spring_boot_project_in_given_directory(application_name, package_name)
    # convert_pom()
    # get_other_file_details()
    data = improve_build(build_result)
    report_generation_build(build_result, data['improvements'])
    return JsonResponse(data, status=status.HTTP_200_OK)

@csrf_exempt
def get_current_status(request):
    productId = json.loads(request.body).get("productId")
    createdBy = json.loads(request.body).get("createdBy")
    try:
            history = get_current_activity(productId=productId,createdBy=createdBy)
            print("here is history:",history["id"])
            if history:
                response = {
                    "historyId":history["id"],
                    "stepsCompleted": history["step_number"],
                    "isRequestCompleted": history["status"] == 'Completed',
                    "repoName": history["repo_name"],
                    "status": history["status"]
                }
                return JsonResponse(response)
            else:
                return JsonResponse({'message': 'No history found.'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
def convert_pom_code(request):
    """
        API endpoint to test http layer.

        Methods:
        - GET: Returns static response.
        - Example url: /hello-world
    """
    convert_pom()
    return JsonResponse({"message": "POM is converted successfully"}, status=status.HTTP_200_OK)