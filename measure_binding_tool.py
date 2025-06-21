import re
import ast
import tempfile
import shutil
import os


def insert_measurements(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    output_lines = []
    in_block = False

    for i, line in enumerate(lines):
        if re.search(r'#\s*start_measurement', line):
            output_lines.append('measure.start_measurement()\n')
            in_block = True
            continue

        elif re.search(r'#\s*end_measurement', line):
            output_lines.append('measure.end_measurement()\n')
            in_block = False
            continue

        elif in_block:
            output_lines.append(f'# original code: {line.rstrip()}\n')
        else:
            output_lines.append(line)

    # יצירת קובץ זמני
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_f:
        temp_f.writelines(output_lines)
        temp_file_name = temp_f.name

    # בדיקת תקינות תחביר
    try:
        with open(temp_file_name, 'r') as temp_f:
            ast.parse(temp_f.read())

        # אם התחביר תקין, העתק את הקובץ הזמני לקובץ המקורי
        shutil.move(temp_file_name, input_file)
        print(f"Modified script written to {input_file}")

    except SyntaxError as e:
        # אם יש שגיאת תחביר, מחק את הקובץ הזמני ואל תדרוס את הקובץ המקורי
        os.unlink(temp_file_name)
        print(f"Syntax error in generated code: {e}. Original file unchanged.")

    except Exception as e:
        # טיפול בשגיאות אחרות (למשל, בעיות קריאה/כתיבה)
        os.unlink(temp_file_name)
        print(f"Error processing file: {e}. Original file unchanged.")


def generate_python_main(student_code):
    try:
        tree = ast.parse(student_code)
        main_func = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'main':
                main_func = node.name
                break
            elif isinstance(node, ast.FunctionDef):
                main_func = node.name

        if main_func:
            return f"""
import measure
{student_code}
if __name__ == '__main__':
    measure.start_measurement()
    result = {main_func}()
    measure.end_measurement()
    print(result)
"""
        else:
            return f"""
import measure
{student_code}
if __name__ == '__main__':
    measure.start_measurement()
    result = None
    measure.end_measurement()
    print(result)
"""
    except SyntaxError:
        return f"""
import measure
{student_code}
if __name__ == '__main__':
    measure.start_measurement()
    result = None
    measure.end_measurement()
    print(result)
"""


if __name__ == '__main__':
    input_file = 'replace_placeholder.py'
    insert_measurements(input_file)