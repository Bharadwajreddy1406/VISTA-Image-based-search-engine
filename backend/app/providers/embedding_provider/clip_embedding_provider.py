from abc import ABC

from io import BytesIO

import torch

from PIL import Image

from transformers import (
    CLIPModel,
    CLIPProcessor
)

from app.core.settings import settings
from .base_embedding_provider import BaseEmbeddingProvider


class CLIPEmbeddingProvider(BaseEmbeddingProvider):

    def __init__(self):

        self.model_name = settings.EMBEDDING_MODEL_NAME
        self.device = self._resolve_device(settings.EMBEDDING_DEVICE)

        self.initialize_model_connection()

    def _resolve_device(self, device_setting: str) -> torch.device:
        requested = (device_setting or "cpu").strip().lower()

        if requested in {"cuda", "gpu", "cuda:0"}:
            if torch.cuda.is_available():
                return torch.device("cuda")
            print(
                f"WARNING: CUDA requested in EMBEDDING_DEVICE={device_setting} "
                "but not available. Falling back to CPU."
            )
            return torch.device("cpu")

        if requested == "cpu":
            return torch.device("cpu")

        try:
            return torch.device(requested)
        except Exception:
            print(
                f"WARNING: Invalid EMBEDDING_DEVICE={device_setting}. "
                "Falling back to CPU."
            )
            return torch.device("cpu")

    def initialize_model_connection(self):

        self.model = CLIPModel.from_pretrained(
            self.model_name
        )

        self.processor = CLIPProcessor.from_pretrained(
            self.model_name
        )

        self.model.to(self.device)

        self.model.eval()

        print(
            f"Loaded CLIP model "
            f"'{self.model_name}' "
            f"on {self.device}"
        )

    async def get_embedding(
        self,
        image_bytes: bytes
    ) -> list[float]:

        image = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            output = self.model.get_image_features(
                **inputs
            )

        embedding = output.pooler_output

        embedding = (
            embedding /
            embedding.norm(
                dim=-1,
                keepdim=True
            )
        )

        return (
            embedding
            .squeeze()
            .cpu()
            .tolist()
        )

    def close_model_connection(self):

        del self.model
        del self.processor

        if torch.cuda.is_available():
            torch.cuda.empty_cache()