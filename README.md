
# Guide d'installation

    Initialiser Ollama :

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

```

# Configurer l'environnement :
```bash
cp .env.example .env```


# Editez .env avec vos clés API

# Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancer le serveur :

```bash
python mcp_server.py

```
##   Utiliser l'agent en CLI :

```bash
python agent.py "Votre question ici"
```