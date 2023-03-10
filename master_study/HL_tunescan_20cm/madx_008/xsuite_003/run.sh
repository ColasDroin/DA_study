#!/bin/bash
source /home/cdroin/example_DA_study/master_study/../../miniconda3/bin/activate
cd /home/cdroin/example_DA_study/master_study/HL_tunescan_20cm/madx_008/xsuite_003
python 000_track.py > output.txt 2> error.txt
rm -rf final_* modules optics_repository optics_toolkit tools tracking_tools temp mad_collider.log __pycache__ twiss* errors fc* optics_orbit_at*
