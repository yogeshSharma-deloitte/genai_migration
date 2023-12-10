from distutils.ccompiler import gen_lib_options
import json
import os
from ..gen_ai.generate_code import migrate_all_java_code, migrate_all_struts_code
from .source_file_loader import get_content_for_ejb_java_code, get_content_for_struts_java_code
from .component_migration import get_partial_migrated_code, handle_method_calls_for_component_migration, handle_method_calls_for_spring_boot_component_migration, handle_method_calls_for_struts_component_migration, handle_method_calls_for_myBatis_component_migration
from ..constants import jpaRepository,controller,service,entity,pojo_model,config,constants
import re
import logging
import datetime
from ..processing.report import report_generation

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("preprocessing")

def  handle_method_calls_for_preprocessing(assistant_response, open_api_key, templates_path, sprint_boot_app_file_path):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "get_migration_details": get_migration_details
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments, open_api_key, templates_path, sprint_boot_app_file_path)

def handle_method_calls_for_struts_preprocessing(assistant_response, open_api_key, struts_filepath, templates_path, sprint_boot_app_file_path):
    function_call = assistant_response["function_call"]["name"]
    print(function_call)
    function_arguments = json.loads(assistant_response["function_call"]["arguments"])
    print(function_arguments)
    available_functions = {
        "get_struts_migration_details": get_struts_migration_details
    }
    function_to_call = available_functions.get(function_call)
    return function_to_call(function_arguments, open_api_key, struts_filepath, templates_path, sprint_boot_app_file_path)


def handle_method_calls_for_mybatis_preprocessing(assistant_response):
    try:
        function_call = assistant_response["function_call"]["name"]
        function_arguments = json.loads(assistant_response["function_call"]["arguments"])
        available_functions = {
            "get_spring_boot_migrated_code_from_iBatis_MyBatis": get_spring_boot_migrated_code_from_iBatis_MyBatis
        }
        function_to_call = available_functions.get(function_call)
        return function_to_call(function_arguments)
    except Exception as e:
        print("Unable to generate the code for the my batis classes")

def extract_java_methods(java_file_path):
    method_pattern = re.compile(r'((?:(?:public|private|protected|static|final|abstract|synchronized|volatile)\s+)*)\s*(\w+(?:<[^>]+>)?)\s*(\w+)\((.*?)\)\s*({(?:{[^{}]*(?:{[^{}]*}|.)*?[^{}]*}|.)*?})', re.DOTALL)

    # Read the Java file
    with open(java_file_path, "r") as java_file:
        java_code = java_file.read()

    # Find and process each method in the Java code
    chunkList = []
    word_count = 0
    chunk_code = ''
    methodList = []
    
    method_matches = method_pattern.findall(java_code)
    for match in method_matches:
        visibility = match[0].strip()
        return_type = match[1].strip()
        method_name = match[2].strip()
        arguments = match[3].strip()
        body = match[4].strip()
        method = visibility + " " + return_type + " " + method_name + "("+arguments+")\n"+body
        if len(methodList) == 0:
            firstMethod = visibility + " " + return_type + " " + method_name
        methodList.append(method)

    index_of_first_method = java_code.find(firstMethod)

    if index_of_first_method != -1:
        # Extract the substring from the beginning to the index of "hello"
        extracted_substring = java_code[:index_of_first_method]
        chunk_code = extracted_substring
        word_count = len(chunk_code.split())

    for match in methodList:
        method_body = match

        # Count words in the method body
        word_count = word_count + len(method_body.split())
    
        # print(f"Word Count: {word_count}")
        # print(f"Method Body:\n{method_body.strip()}\n")

        if word_count >750:
            chunkList.append(chunk_code)
            word_count = 0
            chunk_code = method_body
            word_count = len(chunk_code.split())
        else:
            chunk_code = chunk_code + method_body
            word_count = len(chunk_code.split())
    chunkList.append(chunk_code)         
    return chunkList

