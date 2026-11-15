FROM python:3.12-slim

# Create a non-root user (UID 1000) as required by Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

WORKDIR $HOME/app

# Install dependencies first for efficient layer caching
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application source code
COPY --chown=user . $HOME/app

EXPOSE 7860

CMD ["gunicorn", "app:server", "--workers", "2", "--threads", "4", "--timeout", "120", "--bind", "0.0.0.0:7860"]

