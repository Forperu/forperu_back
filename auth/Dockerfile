FROM python:3.11.12
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install python-dotenv
RUN pip install -r requirements.txt
COPY . /app

CMD python manage.py runserver 0.0.0.0:8000