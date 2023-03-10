# %%
"""
Example of a chronjob
"""

# %%
import tree_maker
import yaml
from tree_maker import NodeJob
import pandas as pd
import awkward as ak
from joblib import Parallel, delayed
import time

start = time.time()


#my_study='opt_flatvh_75_300_1500'
my_study='opt_flathv_75_1500_withBB'
#my_study='./full_tune_scan_wfix'
#my_study='./full_tune_scan_wfix_more_particles'
#my_study='./full_tune_scan_wfix_more_particles_tunes_as_sixt'
problematic = []
try:
    #root=tree_maker.tree_from_json(f'{my_study}/tree_maker.json')
    root=tree_maker.tree_from_json(f'tree_maker_{my_study}.json')
except Exception as e:
    print(e)
    print('Probably you forgot to edit the address of you json file...')

my_list=[]
#if root.has_been('completed'):
#    print('All descendants of root are completed!')
if True:
    for node in root.generation(2):
        #print(node, root.get_abs_path())
        #quit()
        #qqq
        #node_df = pd.read_parquet(f'{node.get_abs_path()}/final_summ_BBOFF.parquet')
        with open(f'{node.get_abs_path()}/config.yaml','r') as fid:
            config_parent=yaml.safe_load(fid)
        #node_df['path']= f'{node.get_abs_path()}'
        for node_child in node.children:
        #os.sytem(f'bsub cd {node.path} &&  {node.path_template} ')
        #my_list.append(pd.read_parquet(f'{node.path}/test.parquet', columns=['x']).iloc[-1].x)
            with open(f'{node_child.get_abs_path()}/config.yaml','r') as fid:
                 config=yaml.safe_load(fid)
            #try:
            if True:
                #print(config['particle_file'])
                #if True:
            	particle=pd.read_parquet(
                     f"{my_study}/{config['particle_file']}")
            	df=pd.read_parquet(
                     f'{node_child.get_abs_path()}/fma.parquet')
            	df['path 1']= f'{node.get_abs_path()}'
            	df['name 1']= f'{node.name}'
            	df['path 2']= f'{node_child.get_abs_path()}'
            	df['name 2']= f'{node_child.name}'
            	#df['q1 final']=node_df['q1'].values[0]
            	#df['q2 final']=node_df['q2'].values[0]
            	df['q1']=config_parent['qx0']
            	df['q2']=config_parent['qy0']
            	df=pd.merge(df, particle, on=["particle_id"])
            	my_list.append(df)
            #except:
            #    problematic.append(node_child.get_abs_path())
            #    print(f"problem {node_child.get_abs_path()}")
	

    my_df = pd.concat(my_list)
    #aux = my_df[my_df['state']!=1] # unstable
    #print(pd.DataFrame([aux.groupby('name 1')['normalized amplitude in xy-plane'].min(),
    #                    aux.groupby('name 1')['q1'].mean(),
    #                    aux.groupby('name 1')['q2'].mean()
    #                   ]).transpose())
    #my_final = pd.DataFrame([aux.groupby('name 1')['normalized amplitude in xy-plane'].min(),
    #                    aux.groupby('name 1')['q1'].mean(),
    #                    aux.groupby('name 1')['q2'].mean()
    #                   ]).transpose()
    my_final = my_df
    my_final.to_parquet(f'{my_study}/fma.parquet')
else:
    print('Complete first all jobs')
print(my_final)
end = time.time()
print(end - start)
