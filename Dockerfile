FROM ubuntu:22.04

# Set timezone and non-interactive mode
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND=noninteractive

# Prevent tzdata from prompting
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Make python3 point to python3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install uWSGI using pip
RUN pip3 install --upgrade pip && pip3 install uwsgi

# Copy just the requirements file first
COPY ./requirements.txt /app/requirements.txt

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy application source
COPY ./app /app

# Expose port 80
EXPOSE 80

# Set entrypoint and default command
ENTRYPOINT ["python3"]
CMD ["gevent_prod.py"]
