from sakura.ml.epoch import range
import torch


class SakuraTrainer:
    def __init__(self,
                 model,
                 optimizer,
                 scheduler,
                 metrics,
                 epochs,
                 model_path,
                 checkpoint_path,
                 device="cpu",
                 device_test="cpu"):
        self._model = model
        self._optimizer = optimizer
        self._scheduler = scheduler
        self._metrics = metrics
        self._epochs = range(0, epochs)
        self._model_path = model_path
        self._checkpoint_path = checkpoint_path
        self._device = device
        self._device_test = device_test

    def run(self, train_loader, test_loader):
        raise NotImplementedError

    def train(self, loader):
        raise NotImplementedError

    def test(self, loader):
        raise NotImplementedError

    def update(self, current, best, loader):
        raise NotImplemented
