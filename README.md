# Proyecto-202314  

Proyecto para el curso de Construcción de Aplicaciones Nativas en Nube en la Universidad de los Andes.

## Tabla de contenido

- [Proyecto-202314](#proyecto-202314)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Pre requisitos para cada microservicio](#pre-requisitos-para-cada-microservicio)
  - [Estructura de cada microservicio](#estructura-de-cada-microservicio)
    - [Estructura de carpetas de cada microservicio](#estructura-de-carpetas-de-cada-microservicio)
    - [Archivos de soporte de cada microservicio](#archivos-de-soporte-de-cada-microservicio)
  - [Estructura del proyecto](#estructura-del-proyecto)
    - [Estructura de carpetas del proyecto](#estructura-de-carpetas-del-proyecto)
    - [Archivos de soporte del proyecto](#archivos-de-soporte-del-proyecto)
  - [Ejecución del proyecto localmente](#ejecución-del-proyecto-localmente)
    - [Crear entorno virtual](#crear-entorno-virtual)
    - [Activar entorno virtual](#activar-entorno-virtual)
      - [Windows](#windows)
      - [Mac](#mac)
    - [Instalar dependencias](#instalar-dependencias)
    - [Variables de entorno](#variables-de-entorno)
    - [Ejecutar el microservicio](#ejecutar-el-microservicio)
    - [Ejecutar pruebas](#ejecutar-pruebas)
    - [Ejecutar desde Dockerfile](#ejecutar-desde-dockerfile)
  - [Ejecución del proyecto con Docker Compose](#ejecución-del-proyecto-con-docker-compose)

## Pre requisitos para cada microservicio

- Python 3.11
- Docker
- Docker Compose
- PostgreSQL

## Estructura de cada microservicio

Cada microservicio utiliza Python y FastAPI para ejecutar el servidor. Se utiliza pytest para las pruebas unitarias.

### Estructura de carpetas de cada microservicio

Cada microservicio tiene la siguiente estructura de carpetas:

- **.vscode**: Contiene la configuración de VSCode para el proyecto.
- **src**: Contiene el código fuente del microservicio.
  - **core**: Contiene la configuración inicial del microservicio. Se hace el manejo de las variables de entorno y la configuración de la base de datos.
  - **db**: Contiene la configuración de la base de datos. Se encuentran también los modelos y esquemas de la base de datos.
    - **models**: Contiene los modelos de la base de datos. Describen cada tabla de la base de datos.
    - **schemas**: Contiene los esquemas utilizados para la validación de los datos de entrada y salida del microservicio.
  - **logic**: Contiene la lógica del microservicio y todas las interacciones con la base de datos.
  - **routers**: Contiene los endpoints del microservicio.
- **tests**: Contiene las pruebas unitarias del microservicio.

### Archivos de soporte de cada microservicio

- **.env.test**: Contiene las variables de entorno para las pruebas unitarias.
- **Dockerfile**: Contiene la configuración de Docker para la construcción de la imagen del microservicio.
- **README.md**: Contiene la documentación del microservicio.
- **requirements.txt**: Contiene las dependencias del microservicio.

## Estructura del proyecto

### Estructura de carpetas del proyecto

El proyecto tiene la siguiente estructura de carpetas:

- **.github/workflows**: Contiene la configuración de GitHub Actions para el proyecto. Contiene el pipeline de pruebas unitarias y los evaluadores de cada entrega.
- **.vscode**: Contiene la configuración de VSCode para el proyecto.
- **offers**: Contiene el microservicio de ofertas.
- **posts**: Contiene el microservicio de publicaciones.
- **routes**: Contiene el microservicio de rutas.
- **users**: Contiene el microservicio de usuarios.

### Archivos de soporte del proyecto

- **.gitignore**: Contiene los archivos y carpetas que se ignoran para subir al repositorio.
- **config.yaml**: Contiene la configuración de los evaluadores de cada entrega y la contribución de cada miembro del equipo.
- **docker-compose.yml**: Contiene la configuración de Docker Compose para la ejecución del proyecto.
- **LICENSE**: Contiene la licencia del proyecto.
- **README.md**: Contiene la documentación del proyecto.

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

### Variables de entorno

El servidor de FastAPI y las pruebas unitarias utilizan variables de entorno para configurar las credenciales de la base de datos y encontrar algunas configuraciones adicionales en tiempo de ejecución. A alto nivel, esas variables son:

- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres
- USERS_PATH: Para los microservicios que se comunican con el microservicio de Usuarios, necesitas especificar esta variable de entorno que contiene la URL utilizada para acceder a los endpoints de usuarios. (Ejemplo: <http://localhost:3000>, <http://users-service>)

Estas variables de entorno deben especificarse en `.env` (el cual toca crear para cada microservicio) y `.env.test`.

### Ejecutar el microservicio

Una vez configuradas las variables de entorno, ejecute el siguiente comando en la carpeta del microservicio:

```python
uvicorn src.main:app --reload --port <NUMERO_DE_PUERTO>
```

### Ejecutar pruebas

Para ejecutar las pruebas unitarias de los microservicios y establecer el porcentaje mínimo de cobertura del conjunto de pruebas en 70%, ejecuta el siguiente comando:

```shell
pytest --cov-fail-under=70 --cov=src
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

Asegúrese de que Docker está corriendo en su máquina.

Esto corre las bases de datos de PostgreSQL y los microservicios de FastAPI.
