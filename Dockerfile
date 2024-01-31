# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

# UPDATE APT-GET
RUN apt-get update

# PYODBC DEPENDENCES
RUN apt-get install -y tdsodbc unixodbc-dev
# RUN apt install unixodbc-bin -y
RUN apt-get clean -y
# ADD odbcinst.ini /etc/odbcinst.ini

# DEPENDECES FOR DOWNLOAD ODBC DRIVER
RUN apt-get install apt-transport-https 
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update

# INSTALL ODBC DRIVER
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 --assume-yes

# CONFIGURE ENV FOR /bin/bash TO USE MSODBCSQL17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile 
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /backend/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "90"]