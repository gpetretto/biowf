from biowf.tasks import GenerateStructuresTask, AnalyseTask
from biowf.tasks import GetFromDBTask, SaveToDBTask, ActionTask
from fireworks import Firework, Workflow


def generate_simulation_analysis_loop_wf(n_structures=10, calculation_options=None):

    generate_task = GenerateStructuresTask(n_structures=n_structures,
                                           calculation_options=calculation_options)
    generate_fw = Firework(generate_task, name="Select structures")

    analyse_task = AnalyseTask(n_structures=n_structures)
    analyse_fw = Firework(analyse_task, name="analyse and check", parents=[generate_fw])

    wf = Workflow([generate_fw, analyse_fw], name="Loop workflow")

    return wf


def generate_pipeline_wf(db_data, item_id, fail=False):

    get_fw = Firework(GetFromDBTask(item_id=item_id, db_data=db_data), name="Fetch from DB")

    fws = [get_fw]

    parent = get_fw
    for i in range(5):
        a_fw = Firework(ActionTask(action="action{}".format(i)), parents=parent, name="task {}".format(i))
        parent = a_fw
        fws.append(a_fw)

    if fail:
        a_fw = Firework(ActionTask(action="action5", fail=True), parents=parent, name="task 5")
        parent = a_fw
        fws.append(a_fw)

    save_fw = Firework(SaveToDBTask(item_id=item_id, db_data=db_data), parents=parent, name="Save to DB")
    fws.append(save_fw)

    wf = Workflow(fws, name="Pipeline workflow")

    return wf

