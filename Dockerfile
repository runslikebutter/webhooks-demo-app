FROM python:3.9

# configure environment
ENV PYTHONUNBUFFERED=1

# set working directory
WORKDIR /app

# copy requirements file
COPY requirements.txt /app/

# copy entrypoint file
COPY entrypoint.sh /app/

# install python dependencies
RUN pip install -r requirements.txt

# copy app files
COPY . /app/

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
