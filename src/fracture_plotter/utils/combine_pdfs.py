import argparse
import os
import subprocess


def create_latex(plot_pdf, legend_pdf, output_tex):
    # Define the LaTeX content with the plot and legend in the same figure
    latex_content = f"""
    \\documentclass{{article}}
    \\usepackage{{graphicx}}
    \\usepackage{{geometry}}
    \\geometry{{margin=1in}}

    \\begin{{document}}

    \\begin{{figure}}[ht]
        \\centering
        % Insert the plot PDF
        \\includegraphics[width=0.9\\textwidth]{{{plot_pdf}}}

        % Add vertical space between the plot and the legend
        \\vspace{{-15em}}

        % Insert the legend PDF
        \\includegraphics[width=0.45\\textwidth]{{{legend_pdf}}}
    \\end{{figure}}

    \\end{{document}}
    """

    # Write the LaTeX content to the output .tex file
    with open(output_tex, "w") as tex_file:
        tex_file.write(latex_content)

    print(f"LaTeX file saved as: {output_tex}")


def compile_latex_to_pdf(tex_file):
    # Compile the LaTeX file into a PDF using pdflatex
    try:
        subprocess.run(["pdflatex", tex_file], check=True)
        print(f"PDF generated from {tex_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")
    except FileNotFoundError:
        print(
            "pdflatex command not found. Make sure LaTeX is installed and added to your PATH."
        )


def combine_pdfs(folder_path="figures/pdf"):
    # Change working directory to the path of the current file
    os.chdir(folder_path)

    # Loop through the folder to find matching plot and legend PDFs
    for file_name in os.listdir(folder_path):
        if "crop" in file_name:
            # Check if the filename with "-crop" replaced by "_legend" exists
            legend_pdf = file_name.replace("-crop", "_legend")
            if os.path.exists(legend_pdf):
                # Create output LaTeX file name
                output_tex = os.path.join(
                    folder_path,
                    file_name.replace("crop", "combined").replace(".pdf", ".tex"),
                )
                # Generate the LaTeX script
                create_latex(file_name, legend_pdf, output_tex)
                # Compile the LaTeX file into a PDF
                compile_latex_to_pdf(output_tex)
            else:
                print(f"Legend PDF not found for: {file_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate LaTeX scripts for plots and legends."
    )
    parser.add_argument(
        "folder_path",
        nargs="?",
        default="figures/pdf",
        help="Path to the folder containing PDFs",
    )

    args = parser.parse_args()

    combine_pdfs(folder_path=args.folder_path)
