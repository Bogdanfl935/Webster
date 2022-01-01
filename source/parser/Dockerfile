FROM python:latest

COPY . /
COPY ./init/vars.env /init/vars.env
EXPOSE 50005
WORKDIR /core
RUN python3 -m pip install -r requirements.txt
RUN mv app/main.py ./main.py
RUN mv /init/vars.env /init/.env
CMD ["python3", "main.py"]
# ENTRYPOINT [ "tail", "-f", "/dev/null" ]