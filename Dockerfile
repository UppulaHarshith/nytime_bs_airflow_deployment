
#FROM ubuntu:16.04
#RUN apt-get update && apt-get install -y curl
#RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
#RUN chmod +x /usr/local/bin/docker-compose


FROM ubuntu:latest
#FROM --platform=linux/amd64 node:14

COPY --from=library/docker:latest /usr/local/bin/docker /usr/local/bin/docker
COPY --from=docker/compose:1.23.0 /usr/local/bin/docker-compose /usr/local/bin/docker-compose
COPY . /app

#RUN curl -L "https://github.com/docker/compose/releases/download/2.9.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
#RUN curl -L "https://github.com/docker/compose/releases/download/v2.9.0/docker-compose-linux-aarch64" -o /usr/local/bin/docker-compose
#RUN apt-get -y install docker-compose=1.29.2
#RUN chmod +x /usr/local/bin/docker-compose 
RUN mkdir /compose
RUN apt-get update && apt-get install -y curl
RUN ln -s docker-compose.yaml /compose/docker-compose.yaml
#RUN --mount=type=bind,target=/var/run/docker.sock,source=/var/run/docker.sock docker-compose -v
RUN curl -LfO https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml
#RUN apt-get -y install vim
RUN export DOCKER_BUILDKIT=1
RUN echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" >.env
ENV AIRFLOW_UID=0
ENV AIRFLOW_GID=0   
COPY ./dags/ ~/dags/