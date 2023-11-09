FROM python:3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 80

COPY ./ /app

WORKDIR /app

CMD python3 -m uvicorn app.main:app --host 0.0.0.0 --port 80
