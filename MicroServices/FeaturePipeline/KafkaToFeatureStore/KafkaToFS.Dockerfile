#Complete Heavy Builder Image to Actually Build the Virtual Env with Complete Docker Image
FROM python:3.11-bookworm as Builder

#Setting Deterministic Environment Variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

#Optional Instead of canonical pip install poetry, we are going to remove Cache later on anyways, but we might need it now.
#RUN pip install --no-cache-dir --upgrade pip \
#    && pip install --no-cache-dir poetry

#Installing Specific Poetry Version
RUN pip install poetry==1.8.3

WORKDIR /app

#Copying Only Necessary Files
COPY pyproject.toml poetry.lock ./

#Adding README or Poetry will complain
RUN touch README.md

#Installing only the Virtual Environment with Dependencies and not the Project, then Removing Cache
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

#Slim Runtime Docker Image, used to just run the code provided its Virtual Environment Built and Passed by the Builder Image
#Here, we don't even need Poetry installed, so we are passing the Virtual Environment, Installing the Project (Optional) and then Removing Poetry
FROM python:3.11-slim-bookworm as Runtime

#Setting up the Venv Location and adding it to PATH
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"		

WORKDIR /app

#Copying the Venv from Builder Image at VIRTUAL_ENV Location to Runtime Image at VIRTUAL_ENV Location
COPY --from=Builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

#Copying Poetry files to actually Install the Project
COPY pyproject.toml poetry.lock /app/

#We don't need Poetry in runtime image, but might be worth it to reinstall it as we built the Virtual Env in our Builder Image, passed only the Venv Specs and Files to our Runtime
#However, if you need to Install Specific Script or anything Like that, you'll want to make sure you are installing the Project in the Runtime Image.
RUN pip install poetry==1.8.3 && cd /app && poetry install --no-cache --without dev && pip uninstall poetry -y

#Copying Actual Codebase
COPY . /app

ENTRYPOINT ["python", "source/KafkaToFSQuixStreamsApp.py"]

#DOCKER_BUILDKIT=1 docker build --target=Runtime -t kafkatofs ./MicroServices/FeaturePipeline/KafkaToFeatureStore -f ./MicroServices/FeaturePipeline/KafkaToFeatureStore/KafkaToFS.Dockerfile
#docker run --network redpanda-network --name kafkatofs -d -it kafkatofs