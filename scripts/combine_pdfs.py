import os
from PyPDF2 import PdfMerger
import argparse

def combine_pdfs(plot_pdf, legend_pdf, output_pdf):
    merger = PdfMerger()

    # Append the plot and the legend in order
    merger.append(plot_pdf)
    merger.append(legend_pdf)

    # Write the combined PDF to a file
    with open(output_pdf, 'wb') as output_file:
        merger.write(output_file)

    print(f"Combined PDF saved as: {output_pdf}")

def main(folder_path='figures/pdf'):
    # Change working directory to the path of the current file
    os.chdir(folder_path)

    # Loop through the folder to find matching plot and legend PDFs
    for file_name in os.listdir(folder_path):
        # If 'crop' is in filename do something
        if "crop" in file_name:
            # Check if the filename with "-crop" replaced by "_legend" exists
            legend_pdf = os.path.join(folder_path, file_name.replace("-crop", "_legend"))
            if os.path.exists(legend_pdf):
                # Perform your processing here
                output_pdf = os.path.join(folder_path, file_name.replace("crop", "combined"))
                combine_pdfs(os.path.join(folder_path, file_name), legend_pdf, output_pdf)
            else:
                print(f"Legend PDF not found for: {file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process PDFs in a specified folder.')
    parser.add_argument('folder_path', nargs='?', default='figures/pdf', help='Path to the folder containing PDFs')

    args = parser.parse_args()

    main(folder_path=args.folder_path)