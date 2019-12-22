FROM python:latest
RUN mkdir setup
WORKDIR setup
COPY ./requirements.txt setup/requirements.txt
RUN pip install -r setup/requirements.txt
#EXPOSE 8000
