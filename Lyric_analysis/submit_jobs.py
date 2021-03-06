# https://wikispaces.psu.edu/display/CyberLAMP/System+Information
# In general 1 GPU per node.

import os
import numpy as np
import itertools

genres = ['country']
n_layers = [1]
lstm_size = [128,256,512]
batch_size = [256,512]
dropout = [0.2,0.6,0.9]

params = list(itertools.product(*[genres, n_layers, lstm_size, batch_size, dropout]))

submit_jobs = 1
jobs_dir = 'jobs'
counter = 0
for genre,nl,lstms,bs,drop in params:
    output_name = 'train_%s_nl%d_size%d_bs%d_drop%.2f'%(genre,nl,lstms,bs,drop)
    job_name = '%s.pbs'%output_name
    with open('%s/%s'%(jobs_dir,job_name), 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('#PBS -l nodes=1:gpus=1\n')
        f.write('#PBS -l walltime=48:00:00\n')
        f.write('#PBS -l pmem=12gb\n')
        f.write('#PBS -A cyberlamp -l qos=cl_open\n')
        f.write('#PBS -j oe\n')
        f.write('cd $PBS_O_WORKDIR\n')
        f.write('module load python/3.3.2\n')
        f.write('export PATH="/storage/work/ajs725/conda/install/bin:$PATH"\n\n')
        f.write('CUDA_VISIBLE_DEVICES=0 python train_lstm_char.py %s %d %d %d %f > output/%s.txt'%(genre,nl,lstms,bs,drop,output_name))
    f.close()

    if submit_jobs == 1:
        os.system('mv %s/%s %s'%(jobs_dir,job_name, job_name))
        os.system('qsub %s'%job_name)
        os.system('mv %s %s/%s'%(job_name,jobs_dir,job_name))
        counter += 1
