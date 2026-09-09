import bentoml
from annotated_types import Ge, Le
from typing_extensions import Annotated
from llama_cpp import Llama
from typing import AsyncGenerator, Optional
from bento_constants import CONSTANT_YAML
import yaml
import fastapi
import fastapi.staticfiles
import os
from fastapi.responses import FileResponse
from typing_extensions import Literal
import sys
import pydantic
from bentoml.io import SSE
import json

CONSTANTS = yaml.safe_load(CONSTANT_YAML)

ENGINE_CONFIG = CONSTANTS["engine_config"]
SERVICE_CONFIG = CONSTANTS["service_config"]
MAX_OUTPUT_TOKENS = CONSTANTS.get("max_tokens", {}).get(
    "maximum", ENGINE_CONFIG["max_model_len"]
)
DEFAULT_OUTPUT_TOKENS = CONSTANTS.get("max_tokens", {}).get(
    "default", MAX_OUTPUT_TOKENS
)
OVERRIDE_CHAT_TEMPLATE = CONSTANTS.get("chat_template")

class Message(pydantic.BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

STATIC_DIR = os.path.join(os.path.dirname(__file__), "ui")

static_app = fastapi.FastAPI()
ui_app = fastapi.FastAPI()
openai_api_app = fastapi.FastAPI()

@openai_api_app.get("/models")
async def show_available_models():
    # Return the available models
    return {
        "data":[
            {
                "id": ENGINE_CONFIG["model"],
                "object": "model",
                "created": 1686935002,
                "owned_by": "bentoml",
            }
        ]
    }

ui_app.mount(
    "/static", fastapi.staticfiles.StaticFiles(directory=STATIC_DIR), name="static"
)


@ui_app.get("/")
async def serve_chat_html():
    return FileResponse(os.path.join(STATIC_DIR, "chat.html"))


@ui_app.get("/{full_path:path}")
async def catch_all(full_path: str):
    file_path = os.path.join(STATIC_DIR, full_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(STATIC_DIR, "chat.html"))


# special handling for prometheus_client of bentoml
if "prometheus_client" in sys.modules:
    sys.modules.pop("prometheus_client")


@bentoml.mount_asgi_app(ui_app, path="/chat")
@bentoml.mount_asgi_app(openai_api_app, path="/v1")
@bentoml.service(**SERVICE_CONFIG)
class LlamaCppChat:

    def __init__(self) -> None:
        self.llm = Llama.from_pretrained(
            repo_id=ENGINE_CONFIG["model"],
            filename=ENGINE_CONFIG.get("filename", "*q4.gguf"),
            n_gpu_layers=ENGINE_CONFIG.get("n_gpu_layers", 0),
            n_ctx=ENGINE_CONFIG.get("n_ctx", ENGINE_CONFIG["max_model_len"]),
            verbose=False,
        )

    @bentoml.api(route="/v1/chat/completions")
    async def chat_completions(
        self,
        messages: list[Message] = [
            {"role": "user", "content": "What is the meaning of life?"}
        ],
        model: str = ENGINE_CONFIG["model"],
        max_tokens: Annotated[
            int,
            Ge(128),
            Le(MAX_OUTPUT_TOKENS),
        ] = DEFAULT_OUTPUT_TOKENS,
        stop: Optional[list[str]] = None,
        stream: Optional[bool] = True,
        temperature: Optional[float] = 0,
        top_p: Optional[float] = 1.0,
        frequency_penalty: Optional[float] = 0.0,
    ) -> AsyncGenerator[str, None]:
        """
        Chat API that takes in a list of messages and returns a response
        """
        try:
            response = self.llm.create_chat_completion(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                stream=stream,
                stop=stop,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
            )
            if not stream:
                yield json.dumps(response)
                return

            for chunk in response:
                try:
                    json_srt = json.dumps(chunk)
                    sse = SSE(data=json_srt)
                    yield sse.marshal()
                except Exception as e:
                    print(e)
                    yield SSE(data=str(e)).marshal()

            yield SSE(data="[DONE]").marshal()
        except Exception as e:
            yield SSE(data=str(e)).marshal()
            yield SSE(data="[DONE]").marshal()
