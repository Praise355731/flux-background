FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime
WORKDIR /app
ENV HF_HOME=/runpod-volume/hf
# Remove torchvision and torchaudio. This worker does not use them, and their mismatched builds break the import.
# The check below stops the build if either one is still installed, so a failed removal cannot pass silently.
RUN pip uninstall -y torchvision torchaudio && \
    python -c "import importlib.util,sys; sys.exit(1 if (importlib.util.find_spec('torchvision') or importlib.util.find_spec('torchaudio')) else 0)"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_r2.py handler.py ./
CMD ["python", "-u", "handler.py"]
