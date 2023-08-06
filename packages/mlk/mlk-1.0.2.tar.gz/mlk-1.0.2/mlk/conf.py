
import os
import tensorflow as tf
from swissarmykit.lib.core import Singleton, Config
from swissarmykit.lib.inspector import Inspector

from mlk.mlk.lib.core import Config as mlkConfig

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


@Singleton
class MLConfig(mlkConfig):

    def __init__(self):
        super().__init__()


mlConfig: MLConfig = MLConfig.instance()


if __name__ == '__main__':
    print(mlConfig.info())