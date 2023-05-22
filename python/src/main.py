import sys


"""
This script is a demonstration for how to use renku workflows.
The workflow itself is defined in the workflow.yml file. It can be executed within a renku environment with 

renku run workflow.yml
"""


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        txt = f.read()

    with open(output_file, "w") as f:
        f.write(txt)
