# %%
import tree_maker
from tree_maker import NodeJob
from tree_maker import initialize
import time
import os
from pathlib import Path
import itertools
import numpy as np
import yaml
from user_defined_functions import generate_run_sh
from user_defined_functions import generate_run_sh_htc

# Import the configuration
config = yaml.safe_load(open("config.yaml"))

# The user defines the variable to scan
# machine parameters scans
qx0 = np.arange(62.305, 62.325 + 0.001, 0.001)


optics_file = ["optics_repository/HLLHCV1.5/flatcc/opt_flathv_75_180_1500_thin.madx"]
beam_sigt = [0.0761]

# beam_npart   = [9.40e+10, 9.60e+10, 1.00e+11, 1.02e+11, 1.04e+11, 1.06e+11, 1.08e+11, 1.10e+11,
#       1.12e+11, 1.14e+11, 1.16e+11, 1.18e+11, 1.20e+11, 1.22e+11,
#       1.24e+11, 1.26e+11, 1.28e+11, 1.30e+11, 1.32e+11, 1.34e+11,
#       1.36e+11, 1.38e+11, 1.40e+11, 1.42e+11, 1.44e+11]

beam_npart = [1.4e11]

oct_current = list(range(-350, 350, 20))
enable_crabs = [True]
mode = "b1_with_bb"

on_x1 = 250.0
on_x8v = 170
on_x8h = 0.0
on_disp = 1
chroma = 15

study_name = f"opt_flathv_75_1500_withBB_chroma15_octscan"

children = {}
children[study_name] = {}
children[study_name]["children"] = {}

for optics_job, (myq1, my_optics, my_sigt, my_npart, my_oct, my_crabs) in enumerate(
    itertools.product(qx0, optics_file, beam_sigt, beam_npart, oct_current, enable_crabs)
):
    optics_children = {}
    children[study_name]["children"][f"madx_{optics_job:03}"] = {
        "qx0": float(myq1),
        "qy0": float(myq1 - 62.0 + 60.0 + 5e-3),
        "mode": mode,
        "optics_file": my_optics,
        "beam_sigt": my_sigt,
        "beam_npart": my_npart,
        "oct_current": my_oct,
        "enable_crabs": my_crabs,
        "chromaticity_x": chroma,
        "chromaticity_y": chroma,
        "knob_settings": {
            "on_x1": on_x1,
            "on_x5": on_x1,
            "on_x8v": on_x8v,
            "on_x8h": on_x8h,
            "on_disp": on_disp,
        },
        "log_file": f"{os.getcwd()}/{study_name}/madx_{optics_job:03}/tree_maker.log",
        "children": optics_children,
    }
    for track_job in range(15):
        optics_children[f"xsuite_{track_job:03}"] = {
            "particle_file": f"../../particles/{track_job:03}.parquet",
            "xline_json": "../xsuite_lines/line_bb_for_tracking.json",
            "n_turns": int(3000000),
            "log_file": f"{os.getcwd()}/{study_name}/madx_{optics_job:03}/xsuite_{track_job:03}/tree_maker.log",
        }

config["root"]["children"] = children
config["root"]["setup_env_script"] = os.getcwd() + "/../miniconda/bin/activate"

# Create tree object
start_time = time.time()
root = initialize(config)
print("Done with the tree creation.")
print("--- %s seconds ---" % (time.time() - start_time))

# From python objects we move the nodes to the file-system.
start_time = time.time()
# root.make_folders(generate_run_sh)
root.make_folders(generate_run_sh_htc)
print("The tree folders are ready.")
print("--- %s seconds ---" % (time.time() - start_time))

import shutil

shutil.move("tree_maker.json", f"tree_maker_{study_name}.json")
shutil.move("tree_maker.log", f"tree_maker_{study_name}.log")
