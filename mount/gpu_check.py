import torch

gpu = torch.cuda.is_available()
print(gpu)