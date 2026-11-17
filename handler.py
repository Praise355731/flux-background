"""
BACKGROUND WORKER (FLUX.1 [schnell], Apache 2.0).
Input:  {"input": {"prompt": "a busy street in the morning", "job_id": "...", "width": 832, "height": 480}}
Output: {"image_url": "https://..."}
"""
import os
import tempfile

import runpod
import torch
from diffusers import FluxPipeline

from common_r2 import upload_to_r2

MODEL_ID = "black-forest-labs/FLUX.1-schnell"
pipe = FluxPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()


def handler(job):
    inp = job.get("input", {})
    prompt = (inp.get("prompt") or "").strip()
    job_id = inp.get("job_id") or "bg"
    width = int(inp.get("width", 832))
    height = int(inp.get("height", 480))
    if not prompt:
        return {"error": "Send a prompt describing the place."}
    try:
        image = pipe(
            prompt,
            width=width,
            height=height,
            guidance_scale=0.0,        # schnell is trained to run without guidance
            num_inference_steps=4,     # schnell is fast with 1 to 4 steps
            max_sequence_length=256,
            generator=torch.Generator("cpu").manual_seed(0),
        ).images[0]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "background.png")
            image.save(path)
            url = upload_to_r2(path, f"backgrounds/{job_id}.png", "image/png")
        return {"image_url": url}
    except Exception as e:
        return {"error": f"Background failed: {e}"}


runpod.serverless.start({"handler": handler})
