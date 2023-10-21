import nbformat
import sys
import os

def extract_markdown_cells(input_file, output_file):
    """
    Extract markdown cells from a Jupyter notebook.

    Args:
    - input_file (str): Path to the input Jupyter notebook.
    - output_file (str): Path to the output text file.
    """
    
    # Load the notebook
    with open(input_file, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Extract markdown cells
    markdown_content = ""
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            markdown_content += cell.source + "\n\n"
    
    # Write to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_markdown.py <input_notebook.ipynb> <output_file.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist!")
        sys.exit(1)

    extract_markdown_cells(input_file, output_file)
    print(f"Markdown content extracted to {output_file}")

