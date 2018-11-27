FROM stackbrew/debian:jessie
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /visualdynamics
WORKDIR /visualdynamics
RUN venv/bin/pip install pip --upgrade
RUN venv/bin/pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["visualdynamics.py"]