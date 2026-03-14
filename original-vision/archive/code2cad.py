#!/usr/bin/env python3

import sys
import os
import subprocess

def main():
    if len(sys.argv) < 3:
        print("Usage: code2cad.py <cad-script.py> <output.stl>")
        sys.exit(1)

    cad_script = sys.argv[1]
    output_stl = sys.argv[2]

    if not os.path.isfile(cad_script):
        print(f"Error: '{cad_script}' not found.")
        sys.exit(1)

    # We assume the generated script exports an STL by default to 'output_stl'
    # or we can pass an argument. For simplicity, let's pass it as an arg:
    # e.g. "python cad_script.py output_stl"
    # That means your generated code should accept sys.argv[1] as the STL path.

    # Use a subprocess call to run the generated python script
    print(f"Running CAD script '{cad_script}' to produce STL '{output_stl}'...")
    try:
        subprocess.run(["python3", cad_script, output_stl], check=True)
        print(f"STL generation complete. File: {output_stl}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running '{cad_script}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
