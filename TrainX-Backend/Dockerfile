# Base image
FROM python:3.7-buster

# Working directory
WORKDIR /code

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/DATEXIS/TeXooPy.git

# Add our code to workdir
COPY . .

# Install our app-module for easier imports
RUN pip install -e .

# Run flask app
# CMD ["flask", "run"]
CMD ["python", "backend.py"]
