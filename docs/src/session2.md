## Objetivos:
En esta sesión nos centramos en iniciar el desarrollo frontend para el segundo ejercicio práctico de nuestro proyecto. Los principales objetivos era desarrollar el frontend, incluyendo:
- Conexión del frontend con la API.
- Implementación del proyecto en la nube.

## Tecnologías y Herramientas:
Las principales tecnologías y herramientas utilizadas en esta sesión incluyen:
- **Vue.js:** Un marco progresivo para crear interfaces de usuario.
- **Bootstrap:** Un marco CSS popular para desarrollar sitios web responsivos y orientados a dispositivos móviles.
- **Axios:** Un cliente HTTP basado en promesas para el navegador y Node.js.

## Finishing Models and CRUD Operations:

### 1. Account Model
Creamos un modelo `Account` para representar una cuenta de usuario en nuestra aplicación. El modelo incluye campos como

- `user_id`: Identificador único del usuario.
- `avaialable_moeny`: Dinero disponible en la cuenta.

### 2. Orders Model
Creamos un modelo `Order` para representar una orden de compra en nuestra aplicación. El modelo incluye campos como

- `tickets_bought`: Número de entradas compradas.
- `total_price`: Precio total del pedido.
- `match_id`: Identificador del partido al que pertenece el pedido.
- `account_id`: Identificador de la cuenta que realizó el pedido.
- `user_id`: Identificador del usuario que realizó el pedido.

## Creación del Frontend

La primera parte de esta sesión la dedicamos a revisar las guías proporcionadas y seguir los pasos para familiarizarnos con Vue.js. Esta fue una parte muy útil del proceso ya que era completamente nueva para nosotros y al principio no entendíamos completamente cómo usarlo.

Los pasos clave realizados durante esta sesión fueron los siguientes:
1. **Integración API:**
   - Configurar Axios para comunicar con la API backend.
   - Se activó CORS en el backend de FastAPI para permitir solicitudes de origen cruzado.
   - 
2. **Comunicación frontend-backend:**
   - Aseguré que el frontend pudiera comunicarse efectivamente con el backend, manejando operaciones CRUD para equipos, partidos y órdenes.
   - Utilicé Axios para enviar solicitudes HTTP a la API del backend y actualizar el frontend en función de las respuestas.

 Al hacer esto, ahora pudimos comenzar a ver los resultados de nuestro trabajo durante la sesión 1 y comenzamos a tener una idea de cómo estructurar el resultado final.

### Matches.vue
En este paso implementamos nuestro primer componente principal para el sitio, que fue el carrito de compras. Inicialmente lo iniciamos como un componente propio, pero luego nos dimos cuenta de que la página principal de coincidencias y el carrito están diseñados en el mismo componente, mostrando una "plantilla" u otra dependiendo de las interacciones de los usuarios. Inicialmente, este fue un paso difícil debido a nuestra falta de conocimiento general de HTML y CSS, pero con la ayuda de recursos en línea logramos finalmente diseñar la página.

## Resumen:
Esta sesión se centró en configurar el entorno de desarrollo frontend, crear componentes Vue, integrar el frontend con la API backend y gestionar el estado y el enrutamiento dentro de la aplicación.