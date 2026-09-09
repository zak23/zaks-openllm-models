
CONSTANT_YAML = '''
engine_config:
  filename: Dolphin3.0-Llama3.1-8B-Q4_K_M.gguf
  max_model_len: 8192
  model: bartowski/Dolphin3.0-Llama3.1-8B-GGUF
  n_ctx: 8192
  n_gpu_layers: -1
extra_labels:
  model_name: bartowski/Dolphin3.0-Llama3.1-8B-GGUF
  openllm_alias: 8b
max_tokens:
  default: 2048
  maximum: 4096
  minimum: 128
  title: Max Tokens
  type: integer
project: llamacpp-chat
service_config:
  name: dolphin3_llama31_8b
  resources:
    gpu: 1
  traffic:
    timeout: 300
  workers: 1

'''
