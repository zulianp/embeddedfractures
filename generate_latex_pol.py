import os
import sys
from itertools import zip_longest
# sys.path.insert(0, '../../../utils')
import utils.styles as styles

### Define the data for plotting ###
refinement_indices = [0, 1, 2]

### Plot settings ###
width = 0.4 # width of each subplot, in terms of textwidth
height = 0.5 # height of each subplot, in terms of textwidth
ymin = 0.5
ymax = 2.75
color = "blue"
style = "solid"

# Generate the preamble for the LaTeX document, which includes the packages and the document class.
def generate_preamble():
    latex_code = []
    latex_code.append(r"\documentclass{article}")
    latex_code.append(r"\usepackage{tikz}")
    latex_code.append(r"\usepackage{pgfplots}")
    latex_code.append(r"\usepgfplotslibrary{groupplots}")
    latex_code.append(r"\usepackage{pgfplotstable}")
    latex_code.append(r"\usepackage{amsmath}")
    latex_code.append(r"\pgfplotsset{compat=newest}")
    latex_code.append(r"\begin{document}")
    return latex_code

# Generate the LaTeX code 
def generate_latex(data_file="", titles=[], xlabel="", rows=1, columns=3, include_preamble=True):
    if data_file == "" or len(titles) == 0 or xlabel == "":
        raise ValueError("Data file and titles must be provided.")

    latex_code = generate_preamble() if include_preamble else []
    latex_code.append(r"\begin{figure}[h!]")
    latex_code.append(r"\centering")
    latex_code.append(r"\begin{tikzpicture}")
    latex_code.append(r"\begin{groupplot}[")
    latex_code.append(rf"group style={{group size={columns} by {rows}, horizontal sep=0.1cm}},")
    latex_code.append(rf"width={width}\textwidth,")
    latex_code.append(rf"height={height}\textwidth]")

    # Generate plots
    # for idx, (title, ref) in enumerate(zip(titles, refinement_indices)):
    for idx, (title, ref) in enumerate(zip_longest(titles, refinement_indices, fillvalue=None)):
        y_tick_label_style = (r"y tick label style={/pgf/number format/fixed,"
                              r"/pgf/number format/precision=2},") if idx == 0 else "yticklabels={},"
        ylabel = "" if idx > 0 else styles.getHeadLabel(3)
        latex_code.append(rf"\nextgroupplot[title={{{title}}}, ylabel={{{ylabel}}}, xlabel={{{styles.getArcLengthLabel()}}},"
                          rf"ymin={ymin}, ymax={ymax}, ytick={{0.5,0.75,...,2.75}}, grid=major,{y_tick_label_style}]")
        
        data_file_ref = data_file.replace('X', str(ref))
        latex_code.append(r"\addplot[")
        latex_code.append(rf"color={{{color}}},")
        latex_code.append(rf"style={{{style}}}]")
        # Skip first n=1 as first row in data are the headers
        latex_code.append(f"table[col sep=comma, header=false, x index=0, y index=1, skip first n=1] {{{data_file_ref.replace('../', './')}}};")

    latex_code.append(r"\end{groupplot}")
    latex_code.append(r"\end{tikzpicture}")
    latex_code.append(r"\end{figure}")
    if include_preamble:
        latex_code.append(r"\end{document}")
    return '\n'.join(latex_code)

# Generate the LaTeX code for each case
directory = "cases"
for case in os.listdir(directory):
    # Check if case is a directory
    if os.path.isdir(os.path.join(directory, case)):
        print(f"Creating LaTeX document for case: {case}")
        if case != "small_features":
            data_file = os.path.join('results', case, "dol_cond1_X.csv")
            titles = ['$\\sim 500$ cells', '$\\sim 4k$ cells', '$\\sim 32k$ cells']

            latex_code = generate_latex(data_file=data_file, titles=titles, xlabel=styles.getArcLengthLabel(), rows=1, columns=3)
            with open(f"{case}.tex", "w") as f:
                f.write(latex_code)
                print(f"Created {case}.tex")
        else:
            titles = ["$\\sim 30k$ cells", "$\\sim 150k$ cells"]
            line_indices = [1, 2]

            for line_index in line_indices:
                data_file = os.path.join('results', case, f"dol_line{line_index}_refinementX.csv")
                latex_code = generate_latex(data_file=data_file, titles=titles, xlabel=styles.getArcLengthLabel(), rows=1, columns=2)
                with open(f"{case}_{line_index}.tex", "w") as f:
                    f.write(latex_code)
                    print(f"Created {case}_{line_index}.tex")

print("All LaTeX documents created successfully.")