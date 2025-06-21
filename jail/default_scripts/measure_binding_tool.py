import re
import ast
import tempfile
import shutil
import os
import sys

def insert_measurements(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    output_lines = []
    for line in lines:
        if re.search(r'#\s*import_measure', line):
            output_lines.append('import measure\n')
        elif re.search(r'#\s*start_measurement', line):
            output_lines.append('measure.start_measurement()\n')
        elif re.search(r'#\s*end_measurement', line):
            output_lines.append('measure.end_measurement()\n')
        else:
            output_lines.append(line)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_f:
        temp_f.writelines(output_lines)
        temp_file_name = temp_f.name

    try:
        with open(temp_file_name, 'r') as temp_f:
            ast.parse(temp_f.read())
        shutil.move(temp_file_name, input_file)
        print(f":white_check_mark: Modified script written to {input_file}")
    except SyntaxError as e:
        os.unlink(temp_file_name)
        print(f":x: Syntax error in generated code: {e}. Original file unchanged.")
    except Exception as e:
        os.unlink(temp_file_name)
        print(f":x: Error processing file: {e}. Original file unchanged.")

if __name__ == '__main__':
    input_file = 'main.py'
    insert_measurements(input_file)