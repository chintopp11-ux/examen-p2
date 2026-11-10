
# Imagen base
FROM ubuntu:22.04

# Evitar preguntas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java, SSH y herramientas necesarias
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    openssh-server \
    wget \
    procps \
    net-tools \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno de Java y Hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Descargar e instalar Hadoop
RUN wget -q https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz \
    && tar -xzf hadoop-3.3.6.tar.gz -C /opt \
    && mv /opt/hadoop-3.3.6 /opt/hadoop \
    && rm hadoop-3.3.6.tar.gz

# Crear usuario para Hadoop
RUN useradd -m -s /bin/bash hadoop

# Configurar Java para Hadoop
RUN echo "export JAVA_HOME=$JAVA_HOME" >> /opt/hadoop/etc/hadoop/hadoop-env.sh

# Preparar SSH
RUN mkdir -p /var/run/sshd \
    && ssh-keygen -A \
    && mkdir -p /home/hadoop/.ssh \
    && ssh-keygen -t rsa -N "" -f /home/hadoop/.ssh/id_rsa \
    && cat /home/hadoop/.ssh/id_rsa.pub >> /home/hadoop/.ssh/authorized_keys \
    && chmod 700 /home/hadoop/.ssh \
    && chmod 600 /home/hadoop/.ssh/authorized_keys \
    && chmod 600 /home/hadoop/.ssh/id_rsa \
    && echo "Host *" > /home/hadoop/.ssh/config \
    && echo "    StrictHostKeyChecking no" >> /home/hadoop/.ssh/config \
    && chown -R hadoop:hadoop /home/hadoop/.ssh

# Permitir autenticación por llave SSH
RUN sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Permisos de Hadoop
RUN chown -R hadoop:hadoop /opt/hadoop

# Copiar script de inicio automático
COPY hadoop/iniciar_hadoop.sh /opt/iniciar_hadoop.sh

# Dar permisos de ejecución
RUN chmod +x /opt/iniciar_hadoop.sh

# Puerto SSH
EXPOSE 22

# Iniciar SSH y ejecutar MapReduce mediante Bash
CMD ["bash", "/opt/iniciar_hadoop.sh"]
