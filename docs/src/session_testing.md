## Objetivos:
En esta sesión, nos centramos en realizar pruebas cruzadas entre diferentes grupos. Los principales objetivos era probar el trabajo hecho por los otros grupos.


## Tareas
Como llegamos a la sesión de prueba solo con nuestro backend, sabíamos que sería muy importante tomar nota de todo lo que vimos en el trabajo de nuestros compañeros.
### A01: 
El proyecto de este grupo se encontraba en la fase en la que la mayor parte del trabajo estaba casi listo y solo necesitaba algunos retoques finales. Como no habían agregado los datos requeridos a la base de datos, no pudimos probar todos los diferentes pasos necesarios.

Finalizando la compra: Como no se mostró ningún mensaje después de finalizar la compra, no pudimos verificar si la compra se realizó correctamente o no. Además no sabríamos si fue por falta de fondos o por falta de billetes.

Lo que sacamos de esto fue que decidimos implementar directamente alguna lógica en el frontend, de modo que si se supera el límite de boletos disponibles o el usuario no tiene más dinero, no puede agregar más boletos al carrito.

### A02 y A11:
Estos grupos tenían un proyecto muy avanzado y pudimos probar todo. Lo que nos ayudó al permitirnos ver diferentes detalles del sitio web y cómo queríamos configurar el nuestro.

### A03:
Al igual que el grupo A01, su sitio web se encontraba en la etapa de los últimos retoques necesarios. La parte principal que noté y agregué cambios a mi propio proyecto fue en la clase XXXOut de los modelos. Mostraron las identificaciones de los equipos y las competiciones, lo que no es ideal para la experiencia del usuario final.

### Comentario General:
Una de las cosas principales que notamos en el sitio web de los demás fue que cuando el sitio se actualizaba y un usuario iniciaba sesión, se desconectaba automáticamente.

Como esto era algo que no queríamos que sucediera, intentamos corregir este error pero a nosotros nos sucedió al revés. Una vez que un usuario cierra sesión y actualiza la página, automáticamente vuelve a iniciar sesión. Para solucionar este problema, agregamos un nuevo método que se llamó en el proceso de cierre de sesión y que establecía todas las variables relacionadas con un usuario en nulas, asegurando que no La información anterior que provenía del componente `Login.vue` persistía.

## Nuestros Comentarios
Como solo teníamos el backend hecho y muchos datos no se habían agregado a la base de datos, los otros grupos no pudieron probar nuestro trabajo. Lo que significa que no recibimos ningún comentario útil.

## Conclusión
En esta sesión de pruebas cruzadas, obtuvimos valiosas perspectivas que nos permitieron mejorar nuestro proyecto. Observamos la importancia de proporcionar retroalimentación clara en el frontend, optimizar la presentación de datos y gestionar adecuadamente las sesiones de usuario. A pesar de no recibir comentarios de otros grupos debido a nuestras limitaciones iniciales, logramos identificar y corregir varios aspectos críticos de nuestro desarrollo, asegurando la calidad y funcionalidad del proyecto.