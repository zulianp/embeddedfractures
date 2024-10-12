import os

def get_paths():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = curr_dir.replace('scripts', 'plots')
    results_dir = curr_dir.replace('scripts', 'results')
    utils_dir = os.path.join(curr_dir, 'utils')
    return curr_dir, plots_dir, results_dir, utils_dir
