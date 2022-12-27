ARG DOCKER_REGISTRY=index.docker.io
# =============================================================================
# base - Python e lista de dependências
# =============================================================================
FROM $DOCKER_REGISTRY/python:3.8 as base

WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings

RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile /code/
COPY Pipfile.lock /code/

# =============================================================================
# development - Instala dependências de dev e copia o código fonte
# =============================================================================
FROM base as dev
RUN pipenv install --system --deploy --dev
COPY . /code/

# =============================================================================
# DevServer - Roda o servidor da API em modo de desenvolvimento
# =============================================================================
FROM dev as DevServer
ENV DEBUG true
ENV ALLOWED_HOSTS *
RUN chmod +x /code/*.sh

CMD ["sh", "start-dev.sh"]

# =============================================================================
# ORION - Roda o servidor Prefect ORION
# =============================================================================
FROM dev as orion

CMD ["prefect", "orion", "start"]

# =============================================================================
# AGENT - Roda o Prefect AGENT
# =============================================================================
FROM dev as agent

ENV PYTHONPATH /code
ENV PREFECT_AGENT_PROCESS true
ENV DJANGO_SETTINGS_MODULE config.settings

CMD ["sh", "start-prefect.sh"]
