# Proyecto-202314  

## Ejecución del proyecto localmente

Para ejecutar el proyecto en su máquina se debe dirigir a la carpeta de cada microservicio y ejecutar los siguiente comandos:

### Crear entorno virtual

```python
python -m venv env
```

### Activar entorno virtual

#### Windows

```python
env\Scripts\activate
```

#### Mac

```python
source env/bin/activate
```

### Instalar dependencias

```python
pip install -r requirements.txt
```

Para salir del entorno virtual ejecute el siguiente comando:

```shell
deactivate
```

### Ejecutar el microservicio

Una vez configuradas las variables de entorno, ejecute el siguiente comando en la carpeta del microservicio:

```python
uvicorn src.main:app --reload --port <NUMERO_DE_PUERTO>
```

### Ejecutar desde Dockerfile

Para construir la imagen del Dockerfile en la carpeta, ejecuta el siguiente comando:

```bash
docker build . -t <NOMBRE_DE_LA_IMAGEN>
```

Y para ejecutar esta imagen construida, utiliza el siguiente comando:

```bash
docker run <NOMBRE_DE_LA_IMAGEN>
```

## Ejecución del proyecto con Docker Compose

Para ejecutar el proyecto completo, vaya al directorio raíz del proyecto y ejecute el siguiente comando:

```shell
docker-compose up --build
```
