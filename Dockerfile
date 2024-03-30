FROM python:3.12-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

# Run the application
CMD ["python", "app.py"]