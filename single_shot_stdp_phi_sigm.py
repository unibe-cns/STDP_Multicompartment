
from util import get_all_save_keys, get_periodic_current, get_inst_backprop, get_phi_spiker, get_dendr_spike_det_dyn_ref, get_fixed_spiker
from helper import do, PeriodicAccumulator, BooleanAccumulator, dump, get_default
import numpy as np
from IPython import embed
import cPickle
from collections import OrderedDict
from simulation import run
import matplotlib.pyplot as plt
import time


def task((repetition_i,p)):

    learn = {}
    learn['eta'] = 1e-3*p["eps"]
    learn['eps'] = p["eps"]
    learn['tau_delta'] = 2.0

    neuron = get_default("neuron")
    neuron["phi"]["function"] = "sigm"
    neuron["phi"]['r_max'] = p["r_max"]
    neuron["phi"]['alpha'] = p["alpha"]
    neuron["phi"]['beta'] = p["beta"]

    my_s = {
        'start': 0.0,
        'end': 300.0,
        'dt': 0.05,
        'pre_spikes': np.array([50.0+p["delta"]]),
        'I_ext': lambda t: 0.0
        }
        
    spikes = np.array([50.0])
    
    seed = int(int(time.time()*1e8)%1e9)
    accs = [PeriodicAccumulator(get_all_save_keys(), interval=10), BooleanAccumulator(['spike', 'dendr_spike', 'pre_spike'])]
    accums = run(my_s, get_fixed_spiker(spikes), get_dendr_spike_det_dyn_ref(p["thresh"],p["tau_ref_0"],p["theta_0"]), accs, seed=seed, learn=learn, neuron=neuron)
        

    dump(accums,p['ident'])

params = OrderedDict()
params["alpha"] = np.linspace(-60.0,-50.0,3)
params["beta"] = np.linspace(0.2,0.7,6)
params["r_max"] = [0.05, 0.1, 0.2, 0.5]
params["thresh"]=[-50]
params["tau_ref_0"]=[10]
params["theta_0"]=[100]
params["eps"] = [1e-3,5e-3]
params["delta"] = [-30,-20,-10,10,20,30]

file_prefix = 'single_shot_stdp_phi_sigm'

do(task, params, file_prefix, prompt=False, withmp=True)