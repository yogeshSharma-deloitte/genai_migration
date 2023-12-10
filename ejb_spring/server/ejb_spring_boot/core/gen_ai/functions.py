
def get_functions_for_pom_generation():
    functions = [
        {
            "name": "get_complete_pom_code",
            "description": "get complete pom.xml code for spring boot",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Code for pom.xml supported in spring boot.",
                    },
                    "isCompletePomGenerated" : {
                        "type": "boolean",
                        "description": "Return true if pom cantent is completed. Return false if still pom content need to be responded",
                    }
                },
                "required": ["code","isCompletedPomGenerated"],
            },
        }
        
    ]
    return functions

def get_functions_for_struts_pom_generation():
    
    functions = [
        {
            "name": "convert_struts_pom_to_spring_boot_pom",
            "description": "Convert a Struts project's POM.xml to a Spring Boot-compatible POM.xml.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spring_boot_pom_code": {
                        "type": "string",
                        "description": "pom.xml code for a Spring Boot application",
                    }
                },
                "required": ["spring_boot_pom_code"]
            }
        }
    ]
    return functions


def get_functions_for_pom_upgradation():
    functions = [
        {
            "name": "get_upgrade_pom_code",
            "description": "get upgraded pom.xml code for spring boot",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Code for pom.xml supported in spring boot.",
                    },
                },
                "required": ["code"],
            },
        }
        
    ]
    return functions



def get_functions_for_build_improvements():
    functions = [
        {
            "name": "get_build_improvements",
            "description": "get steps to fix the build",
            "parameters": {
                "type": "object",
                "properties": {
                    "improvements": {
                        "type": "string",
                        "description": "steps to fix the build",
                    },
                },
                "required": ["improvements"],
            },
        }
        
    ]
    return functions

def get_functions_for_data_migration_code():
    functions = [
        {
            "name": "get_data_migration_code_in_pyspark",
            "description": "get data migration code in pyspark",
            "parameters": {
                "type": "object",
                "properties": {
                    "pysparkcode": {
                        "type": "string",
                        "description": "pyspark code generated for data migration",
                    },
                },
                "required": ["pysparkcode"],
            },
        }

    ]
    return functions

def get_functions_for_batch_code():
    functions = [
        {
            "name": "get_batch_code_in_pyspark",
            "description": "get batch code in pyspark",
            "parameters": {
                "type": "object",
                "properties": {
                    "batchcode": {
                        "type": "string",
                        "description": "pyspark code generated for batch application",
                    },
                },
                "required": ["batchcode"],
            },
        }

    ]
    return functions

def get_functions_for_data_lake_code():
    functions = [
        {
            "name": "get_data_lake_code_in_pyspark",
            "description": "get data lake code in pyspark",
            "parameters": {
                "type": "object",
                "properties": {
                    "datalakecode": {
                        "type": "string",
                        "description": "pyspark code generated for data lake",
                    },
                },
                "required": ["datalakecode"],
            },
        }

    ]
    return functions

def get_functions_for_sql():
    functions = [
        {
            "name": "get_db_queries_in_sql",
            "description": "generate SQL queries based on the functional requirements provided.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sqlcode": {
                        "type": "string",
                        "description": "SQL code generated from functional requirements and given database schema.",
                    },
                },
                "required": ["sqlcode"],
            },
        }

    ]
    return functions

def get_functions_for_unit_tests():
    functions = [
        {
            "name": "get_unit_tests",
            "description": "get unit tests",
            "parameters": {
                "type": "object",
                "properties": {
                    "unittestscode": {
                        "type": "string",
                        "description": "unit test code generated",
                    },
                },
                "required": ["unittestscode"],
            },
        }

    ]
    return functions

def get_functions_for_docs():
    functions = [
        {
            "name": "get_docs",
            "description": "get docs for code",
            "parameters": {
                "type": "object",
                "properties": {
                    "docs": {
                        "type": "string",
                        "description": "docs for code",
                    },
                },
                "required": ["docs"],
            },
        }

    ]
    return functions

def get_functions_for_infra_code():
    functions = [
        {
            "name": "get_cloudformation_code_for_infra",
            "description": "Generate cloudformation template for AWS resources/infrastructure.",
            "parameters": {
                "type": "object",
                "properties": {
                    "infracode": {
                        "type": "string",
                        "description": "The cloudformation code generated in json for AWS resources/infrastructure.",
                    },
                },
                "required": ["infracode"],
            },
        }

    ]
    return functions


def get_functions_for_code_identification():
    functions = [
        {
            "name" : "get_migration_details",
            "description" : "Get migration details for the given java file paths",
            "parameters" : {
                "type": "object",
                "properties": {
                    "details" : {
                        "type" : "array",
                        "items" : {
                            "type" : "object",
                            "properties": {
                                "path": {"type": "string","description": "Path of the file given as input in the prompt"},
                                "component" : {"type": "string","enum": ["controller", "service", "entity", "JPA Repository", "POJO model", "Config", "Constants"],"description": "component for the given file path to be migrated in the spring boot"},
                                "filename" : {"type":"string", "description" : "Name of the file for example UserController.java"},
                                "fileRequired" : {"type":"boolean", "description" : "If class is not required for a springboot project send false else send true"}
                            },
                            "required": ["path", "component", "filename", "fileRequired"]
                        }
                    }
                },
                "required": ["details"]
            }
        }
    ]
    return functions


