# Use Python 3.9 as base image
FROM python:3.9

# Set the environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV GECKODRIVER_VER v0.31.0
ENV FIREFOX_VER 86.0

# Update packages and install necessary packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libc6 wget bzip2 libxtst6 firefox-esr libgtk-3-0 libx11-xcb-dev \
    libdbus-glib-1-2 libxt6 libpci-dev libx11-xcb1 libdbus-glib-1-2

# Download and install Firefox
WORKDIR /browsers
RUN curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
    && tar -jxf firefox-* \
    && mv firefox /opt/ \
    && chmod 755 /opt/firefox \
    && chmod 755 /opt/firefox/firefox

# Download and install Geckodriver
WORKDIR /drivers
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
    && tar zxf geckodriver-*.tar.gz \
    && mv geckodriver /usr/bin/

# Set the working directory
ENV PATH="/drivers:/browsers/firefox:${PATH}"
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python", "./main.py"]
