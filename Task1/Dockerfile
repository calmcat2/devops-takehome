FROM python:3.7-slim

LABEL description="A Python application with PostgreSQL and Google Cloud SDK"

# Set env variable MODE to be the value of argument mode 
ARG mode
ENV MODE=$mode 

# Install psql-13 
RUN apt-get update &&\
    apt-get install -y curl ca-certificates apt-transport-https gnupg &&\
    install -d /usr/share/postgresql-common/pgdg &&\
    curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc &&\
    sh -c 'echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list' &&\
    apt-get update && apt-get install -y postgresql-13 &&\
# Install Gcloud SDK
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - &&\
    apt-get update && apt-get install -y google-cloud-sdk &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install packages in requirements.txt
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app

# Container should sleep indefinitely
CMD ["sleep","inf"]