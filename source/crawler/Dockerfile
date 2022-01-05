FROM python:latest

COPY /core/app /app
COPY /core/requirements.txt /
RUN python3 -m pip install -r requirements.txt
RUN mv app/main.py ./main.py
CMD ["python3", "main.py"]