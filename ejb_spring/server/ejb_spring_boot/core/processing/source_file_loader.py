from langchain.document_loaders import DirectoryLoader,UnstructuredXMLLoader
from decouple import config
from ..gen_ai.prompts import pom_migration_prompt_template,user_prompt_identify_java_file_details_template,pom_migration_prompt_template_struts, user_prompt_identify_java_file_details_template_for_struts, userPrompt_mybatis
import os
from ..constants import controller,service
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("source_file_loader")


def load_pom_file(path):
    #source_directory = config('path')
    logger.info(f"While loading the pom path {path}")
    loader = DirectoryLoader(path, glob="**/pom.xml")
    # loader = DirectoryLoader('../', glob="**/*.txt")
    docs = loader.load()
    logger.info(len(docs))
    application_name = os.environ["APPLICATION_NAME"]
    content_for_prompt =  pom_migration_prompt_template + "\n Root path of this EJB application is "+path+".\n Additionally include the name of the spring boot artificat as "+application_name+""
    for doc in docs:
        logger.info(doc.metadata['source'])
        content_for_prompt = content_for_prompt + ".\n"
        content_for_prompt = content_for_prompt + " Here is pom.xml file with path "+doc.metadata['source']+" and its content is "
        with open(doc.metadata['source']) as f:
            lines = f.readlines()
            # logger.info(lines)
            for line in lines:
                content_for_prompt = content_for_prompt + line
    
    # logger.info(content_for_prompt)

    return content_for_prompt

def load_pom_file_struts(path):
    #source_directory = config('path')
    logger.info(f"While loading the pom path {path}")
    loader = DirectoryLoader(path, glob="**/pom.xml")
    # loader = DirectoryLoader('../', glob="**/*.txt")
    docs = loader.load()
    logger.info(len(docs))
    application_name = os.environ["APPLICATION_NAME"]
    content_for_prompt = pom_migration_prompt_template_struts + "\n Root path of this struts application is "+path+".\n Additionally include the name of the spring boot artificat as "+application_name+""
    for doc in docs:
        logger.info(doc.metadata['source'])
        content_for_prompt = content_for_prompt + ".\n"
        content_for_prompt = content_for_prompt + " Here is pom.xml file with path "+doc.metadata['source']+" and its content is "
        with open(doc.metadata['source']) as f:
            lines = f.readlines()
            # logger.info(lines)
            for line in lines:
                content_for_prompt = content_for_prompt + line

    # logger.info(content_for_prompt)

    return content_for_prompt



def load_all_java_file_paths(path):
    logger.info(f"while finding component path is {path}")
    loader = DirectoryLoader(path, glob="**/*.java")
    docs = loader.load()
    content_for_prompt = user_prompt_identify_java_file_details_template
    for doc in docs:
        if str(doc.metadata['source']).__contains__('/test/'):
            logger.info("nothing to do for "+doc.metadata['source'])
        else:
            content_for_prompt = content_for_prompt + ".\n" + doc.metadata['source']


    return content_for_prompt

def load_all_java_file_paths_struts(path):
    logger.info(f"while finding component path is {path}")
    loader = DirectoryLoader(path, glob="**/*.java")
    docs = loader.load()
    content_for_prompt = user_prompt_identify_java_file_details_template_for_struts
    for doc in docs:
        if str(doc.metadata['source']).__contains__('/test/'):
            logger.info("nothing to do for "+doc.metadata['source'])
        else:
            content_for_prompt = content_for_prompt + ".\n" + doc.metadata['source']


    return content_for_prompt


