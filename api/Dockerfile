#   See api-base.dockerfile
#

FROM hackfsu/api-base

#
#   Install Nginx to serve static files
#   We'll collect them later
#

RUN apt-get update && apt-get install -y nginx
COPY ./nginx-static.conf /etc/nginx/conf.d

#
#   Install python dependencies
#

COPY requirements.txt ./
RUN pip install -r requirements.txt

#
#   Update Python source
#

COPY . .


#
#   Port 8080 is for the Nginx server (prod)
#   Port 8000 goes directly to Django (dev)
#

EXPOSE 8080
EXPOSE 8000

#
#   Launch the Nginx and Django
#

CMD ["./entrypoint.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
