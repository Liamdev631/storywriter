# app/Dockerfile

FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    openssh-client \
    openssh-server

RUN rm -rf /var/lib/apt/lists/*

ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN}

RUN git config --global url."https://x-access-token:${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"

RUN git clone https://github.com/Liamdev631/storywriter.git .

RUN bash -c 'echo -e "\
[general]\n\
email = \"aistoryforgeapp@gmail.com\"\n\
" > /root/.streamlit/credentials.toml'

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]