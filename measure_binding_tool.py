import re
import os
import subprocess

def insert_measurements(input_file, output_file):
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file {input_file} does not exist")
        
        print(f"Processing file: {input_file}")
        
        with open(input_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        block_level = 0
        import_added = False

        # בדיקה אם יש כבר import measure
        for line in lines:
            if re.match(r'\s*import\s+measure\s*', line):
                import_added = True
                break

        # הוספת import measure בתחילת הקובץ
        if not import_added:
            output_lines.append('import measure\n')
            print("Added 'import measure' to the file")

        for line in lines:
            # התחלת מדידה
            if re.match(r'\s*#\s*start\b', line, re.IGNORECASE):
                output_lines.append('measure.start_measurement()\n')
                block_level += 1
                continue

            # סיום מדידה
            elif re.match(r'\s*#\s*end\b', line, re.IGNORECASE):
                if block_level > 0:
                    output_lines.append('measure.end_measurement()\n')
                    block_level -= 1
                continue

            # בתוך בלוק מדידה – שמור את הקוד
            elif block_level > 0:
                output_lines.append(line)
            else:
                output_lines.append(line)

        if block_level > 0:
            print("Warning: Unclosed measurement block detected")

        # כתיבת הקובץ החדש
        with open(output_file, 'w') as f:
            f.writelines(output_lines)

        # בדיקת תחביר
        try:
            subprocess.run(['python3', '-m', 'py_compile', output_file], check=True, capture_output=True)
            print(f"Modified script written to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error: Generated code is not syntactically valid: {e.stderr.decode()}")
            raise

    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == '__main__':
    input_file = 'original.py'
    output_file = 'modified.py'
    insert_measurements(input_file, output_file)