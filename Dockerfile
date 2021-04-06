FROM jjanzic/docker-python3-opencv

LABEL maintainer=tony

RUN mkdir -p /opt/project
WORKDIR /opt/project

COPY requirements.txt /opt/project.txt
RUN pip install -r /opt/project.txt

COPY ./ /opt/project

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8080"]
