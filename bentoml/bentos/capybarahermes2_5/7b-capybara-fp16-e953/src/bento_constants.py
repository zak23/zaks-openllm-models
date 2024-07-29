
CONSTANT_YAML = '''
chat_template: mistral-instruct
engine_config:
  dtype: half
  enforce_eager: true
  max_model_len: 1024
  model: argilla/CapybaraHermes-2.5-Mistral-7B
extra_labels:
  model_name: argilla/CapybaraHermes-2.5-Mistral-7Bv0.1
  openllm_alias: 7b
project: vllm-chat
service_config:
  name: capybarahermes2_5
  resources:
    gpu: 1
    gpu_type: nvidia-rtx-3090
  traffic:
    timeout: 300

'''
