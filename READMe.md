
*Clase Solucion* nuestro gen es una imagen generada y se almacena como un objeto de la clase Image de la biblioteca PIL

- imagen color rgb random 
- pintarFigura (num_figuras, subdivision: area en donde pintar)
- aptitud: media de la diferencia de color entre la imagen generada y la imagen objetivo(metodo delta_E de la biblioteca colour y se utiliza el método CIE1976)


*Crear Poblacion* genera objetos Solucion y le coloca N figuras aleatoriamente

*calcular Aptitud* calcular la aptitud de cada solución en la población y luego ordenar las soluciones bajo este criterio

*cruzar* toma al padre que es el mejor de la generacion anterior ya quer es la base para sig generaciones
se elige un punto de corte alet 
- h1: la parte izquierda del padre hasta el punto de corte y la imagen en blanco
- h2: desde el punto de corte la parte derecha del padre  y la imagen en blanco

*mutacion* aplica mutaciones a todas menos a una, que es la padre (la inicial)

*equilibrar* se imprime la aptitud por generacion
si la aptitud no ha cambiado entre generaciones, incrementa el contador lo que refleja la falta durante el progreso
si la aptitud ha mejorado en la generación actual, se disminuye el contador. indica queexiste progreso en la aptitud