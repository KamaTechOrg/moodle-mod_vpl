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
            output_lines.append(f'# {line.rstrip()}\n')  # שמירת השורה המקורית כהערה
            output_lines.append('measure.start_measurement()\n')
            in_block = True
            continue

        elif re.search(r'#\s*end_measurement', line):
            output_lines.append('measure.end_measurement()\n')
            output_lines.append(f'# {line.rstrip()}\n')  # שמירת השורה המקורית כהערה
            in_block = False
            continue

        else:
            output_lines.append(line)  # שמירת השורה כפי שהיא, גם בתוך הבלוק

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


if __name__ == '__main__':
    input_file = 'main.py'  # עיבוד קובץ main.py שנוצר על ידי generate_python_main_py
    insert_measurements(input_file)