FROM mcr.microsoft.com/devcontainers/miniconda

RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list && apt update && apt install -y terraform

RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

RUN apt-get update

RUN apt-get install dnsutils -y

RUN curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
