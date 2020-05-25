from typing import Optional, Callable

from tensorflow.keras.losses import Loss
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.utils import Sequence


def fit_generator(model: Callable[[], Model], train_set, validation_set, epochs: int,
                  optimizer: Optimizer,
                  loss: Loss,
                  callbacks=None,
                  steps_per_epoch: Optional[int] = None,
                  validation_steps: Optional[int] = None,
                  ):

    model = model()
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    # This callback is only temporary till issue in tf.keras is fixed where
    # Sequence.on_epoch_end() is not called correctly
    cb = DataSetOnEndCallback(train_set)
    if callbacks is None:
        callbacks = [cb]
    else:
        callbacks.append(cb)
    history = model.fit_generator(train_set,
                                  epochs=epochs,
                                  validation_data=validation_set,
                                  callbacks=callbacks,
                                  validation_steps=validation_steps,
                                  steps_per_epoch=steps_per_epoch)

    return dict(history=history.history)


class DataSetOnEndCallback(Callback):

    def __init__(self, dataset: Sequence):
        super().__init__()
        self.dataset = dataset

    def on_epoch_end(self, epoch, logs=None):
        self.dataset.on_epoch_end()
