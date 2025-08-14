import os
import tempfile
import subprocess

def bits_to_text(bits):
    try:
        byte_values = [int(b, 2) for b in bits.split()]
        data = bytes(byte_values)
        text = data.decode('utf-8')
        return text
    except Exception as e:
        print(f"Error converting bits to text: {e}")
        return ""

def make_and_run(contents, files, main_file):
    with tempfile.TemporaryDirectory() as tempdir:
        py_files = []
        for i, f in enumerate(files):
            py_path = os.path.join(tempdir, os.path.basename(f).replace(".de", ".py"))
            with open(py_path, "w", encoding="utf-8") as fi:
                fi.write(contents[i])
            py_files.append(py_path)

        main_py = os.path.join(tempdir, os.path.basename(main_file).replace(".de", ".py"))
        print(f"Running main file: {main_py}")
        result = subprocess.run(["python3", main_py], capture_output=True, text=True)

        print("=== Output ===")
        print(result.stdout)
        if result.stderr:
            print("=== Errors ===")
            print(result.stderr)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(script_dir, "project")
    print(f"Project directory: {root_dir}")

    de_files = []
    de_contents = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            full_path = os.path.join(dirpath, filename)
            if ext == ".de":
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    text = bits_to_text(content)
                    de_files.append(full_path)
                    de_contents.append(text)
                except Exception as e:
                    print(f"Error reading file {full_path}: {e}")

    if not de_files:
        print("No .de files found.")
        return

    if len(sys.argv) < 2:
        print("Please provide the path to the main .de file as an argument")
        return

    main_file = os.path.abspath(sys.argv[1])

    if main_file not in de_files:
        print(f"Main file {main_file} not found in the project.")
        return

    make_and_run(de_contents, de_files, main_file)

if __name__ == "__main__":
    import sys
    main()
