#!/bin/bash
source /home/cdroin/DA_study/master_study/../miniconda/bin/activate
cp -rf /home/cdroin/DA_study/master_study/opt_flathv_75_1500_withBB_chroma15_1p4/madx_000/* .
ls
pwd
python 000_pymask.py > output_ht.txt 2> error_ht.txt
tar -zcvf xsuite_lines.tar.gz xsuite_lines
cp -rf xsuite_lines.tar.gz /home/cdroin/DA_study/master_study/opt_flathv_75_1500_withBB_chroma15_1p4/madx_000
