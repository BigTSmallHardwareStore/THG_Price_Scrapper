FROM python:3.12.4-slim

# Set working directory
WORKDIR /app

# Copy the script and the crontab file
COPY script.py /app/script.py
COPY crontab.txt /etc/cron.d/mycron
COPY requirements.txt /app/requirements.txt

# Update and install cron and vim
RUN apt update && apt upgrade -y
RUN apt install -y cron vim && apt clean


# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/mycron

# Apply cron job
RUN crontab /etc/cron.d/mycron


# Install Python dependencies
RUN pip install -r /app/requirements.txt

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Set the environment variable (can also be set during docker run)
ENV PATH_TO_DB=/data/verivox_thg.db


# Use JSON array syntax for CMD instruction
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