def get_functions_for_code_struts_identification():
    functions = [
        {
            "name" : "get_struts_migration_details",
            "description" : "Get migration details for the given java file paths",
            "parameters" : {
                "type": "object",
                "properties": {
                    "details" : {
                        "type" : "array",
                        "items" : {
                            "type" : "object",
                            "properties": {
                                "path": {"type": "string","description": "Path of the file given as input in the prompt"},
                                "component" : {"type": "string","enum": ["controller", "service", "entity", "JPA Repository", "POJO model", "Config", "Constants"],"description": "component for the given file path to be migrated in the spring boot"},
                                "filename" : {"type":"string", "description" : "Name of the file for example UserController.java"},
                                "fileRequired" : {"type":"boolean", "description" : "If class is not required for a springboot project send false else send true"}
                            },
                            "required": ["path", "component", "filename", "fileRequired"]
                        }
                    }
                },
                "required": ["details"]
            }
        }
    ]
    return functions

def get_functions_for_mybatis_code_migration():
    functions = [
        {
            "name": "get_spring_boot_migrated_code_from_iBatis_MyBatis",
            "description": "get complete migrated java code for spring boot",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_code": {
                        "type": "string",
                        "description": "Spring boot service class code converted from iBatis/MyBatis",
                    },
                    "entity_code": {
                        "type": "string",
                        "description": "Spring boot Entity class code converted from iBatis/MyBatis",
                    },
                    "repository_code": {
                        "type": "string",
                        "description": "Spring boot repository class code converted from iBatis/MyBatis",
                    },
                    "component" : {"type": "string","enum": ["service", "entity", "JPA Repository"],"description": "component for the given file path to be migrated in the spring boot"},
                    "filename" : {"type":"string", "description" : "Name of the file for example UserService.java"}
                    },
                
                "required": ["service_code","entity_code","repository_code" , "component", "filename"],
            },
        }
    ]
    return functions




def get_functions_for_code_migration():
    functions = [
        {
            "name": "get_migrated_code",
            "description": "get complete migrated java code for spring boot",
            "parameters": {
                "type": "object",
                "properties": {
                    "isCompleteCodeGenerated": {
                        "type": "boolean",
                        "description": "Return true if passed file code cantent is completed. Return false if still passed file content need to be responded",
                    },
                    "ejbCode": {
                        "type": "string",
                        "description": "Original code written in EJB",
                    },
                    "springBootCode": {
                        "type": "string",
                        "description": "Spring boot code which is converted from EJB",
                    },
                    "component" : {"type": "string","enum": ["controller", "service", "entity", "JPA Repository", "POJO model", "Config", "Constants"],"description": "component for the given file path to be migrated in the spring boot"},
                    "filename" : {"type":"string", "description" : "Name of the file for example UserController.java"}
                    },
                
                "required": ["ejbCode","springBootCode", "component", "filename"],
            },
        }
    ]
    return functions


def get_functions_for_jpa_repository():
    functions = [
        {
            "name": "get_jpa_repository_code",
            "description": "get jpa repository code",
            "parameters": {
                "type": "object",
                "properties": {
                    "jpaRepositoryCode": {
                        "type": "string",
                        "description": " JPA Repository code",
                    },
                    "component" : {"type": "string","enum": ["JPA Repository"],"description": "component for the given file path to be migrated in the spring boot"},
                    "filename" : {"type":"string", "description" : "Name of the file for example UserRepository.java"}
                    },
                
                "required": ["jpaRepositoryCode", "component", "filename"],
            },
        }
    ]
    return functions


