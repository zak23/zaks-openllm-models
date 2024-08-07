
CONSTANT_YAML = '''
engine_config:
  dtype: half
  enforce_eager: true
  max_model_len: 28704
  model: argilla/CapybaraHermes-2.5-Mistral-7B
  tensor_parallel_size: 2
extra_labels:
  model_name: argilla/CapybaraHermes-2.5-Mistral-7Bv0.1
  openllm_alias: 7b
max_tokens:
  default: 28704
  maximum: 28704
  minimum: 128
  title: Max Tokens
  type: integer
project: vllm-chat
service_config:
  name: capybarahermes2_5
  resources:
    gpu: 2
    gpu_type: nvidia-rtx-3090
  traffic:
    timeout: 300
  workers: 1

'''
