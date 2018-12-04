from fireworks import LaunchPad
from biowf.wf_generators import generate_simulation_analysis_loop_wf

lp = LaunchPad.auto_load()

lp.add_wf(generate_simulation_analysis_loop_wf(n_structures=10))