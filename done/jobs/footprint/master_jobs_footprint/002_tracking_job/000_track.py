import json
import yaml
import time
import logging

import numpy as np
import pandas as pd

import xtrack as xt
import xpart as xp

####################
# Read config file #
####################

with open("config.yaml", "r") as fid:
    config = yaml.safe_load(fid)

######################
# Tag job as started #
######################

try:
    import tree_maker

    tree_maker.tag_json.tag_it(config["log_file"], "started")
except ImportError:
    logging.warning("tree_maker not available")
    tree_maker = None

##########################################
# Read line, part_on_co, one-turn matrix #
##########################################
# from pathlib import Path
# path = Path(config['xline_json'])
# mypath = str(path.parent.absolute()) + ".tar.gz"
# mypath2  = path.parent.absolute().parent.absolute()

# import subprocess
# subprocess.call(["tar","-xvf", mypath, '-C', mypath2], shell=False)
#
with open(config["xline_json"]) as fid:
    dd = json.load(fid)

# subprocess.call(["rm", "-rf", f"{mypath2}/xsuite_lines"], shell=False)
#
p_co = xp.Particles.from_dict(dd["particle_on_tracker_co"])
line = xt.Line.from_dict(dd)
R_matrix = np.array(dd["RR_finite_diffs"])

# line._var_management = None # Remove knobs
#####################################################
# Get normalized coordinateds of particles to track #
#####################################################

particle_df = pd.read_parquet(config["particle_file"])

r_vect = particle_df["normalized amplitude in xy-plane"].values
theta_vect = particle_df["angle in xy-plane [deg]"].values * np.pi / 180  # [rad]

A1_in_sigma = r_vect * np.cos(theta_vect)
A2_in_sigma = r_vect * np.sin(theta_vect)

####################################################
# Generate particles object (physical coordinates) #
####################################################

particles = xp.build_particles(
    particle_on_co=p_co,
    x_norm=A1_in_sigma,
    y_norm=A2_in_sigma,
    delta=config["delta_max"],
    R_matrix=R_matrix,
    scale_with_transverse_norm_emitt=(config["epsn_1"], config["epsn_2"]),
)
particles.particle_id = particle_df.particle_id.values

#################
# Symplify line #
#################

# line.remove_inactive_multipoles(inplace=True)
# line.remove_zero_length_drifts(inplace=True)
# line.merge_consecutive_drifts(inplace=True)
# line.merge_consecutive_multipoles(inplace=True)

#################
# Build tracker #
#################

tracker = xt.Tracker(
    line=line,
    extra_headers=["#define XTRACK_MULTIPOLE_NO_SYNRAD"],
)
tracker.optimize_for_tracking()
############################
# Save initial coordinates #
############################

pd.DataFrame(particles.to_dict()).to_parquet("input_particles.parquet")

##########
# Track! #
##########

num_turns = config["n_turns"]
a = time.time()
tracker.track(particles, turn_by_turn_monitor=True, num_turns=num_turns, freeze_longitudinal=True)
b = time.time()

print(f"Elapsed time: {b-a} s")
print(f"Elapsed time per particle per turn: {(b-a)/particles._capacity/num_turns*1e6} us")

##########################
# Save final coordinates #
##########################

pd.DataFrame(particles.to_dict()).to_parquet("output_particles.parquet")

tbt_x = tracker.record_last_track.x.flatten()  # particle_id, turns
tbt_y = tracker.record_last_track.y.flatten()  # particle_id, turns
particles_id = tracker.record_last_track.particle_id.flatten()
turns = tracker.record_last_track.at_turn.flatten()
df = pd.DataFrame({"particle_id": particles_id, "x": tbt_x, "y": tbt_y, "turn": turns})
import NAFFlib

keys = []
qx_tot1 = []
qx_tot2 = []
qy_tot1 = []
qy_tot2 = []
diffusions = []
for key, group in df.groupby("particle_id"):
    qx1 = abs(NAFFlib.get_tune(group.x.values[:2000], 2))
    qy1 = abs(NAFFlib.get_tune(group.y.values[:2000], 2))
    qx2 = abs(NAFFlib.get_tune(group.x.values[-2000:], 2))
    qy2 = abs(NAFFlib.get_tune(group.y.values[-2000:], 2))
    qx_tot1.append(qx1)
    qy_tot1.append(qy1)
    qx_tot2.append(qx2)
    qy_tot2.append(qy2)
    keys.append(key)
    diffusion = np.sqrt(abs(qx1 - qx2) ** 2 + abs(qy1 - qy2) ** 2)
    if diffusion == 0.0:
        diffusion = 1e-60
    diffusion = np.log10(diffusion)
    diffusions.append(diffusion)
dff = pd.DataFrame(
    {
        "particle_id": keys,
        "qx1": qx_tot1,
        "qy1": qy_tot1,
        "qx2": qx_tot2,
        "qy2": qy_tot2,
        "diffusion": diffusions,
    }
)
dff = dff.merge(particle_df, on="particle_id")
dff.to_parquet(f"fma.parquet")


if tree_maker is not None:
    tree_maker.tag_json.tag_it(config["log_file"], "completed")
