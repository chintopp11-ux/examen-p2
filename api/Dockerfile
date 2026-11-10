
FROM python:3.11-slim

WORKDIR /app

# Instalar y configurar el servidor SSH
RUN apt-get update && apt-get install -y \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario para la conexión SSH
RUN useradd -m -s /bin/bash hadoop \
    && mkdir -p /var/run/sshd /home/hadoop/.ssh \
    && chmod 700 /home/hadoop/.ssh

# Autorizar la llave pública del contenedor Hadoop
COPY hadoop_id_rsa.pub /home/hadoop/.ssh/authorized_keys

RUN chmod 600 /home/hadoop/.ssh/authorized_keys \
    && chown -R hadoop:hadoop /home/hadoop/.ssh \
    && sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Instalar dependencias de Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY app.py .

EXPOSE 22 5000

# Iniciar SSH y Flask
CMD ["sh", "-c", "service ssh start && exec python app.py"]