def load_all_java_file_paths_mybatis(path):
    
    try:
        package_name = os.environ["PACKAGE_NAME"]
        xml_file_path = os.path.join(path,'src','main','java')
        loader = DirectoryLoader(xml_file_path, glob="**/*.xml")
        docs = loader.load()
        methodList = [] 
        for doc in docs:
            print("File path is here:",str(doc.metadata['source']))
            with open(str(doc.metadata['source'])) as f:
                code_prompt=""
                lines = f.readlines()
                for line in lines:
                    code_prompt = code_prompt + line
                input_code = code_prompt 
            mybatis_prompt = """"3. **Migration Options:** Spring-boot "Guidelines for Migration:\n" +
            "- Double-check the file path and name to ensure accuracy.\n" +
            "- Select appropriate migration options based on the old technology.\n" +
            "- Provide clear additional configurations if required (optional).\n" +
            "- Ensure a backup of the original file is available before migration.\n" +
            "- Follow best practices of the target technology during migration.\n" +
            "- If uncertain, ask for clarifications before proceeding.\n" +
            " \n" +
            "Please provide accurate and detailed information for successful migration.\n"+
            """ 
            package_prompt= "add imports for service_code : \npackage "+package_name+".services and use import for any repository_code "+package_name+".repository and use import for any entity_code "+package_name+".entity and always generate the getter and setter for the entity code"
            final_promt = userPrompt_mybatis+input_code+mybatis_prompt+package_prompt
            methodList.append(final_promt)
        return methodList
    except Exception as e:
        print("Unable to generate the prompt for the mybatis")


def get_content_for_ejb_java_code(partialFlag, additionalPromptRequired, path, component, entityNameList, repoNameList,controllerNameList,serviceNameList):

    additional_prompt = ""
    package_name = os.environ["PACKAGE_NAME"]

    if component == controller:
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".controllers\n\n and use import for any service classes "+package_name+".services and use import for any entity classes "+package_name+".entity in spring boot code\n\n Do not include existing ejb code package statement.\n And also file name should end with Controller.For example ListCountryServlet.java should change to ListCountryController.java follow the similar pattern UserController.java,UserLoginController.java Autowired services class name fields should end with Service. Only add API related code. Do not add any setter or getters"
    elif component == service:
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".services\n\n and use import for any repository classes "+package_name+".repository and use import for any entity classes "+package_name+".entity. Do not include existing ejb code package statement.\n And also file name should end with Service. For example UserService."
    elif component.lower() == 'dao' or component.lower() == 'repository' or component.lower() == 'jpa repository':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".repository\n\n Do not include existing ejb code package statement.use import for any entity classes "+package_name+".entity in spring boot code\n . Do not create duplicate methods inside the code and do not override JPARepository inbuilt methods.And file name must end with Repository. Interface should extend JPARepository. For example UserRepository, UserLoginRepository"
    elif component.lower() == 'entity':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".entity\n\n. Always generate the getter and setter methods for all the properties in the generated java file. Do not include existing ejb code package statement.\n For example User.java, UserLogin.java"
    elif component.lower() == 'config':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".config\n\n Do not include existing ejb code package statement.\nAnd also file name should end with Config.java For example UserConfig.java"
    elif component.lower() == 'constants':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".constants\n\n Do not include existing ejb code package statement.And also file name should end with Constants.java \n For example UserConstants.java"
    elif component.lower() == 'pojo model':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".models\n\n . Always generate the getter and setter methods for all the properties in the generated java file.Do not include existing ejb code package statement.\n And also file name should end with Model.java. For example UserModel.java"

    # content_for_prompt = "Act as a experienced Java developer, Providing you the code written in EJB whcih need to be migrated to spring boot.\n Providing you the path of the java class: "+path+".\n "+additional_prompt+"\n. Do not respond the same content back. Created filename must be same as public class name inside the code and do not generate the unused code. Entity class created with name ".join(entityNameList)+". Service class created with name".join(serviceNameList)+". Repository class created with name ".join(repoNameList)+". Controller class created with name".join(controllerNameList)+"\n Here is EJB code for you to migrate or convert to Spring Boot."        
    content_for_prompt = ''
    if(partialFlag == True):
        if(additionalPromptRequired):
            content_for_prompt = (
            f"Act as an experienced Java developer, providing you with the code written in EJB that needs to be migrated to Spring Boot.\n"
            f"Providing you the path of the Java class: {path}.\n"
            f"{additional_prompt}\n"
            f"Do not respond with the same content. Do not remove any unused import statement, just convert those according to user input. Created filenames must be the same as public class names inside the code.\n"
            f"Entity classes created with names: {', '.join(entityNameList)}.\n"
            f"Service classes created with names: {', '.join(serviceNameList)}.\n"
            f"Repository classes created with names: {', '.join(repoNameList)}.\n"
            f"Controller classes created with names: {', '.join(controllerNameList)}.\n"
            f"Here is the partial EJB code for you to migrate or convert to Spring Boot.")
        else:
            content_for_prompt = (
            f"Act as an experienced Java developer, providing you with the code written in EJB that needs to be migrated to Spring Boot.\n"
            f"Providing you the path of the Java class: {path}.\n"
            f"Do not generate class name if it is not there in the original code. Do not add extra code."
            f"Do not respond with the same content. Created filenames must be the same as public class names inside the code.\n"
            f"Entity classes created with names: {', '.join(entityNameList)}.\n"
            f"Service classes created with names: {', '.join(serviceNameList)}.\n"
            f"Repository classes created with names: {', '.join(repoNameList)}.\n"
            f"Controller classes created with names: {', '.join(controllerNameList)}.\n"
            f"Here is the partial EJB code for you to migrate or convert to Spring Boot.")
    else:
        content_for_prompt = (
        f"Act as an experienced Java developer, providing you with the code written in EJB that needs to be migrated to Spring Boot.\n"
        f"Providing you the path of the Java class: {path}.\n"
        f"{additional_prompt}\n"
        f"Do not respond with the same content. Created filenames must be the same as public class names inside the code, and do not generate unused code.\n"
        f"Entity classes created with names: {', '.join(entityNameList)}.\n"
        f"Service classes created with names: {', '.join(serviceNameList)}.\n"
        f"Repository classes created with names: {', '.join(repoNameList)}.\n"
        f"Controller classes created with names: {', '.join(controllerNameList)}.\n"
        f"Here is the EJB code for you to migrate or convert to Spring Boot.")

    

    #logger.info(content_for_prompt)
    return content_for_prompt


