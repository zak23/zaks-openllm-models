
CONSTANT_YAML = '''
default: 28704
engine_config:
  dtype: half
  enforce_eager: true
  max_model_len: 28704
  model: cognitivecomputations/dolphin-2.9.3-mistral-7B-32k
  tensor_parallel_size: 1
extra_labels:
  model_name: cognitivecomputations/dolphin-2.9.3-mistral-7B-32k
  openllm_alias: 7b
max_tokens: null
maximum: 28704
minimum: 128
project: vllm-chat
service_config:
  name: dolphin2_9_3
  resources:
    gpu: 1
    gpu_type: nvidia-rtx-3090
  traffic:
    timeout: 300
  workers: 1
title: Max Tokens
type: integer

'''
