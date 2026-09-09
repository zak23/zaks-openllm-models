# Dolphin3 local worker

This repository provides `dolphin3:8b-q4-k-m`, a llama.cpp Bento for
`bartowski/Dolphin3.0-Llama3.1-8B-GGUF` on an NVIDIA GPU with 8 GB of VRAM.
It downloads `Dolphin3.0-Llama3.1-8B-Q4_K_M.gguf` on first start.

## Configuration

The recipe uses one GPU, full layer offload (`n_gpu_layers: -1`), an 8,192-token
context, and a 4,096-token maximum response. It is intended to be the sole
resident 8B model on the GPU; do not run a second substantial model alongside it.

The llama.cpp project is Linux/CUDA-only. Its Bento environment builds
`llama-cpp-python` with `-DLLAMA_CUBLAS=on`.

## Build or update the model repository

Prerequisites: Git, Python, a supported BentoML build environment, and CUDA
tooling on the target build host. Accept any upstream model licence or access
terms before deploying if the Hugging Face account prompts for them.

```bash
git clone https://github.com/<ACCOUNT>/<MODEL_REPOSITORY>.git
cd <MODEL_REPOSITORY>
git pull --ff-only
cd src
BENTOML_HOME="$(cd .. && pwd)/bentoml" python3 make.py "dolphin3:8b-q4-k-m"
cd ..
git add src/recipe.yaml src/llamacpp-chat bentoml/bentos/dolphin3_llama31_8b
git commit -m "add Dolphin3 8B Q4_K_M worker"
git push
```

The generated Bento tag is versioned from the recipe and source hash. Do not
hand-edit its generated contents.

## Register and serve

On the OpenLLM host, register this repository once (or refresh an existing
registration), then start the generated model alias:

```bash
openllm repo add <REPOSITORY_ALIAS> https://github.com/<ACCOUNT>/<MODEL_REPOSITORY>.git
openllm repo update
openllm hello
openllm serve dolphin3_llama31_8b:8b
```

The first start downloads the GGUF and can take several minutes. Confirm the
model starts without CPU fallback and that the OpenAI-compatible `/v1` routes
are available before adding a systemd unit.

## Optional systemd service

Create `/etc/systemd/system/openllm-dolphin3.service` with placeholders suited
to the target host:

```ini
[Unit]
Description=OpenLLM Dolphin3 local worker
After=network.target

[Service]
Type=simple
User=<SERVICE_USER>
Group=<SERVICE_GROUP>
WorkingDirectory=<MODEL_REPOSITORY_PATH>
ExecStart=<OPENLLM_BIN> serve dolphin3_llama31_8b:8b
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now openllm-dolphin3
sudo systemctl status openllm-dolphin3
```

## Verification and rollback

- Check `openllm hello` lists `dolphin3_llama31_8b:8b`.
- Send both streaming and non-streaming requests to the service's `/v1/chat/completions` endpoint.
- Monitor GPU memory while loading and serving at the 8K context limit.
- To roll back, stop/disable `openllm-dolphin3` and start the previously known-good model; keep the previous Bento directory until the replacement has been validated.

## Source notes

This runbook consolidates the former BentoML/OpenLLM setup, custom model
repository, update-helper, and service notes from the companion knowledge base.
Those notes contain historical dependency and path examples and should not be
used as the current deployment procedure.
