import torch


def hf_device():
    return 0 if torch.cuda.is_available() else -1