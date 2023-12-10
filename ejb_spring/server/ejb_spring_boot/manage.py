#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import openai
from core.processing.ejb_springboot import migrate_ejb_to_spring_boot, migrate_struts_to_spring_boot, \
    migrate_mybatis_to_spring_boot, GENERATE_DOCUMENTS, GENERATE_TESTCASE, GENERATE_JPA_REPOSITORY, \
    GENERATE_ENTITY_BY_SPECIFICATION, GENERATE_KITTY_FILE, GENERATE_DATA_MIGRATION_SCRIPT, GENERATE_BATCH_SCRIPT, \
    GENERATE_DATA_LAKE_SCRIPT, GENERATE_SQL_SCRIPT, GENERATE_UNIT_TESTS, GENERATE_DOCS, GENERATE_INFRA_CODE


def main():
    if sys.argv[2] == 'GENERATE-DOCUMENTS':
        file_path = sys.argv[1]
        GENERATE_DOCUMENTS(file_path,'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')
    elif sys.argv[2] == 'GENERATE-TESTCASE':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
    
        GENERATE_TESTCASE(file_path,'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')
    elif sys.argv[2] == 'GENERATE-JPA-REPOSITORY':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_JPA_REPOSITORY(file_path,'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')
    
    elif sys.argv[2] == 'GENERATE-WALMART-DEPLOYMENT-FILE':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_KITTY_FILE(file_path,'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')

    # =============================VG BRUSHES START=============================

    elif sys.argv[2] == 'GENERATE-ENTITY':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_ENTITY_BY_SPECIFICATION(file_path,'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')

    elif sys.argv[2] == 'GENERATE-UNIT-TESTS':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_UNIT_TESTS(file_path,'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')

    elif sys.argv[2] == 'GENERATE-DOCS':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_DOCS(file_path,'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')

    elif sys.argv[2] == 'GENERATE-BATCH-SCRIPT':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_BATCH_SCRIPT(file_path,'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')

    elif sys.argv[2] == 'GENERATE-DATA-MIGRATION-SCRIPT':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_DATA_MIGRATION_SCRIPT(file_path,'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')

    elif sys.argv[2] == 'GENERATE-DATA-LAKE-SCRIPT':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_DATA_LAKE_SCRIPT(file_path,'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')

    elif sys.argv[2] == 'GENERATE-SQL-SCRIPT':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_SQL_SCRIPT(file_path,'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')

    elif sys.argv[2] == 'GENERATE-INFRA-CODE':
        file_path = sys.argv[1]
        print(f"Running script with file location: {file_path}")
        GENERATE_INFRA_CODE(file_path,'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')

    # =============================VG BRUSHES END=============================

    else:
        file_location = sys.argv[1]
        print(f"Running script with file location: {file_location}")
        file_path= sys.argv[1]
        input_file=sys.argv[3]
        with open(input_file) as t:
            input_lines = t.readlines()
            i=1
            for input_line in input_lines:
                if len(input_line.split("="))<2:
                    break
                val = input_line.split("=")[1].strip().removesuffix("\n")
                if i==1:
                    application_name=val
                elif i==2:
                    package_name=val
                elif i==3:
                    springBootRepoUrl=val
                elif i==4:
                    gitUserName=val
                elif i==5:
                    gitEmail=val
                else:
                    break;
                i = i+1
    if sys.argv[2] == 'EJB-SPRING':
    
        migrate_ejb_to_spring_boot(45,file_path,springBootRepoUrl,application_name,package_name,'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',gitUserName,gitEmail)

    elif sys.argv[2] == 'STRUTS-SPRING':

        migrate_struts_to_spring_boot(file_path,springBootRepoUrl,application_name,package_name,'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',gitUserName,gitEmail)
    
    elif sys.argv[2] == 'MYBATIS-SPRING':
        
        migrate_mybatis_to_spring_boot(file_path,springBootRepoUrl,application_name,package_name,'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',gitUserName,gitEmail)
        
        
    
    elif sys.argv[2] == 'GENERATE-JPA-REPO':
        
        migrate_mybatis_to_spring_boot(file_path,springBootRepoUrl,application_name,package_name,'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',gitUserName,gitEmail)
    
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ejb_spring_boot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    #execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
