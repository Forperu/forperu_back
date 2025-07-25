FROM python:3.11.12
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Dependencias del sistema para mysqlclient y otras
RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  build-essential \
  libssl-dev \
  libffi-dev \
  libxml2-dev \
  libxslt1-dev \
  zlib1g-dev \
  libjpeg-dev \
  libpq-dev \
  && apt-get clean

COPY requirements.txt /app/requirements.txt
RUN pip install python-dotenv
RUN pip install -r requirements.txt
COPY . /app

CMD python manage.py runserver 0.0.0.0:8000