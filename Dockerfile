FROM python:3.11-slim

RUN mkdir -p /opt/ml

# Set working directory
WORKDIR /opt/ml/

# Set PATH to use virtual environment
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/ml/.venv/bin:$PATH"

COPY pyproject.toml uv.lock /opt/ml/


RUN apt-get -y update

# Install system dependencies (if needed)
RUN apt-get install -y --no-install-recommends build-essential libgomp1 nginx wget

# Install UV - faster Python package installer
RUN pip install --no-cache-dir uv

RUN uv venv

# RUN source .venv/bin/activate

RUN . .venv/bin/activate

RUN uv sync --frozen

# RUN .venv/bin/uv

#RUN uv add -r requirements.txt

COPY ./ml-base/ /opt/ml/ml-base

# Create non-root user for security
RUN chmod +x /opt/ml/* 

# Make port 8000 available (if your app exposes a web interface)
EXPOSE 8000


CMD ["python", "ml-base/train.py"]
