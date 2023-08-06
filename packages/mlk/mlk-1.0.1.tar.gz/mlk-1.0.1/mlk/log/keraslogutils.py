import sys
import tensorflow as tf
import pandas as pd
import autokeras as ak

from swissarmykit.db.mongodb import BaseDocument
from swissarmykit.utils.dateutils import DateUtils
from swissarmykit.utils.loggerutils import LoggerUtils

ann_log = BaseDocument.get_class('meta.ann_log')

class KerasLogUtils:

    @staticmethod
    def log(model: tf.keras.Model, clf: ak.StructuredDataClassifier = None, X=None, loss=0, accuracy=0, duration=0):
        log: LoggerUtils = LoggerUtils.instance()

        data = {
            'duration': str(duration).rsplit('.', 1)[0],
            'loss': loss,
            'accuracy': accuracy,
            'source_code': sys.argv[0],
            'log_file': log.get_log_file(),
            'log_name': log.get_log_name(),

            'input_shape': model.input_shape,
            'output_shape': model.output_shape,
        }

        loss_obj = model.loss.get(model.output_names[0])
        data['loss.name'] = loss_obj.name
        data['loss.reduction'] = loss_obj.reduction

        if clf:
            input = clf.inputs[0]

            data['clf.batch_size'] = input.batch_size
            data['clf.dtype'] = input.dtype.name

            data['clf.name'] = input.name
            data['clf.num_samples'] = input.num_samples
            data['clf.max_trials'] = clf.max_trials
            data['clf.objective'] = clf.objective.name
            data['clf.overwrite'] = clf.overwrite
            data['clf.project_name'] = clf.project_name

            data['clf.column_types'] = input.column_types
            data['clf.column_names'] = input.column_names

        lst = []
        model.summary(print_fn=lambda x: lst.append(x))
        data['summary'] = "\n".join(lst)

        if isinstance(X, pd.DataFrame):
            data['X'] = X.describe().to_dict()

        data['log_tail'] = log.get_tail_log()
        file = sys.argv[0].rsplit('/', 1)[-1]

        ann_log.save_url(DateUtils.get_current_time_for_file(file + ' '),
                         attr={
                             'name': data.get('clf.project_name', ''),
                             'data': data,
                             'description': data.get('summary'),
                             'file': log.get_log_name(),
                         },
                         update_modified_date=True)
