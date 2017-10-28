FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - \
    && apt-get install -y nodejs

WORKDIR /usr/src/app

RUN npm install -g gulp
COPY package.json ./
RUN npm install

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN gulp

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
