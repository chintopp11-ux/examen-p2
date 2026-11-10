# Segundo Parcial: Pipeline de Datos Contenerizado

## 1. Descripción del proyecto

Este proyecto implementa un pipeline de procesamiento de datos utilizando Docker, Hadoop MapReduce, Python, Flask y PostgreSQL.

El objetivo es procesar un conjunto de 5 millones de registros de ventas, calcular los ingresos totales por hora del día y categoría, y almacenar los resultados en una base de datos para consultarlos mediante una API REST.

## 2. Pregunta asignada

**Ingreso total por hora del día (0–23) y categoría.**

Para cada registro se calcula:

Ingreso = cantidad × precio_unitario

Posteriormente, se agrupan los ingresos utilizando:
- Hora extraída de fecha_hora.
- Categoría del producto.

## 3. Tecnologías utilizadas

- Python 3.
- Hadoop 3.3.6.
- Hadoop Streaming.
- Docker y Docker Compose.
- Flask.
- PostgreSQL 16.
- OpenSSH.

## 4. Arquitectura del proyecto

El sistema está compuesto por tres servicios:

1. **Hadoop:** procesa el archivo CSV mediante Mapper y Reducer.
2. **PostgreSQL:** almacena los resultados agrupados.
3. **API Flask:** importa automáticamente los resultados de Hadoop y permite consultarlos mediante HTTP.

Los servicios se comunican mediante una red interna de Docker y utilizan volúmenes para compartir y conservar información.

## 5. Procesamiento MapReduce

El Mapper:
- Lee los registros del archivo CSV.
- Omite el encabezado.
- Extrae la hora y categoría.
- Calcula el ingreso de cada registro.
- Emite la clave hora-categoría y su ingreso.

El Reducer:
- Agrupa los registros por hora y categoría.
- Suma los ingresos.
- Genera los resultados finales.

## 6. Resultados obtenidos

- Registros procesados: 5,000,000.
- Grupos generados: 240.
- Registros de salida almacenados: 240.
- Diferencias entre procesamiento secuencial y Hadoop: 0.

El procesamiento secuencial tardó aproximadamente 85.77 segundos y Hadoop en modo local aproximadamente 144.79 segundos.

La ejecución de Hadoop se realizó en modo local dentro de un contenedor, por lo que no representa un clúster distribuido.

## 7. API REST

La API ofrece los siguientes endpoints:

### GET /health

Verifica la conexión con PostgreSQL.

### GET /resultados

Devuelve los resultados agrupados por hora y categoría.

### POST /resultados

Permite insertar o actualizar un resultado mediante JSON.

Ejemplo:

    {
      "hora": 10,
      "categoria": "Abarrotes",
      "ingreso": 1500.50
    }

## 8. Seguridad y comunicación

Se configuró autenticación SSH mediante llaves públicas y privadas, deshabilitando la autenticación por contraseña.

Se comprobó la comunicación SSH entre los contenedores Hadoop y API.

Las credenciales de PostgreSQL se administran mediante variables de entorno en el archivo .env, el cual no debe publicarse.

## 9. Ejecución del proyecto

Para construir e iniciar los servicios:

    docker compose up -d --build

Para consultar los contenedores:

    docker compose ps

Para consultar los resultados:

    Invoke-RestMethod http://localhost:5000/resultados

Para consultar el estado de la API:

    Invoke-RestMethod http://localhost:5000/health

## 10. Conclusión

El proyecto permitió implementar un pipeline de datos contenerizado que integra procesamiento MapReduce, almacenamiento relacional y consulta mediante una API REST.

La automatización de la ejecución de Hadoop y la carga de resultados en PostgreSQL permitió conectar las distintas etapas del procesamiento. También se comprobó la comunicación segura entre contenedores mediante autenticación SSH con llaves.

La comparación entre el procesamiento secuencial y Hadoop permitió verificar que ambos generaron los mismos 240 resultados.