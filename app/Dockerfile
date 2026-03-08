# 1. Base Imagem: Usamos a versão 'slim' (enxuta) do Debian. 
# Imagens menores significam deploys mais rápidos e menos vulnerabilidades de segurança.
FROM python:3.11-slim

# 2. Variáveis de Ambiente Críticas para Python no Docker
# Impede a criação de arquivos .pyc inúteis no container
ENV PYTHONDONTWRITEBYTECODE=1 
# Força o log a aparecer no terminal instantaneamente (vital para debug)
ENV PYTHONUNBUFFERED=1

# 3. Diretório de Trabalho
WORKDIR /app

# 4. Dependências do Sistema Operacional
# O driver asyncpg (PostgreSQL) precisa de compiladores em C para ser instalado.
# Instalamos, usamos e depois limpamos o cache do apt-get para manter a imagem leve.
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. O Truque do Cache de Camada (Layer Caching)
# Copiamos APENAS o requirements.txt primeiro. Por que? 
# O Docker faz cache de cada linha. Se você alterar seu código Python, mas não instalar 
# bibliotecas novas, o Docker pula a instalação pesada do pip e o build leva 2 segundos.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o resto do projeto
COPY . .

# 7. Boas Práticas de Segurança (Não rode como Root!)
# Por padrão, o Docker roda tudo como administrador (root). Se a API for invadida, 
# o hacker ganha controle total. Criamos um usuário restrito para rodar a aplicação.
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# 8. Porta exposta
EXPOSE 8000

# 9. Comando de inicialização padrão (FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]