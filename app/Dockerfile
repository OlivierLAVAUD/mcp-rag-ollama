# Étape de construction
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install --user -r requirements.txt

# Étape finale
FROM python:3.9-slim

WORKDIR /app

# Copier les dépendances installées
COPY --from=builder /root/.local /root/.local
COPY . .

# Ollama nécessite certaines dépendances système
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libssl-dev \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Installer Ollama
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama && \
    chmod +x /usr/bin/ollama

# Ajouter .local/bin au PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Port exposé (si API)
EXPOSE 8000

# Commande par défaut (peut être override dans compose)
CMD ["python", "main.py"]