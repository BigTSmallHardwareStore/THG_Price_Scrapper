FROM python:3.12
# FROM ubuntu:latest

RUN apt-get update && apt-get -y install cron vim
# RUN apt-get -y install apt-transport-https  g++ gcc tar libffi-dev libpng-dev cmake ninja-build



WORKDIR /app

ADD scraperv2.py requirements.txt /app/



# RUN pip install -U pip
# RUN pip install -U wheel
# RUN pip install -U setuptools
# RUN pip install Cython
# RUN pip install --upgrade cython



RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt
ENV PYTHONPATH /usr/local/lib/python3.11/site-packages



ADD crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab




# Create the log file to be able to run tail
#RUN touch /var/log/cron.log

# Run the command on container startup
#CMD cron && tail -f /var/log/cron.log
# run crond as main process of container
CMD ["cron", "-f"]


