import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))

import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