def get_migration_details(content, open_api_key, templates_path, sprint_boot_app_file_path):
    try:

        controllerNameList = []
        serviceNameList = []
        repoNameList = []
        entityNameList = []
        current_datetime = datetime.datetime.now()
        date_formatted = current_datetime.strftime("%d-%m-%Y")
        time_formatted = current_datetime.strftime("%H:%M:%S")
        pom_time = 'Date: '+str(date_formatted)+' and Time: '+str(time_formatted)
                         
        components_order = [constants, config, pojo_model, entity, jpaRepository, service, controller]
        
        reportContent = '''<table><tr><th>EJB File</th><th>SpringBoot File</th><th>Component</th><th>Timestamp</th></tr>'''
        reportContent = reportContent + '''<tr><td>'''+'pom.xml' + '''</td><td>'''+'pom.xml' + '''</td><td>'''+'xml'+'''</td><td>'''+pom_time+'''</td></tr>'''
        report_generation(templates_path, "", reportContent, sprint_boot_app_file_path)        
        for component_type in components_order:
            for data in content['details']:
                if data['fileRequired'] == True and data['component'] == component_type:
                    print(data['path'])
                    code_prompt = get_content_for_ejb_java_code(False, True, data['path'], data['component'],entityNameList,repoNameList,controllerNameList,serviceNameList)
                    with open(data['path']) as f:
                        lines = f.readlines()
                        for line in lines:
                            code_prompt = code_prompt + line
                    #extract_java_methods(lines)
                    chunkList = []
                    partialCodeList = []
                    component = data['component']
                    partial_chat_response = None
                    firstTimeFlag = True
                    chat_response = migrate_all_java_code(code_prompt, open_api_key)                
                    #Chunking approach : If 32k token error comes from OpenAI
                    if(chat_response.status_code >= 400):
                    #if data['component'] == service :
                        chunkList = extract_java_methods(data['path'])
                        partialCodePromptTest = get_content_for_ejb_java_code(True, True, data['path'], data['component'],entityNameList,repoNameList,controllerNameList,serviceNameList)
                        #Looping through all the chunks created for Request
                        for chunk in chunkList:
                            if firstTimeFlag:
                                chunkPrompt = partialCodePromptTest+chunk
                            else:  
                                chunkPrompt = get_content_for_ejb_java_code(True, False, data['path'], data['component'],entityNameList,repoNameList,controllerNameList,serviceNameList)+chunk
                            partial_chat_response = migrate_all_java_code(chunkPrompt, open_api_key)
                            partial_assistant_response = partial_chat_response.json()['choices'][0]['message']
                            if firstTimeFlag:
                                getClassNames(data, partial_chat_response, entityNameList, repoNameList, serviceNameList, controllerNameList)
                                firstTimeFlag = False
                            function_argument = json.loads(partial_assistant_response["function_call"]["arguments"])
                            partialCodeList.append(function_argument)
                                            
                        finalCode = ''
                        component = ''
                        filename = ''
                        #Stitching of the responses received from OpenAI
                        for partialCode in partialCodeList:
                            if(component == '' and filename == ''):
                                component = partialCode['component']
                                filename = partialCode['filename']
                                #partialCode['springBootCode'] = partialCode['springBootCode'][:-1] + " "
                            finalCode = finalCode + partialCode['springBootCode']
                        finalCode = finalCode + '}'
                        get_partial_migrated_code(finalCode,component,filename)
                        reportContent = reportContent + '''<tr><td>'''+data['filename'] + '''</td><td>'''+filename + '''</td><td>'''+component+'''</td></tr>'''

                    else: 
                        current_datetime = datetime.datetime.now()
                        date_formatted = current_datetime.strftime("%d-%m-%Y")
                        time_formatted = current_datetime.strftime("%H:%M:%S")
                        tme = 'Date: '+str(date_formatted)+' and Time: '+str(time_formatted)
                        print("String time: ",tme)
                        getClassNames(data, chat_response, entityNameList, repoNameList, serviceNameList, controllerNameList)
                        transformedContent = handle_method_calls_for_component_migration(chat_response.json()['choices'][0]['message'])
                        reportContent = reportContent + '''<tr><td>'''+data['filename'] + '''</td><td>'''+transformedContent['filename'] + '''</td><td>'''+transformedContent['component']+'''</td><td>'''+tme+'''</td></tr>'''
                        report_generation(templates_path, "", reportContent, sprint_boot_app_file_path)
        reportContent = reportContent + '''</table>'''
        return reportContent
    except Exception as e:
        print("Unable to generate the code for the file") 
        
