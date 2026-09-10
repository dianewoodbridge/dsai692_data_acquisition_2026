FROM continuumio/miniconda3
WORKDIR /Day6
COPY * .
# Creating crontab to call the api server
# install cron
RUN apt-get update && apt-get -y install cron
# create a log file
RUN touch /var/log/cron.log
#  Add crontab file 
# Note : /etc/cron.d is a directory for cron
COPY api-cron /etc/cron.d/api-cron
# RUN chmod 0644 /etc/cron.d/api-cron
# Apply cron job
RUN crontab /etc/cron.d/api-cron
# Normally crontab is working on the background.
# However, for the Docker image, this is a single process
# running in the foreground in the container, and remain active.
CMD ["cron", "-f"] 