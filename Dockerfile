FROM apache/airflow:2.10.5-python3.10
ENV AIRFLOW_CONN_TEST_CONN="true"
ENV AIRFLOW__CORE__TEST_CONNECTION="true"
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

USER root

# Java install
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  openjdk-17-jre-headless \
  procps \
  curl \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# chceck Java home
RUN JAVA_REAL_PATH=$(dirname $(dirname $(readlink -f $(which java)))) && \
  echo "JAVA_HOME found at: $JAVA_REAL_PATH" && \
  echo "export JAVA_HOME=$JAVA_REAL_PATH" >> /etc/profile.d/java.sh

# JAVA_HOME 
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# checks
RUN echo "JAVA_HOME is: $JAVA_HOME" && \
  ls -la $JAVA_HOME/bin/java || echo "WARNING: Java not found at $JAVA_HOME"

USER airflow


