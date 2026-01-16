import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from open_webui.constants import ERROR_MESSAGES
from open_webui.env import SRC_LOG_LEVELS
from open_webui.utils.auth import get_admin_user, get_verified_user

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["OLLAMA"])

router = APIRouter()


class GenerateEmbeddingsForm(BaseModel):
    model: str
    input: Optional[list[Any] | Any] = None
    prompt: Optional[str] = None
    options: Optional[dict[str, Any]] = None
    truncate: Optional[bool] = None
    keep_alive: Optional[str] = None


class OllamaConfigForm(BaseModel):
    ENABLE_OLLAMA_API: Optional[bool] = None
    OLLAMA_BASE_URLS: list[str]
    OLLAMA_API_CONFIGS: dict


def _raise_ollama_disabled() -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.OLLAMA_API_DISABLED,
    )


def _get_config_payload(request: Request) -> dict:
    config = getattr(request.app.state, "config", None)
    if not config:
        return {
            "ENABLE_OLLAMA_API": False,
            "OLLAMA_BASE_URLS": [],
            "OLLAMA_API_CONFIGS": {},
        }

    return {
        "ENABLE_OLLAMA_API": config.ENABLE_OLLAMA_API,
        "OLLAMA_BASE_URLS": config.OLLAMA_BASE_URLS,
        "OLLAMA_API_CONFIGS": config.OLLAMA_API_CONFIGS,
    }


@router.get("/config")
async def get_config(request: Request, user=Depends(get_admin_user)):
    return _get_config_payload(request)


@router.post("/config/update")
async def update_config(
    request: Request, form_data: OllamaConfigForm, user=Depends(get_admin_user)
):
    _raise_ollama_disabled()


@router.get("/urls")
async def get_urls(request: Request, user=Depends(get_admin_user)):
    return {"OLLAMA_BASE_URLS": _get_config_payload(request)["OLLAMA_BASE_URLS"]}


@router.post("/urls/update")
async def update_urls(request: Request, user=Depends(get_admin_user)):
    _raise_ollama_disabled()


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
async def disabled_route(request: Request, user=Depends(get_verified_user)):
    _raise_ollama_disabled()


async def get_all_models(request: Request, user=None) -> dict:
    if getattr(request.app.state, "config", None) and request.app.state.config.ENABLE_OLLAMA_API:
        log.warning("Ollama API is enabled but not available in lite build.")
    return {"models": []}


@router.post("/api/chat")
async def generate_chat_completion(
    request: Request,
    form_data: dict,
    user=Depends(get_verified_user),
    bypass_filter: Optional[bool] = False,
):
    _raise_ollama_disabled()


@router.post("/api/embeddings")
async def embeddings(
    request: Request,
    form_data: GenerateEmbeddingsForm,
    user=Depends(get_verified_user),
):
    _raise_ollama_disabled()