def get_content_for_struts_java_code(path, component, entityNameList, repoNameList,controllerNameList,serviceNameList):

    additional_prompt = ""
    package_name = os.environ["PACKAGE_NAME"]

    if component == controller:
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".controllers\n\n and use import for any service classes "+package_name+".services and use import for any entity classes "+package_name+".entity in spring boot code\n\n. While converting code call the service method which is present do not copy paste the existing code as it is. Do not include existing ejb code package statement.\n And also file name should end with Controller. For example ListCountryAction.java should change to ListCountryController.java, UserAction.java should change to UserController.java, UserRegistrationAction should change to UserRegistrationController and Autowired services class name fields should end with Service. Only add API related code. Do not add any setter or getters"
    elif component == service:
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".services\n\n and use import for any repository classes "+package_name+".repository and use import for any entity classes "+package_name+".entity. While converting service code analyse the existing code and convert as spring boot developers do not leave the any code. Do not include existing ejb code package statement.\n And also file name should end with Service or ServiceImpl based on passed file name. For example UserService, UserLoginService, UserRegistrationService, ListUserService while generating file name please make sure ControlModDAOImpl should be ControlModDAOImplService and ControlModService should be ControlModService only and ControlModServiceImpl should be ControlModServiceImpl only "
    elif component.lower() == 'dao' or component.lower() == 'repository' or component.lower() == 'jpa repository':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".repository\n\n Do not include existing ejb code package statement.use import for any entity classes "+package_name+".entity in spring boot code\n . While converting JPA repository code analyse existing code and create method remembering camel case and should not missed any existing method. Do not create duplicate methods inside the code and do not override JPARepository inbuilt methods.And file name must end with Repository. Interface should extend JPARepository and Carefully remember the Id type of entity and put properly data type Id in JPA repository . For example UserRepository, UserLoginRepository"
    elif component.lower() == 'entity':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".entity\n\n. Always generate the getter and setter methods for the all properties. Do not include existing ejb code package statement.\n For example User.java, UserLogin.java, ListUser.java."
    elif component.lower() == 'config':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".config\n\n Do not include existing ejb code package statement.\nAnd also file name should end with Config.java For example UserConfig.java, UserLoginConfig.java"
    elif component.lower() == 'constants':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".constants\n\n Do not include existing ejb code package statement.And also file name should end with Constants.java \n For example UserConstants.java"
    elif component.lower() == 'pojo model':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".models\n\n. Always generate the getter and setter methods for the all properties. Do not include existing ejb code package statement.\n And also file name should end with Model.java. For example UserModel.java, UserLoginModel.java"

    content_for_prompt = (
            f"Act as an experienced Java developer, providing you with the code written in struts that needs to be migrated to Spring Boot.\n"
            f"Providing you the path of the Java class: {path}.\n"
            f"{additional_prompt}\n"
            f"Do not respond with the same content. Created filenames must be the same as public class names inside the code, and do not generate unused code.\n"
            f"Entity classes created with names: {', '.join(entityNameList)}.\n"
            f"Service classes created with names: {', '.join(serviceNameList)}.\n"
            f"Repository classes created with names: {', '.join(repoNameList)}.\n"
            f"Controller classes created with names: {', '.join(controllerNameList)}.\n"
            f"Return the component for this file as : {component}.\n"
            f"Here is the struts code for you to migrate or convert to Spring Boot.")
    return content_for_prompt


