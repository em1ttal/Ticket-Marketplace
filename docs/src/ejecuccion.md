# Ejecucción

Hemos intentado utilizar render, pero el servicio web no se implementa. Por tanto, será necesario ejecutar el backend y el frontend en la terminal. Para hacer esto, será necesario instalar y configurar `Poetry`, `NodeJS`, `npm` and `Vue`en el proyecto.

Backend: Para ejecutar el backend, es necesario estar dentro del directorio del backend en la terminal y ejecutar el comando:
```bash
cd backend
poetry run uvicorn app.main:app
```

Frontend: Para ejecutar el frontend, es necesario estar dentro del directorio del frontend en la terminal y ejecutar el comando:
```bash
cd frontend
npm run dev
```

Será necesario agregar los datos requeridos a la base de datos. Todas las pruebas que hicimos se realizaron con los datos proporcionados en la sesión de prueba.