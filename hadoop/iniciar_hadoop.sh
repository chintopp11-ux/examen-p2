
#!/bin/bash
set -e
rm -f /tmp/examen/hadoop_listo

echo "Iniciando servicio SSH..."
service ssh start

echo "Preparando salida de Hadoop..."

rm -rf /tmp/examen/salida_automatico

echo "Ejecutando trabajo MapReduce..."

su - hadoop -c '
/opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
-D mapreduce.framework.name=local \
-D mapreduce.local.map.tasks.maximum=1 \
-input /tmp/examen/ventas.csv \
-output /tmp/examen/salida_automatico \
-mapper "python3 /tmp/examen/mapper.py" \
-reducer "python3 /tmp/examen/reducer.py"
'

echo "Verificando resultados..."

wc -l /tmp/examen/salida_automatico/part-00000

echo "PROCESAMIENTO HADOOP FINALIZADO"

touch /tmp/examen/hadoop_listo

tail -f /dev/null
