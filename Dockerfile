FROM python:latest

COPY . /vtt
WORKDIR /vtt
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["vtt.py"]
