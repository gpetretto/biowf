import time
import random
from fireworks import FiretaskBase, FWAction, Firework
from fireworks.utilities.fw_utilities import explicit_serialize
from biowf.utils import get_logger

logger = get_logger(__name__)


@explicit_serialize
class RunMdTask(FiretaskBase):

    required_params = ["structure"]

    def run_task(self, fw_spec):
        logger.info("Running MD calculation on structure {}".format(self.get("structure")))
        time.sleep(0)

        # return FWAction(update_spec={"_push": {"md_result": {self.get("structure"): random.random()}})
        return FWAction(mod_spec={"_set": {"md_results->structure{}".format(self.get("structure")): random.random()}})


@explicit_serialize
class GenerateStructuresTask(FiretaskBase):

    required_params = ["n_structures"]

    def run_task(self, fw_spec):

        structures = self.generate_structures()

        fws = []

        for s in structures:
            fws.append(Firework(RunMdTask(structure=s), name="run_md_{}".format(s)))

        return FWAction(detours=fws)

    def generate_structures(self):
        return range(self["n_structures"])


@explicit_serialize
class AnalyseTask(FiretaskBase):

    required_params = ["n_structures"]

    def run_task(self, fw_spec):

        results = fw_spec.get("md_results")

        logger.info("Results from previous calculations: {}".format(results))

        success = self.process_results(results, fw_spec)

        if success:
            logger.info("Saving to DB")
            self.write_to_db()
        else:
            logger.info("Generating new set of calculations")
            from biowf.wf_generators import generate_simulation_analysis_loop
            new_wf = generate_simulation_analysis_loop(n_structures=self.get("n_structures"))
            new_wf.fws[-1].spec["success"] = True
            return FWAction(detours=new_wf)

    def process_results(self, results, fw_spec):
        return fw_spec.get("success", False)

    def write_to_db(self):
        pass


@explicit_serialize
class GetFromDBTask(FiretaskBase):

    required_params = ["item_id", "db_data"]

    def run_task(self, fw_spec):
        logger.info("Getting item {} from {}".format(self.get("item_id"), self.get("db_data")))
        item = self.get_from_db()

        return FWAction(update_spec={"item_to_process": item})

    def get_from_db(self):
        return "item-{}".format(self.get("item_id"))


@explicit_serialize
class SaveToDBTask(FiretaskBase):
    required_params = ["item_id"]

    def run_task(self, fw_spec):
        item = fw_spec.get("item_to_process")
        logger.info("Saving item {} to {}".format(item, self.get("db_data")))
        self.save_to_db()

    def save_to_db(self):
        pass


@explicit_serialize
class ActionTask(FiretaskBase):
    required_params = ["action"]

    def run_task(self, fw_spec):
        item = fw_spec.get("item_to_process")
        logger.info("processing item {} with action: {}".format(item, self.get("action")))
        new_item = self.process_item(item)

        return FWAction(update_spec={"item_to_process": new_item})

    def process_item(self, item):
        if self.get("fail", False):
            raise RuntimeError("Error while processing item {}".format(item))

        return item