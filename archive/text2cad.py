#!/usr/bin/env python3

import os
from openai import OpenAI
import subprocess

def main():
    """
    A command-line interface to request QueryCAD code from OpenAI based on
    a file containing battery context. Then optionally run code2cad.py on the
    generated file to produce an STL.
    """

    # Instantiate the client (make sure you have your environment/API key set up)
    client = OpenAI()

    # Provide a robust system prompt to set context.
    system_prompt = (
        "You are a specialized 'Robot Design Planner' AI. "
        "You design quadruped robots and their components. "
        "Now your main focus is to take a textual specification (e.g. about a battery), "
        "and produce valid QueryCAD code that can be used to generate CAD (STL) files. "
        "Ask for any clarifications if needed, but ideally produce detailed, valid QueryCAD code. "
        "Stay on topic, and only produce QueryCAD instructions or relevant clarifications."
    )

    # We'll gather conversation messages here
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    print("=== Robot CAD Planner CLI ===")
    print("Provide the path to a text file containing battery context.")
    context_file = input("Context file path (e.g. battery.txt): ").strip()

    if not os.path.isfile(context_file):
        print("File does not exist. Exiting.")
        return

    with open(context_file, "r", encoding="utf-8") as f:
        battery_context = f.read()

    # Append the battery context as a user message
    messages.append({
        "role": "user",
        "content": (
            "Here is the specification for the battery:\n\n"
            f"{battery_context}\n\n"
            "Please produce QueryCAD code to generate the necessary battery housing or mounting."
        )
    })

    # Call the API to get the QueryCAD code
    try:
        completion = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 as the model
            messages=messages,
            temperature=0.7  # Add some creativity while maintaining coherence
        )
        querycad_code = completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return

    # Save the QueryCAD code to a file
    output_file = "battery_design.qcad"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(querycad_code)

    print(f"\n=== Generated QueryCAD code saved to {output_file} ===\n")
    print("Would you like to run code2cad.py to generate an STL from this code? (y/n):")
    answer = input().strip().lower()

    if answer == "y":
        try:
            subprocess.run(["python3", "code2cad.py", output_file], check=True)
        except subprocess.CalledProcessError as e:
            print("Error running code2cad.py:", e)
    else:
        print("Not generating STL at this time. Exiting.")

if __name__ == "__main__":
    main()