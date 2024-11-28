
# Instrucciones para Ejecutar el Backend

## Requisitos Previos

- **Python 3.x** instalado.
- **Virtualenv** para crear entornos virtuales en Python.
- **Base de datos**: Si utilizas una base de datos distinta a SQLite (por ejemplo, PostgreSQL), asegúrate de instalarla y configurarla.

## Pasos para Configurar y Ejecutar el Backend (Django)

### 1. Clonar el Repositorio

Abrir un termina y clonar el repositorio:

```bash
git clone https://github.com/jpajoyl/meli-scraping-back
```

### 2. Navegar al Directorio del Proyecto

```bash
cd meli-scraping-back
```

### 3. Crear y Activar un Entorno Virtual

#### Con Virtualenv:

1. **Crear un entorno virtual:**

   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual:**

   - **En Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **En macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```
3. **Acceder a la carpeta del proyecto**
   ```bash
     cd webAPI
     ```

### 4. Instalar las Dependencias de Python

```bash
pip install -r requirements.txt
```

### 5. Aplicar Migraciones y Crear la Base de Datos

Ejecutar migraciones:

```bash
python manage.py migrate
```

### 6. Crear un Superusuario

Se debe crear un super usuario para acceder al panel de control de Django y crear un usuario con el rol 'admin'. Se debe tener en cuenta que el username debe ser igual al email para acceder a la aplicación

```bash
python manage.py createsuperuser
```

Sigue las indicaciones para crear el superusuario.

### 8. Ejecutar el Servidor de Desarrollo de Django

Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor se ejecutará por defecto en `http://localhost:8000/`.

## Notas Adicionales

- **Entorno Virtual**

  - Para desactivar el entorno virtual:

    ```bash
    deactivate
    ```