def get_struts_migration_details(content, open_api_key, struts_filepath, templates_path, sprint_boot_app_file_path):
    try:
        controllerNameList = []
        serviceNameList = []
        repoNameList = []
        entityNameList = []
        current_datetime = datetime.datetime.now()
        date_formatted = current_datetime.strftime("%d-%m-%Y")
        time_formatted = current_datetime.strftime("%H:%M:%S")
        pom_time = 'Date: '+str(date_formatted)+' and Time: '+str(time_formatted) 
        components_order = [constants, config, pojo_model, entity, jpaRepository, service, controller]
        reportContent = '''<table><tr><th>Struts File</th><th>SpringBoot File</th><th>Component</th><th>Timestamp</th></tr>'''
        reportContent = reportContent + '''<tr><td>'''+'pom.xml' + '''</td><td>'''+'pom.xml' + '''</td><td>'''+'xml'+'''</td><td>'''+pom_time+'''</td></tr>'''
        report_generation(templates_path, "", reportContent, sprint_boot_app_file_path)        
        for component_type in components_order:
            for data in content['details']:
                if data['fileRequired'] == True and data['component'].lower() == component_type.lower():
                    print(data['path'])
                    code_prompt = get_content_for_struts_java_code(data['path'], data['component'],entityNameList,repoNameList,controllerNameList,serviceNameList)
                    with open(data['path']) as f:
                        lines = f.readlines()
                        for line in lines:
                            code_prompt = code_prompt + line
                    if data['component'] == entity:
                        try:
                            file_name_without_extention = data['filename'].split(".")[0]
                            file_name = file_name_without_extention.lower()+'.hbm.xml'
                            hbm_file_path = os.path.join(struts_filepath,'src','main','java',file_name) 
                            with open(hbm_file_path) as t:
                                code_prompt = code_prompt+" Providing you hbm file analyse both the files and add relation in spring boot entity properly based on hbm file below are the hbm file:"
                                hbm_lines = t.readlines()
                                for hbm_line in hbm_lines:
                                    code_prompt= code_prompt + hbm_line
                        except Exception as e:
                            print("Unable to add hbm file")
                    chat_response = migrate_all_struts_code(code_prompt, open_api_key)
                    getClassNames(data, chat_response, entityNameList, repoNameList, serviceNameList, controllerNameList)
                    transformedContent = handle_method_calls_for_struts_component_migration(chat_response.json()['choices'][0]['message'])
                    current_datetime = datetime.datetime.now()
                    date_formatted = current_datetime.strftime("%d-%m-%Y")
                    time_formatted = current_datetime.strftime("%H:%M:%S")
                    tme = 'Date: '+str(date_formatted)+' and Time: '+str(time_formatted)
                    reportContent = reportContent + '''<tr><td>'''+data['filename'] + '''</td><td>'''+transformedContent['filename'] + '''</td><td>'''+transformedContent['component']+'''</td><td>'''+tme+'''</td></tr>'''
                    report_generation(templates_path, "", reportContent, sprint_boot_app_file_path)
        reportContent = reportContent + '''</table>'''
        return reportContent
    except Exception as e:
        print("Unable to generate the code for particular file")

def get_spring_boot_migrated_code_from_iBatis_MyBatis(content):
    try:
        service_data = content['service_code']
        entity_code = content['entity_code']
        repository_code = content['repository_code']
        repository_name = content['filename'].replace("Service", "Repository")
        entity_name = content['filename'].replace("Service", "")
        
        handle_method_calls_for_myBatis_component_migration(entity_code, 'entity', entity_name)
        handle_method_calls_for_myBatis_component_migration(service_data, 'service', content['filename'])
        handle_method_calls_for_myBatis_component_migration(repository_code, 'repository', repository_name)
    
    except Exception as e:
        print("Unable to generate the code for particular file")


                    
def getClassNames(data, chat_response, entityNameList, repoNameList, serviceNameList, controllerNameList):
    if data['component'] == entity:
        entityNameList.append(json.loads((chat_response.json()['choices'][0]['message'])["function_call"]["arguments"])['filename'])
    elif data['component'] == jpaRepository:
        repoNameList.append(json.loads((chat_response.json()['choices'][0]['message'])["function_call"]["arguments"])['filename'])
    elif data['component'] == service:
        serviceNameList.append(json.loads((chat_response.json()['choices'][0]['message'])["function_call"]["arguments"])['filename'])
    elif data['component'] == controller:
        controllerNameList.append(json.loads((chat_response.json()['choices'][0]['message'])["function_call"]["arguments"])['filename'])
