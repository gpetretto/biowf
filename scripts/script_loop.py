from fireworks import LaunchPad
from biowf.wf_generators import generate_simulation_analysis_loop

lp = LaunchPad.auto_load()

lp.add_wf(generate_simulation_analysis_loop(n_structures=10))