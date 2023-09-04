FROM python:3.9

# Install necessary packages
RUN apt-get update &&  \
            apt-get install -y libc6 wget bzip2 libxtst6 firefox-esr \
            libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev

# Download Firefox
WORKDIR /browsers

RUN curl -O https://ftp.mozilla.org/pub/firefox/releases/86.0/linux-x86_64/en-US/firefox-86.0.tar.bz2 
RUN tar -jxf firefox-86.0.tar.bz2 \
    && mv firefox /opt/ \
    && chmod 755 /opt/firefox \
    && chmod 755 /opt/firefox/firefox

# Download Geckodriver
RUN mkdir /drivers/
RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz -o /drivers/geckodrive.tar.gz \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
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
