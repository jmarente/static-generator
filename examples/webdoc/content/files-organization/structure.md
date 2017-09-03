+++
weight=0
title="Estructura"
+++

Sitic toma un directorio y lo usa como entrada para crear una página web completa.

El nivel más alto del directorio principal tendrá los siguientes elementos:

    +--content/
    +--data/
    +--locales/
    +--templates/
    +--static/
    +--sitic.yml

El proposito para cada fichero/directorio se decribe a continuación:

* **content**: Aquí es donde se almacenan los contenidos de la web, se crearán
        sub-directorios para crear las distintas secciones de la web. Supongamos, que nuestra web
        tiene cuatro secciones: `blog`, `news`, `about` y `contact`,
        entonces será necesario crear una carpeta para cada una de ellas.
* **data**: Este directorio contiene distintos ficheros de configuración que pueden
        ser usado mientras se genera la web. El contenido de estos ficheros puede estar en format
        YAML, JSON o TOML.
* **locales**: Ficheros con las traducciones de las cadenas usadas en las plantillas.
* **templates**: Los contenidos dentro de este directorio especifican como se convertirán
        los contenidos en una web estática.
* **static**: Directorio usado almacenar todos los contenidos estáticos que la web
        necesitará como imágenes, CSS, Javascript u otro tipo de contenido estático.
* **sitic.yml**: Todo proyecto hecho con Sitic debe de tener un fichero
        de configuración en la raíz del proyecto. Este debe de tener el nombre `sitic.yml`,
        usando el formato YAML. Esta configuración se aplica a todo el siti completo,
        que incluye la `base_url` y `title` de la página web.
