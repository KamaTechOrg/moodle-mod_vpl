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
        # החלפת תגיות ישירות
        if re.search(r'#\s*import_measure', line):
            output_lines.append('import measure\n')
        elif re.search(r'#\s*start_measurement', line):
            output_lines.append('measure.start_measurement()\n')
        elif re.search(r'#\s*end_measurement', line):
            output_lines.append('measure.end_measurement()\n')
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
        shutil.move(temp_file_name, input_file)
        print(f":white_check_mark: Modified script written to {input_file}")
    except SyntaxError as e:
        os.unlink(temp_file_name)
        print(f":x: Syntax error in generated code: {e}. Original file unchanged.")
    except Exception as e:
        os.unlink(temp_file_name)
        print(f":x: Error processing file: {e}. Original file unchanged.")

if __name__ == '__main__':
    # בדיקת ארגומנטים משורת הפקודה
    if len(sys.argv) > 1 and len(sys.argv) < 4:
        print("Usage: python3 measure_binding_tool.py <func_name> <param_name> <param_type> [<param_subtype>] [<return_type> [<return_subtype>]]")
        sys.exit(1)

    # קבלת הארגומנטים (אם סופקו)
    func_name = sys.argv[1] if len(sys.argv) > 1 else None
    param_name = sys.argv[2] if len(sys.argv) > 2 else None
    param_type = sys.argv[3] if len(sys.argv) > 3 else None
    param_subtype = sys.argv[4] if len(sys.argv) > 4 else None
    return_type = sys.argv[5] if len(sys.argv) > 5 else None
    return_subtype = sys.argv[6] if len(sys.argv) > 6 else None

    # הדפסת הארגומנטים לבדיקה
    if func_name:
        print(f"Processing with: func_name={func_name}, param_name={param_name}, param_type={param_type}, "
              f"param_subtype={param_subtype}, return_type={return_type}, return_subtype={return_subtype}")

    # עיבוד קובץ main.py
    input_file = 'main.py'
    insert_measurements(input_file)