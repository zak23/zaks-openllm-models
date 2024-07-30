
CONSTANT_YAML = '''
default: 20480
engine_config:
  dtype: half
  enforce_eager: true
  max_model_len: 20480
  model: cognitivecomputations/dolphin-2.9.3-mistral-nemo-12b
extra_labels:
  model_name: cognitivecomputations/dolphin-2.9.3-mistral-nemo-12b
  openllm_alias: 12b
max_tokens: null
maximum: 20480
minimum: 128
project: vllm-chat
service_config:
  name: dolphin2_9_3
  resources:
    gpu: 1
    gpu_type: nvidia-rtx-3090
  traffic:
    timeout: 300
title: Max Tokens
type: integer

'''
