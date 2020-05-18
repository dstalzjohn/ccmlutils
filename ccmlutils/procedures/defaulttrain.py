from typing import Optional, Callable

from keras import Model
from keras.losses import Loss
from keras.optimizers import Optimizer


def fit_generator(model: Callable[[], Model], train_set, validation_set, epochs: int,
                  optimizer: Optimizer,
                  loss: Loss,
                  callbacks=None,
                  steps_per_epoch: Optional[int] = None,
                  validation_steps: Optional[int] = None,
                  ):

    model = model()
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

    history = model.fit_generator(train_set,
                                  epochs=epochs,
                                  validation_data=validation_set,
                                  callbacks=callbacks,
                                  validation_steps=validation_steps,
                                  steps_per_epoch=steps_per_epoch)

    return dict(history=history)
