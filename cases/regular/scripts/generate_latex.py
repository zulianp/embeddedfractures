import os
import sys
sys.path.insert(0, '../../../utils')
import styles

# Define the data for plotting
titles = ['$\\sim 500$ cells', '$\\sim 4k$ cells', '$\\sim 32k$ cells']
refinement_index = [0, 1, 2]
conds = [1]  # Assuming condition 1 for this example
places_and_methods = {"USI": ["FEM_LM"],}

# Define the linestyle and color dictionaries (example)
linestyle = {"USI": {"FEM_LM": "solid"}}
color = {"USI": {"FEM_LM": "blue"}}

def generate_latex():
    latex_code = []

    latex_code.append(r"\documentclass{article}")
    latex_code.append(r"\usepackage{tikz}")
    latex_code.append(r"\usepackage{pgfplots}")
    latex_code.append(r"\usepgfplotslibrary{groupplots}")
    latex_code.append(r"\usepackage{pgfplotstable}")
    latex_code.append(r"\usepackage{amsmath}")
    latex_code.append(r"\pgfplotsset{compat=newest}")
    latex_code.append(r"\begin{document}")
    latex_code.append(r"\begin{figure}[h!]")
    latex_code.append(r"\centering")
    latex_code.append(r"\begin{tikzpicture}")
    latex_code.append(r"\begin{groupplot}[")
    latex_code.append(r"group style={group size=3 by 1, horizontal sep=0.1cm},")
    latex_code.append(r"width=0.4\textwidth,")
    latex_code.append(r"height=0.5\textwidth]")

    # Generating plots
    for idx, (title, ref) in enumerate(zip(titles, refinement_index)):
        ylabel = styles.getHeadLabel(3) if idx == 0 else ""
        y_tick_label_style = (r"y tick label style={/pgf/number format/fixed,"
                              r"/pgf/number format/precision=2},") if idx == 0 else "yticklabels={},"

        latex_code.append(rf"\nextgroupplot[title={{{title}}}, ylabel={{{ylabel}}}, xlabel={{{styles.getArcLengthLabel()}}},"
                          rf"ymin=0.5, ymax=2.75, ytick={{0.5,0.75,...,2.75}}, grid=major,{y_tick_label_style}"
                          r"legend pos=north east,legend style={draw=none},]")

        for place in places_and_methods:
            for method in places_and_methods[place]:
                data_file = f"../results/dol_cond1_{ref}.csv"
                if os.path.isfile(data_file):
                    label = f"{place}"
                    latex_code.append(r"\addplot[")
                    latex_code.append(f"color={color[place][method]},")
                    latex_code.append(f"style={linestyle[place][method]}]")
                    latex_code.append(f"table[col sep=comma, header=false, x index=0, y index=1, skip first n=1] {{{data_file.replace('../', './')}}};")
                    latex_code.append(f"\\addlegendentry{{{label}}}")

    latex_code.append(r"\end{groupplot}")
    latex_code.append(r"\end{tikzpicture}")
    latex_code.append(r"\end{figure}")
    latex_code.append(r"\end{document}")

    return '\n'.join(latex_code)

# Generate the LaTeX code
latex_code = generate_latex()
print(latex_code)

# Save the LaTeX code to a file called regular.tex
with open("regular.tex", "w") as f:
    f.write(latex_code)
