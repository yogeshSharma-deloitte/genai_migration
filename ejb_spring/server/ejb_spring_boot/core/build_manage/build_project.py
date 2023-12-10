import subprocess
import os
import subprocess
from ..processing.report import report_generation
import logging
import re

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("build_project")


def migration_report(templates_path, project_directory, reportContent, sprint_boot_app_file_path):
    generate_migration_report(templates_path, project_directory,reportContent, sprint_boot_app_file_path)
    
def generate_migration_report(templates_path, project_directory,reportContent, sprint_boot_app_file_path):
    try:
        mvn_command = 'mvn -f '+project_directory+' clean install'
        completed_process_build = subprocess.run(mvn_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Build is completed with logs: ",completed_process_build.stdout)
        report_generation(templates_path, completed_process_build.stdout,reportContent, sprint_boot_app_file_path)
    except Exception as e: 
        logger.info(f"Exception occured in report generation flow. Unable to generate the reports");

   

def run_jar_file(project_directory, application_name):
    run_java = "java -jar "+project_directory+'/target/'+application_name+'.jar'
    os.system(run_java)


if __name__ == "__main__":
    run_jar_file("/Users/skarnawadi/Documents/codetest/ejb-to-spring-boot","ejb-to-spring-boot-1.0")