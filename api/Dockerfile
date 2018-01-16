#   See api-base.dockerfile
#

FROM hackfsu/api-base

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
#   Launch the server.
#

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