def get_content_for_spring_boot_code(partialFlag, additionalPromptRequired, path, component, entityNameList, repoNameList,controllerNameList,serviceNameList):

    additional_prompt = ""
    package_name = os.environ["PACKAGE_NAME"]

    if component == controller:
        #additional_prompt = "Add the following code in the migrated spring boot code  And also file name should end with Controller. For example UserController and Autowired services class name fields should end with Service. Only add API related code. Do not add any setter or getters"
        additional_prompt = "Add the following code into new spring boot project.  You are provided a code snippet from Spring based Controller. Convert this to an equivalent REST API using Spring Boot's RestController. Only provide code from AccountRestController.java - do not include any other code. Account.java is provided from reference only and for new package and imports: \npackage "+package_name+".controllers\n\n and use import for any service classes "+package_name+".services and use import for any entity classes "+package_name+".entity in spring boot code\n\n " 
    elif component.lower() == 'entity':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".entity\n\n Do not include existing ejb code package statement.\n For example User.java"
    # content_for_prompt = "Act as a experienced Java developer, Providing you the code written in EJB whcih need to be migrated to spring boot.\n Providing you the path of the java class: "+path+".\n "+additional_prompt+"\n. Do not respond the same content back. Created filename must be same as public class name inside the code and do not generate the unused code. Entity class created with name ".join(entityNameList)+". Service class created with name".join(serviceNameList)+". Repository class created with name ".join(repoNameList)+". Controller class created with name".join(controllerNameList)+"\n Here is EJB code for you to migrate or convert to Spring Boot."        
    content_for_prompt = ''
    if(partialFlag == True):
        if(additionalPromptRequired):
            content_for_prompt = (
            f"Act as an experienced Java developer, providing you with the code written spring boot needs to be upgraded to Spring Boot.\n"
            f"Providing you the path of the Java class: {path}.\n"
            f"{additional_prompt}\n"
            f"Do not respond with the same content. Do not remove any unused import statement, just convert those according to user input. Created filenames must be the same as public class names inside the code.\n"
            f"Entity classes created with names: {', '.join(entityNameList)}.\n"
            #f"Service classes created with names: {', '.join(serviceNameList)}.\n"
            #f"Repository classes created with names: {', '.join(repoNameList)}.\n"
            f"Controller classes created with names: {', '.join(controllerNameList)}.\n"
            f"Here is the partial EJB code for you to migrate or convert to Spring Boot.")
        else:
            content_for_prompt = (
            f"Act as an experienced Java developer, providing you with the code written in Spring boot that needs to be upgraded to Spring Boot latest version.\n"
            f"Providing you the path of the Java class: {path}.\n"
            f"Do not generate class name if it is not there in the original code. Do not add extra code."
            f"Do not respond with the same content. Created filenames must be the same as public class names inside the code.\n"
            f"Entity classes created with names: {', '.join(entityNameList)}.\n"
            #f"Service classes created with names: {', '.join(serviceNameList)}.\n"
            #f"Repository classes created with names: {', '.join(repoNameList)}.\n"
            f"Controller classes created with names: {', '.join(controllerNameList)}.\n"
            f"Here is the partial Spring boot code for you to upgrade to latest")
    else:
        content_for_prompt = (
        f"Act as an experienced Java developer, providing you with the code written in Spring boot that needs to be upgraded with latest version of Spring Boot.\n"
        f"Providing you the path of the Java class: {path}.\n"
        f"{additional_prompt}\n"
        f"Do not respond with the same content. Created filenames must be the same as public class names inside the code, and do not generate unused code.\n"
        f"Entity classes created with names: {', '.join(entityNameList)}.\n"
        f"Service classes created with names: {', '.join(serviceNameList)}.\n"
        f"Repository classes created with names: {', '.join(repoNameList)}.\n"
        f"Controller classes created with names: {', '.join(controllerNameList)}.\n"
        f"Here is the EJB code for you upgrade  with Spring Boot latest version")

    

    logger.info(content_for_prompt)
    return content_for_prompt


