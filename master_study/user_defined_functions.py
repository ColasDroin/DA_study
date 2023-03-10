def generate_run_sh(node, generation_number):
   python_command =  (node
                     .root
                     .parameters["generations"]
                     [generation_number]
                     ["job_executable"])
   return (f'source {node.root.parameters["setup_env_script"]}\n'
           f'cd {node.get_abs_path()}\n'
           f'python {python_command} > output.txt 2> error.txt\n')

def generate_run_sh_htc(node, generation_number):
   python_command =  (node
                     .root
                     .parameters["generations"]
                     [generation_number]
                     ["job_executable"])
   if generation_number==2:
   	return (f'#!/bin/bash\n'
           f'source {node.root.parameters["setup_env_script"]}\n'
           f'cp -rf {node.get_abs_path()}/* .\n'
           f'ls\n'
           f'pwd\n'
           f'python {python_command} > output_ht.txt 2> error_ht.txt\n'
           f'tar -zcvf xsuite_lines.tar.gz xsuite_lines\n'
           f'cp -rf xsuite_lines.tar.gz {node.get_abs_path()}\n')
   if generation_number==3:
   	return (f'#!/bin/bash\n'
           f'source {node.root.parameters["setup_env_script"]}\n'
           f'cp -rf {node.get_abs_path()}/* .\n'
           f'cp -rf {node.get_abs_path()}/../xsuite_lines.tar.gz .\n'
           f'cp -rf {node.get_abs_path()}/../../particles .\n'
           f'tar -xvf xsuite_lines.tar.gz\n'
           f'ls\n'
           f'pwd\n'
           f'python {python_command} > output_ht.txt 2> error_ht.txt\n'
           #f'rm -rf xsuite_lines\n'
           f'cp -rf output* log* fma* {node.get_abs_path()}\n')
   else:
   	return (f'#!/bin/bash\n'
           f'source {node.root.parameters["setup_env_script"]}\n'
           f'cd {node.get_abs_path()}\n'
           f'python {python_command} > output_ht.txt 2> error_ht.txt\n'
           f'rm -rf final_* modules optics_repository optics_toolkit tools tracking_tools temp mad_collider.log __pycache__ twiss* errors fc* optics_orbit_at*\n')
