from jinja2 import Environment, FileSystemLoader
import logging
from decouple import config
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("report")


def report_generation(migration_report_path, completed_process_build, transformationContent, sprint_boot_app_file_path):
    try: 
        # Set up the template environment
        logger.info(f"while build generation path is {migration_report_path}")
        template_loader = FileSystemLoader(migration_report_path)
        template_env = Environment(loader=template_loader)

        # Get the template using its relative name
        
        if str(completed_process_build) is None or str(completed_process_build) == "":
            report_template = template_env.get_template('migration_report_template.html')
            print("The variable is empty")
            html_report = report_template.render(content=transformationContent, build_content=completed_process_build)
            MIGRATION_REPORT = os.path.join(sprint_boot_app_file_path,'documentation','migration_report.html')
            with open(MIGRATION_REPORT, "w") as file:
                file.write(html_report)
            logger.info("Migration reports generated successfully.")
        else:
            report_template = template_env.get_template('build_report_template.html')
            html_report = report_template.render(build_content=completed_process_build)
            BUILD_REPORT = os.path.join(sprint_boot_app_file_path,'documentation','build_report.html')
            with open(BUILD_REPORT, "w") as file:
                file.write(html_report)
            logger.info("Build reports generated successfully.")
        
        # Render the templates with data
        
        
    except Exception as e:
       print("Unable to generate the migration reports") 

def report_generation_build(buildContent, improvements):
    # Set up the template environment
    base_path = os.path.join(os.getcwd(),'temp','templates')
    template_loader = FileSystemLoader(base_path)
    template_env = Environment(loader=template_loader)
    # Get the template using its relative name
    report_template = template_env.get_template('migration_report_template.html')
    
    SUGGESTION_REPORT = os.path.join(base_path, 'Imrovements_report.html')


    # Render the templates with data
    html_report = report_template.render(build_content = buildContent,build_improvements = improvements)
    # Save the "before" and "after" HTML reports to files
    with open(SUGGESTION_REPORT, "w") as file:
        file.write(html_report)

    logger.info("HTML improvements reports generated successfully.")
