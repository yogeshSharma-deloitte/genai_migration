FROM python:3.9.16-slim-buster

# Install Git
RUN apt-get update && \
    apt-get install -y git

# Install Java 11
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk

# Install Maven 3.9
ENV MAVEN_VERSION=3.9.4
ENV MAVEN_HOME=/opt/maven

RUN apt-get update && \
    apt-get install -y wget && \
    wget -q https://dlcdn.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz && \
    tar xf apache-maven-${MAVEN_VERSION}-bin.tar.gz -C /opt && \
    mv /opt/apache-maven-${MAVEN_VERSION} ${MAVEN_HOME} && \
    rm apache-maven-${MAVEN_VERSION}-bin.tar.gz
ENV PATH=${MAVEN_HOME}/bin:${PATH}

# Set working directory
WORKDIR /usr/src/app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install uvicorn
RUN apt-get update && apt-get upgrade -y && apt-get install -y nginx && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN [ "python3", "-c", "import nltk; nltk.download('punkt', download_dir='/usr/local/nltk_data')" ]
# Copy the entire project and install requirements
COPY . .
COPY .project-root ./
RUN python manage.py collectstatic --noinput
COPY default.conf /etc/nginx/sites-available/dev
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/dev /etc/nginx/sites-enabled/
RUN nginx -t
EXPOSE 80 8000
RUN chmod +x run.sh
ENTRYPOINT ["./run.sh"]