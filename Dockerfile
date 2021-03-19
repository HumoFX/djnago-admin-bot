FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
# copy entrypoint.sh
COPY ./entrypoint.sh .
COPY . /code/
CMD bash entrypoint.sh