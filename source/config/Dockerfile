FROM python:latest

COPY . /
EXPOSE 50004
WORKDIR /core
RUN python3 -m pip install -r requirements.txt
RUN mv app/main.py ./main.py
CMD ["python3", "main.py"]