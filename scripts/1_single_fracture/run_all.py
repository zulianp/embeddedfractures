import os

curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
case = curr_dir.split(os.sep)[-1] # case we are dealing with

# os.system("python percentiles.py")
os.system(f"python {curr_dir}/pol.py")
os.system(f"python {curr_dir}/pot.py")

# this goes after the others
# os.system(f"python ./{curr_dir}/overlay.py")
