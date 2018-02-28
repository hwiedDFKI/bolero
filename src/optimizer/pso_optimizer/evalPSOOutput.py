#!/bin/python
'''
This script transforms the output of the PSO optimizer in pso_best_params.dat to the parameters given to it. Therefore provide the file with the parameter limits as second argument and the target as third. The parameter file should be in the yaml-format:

Parameters:
  - { name: $PARAMETER_NAME, min: 0.0, max: 0.0}

'''
import yaml
import sys
import os
import numpy as np


def saw(val, param_min, param_max):
    param_range = param_max - param_min
    if param_range == 0.0:
        return param_min
    else:
        val = np.mod(np.abs(val), param_range * 2)
        if val > param_range:
            val = param_range * 2 - val
        val += param_min
        return val


if len(sys.argv) >= 3:
    param_path = os.path.abspath(sys.argv[2])
    param_file = yaml.load(open(param_path).read())["Parameters"]
    pso_file = open(sys.argv[1]).read().split("\n")
    pOut = pso_file[2].split(', ')
    if len(param_file) == (len(pOut) - 1):
        out_file = open(os.path.abspath(sys.argv[3]), "w")
        out_file.write("#" + pso_file[0] + "\n")
        for i in range(len(pOut) - 1):
            param_min = param_file[i]["min"]
            param_max = param_file[i]["max"]
            out_file.write(param_file[i]["name"])
            out_file.write(": ")
            out_file.write(str(round(saw(float(pOut[i]),
                           param_min, param_max), 5)) + "\n")
    else:
        print("ERROR: Number of parameters do not match!")
else:
    print("Failed. Usage: python evalPSOOutput.py $pso_best_params.dat\
           $param.yml $output_parameters.yml")
