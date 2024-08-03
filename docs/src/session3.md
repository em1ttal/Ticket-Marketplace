## Objetivos:
En esta sesión, nos centramos en implementar la autenticación y autorización de usuarios para asegurar el acceso a la API. Los principales objetivos eran:
1. Proteger los datos en la aplicación.
2. Comprender los conceptos de autenticación y autorización.
3. Familiarizarnos con las tecnologías básicas de autenticación de solicitudes y gestión de usuarios.
4. Desarrollar la seguridad de las aplicaciones mediante:
   - Autenticar usuarios.
   - Protección de puntos finales API.
   - Finalizar la implementación de la aplicación.

## Tecnologías y Herramientas:
Las principales tecnologías y herramientas utilizadas en esta sesión incluyen:
- **JWT (JSON Web Tokens):** Un medio compacto y seguro para URL para representar reclamaciones que se transferirán entre dos partes.
- **Curl:** Una herramienta de línea de comandos para transferir datos con URL.

## Actividades:

1. **Autenticación de token:**
   - Utilizamos el endpoint `/login/access-token` para generar tokens de acceso para los usuarios.

2. **Protección de terminales:**
   - Añadimos dependencias de autenticación para proteger los enpoints del API.
   - Control de acceso verificado al requerir tokens válidos para acceder a rutas protegidas.

3. **Autenticación de interfaz:**
   - Creamos un componente `Login` en Vue para manejar la autenticación del usuario.
   - Implementamos la funcionalidad de inicio de sesión para obtener y almacenar el token del usuario.

4. **Finalización de la aplicación:**
    - Completamos la implementación de la aplicación asegurando que los usuarios estén autenticados antes de acceder a los datos.
    - Ahora podríamos navegar por la web como estaba previsto, pudiendo comprar entradas como usuarios, implementando toda la lógica necesaria sobre si una compra era posible o no.

5. **Cifrado del dinero de la usuaria**
    - En este paso, se suponía que íbamos a cifrar el dinero que tiene un usuario usando `cryptography.Fernet`, sin embargo, nos encontramos con varios problemas.
      - El primer problema con el que nos topamos fue que tuvimos que cambiar la base de datos para que el dinero ahora fuera LargeBinary en lugar de flotante, lo que significa que tuvimos que cambiar la forma en que funcionaban los modelos.
      - Después de eso, en `security.py` comenzamos a implementar un método de cifrado que inicialmente pensamos que funcionaba, sin embargo, poco después nos dimos cuenta de que cada vez que se recargaba el backend, se creaba una nueva clave, lo que significa que los datos nunca se podían descifrar.
      - La solución que se nos ocurrió fue generar una clave en otro proyecto y guardarla en el archivo .env de nuestro proyecto y leerla durante el inicio del backend. Sin embargo, por razones que no podemos entender, partes del backend comenzaron a darnos errores que nunca antes habíamos visto, como un error al realizar una búsqueda de coincidencias en la base de datos. Un error que nos confundió mucho ya que buscar una coincidencia específica no tiene nada que ver con cifrar el dinero en la base de datos.
      - Debido a esto, decidimos dejarlo para el final y finalmente decidimos no implementar la función porque no nos quedaba tiempo.

## Resumen:
Esta sesión se centró en implementar la autenticación y autorización de usuarios para asegurar el acceso a la API. Nos aseguramos de que el backend estuviera correctamente protegido y actualizamos el frontend para manejar la autenticación del usuario.