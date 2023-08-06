r"""
REGenerator class for sample generating 
"""
__all__ = ["REGenerator"]
from .generator import Generator
from tqdm import tqdm
from ...common import logger
from ...input_layer.dataset import Dataset
from ...common.settings import TASK_TRANSFORMATION_PATH, \
    ALLOWED_TRANSFORMATIONS, TASK_SUBPOPULATION_PATH, ALLOWED_SUBPOPULATIONS


class REGenerator(Generator):
    r"""
    generate RE sample

    """
    def __init__(
        self,
        task='RE',
        max_trans=1,
        fields='x',
        transformation_methods=None,
        transformation_config=None,
        return_unk=True,
        subpopulation_methods=None,
        subpopulation_config=None,
        attack_methods=None,
        validate_methods=None
    ):
        super().__init__(
            task=task,
            max_trans=max_trans,
            fields=fields,
            transformation_methods=transformation_methods,
            transformation_config=transformation_config,
            return_unk=return_unk,
            subpopulation_methods=subpopulation_methods,
            subpopulation_config=subpopulation_config,
            attack_methods=attack_methods,
            validate_methods=validate_methods
        )

    def generate_by_transformations(self, dataset, **kwargs):
        r"""
        Returns a list of all possible transformed samples for "dataset".

        :param ~TextRobustness.dataset.Dataset dataset: the original dataset
            ready for transformation or subpopulation
        :return: yield transformed samples + transformation name string.
        """
        self.prepare(dataset)
        dataset.init_iter()
        transform_objs = self._get_flint_objs(
            self.transform_methods,
            TASK_TRANSFORMATION_PATH,
            ALLOWED_TRANSFORMATIONS)

        for obj_id, trans_obj in enumerate(transform_objs):
            logger.info('******Start {0}!******'.format(trans_obj))
            generated_samples = dataset.new_dataset()
            original_samples = dataset.new_dataset()
            # initialize current index of dataset
            dataset.init_iter()

            for index in tqdm(range(len(dataset))):
                concat_samples = dataset[index + 1: index + 3]
                sample = dataset[index]
                # default return list of samples
                trans_rst = trans_obj.transform(sample,
                                                n=self.max_trans,
                                                field=self.fields,
                                                concat_samples=concat_samples)
                # default return list of samples
                if trans_rst:
                    generated_samples.extend(trans_rst)
                    original_samples.append(sample)

            yield original_samples, generated_samples, trans_obj.__repr__()
            logger.info('******Finish {0}!******'.format(trans_obj))


