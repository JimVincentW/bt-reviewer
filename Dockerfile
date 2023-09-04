FROM python:latest

# Install necessary packages
RUN apt-get update && apt-get install -y libc6 wget bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev

# Download Firefox
RUN mkdir /browsers
RUN curl http://mirror.archlinuxarm.org/aarch64/extra/firefox-117.0-1-aarch64.pkg.tar.xz -o /browsers/firefox-117.0-1-aarch64.pkg.tar.xz
RUN tar xvf /browsers/firefox-117.0-1-aarch64.pkg.tar.xz -C /browsers

# Here you might need to adjust paths depending on the contents of the Arch Linux ARM package.

# Download Geckodriver
RUN mkdir /drivers/
RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz -o /drivers/geckodrive.tar.gz
RUN tar -xzvf /drivers/geckodrive.tar.gz -C /drivers/

# Set the working directory
ENV PATH="/drivers:/browsers/firefox:${PATH}"

WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python", "./main.py"]
