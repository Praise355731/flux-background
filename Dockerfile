FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime
WORKDIR /app
ENV HF_HOME=/runpod-volume/hf
# Install a matching torch and torchvision pair, so the image-processing code can load.
RUN pip install --no-cache-dir torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_r2.py handler.py ./
CMD ["python", "-u", "handler.py"]
