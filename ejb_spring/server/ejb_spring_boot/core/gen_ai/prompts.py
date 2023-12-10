pom_migration_prompt_template = """Act as a next generation Java developer and experienced in both EJB and spring boot, migrate the EJB application code to spring boot application code.
Analyse all the configuration written in all pom.xml which is provided to you. Create new code for new pom.xml supported in spring boot.
Do not include any names related to ejb/EJB and not even ejb/EJB. Include spring-boot-starter-parent, spring-boot-starter-data-jpa and javax-persistence. Use the following tech stacks: Spring boot : 3.1.4, Java 17. Use 8.0.26 version for mysql-connector-java And also use web,test and devtools libraries and add JaCoCo plugin. Please do not respond with same pom which is in request. Respond migrated pom with function get_complete_pom_code when your response is under the limit of AI or if not exceeding 32000 token limit of AI , otherwise Respond migrated pom with function get_partial_pom_code if you have response partially"""


pom_migration_prompt_template_struts = """Act as a next generation Java developer and experienced in both struts 1 and spring boot, migrate the struts 1 application code to spring boot application code. Analyze the configurations in the existing pom.xml file provided and create a new pom.xml file for Spring Boot. The new configuration should include dependencies for spring-boot-starter-parent, spring-boot-starter-data-jpa, javax-persistence, and use Spring Boot version 3.0 along with Java 17. Additionally, please include version 8.0.26 for mysql-connector-java. Include libraries for web, test, and devtools, and add the JaCoCo plugin. Avoid any references to struts 1 in the configuration. Do not generate the same pom like struts generate always spring boot supported pom"""


system_prompt_struts_pom = """Assist in converting a Struts 1 project's POM.xml configuration to a Spring Boot-compatible POM.xml. The user will provide the original Struts POM.xml, and you need to generate the Spring Boot-compatible version of the POM.xml file."""


system_prompt_other_file_description_template = """Help in identifying what is the suitable files of EJB code to be converted to Spring boot. Provide information if provided file can be converted to controller/service/jpa repository/entity/model POJO or configuration. User will provide the input for file paths of the EJB application."""

system_prompt_other_file_description_template_struts = """Help in identifying what is the suitable files of Struts code to be converted to Spring boot. Provide information if provided file can be converted to controller/service/jpa repository/entity or configuration. User will provide the input for file paths of the struts application."""

system_prompt_other_spring_boot_file_description_template = """Help in identifying what is the suitable files of spring boot code to be upgraded with spring boot latest version. Provide information if provided file can be converted to controller/service/jpa repository/entity/model POJO or configuration. User will provide the input for file paths of the spring boot application."""


system_prompt_convert_code_template = """Help in converting EJB code to spring boot compatible code as part of migration. Do proper analysis and generate the code. Java docs must be added each java class. Do not use the existing package statement and import statement. Replace them with user provided input in the user prompt.Respond migrated code with function get_migrated_code when your response is under the limit of AI or if not exceeding 32000 token limit of AI , otherwise Respond migrated code with function get_partial_migrated_code if you have response partially """


system_prompt_convert_struts_code_template = """Help in converting struts code to spring boot compatible code as part of migration. Do proper analysis and generate the code. Add the validation in model only if it is present in struts class. Do not use the existing package statement and import statement. Replace them with user provided input in the user prompt. Respond migrated code with function get_spring_boot_migrated_code"""

system_prompt_upgrade_template = """Help in Upgrading spring boot compatible code as part of upgradation. Do proper analysis and generate the code. Java docs must be added each java class. Do not use the existing package statement and import statement. Replace them with user provided input in the user prompt.Respond upgraded code with function get_upgrade_code """


system_prompt_convert_partial_code_template = """Help in converting EJB code to spring boot compatible code as part of migration. Do proper analysis and generate the code. Do not use the existing package statement and import statement. Replace them with user provided input in the user prompt. Do not remove unused code."""

user_prompt_identify_java_file_details_template = """Here are file paths of the EJB application available. Provide which files are necessary to migrate to spring boot and what component those will be converted to. If the file contains an @Entity annotation, consider it an entity class. Dao/Repository classes will be categorized as repository component. Please exclude the use of a Base DAO concept and files that ends with "daoImpl" or "repositoryImpl" cannot be considered as service components during migration. Do not exclude constants component."""


user_prompt_identify_java_file_details_template_for_struts = """Here are the file paths of the Struts application. Identify the necessary files for migrating to Spring Boot and specify the corresponding components they will be converted to. Classes with Dao/Repository annotations will be categorized as repository components and only form classes will be categorized as POJO Model component remaing pojo classes will be categorized as entity and analyse clearfully if action class is present with Similar name categorized class as entity not POJO Model. If for any action class does not have service class then consider DAO interface as repo class and daoImpl as service class apply similar logic for service layer as well Service interface will be Repository and ServiceImpl will be Service class.If name of files is Services.java class and do not have actions class migrate that separetely with same name like Services.java and categorised as config. Do not exclude constants components."""


