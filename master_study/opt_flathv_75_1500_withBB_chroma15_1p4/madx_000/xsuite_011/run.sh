#!/bin/bash
source /home/cdroin/DA_study/master_study/../miniconda/bin/activate
cp -rf /home/cdroin/DA_study/master_study/opt_flathv_75_1500_withBB_chroma15_1p4/madx_000/xsuite_011/* .
cp -rf /home/cdroin/DA_study/master_study/opt_flathv_75_1500_withBB_chroma15_1p4/madx_000/xsuite_011/../xsuite_lines.tar.gz .
cp -rf /home/cdroin/DA_study/master_study/opt_flathv_75_1500_withBB_chroma15_1p4/madx_000/xsuite_011/../../particles .
tar -xvf xsuite_lines.tar.gz
ls
pwd
python 000_track.py > output_ht.txt 2> error_ht.txt
cp -rf output* log* fma* /home/cdroin/DA_study/master_study/opt_flathv_75_1500_withBB_chroma15_1p4/madx_000/xsuite_011
