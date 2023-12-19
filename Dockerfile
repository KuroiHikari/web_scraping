# Cool utility image that makes hot-reload etc. very simple, not good for more serious projects
# if you're planning on using k8s etc
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
WORKDIR /code/app/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app .