user_prompt_identify_java_file_details_template_for_mybatis = """Here are the file paths of the mybatis application. Identify the necessary files for migrating to Spring Boot and specify the corresponding components they will be converted to. Classes with Dao/Repository annotations will be categorized as repository components and only form classes will be categorized as POJO Model component remaing pojo classes will be categorized as entity. Exclude the use of a Base DAO concept, and files ending with "daoImpl" or "repositoryImpl" cannot be considered as service components during migration. Do not exclude constants components."""


systemPrompt_mybatis = """You are a seasoned software engineer working on a project migration tool. Your task is to assist users in migrating individual files from older technologies (iBatis/MyBatis) to the latest technologies (Spring Boot, JPA). Users will provide specific files and migration preferences. Understand the old technologies specific file (class, configuration) selected or piece of code passed and convert it to latest technology selected by user to its corresponding file or code. Analyse the MyBatis file and repond with three section of get_spring_boot_migrated_code_from_iBatis_MyBatis function. """

userPrompt_mybatis="""1. **Old Technology:**  MyBatis/iBatis 2. **File or Code to Migrate:** """  
        

system_prompt_generate_test_cases_template = """Generate the Junit test cases for the code given by the user. Include all the import statemnets needed. Use @MockBean where ever is required and If any annotation used in file import the package from which annotaion is coming.import org.junit.jupiter.api.Assertions.*  in all the testcase classes. Analyse the first method for which you are writting test case will now correctly mock the behavior of both findById and save methods of the userRepository. Generate the delete test-case with extra analysis and Do not forgot to mock any depedent call. EditUser testcase should generate with extra analysis should not throw the exception while running. While writing testcase for Controller do the proper analysis and follow the POST and PUT method like below example and do not remove \ from content json always add like below
example:

mockMvc.perform(MockMvcRequestBuilders.post("/users").content("{\"id\": 1, \"email\": \"user@gmail.com\"}").contentType(MediaType.APPLICATION_JSON))

mockMvc.perform(MockMvcRequestBuilders.put("/users/1").content("{\"id\": 1, \"email\": \"user@gmail.com\"}").contentType(MediaType.APPLICATION_JSON)).andExpect(MockMvcResultMatchers.status().isOk());                        
 
and service test case write like below 

@Test
    public void editUserTest() {
        User user = new User();
        user.setId(1L);
        user.setUsername("test");
        user.setPassword("password");
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(userRepository.save(user)).thenReturn(user);
        assertNotNull(userService.editUser(1L, user));
    }
"""

system_prompt_generate_kitty_file= """Generate the kitty.yml file.below are the sample kitty.yml file

setup:
  featureFlagMap:
    useArtifactory: true
    imageValidation: false
  releaseRefs: ["main"]
owner:
  group: group-name
profiles:
  - springboot-web-jre11
build:
  skip: false
deploy:
  namespace: namespace-name
  releaseType:
    rollbackOnError: false
    waitForReady: true
    deployTimeout: 500
  helm:
    values:
      min:
        cpu: 400m
        memory: 1G
      max:
        cpu: 600m
        memory: 1.5G
      scaling:
        enabled: "true"
        cpuPercent: 80
        min: 1
        max: 2
      # networking:
      #   httpEnabled: true
      #   httpsEnabled: true
      #   httpsRedirect: true
      livenessProbe:
        wait: 120
      readinessProbe:
        path: "/actuator/health"
        wait: 120
      networking:
        pathPrefix: /
        externalPort: "8080"
        internalPort: "8080"
      metadata:
        annotations:
          sidecar.istio.io/inject: "false"
  stages:
    - name: dev
      approvers:
        user: vn56bax
      target:
        cluster_id: ['deployment_cluster_id']
      refs: ['main']
      helm:
        values:
          secrets:
            akeyless: true
            files:
              - destination: sample.properties
                content: sampleapp/app
            config:
              path: /secrets/
              akeyless:
                path: /Prod/WCNP/homeoffice/location
    - name: stage
      approvers:
        user: vn56bax
      target:
        cluster_id: ['deployment_cluster_id']
      refs: ['main']
      helm:
        values:
          secrets:
            akeyless: true
            files:
              - destination: sample.properties
                content: sampleapp/app
            config:
              path: /secrets/
              akeyless:
                path: /Prod/WCNP/homeoffice/location
notify:
   msTeams:
    channelId: channelid
   slack: 
     channelName: dummy-channel 
"""

system_prompt_generate_application_properties_template = """Generate the default application properties based on the dependencies in the pom.xml. Do not include unnecessary properties."""

partialCodePrompt = """Act as a next generation Java Developer and experienced in both EJB and Spring boot, migrate the ejb code provided into equivalent spring boot code. Respond with proper function call. Add the converted springboot code inside 'springBootCode' component of get_functions_for_partial_code_migration function call. The code provided below is partial ejb code so do not remove any unused code.\nAdd the following code in the migrated spring boot code for new package and imports: \npackage "+package_name+".services\n\n and use import for any repository classes "+package_name+".repository and use import for any entity classes "+package_name+".entity. Do not include existing ejb code package statement.\n And also file name should end with Service. For example UserService."""

mainclassPrompt = """Act as a next generation Java Developer and experienced in Spring boot, Generate the spring boot main class. Respond with proper function call. Do not respond inside content key"""

