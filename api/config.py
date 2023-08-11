
import os
from torch import cuda, bfloat16

os.environ["CUDA_VISIBLE_DEVICES"]="0"
class CONFIG:
    model_id = '7b-vi'
    device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
    model_name = "vinai/bartpho-syllable"
