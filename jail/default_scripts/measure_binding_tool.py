import re
import ast

def insert_measurements(input_file, output_file='main.py'):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    output_lines = []
    in_block = False
    import_added = False

    for line in lines:
        if re.match(r'\s*import\s+measure\s*', line):
            import_added = True
            break

    inserted_import = False

    for i, line in enumerate(lines):
        if not inserted_import and not import_added:
            if line.strip() and not line.strip().startswith('#'):
                output_lines.append('import measure\n')
                inserted_import = True

        if re.match(r'\s*#\s*start\s*', line):
            if not import_added and not inserted_import:
                output_lines.append('import measure\n')
                inserted_import = True
            output_lines.append('measure.start_measurement()\n')
            in_block = True
            continue

        elif re.match(r'\s*#\s*end\s*', line):
            output_lines.append('measure.end_measurement()\n')
            in_block = False
            continue

        elif in_block:
            output_lines.append(f'# original code: {line.rstrip()}\n')
        else:
            output_lines.append(line)

    with open(output_file, 'w') as f:
        f.writelines(output_lines)

    print(f"Modified script written to {output_file}")

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
measure.start_measurement()
{student_code}
measure.end_measurement()
"""
    except SyntaxError:
        return f"""
import measure
{student_code}
measure.start_measurement()
{student_code}
measure.end_measurement()
"""

if __name__ == '__main__':
    input_file = 'student.py'
    insert_measurements(input_file, 'main.py')
