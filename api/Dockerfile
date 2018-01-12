#   See api-base.dockerfile
#

FROM hackfsu/api-base

#
#   Install python dependencies
#

COPY requirements.txt ./
RUN pip install -r requirements.txt

#
#   Add files and run static build.
#

COPY . .
RUN gulp

#
#   Launch the server.
#

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
