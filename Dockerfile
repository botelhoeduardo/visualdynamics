FROM stackbrew/debian:jessie
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /visualdynamics
WORKDIR /visualdynamics
RUN python3 -m venv env/
RUN env/bin/pip install pip --upgrade
# One important step that may seem out of place is that I copy in the Python requirements.txt 
# file and install the Python requirements early on in the Dockerfile build process. 
# Installing the Python requirements is a time-consuming process, and I can leverage Docker's 
# build-in caching feature to ensure that Docker only needs to install the requirements if a 
# change is specifically made to the requirements file. If I were push that step further down 
# in the Dockerfile, I'd risk unnecessarily re-installing the Python requirements every time 
# I make an arbitrary change to the code.
COPY requirements.txt requirements.txt
RUN env/bin/pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["visualdynamics.py"]