# Use the official Apache Spark image
FROM apache/spark:3.4.0

ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyspark==3.4.0

RUN mkdir -p /root/.ivy2/local

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# COPY spark-defaults.conf /opt/spark/conf/


