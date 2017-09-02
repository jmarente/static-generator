+++
weight=2
title='Diferencia con los generadores dinámicos'
+++

Los generadores de sitios web generan contenidos en ficheros HTML. La mayoría son "generadores dinámicos".
Esto significa que el servidor HTTP (que es el programa que se ejecuta en su sitio web con el que el navegador del
usuario habla) ejecuta el generador para crear un nuevo fichero HTML cada vez que un usuario desea ver una página.

Crear la página de forma dinámica significa que la máquina que aloja el servidor HTTP tiene que tener suficiente
memoria y CPU para ejecutar el generador de forma eficaz durante todo el día. Si no, entonces el usuario tiene que
esperar a que la página se genere.

Nadie quiere que los usuarios esperen más de lo necesario, por lo que los generadores de sitios dinámicos programaron
sus sistemas para almacenar en caché los ficheros HTML. Cuando un fichero se almacena en caché, una copia se
almacena temporalmente en el equipo. Es mucho más rápido que el servidor envíe esa copia la próxima vez que
se solicite la página en lugar generarla desde cero.

Sitic intenta llevar el almacenamiento en caché un paso más allá. Todos los ficheros HTML se representan en su máquina.
Puede revisar los ficheros antes de copiarlos en la máquina que aloja el servidor HTTP. Dado que los ficheros HTML
no se generan dinámicamente, decimos que Sitic es un "generador estático".

No tener que ejecutar la generación de HTML cada vez que se recibe una petición tiene varias ventajas. Entre ellas,
la más notable es el rendimiento, los servidores HTTP son muy buenos en el envío de ficheros. Tan bueno que puede
servir eficazmente el mismo número de páginas con una fracción de memoria y CPU necesaria para un sitio dinámico.

Sitic tiene dos componentes para ayudarle a construir y probar su sitio web. El que probablemente usará más a menudo es el
servidor HTTP incorporado. Cuando ejecuta el servidor, Sitic procesa todo su contenido en ficheros HTML y luego ejecuta
un servidor HTTP en su máquina para que pueda ver cómo son las páginas.

El segundo componente se utiliza una vez que el sitio esté listo para ser publicado.
Ejecutar Sitic sin ninguna acción reconstruirá su sitio web completo utilizando la configuración `base_url`
del fichero de configuración de su sitio. Eso es necesario para que sus enlaces de página funcionen correctamente 
con la mayoría de las empresas de alojamiento.