def get_content_for_ejb_java_code_partial(path, component, entityNameList, repoNameList,controllerNameList,serviceNameList):

    additional_prompt = ""
    package_name = os.environ["PACKAGE_NAME"]

    if component == controller:
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".controllers\n\n and use import for any service classes "+package_name+".services and use import for any entity classes "+package_name+".entity in spring boot code\n\n Do not include existing ejb code package statement.\n And also file name should end with Controller. For example UserController and Autowired services class name fields should end with Service. Only add API related code. Do not add any setter or getters"
    elif component == service:
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".services\n\n and use import for any repository classes "+package_name+".repository and use import for any entity classes "+package_name+".entity. Do not include existing ejb code package statement.\n And also file name should end with Service. For example UserService."
    elif component.lower() == 'dao' or component.lower() == 'repository' or component.lower() == 'jpa repository':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".repository\n\n Do not include existing ejb code package statement.use import for any entity classes "+package_name+".entity in spring boot code\n . Do not create duplicate methods inside the code and do not override JPARepository inbuilt methods.And file name must end with Repository. Interface should extend JPARepository. For example UserRepository"
    elif component.lower() == 'entity':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".entity\n\n Do not include existing ejb code package statement.\n For example User.java"
    elif component.lower() == 'config':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".config\n\n Do not include existing ejb code package statement.\nAnd also file name should end with Config.java For example UserConfig.java"
    elif component.lower() == 'constants':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".constants\n\n Do not include existing ejb code package statement.And also file name should end with Constants.java \n For example UserConstants.java"
    elif component.lower() == 'pojo model':
        additional_prompt = "Add the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".models\n\n Do not include existing ejb code package statement.\n And also file name should end with Model.java. For example UserModel.java"

    # content_for_prompt = "Act as a experienced Java developer, Providing you the code written in EJB whcih need to be migrated to spring boot.\n Providing you the path of the java class: "+path+".\n "+additional_prompt+"\n. Do not respond the same content back. Created filename must be same as public class name inside the code and do not generate the unused code. Entity class created with name ".join(entityNameList)+". Service class created with name".join(serviceNameList)+". Repository class created with name ".join(repoNameList)+". Controller class created with name".join(controllerNameList)+"\n Here is EJB code for you to migrate or convert to Spring Boot."        
    content_for_prompt = (
    f"Act as an experienced Java developer, providing you with the code written in EJB that needs to be migrated to Spring Boot.\n"
    f"Providing you the path of the Java class: {path}.\n"
    f"{additional_prompt}\n"
    f"Do not respond with the same content. Created filenames must be the same as public class names inside the code, and do not generate unused code.\n"
    f"Entity classes created with names: {', '.join(entityNameList)}.\n"
    f"Service classes created with names: {', '.join(serviceNameList)}.\n"
    f"Repository classes created with names: {', '.join(repoNameList)}.\n"
    f"Controller classes created with names: {', '.join(controllerNameList)}.\n"
    f"Here is the EJB code for you to migrate or convert to Spring Boot.")
    logger.info(content_for_prompt)
    return content_for_prompt


        

# if __name__ == "__main__":
#     load_pom_file()