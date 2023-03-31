FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
COPY /code .
COPY /lib /lib
COPY /credentials /credentials
# Install Python 3 and dependencies 
RUN apt update && apt install -y wget curl procps nano git
RUN pip install -r requirements.txt
RUN pip install google-cloud-storage

ENV HADOOP_HOME=/opt/hadoop \
    HADOOP_CLASSPATH=/opt/hadoop/share/hadoop/tools/lib/*:/opt/hadoop/share/hadoop/common/*:/opt/hadoop/share/hadoop/common/lib/*:/opt/hadoop/share/hadoop/hdfs/*:/opt/hadoop/share/hadoop/hdfs/lib/*:/opt/hadoop/share/hadoop/mapreduce/*:/opt/hadoop/share/hadoop/mapreduce/lib/*:/opt/hadoop/share/hadoop/yarn/*:/opt/hadoop/share/hadoop/yarn/lib/*:/opt/hadoop/share/hadoop/tools/lib/*:/opt/hadoop/share/hadoop/tools/lib/*


RUN mkdir -p /usr/lib/hadoop/lib/ && \
    wget "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-latest-hadoop3.jar" -O /usr/lib/hadoop/lib/gcs-connector-latest-hadoop3.jar
ENV HADOOP_HOME="/usr/lib/hadoop/lib"
ENV PATH="${HADOOP_HOME}/gcs-connector-latest-hadoop3.jar:$PATH"


# VERSIONS
ENV SPARK_VERSION=3.3.2 \
HADOOP_VERSION=3 \
JAVA_VERSION=11

# SET JAVA ENV VARIABLES
ENV JAVA_HOME="/home/jdk-${JAVA_VERSION}.0.1"
ENV PATH="${JAVA_HOME}/bin/:${PATH}"

# DOWNLOAD JAVA 11 AND INSTALL

RUN DOWNLOAD_URL="https://download.java.net/java/GA/jdk${JAVA_VERSION}/13/GPL/openjdk-${JAVA_VERSION}.0.1_linux-x64_bin.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/openjdk-${JAVA_VERSION}.0.1_linux-x64_bin.tar.gz" \
    && mkdir -p "${JAVA_HOME}" \
    && tar xzf "${TMP_DIR}/openjdk-${JAVA_VERSION}.0.1_linux-x64_bin.tar.gz" -C "${JAVA_HOME}" --strip-components=1 \
    && rm -rf "${TMP_DIR}" \
    && java --version

# DOWNLOAD SPARK AND INSTALL
RUN DOWNLOAD_URL_SPARK="https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    && wget --no-verbose -O apache-spark.tgz  "${DOWNLOAD_URL_SPARK}"\
    && mkdir -p /home/spark \
    && tar -xf apache-spark.tgz -C /home/spark --strip-components=1 \
    && rm apache-spark.tgz

# SET SPARK ENV VARIABLES
ENV SPARK_HOME="/home/spark"
ENV PATH="${SPARK_HOME}/bin/:${PATH}"

# SET PYSPARK VARIABLES
ENV PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"

ENV PREFECT_KEY="$(cat /credentials/prefect_key.txt)"


USER $NB_UID

CMD bash -c "prefect cloud login \
              --key ${PREFECT_KEY}\
              --workspace gbotemibolarinwagmailcom/gharchive && prefect agent start -q default"
