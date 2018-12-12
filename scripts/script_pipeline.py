from fireworks import LaunchPad
from biowf.wf_generators import generate_pipeline_wf

lp = LaunchPad.auto_load()

lp.add_wf(generate_pipeline_wf(item_id="id-149", db_data="localhost"))
# lp.add_wf(generate_pipeline_wf(item_id="id-149", db_data="localhost", preserve_launch_dir=True))
# lp.add_wf(generate_pipeline_wf(item_id="id-149", db_data="localhost", fail=True))