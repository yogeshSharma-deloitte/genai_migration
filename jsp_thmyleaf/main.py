#!/usr/bin/env python3

import os
import subprocess
import sys
import datetime

import openai
import yaml
from prompt import system_prompt, servlet_to_Spring_prompt, mainclassPrompt, pom_migration_prompt_template
import re
from from_root import from_root


def find_jsp_files(directory):
    jsp_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".jsp"):
                jsp_files.append(os.path.join(root, file))
    return jsp_files


def convert_jsp_thymeleaf(jsp_code, prompt):
    code_response = generate_response(jsp_code, prompt)
    return code_response


def convert_jsp_files(input_dir, jsp_file_path):
    jsp_files = find_jsp_files(input_dir)
    if len(jsp_files) == 0:
        print(f"No JSP File Found in Directory {input_dir}")
    else:
        for jsp_file in jsp_files:
            with open(jsp_file, 'r') as file:
                try:
                    jsp_content = file.read()
                    thymeleaf_code = convert_jsp_thymeleaf(jsp_content, system_prompt)
                    th_file_name = os.path.splitext(os.path.basename(jsp_file))[0] + ".html"
                    write_to_path(th_file_name, thymeleaf_code, jsp_file_path)
                except Exception as e:
                    print(f"Error reading file '{jsp_file}': {str(e)}")


def convert_java_spring_boot(output_dir, package_structure):
    file_path_dict = {"@Controller": ["src/main/java/com/springframework/sample/controller", "controller"],
                      "@Service": ["src/main/java/com/springframework/sample/service", "service"],
                      "@Component": ["src/main/java/com/springframework/sample/util", "util"],
                      "@Repository": ["src/main/java/com/springframework/sample/repository", "repository"],
                      "@Data": ["src/main/java/com/springframework/sample/model", "model"],
                      "@Getter": ["src/main/java/com/springframework/sample/model", "model"],
                      None: ["src/main/java/com/springframework/sample/util", "util"]}
    java_files = find_java_files(input_dir)
    if len(java_files) == 0:
        print(f"No JSP File Found in Directory {input_dir}")
    else:
        for java_file in java_files:
            with open(java_file, 'r') as file:
                try:
                    java_content = file.read()
                    java_code = convert_jsp_thymeleaf(java_content, servlet_to_Spring_prompt)
                    annotation = find_class_annotation(java_code)
                    full_path = output_dir + "/" + file_path_dict[annotation][0]
                    package_import = "package " + package_structure.replace("/", ".") + "." + \
                                     file_path_dict[annotation][1] + ";"
                    java_code = package_import + "\n\n" + java_code
                    class_name = parse_the_class_name(java_code) + ".java"
                    write_to_path(class_name, java_code, full_path)
                except Exception as e:
                    print(f"Error reading file '{java_file}': {str(e)}")


def find_java_files(directory):
    java_files = []
    for root, dirs, files in os.walk(directory):
        destination_root = os.path.join(output_dir, os.path.relpath(root, input_dir))
        if destination_root.find('/java') > 0:
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
    return java_files


def parse_the_class_name(java_code):
    class_pattern = re.compile(r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)\b')
    match = class_pattern.search(java_code)
    if match:
        class_name = match.group(1)
        return class_name
    else:
        print("Class name not found in the Java source code.")
    return None


def find_class_annotation(text):
    substring_list = ["@Controller", "@Service", "@Repository", "@Component", "@Data", "@Getter"]
    for substring in substring_list:
        if substring in text:
            return substring
    return None


def create_pom_file_for_application(file_path):
    pom_code = convert_jsp_thymeleaf('', pom_migration_prompt_template)
    xml_content = re.sub(r'```xml\s*([\s\S]*?)```', r'\1', pom_code, flags=re.MULTILINE)
    write_to_path('pom.xml', xml_content, file_path)


def create_main_class_for_application(file_path, dir_structure):
    main_code = convert_jsp_thymeleaf('', mainclassPrompt)
    main_class_code = re.sub(r'```java\s*([\s\S]*?)```', r'\1', main_code, flags=re.MULTILINE)
    package_import = "package " + dir_structure.replace("/", ".") + ";"
    main_class_code = package_import + "\n" + main_class_code
    class_name = parse_the_class_name(main_class_code) + ".java"
    write_to_path(class_name, main_class_code, file_path)


def write_to_path(filename, converted_code, file_path):
    output_file_path = os.path.join(file_path, filename)
    print("output file path", output_file_path)
    with open(output_file_path, 'w') as outputfile:
        try:
            outputfile.write(converted_code)
            outputfile.close()
        except Exception as e:
            print(f"Error writing  file '{output_file_path}': {str(e)}")


def generate_response(code, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt},
                  {'role': 'user', 'content': code}],
        max_tokens=2048,
        n=1,
        temperature=0,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.5,

    )

    response_text = response['choices'][0]['message']['content']
    return response_text


def create_dir():
    os.makedirs(jsp_file_path, exist_ok=True)
    os.makedirs(os.path.join(java_file_path, "controller"), exist_ok=True)
    os.makedirs(os.path.join(java_file_path, "service"), exist_ok=True)
    os.makedirs(os.path.join(java_file_path, "repository"), exist_ok=True)
    os.makedirs(os.path.join(java_file_path, "model"), exist_ok=True)
    os.makedirs(os.path.join(java_file_path, "util"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "src", "test"), exist_ok=True)


def push_spring_boot_code_to_repository(sprint_boot_app_file_path, spring_boot_repo_url, git_username, git_email):
    file_complete_path = sprint_boot_app_file_path
    try:
        subprocess.run(["git", "init"], cwd=file_complete_path)
        subprocess.run(["git", "config", "--global", "user.name", git_username])
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
        print(f"Code pushed successfully to {spring_boot_repo_url}")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


if __name__ == "__main__":
    input_dir = sys.argv[1]
    yaml_file_path = sys.argv[2]

    # Read the YAML file
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        # Access specific values from the YAML data
        java_file_base_path = yaml_data['java_source_folder'][0]['destination']
        folder_structure = yaml_data['project']['groupId'] + "." + yaml_data['project']['artifactId']
        jsp_file_path = yaml_data['jsp_source_folder'][0]['destination']
        openai.api_key = yaml_data['api_key']
        spring_boot_repo_url = yaml_data['git']['url']
        git_username = yaml_data['git']['username']
        git_email = yaml_data['git']['email']
        project_name = yaml_data['project']['name']

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = str(from_root(timestamp, project_name, mkdirs=True))

    folder_structure = folder_structure.replace(".", "/")
    java_file_path = os.path.join(output_dir, java_file_base_path, folder_structure)
    jsp_file_path = os.path.join(output_dir, jsp_file_path)

    create_dir()
    convert_java_spring_boot(output_dir, folder_structure)
    convert_jsp_files(input_dir, jsp_file_path)
    create_pom_file_for_application(output_dir)
    create_main_class_for_application(java_file_path, folder_structure)
    push_spring_boot_code_to_repository(output_dir, spring_boot_repo_url, git_username, git_email)