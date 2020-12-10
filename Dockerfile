FROM python:3.6-slim

RUN apt-get update
ADD req.txt /
RUN pip install -r req.txt
ADD slots slots/
EXPOSE 8000
WORKDIR /slots
CMD python3 manage.py runserver 0.0.0.0:8000