def get_function_for_spring_boot_api_code_by_specification():
    functions = [
        {
            "name": "get_spring_boot_code_by_API_specification",
            "description": "get spring boot code of java",
            "parameters": {
                "type": "object",
                "properties": {
                    "details": {
                        "type": "array",
                        "description": "List of the spring boot all the layers in the API specification",
                        "items": {
                            "type": "object",
                            "properties": {
                                "entityCode": {
                                    "type": "string",
                                    "description": "Spring Boot Entity code: Return the entity code if at least one entity exists in API specification",
                                },
                                "repositoryCode": {
                                    "type": "string",
                                    "description": "Spring Boot Repository code: Return the JPA repository based on the entity by API specification",
                                },
                                "serviceCode": {
                                    "type": "string",
                                    "description": "Service code generated by API specification",
                                },
                                "dtoCode": {
                                    "type": "string",
                                    "description": "Data transfer code generated by API specification",
                                },
                                "controllerCode": {
                                    "type": "string",
                                    "description": "Controller code generated by API specification",
                                },
                                "entityFilename": {
                                    "type": "string",
                                    "description": "Name of the file for the entity (e.g., User.java)",
                                },
                                "repositoryFilename": {
                                    "type": "string",
                                    "description": "Name of the file for the repository (e.g., UserRepository.java)",
                                },
                                "serviceFilename": {
                                    "type": "string",
                                    "description": "Name of the file for the service (e.g., UserService.java)",
                                },
                                "dtoFilename": {
                                    "type": "string",
                                    "description": "Name of the file for the DTO (e.g., UserDto.java)",
                                },
                                "controllerFilename": {
                                    "type": "string",
                                    "description": "Name of the file for the controller (e.g., UserController.java)",
                                },
                            },
                            "required": ["entityCode", "repositoryCode", "serviceCode", "dtoCode", "controllerCode", "entityFilename", "repositoryFilename", "serviceFilename", "dtoFilename", "controllerFilename"],
                        },
                    },
                },
                "required": ["details"],
            },
        }
    ]
    return functions





def get_function_for_kitty_specification():
    functions = [
        {
            "name": "get_kitty_file",
            "description": "get kitty.yml content",
            "parameters": {
                "type": "object",
                "properties": {
                    "kittyCode": {
                        "type": "string",
                        "description": "Kitty file which will be used for deployment",
                    },
                    
                    "filename" : {"type":"string", "description" : "Name of the file for kitty.yml"}
                },

                "required": ["kittyCode","filename"],
            },
        }
    ]
    return functions





def get_functions_for_struts_code_migration():
    functions = [
        {
            "name": "get_spring_boot_migrated_code",
            "description": "get complete migrated java code for spring boot",
            "parameters": {
                "type": "object",
                "properties": {
                    "strutsCode": {
                        "type": "string",
                        "description": "Original code written in struts 1",
                    },
                    "springBootCode": {
                        "type": "string",
                        "description": "Spring boot code which is converted from struts 1",
                    },
                    "component" : {"type": "string","enum": ["controller", "service", "entity", "JPA Repository", "POJO model", "Config", "Constants"],"description": "component for the given file path to be migrated in the spring boot"},
                    "filename" : {"type":"string", "description" : "Name of the file for example UserRegisterController.java or UserLoginController.java or UserRegisterModel.java"}
                },

                "required": ["strutsCode","springBootCode", "component", "filename"],
            },
        }
    ]
    return functions

def get_functions_for_main_class_creation():
    functions = [
        {
            "name": "get_main_class_code",
            "description": "Get main class code for spring boot application for given input",
            "parameters": {
                "type": "object",
                "properties": {
                    "mainClassCode": {
                        "type": "string",
                        "description": "Main class code of the application in spring boot with @SpringBootApplication annotation",
                    },
                    "filename" : {"type":"string", "description" : "Name of main class in spring boot for example SampleApplication.java"}
                },
                "required": ["mainClassCode", "filename"],
            },
        }
    ]
    return functions

def get_functions_for_test_cases_generation():
    functions = [
        {
            "name": "write_test_cases",
            "description": "Writes test cases in the test class for the given spring boot code",
            "parameters": {
                "type": "object",
                "properties": {
                    "generatedTestCode": {
                        "type": "string",
                        "description": "It is test case code for given java code",
                    },
                    # "originalCode": {
                    #     "type": "string",
                    #     "description": "It is actual java code passed as input",
                    # },
                    "filename" : {"type":"string", "description" : "Name of test case class written in Junit, for example UserControllerTest.java"},
                    "component" : {"type": "string","enum": ["controller test", "service test", "main class test", "entity test", "JPA Repository test", "POJO model test", "Config test", "Constants test"],"description": "component for the given code to be test cases generated in the spring boot"},
                },
                "required": ["generatedTestCode", "filename", "component", "originalCode"],
            },
        }
    ]
    return functions



def get_functions_for_application_properties_generation():
    functions = [
        {
            "name": "create_application_properties",
            "description": "Creates application properties based on the dependencies in the pom.xml",
            "parameters": {
                "type": "object",
                "properties": {
                    "generatedProperties": {
                        "type": "string",
                        "description": "Properties for the application. For example, server.port=8080",
                    },
                },
                "required": ["generateProperties"],
            },
        }
    ]
    return functions

def get_functions_for_documentation_generation():
    functions = [
        {
            "name": "documentation_generation",
            "description": "Generate comprehensive documentation for a Java class.",
            "parameters": {
                "type": "object",
                "properties": {
                    "markdownDocumetation": {
                        "type": "string",
                        "description": "The markdown documentation content for the Java class.",
                    },
                    "EntityName": {
                        "type": "string",
                        "description": "The name of the Java class for which documentation is generated.",
                    }
                },
                "required": ["markdownDocumetation", "EntityName"],
            },
        }
    ]
    return functions