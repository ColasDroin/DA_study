#!/bin/bash
source /home/cdroin/DA_study/master_study/../miniconda/bin/activate
cd /home/cdroin/DA_study/master_study/opt_flathv_75_1500_withBB_chroma15_1p4
python 000_make_distrib.py > output_ht.txt 2> error_ht.txt
rm -rf final_* modules optics_repository optics_toolkit tools tracking_tools temp mad_collider.log __pycache__ twiss* errors fc* optics_orbit_at*
