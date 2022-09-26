# FastAPI & Mongo CRUD with Authorization JWT

1. Clonar proyecto

2. Instalar dependencias

```bash
pipenv shell

pipenv install
```

3. Levantar la base de datos mongo

```bash
docker-compose up -d
```

4. Ejecutar el servidor

```bash
uvicorn app.main:app --host localhost --port 8000 --reload
```

5. Acceso a la API
 <http://127.0.0.1:8000/docs>

 ---

##### Made with ❤️ by Leandro Arturi
