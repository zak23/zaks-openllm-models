
CONSTANT_YAML = '''
engine_config:
  dtype: half
  max_model_len: 4096
  model: ReadyArt/The-Omega-Directive-M-8B-v1.0
  trust_remote_code: true
project: vllm-chat
service_config:
  name: mistral
  resources:
    gpu: 1
    gpu_type: nvidia-rtx-3090
  traffic:
    timeout: 300
  workers: 1

'''
