+++
weight=1
title="Ejemplo"
+++

A continuación se muestra el fichero de configuración básico:

    base_url: "http://Sitic.example.com/"

Seguidamente podemos un fichero un poco más completo con distintos elementos:

    base_url: "www.Sitic.net"
    paginable: "1"
    main_language: "en"

    lazy_menu: "main"

    sitemap:
        change_frequency: "monthly"
        priority: 0.5

    menus:
        main:
            - title: "title test"
              url: "/test-url"
              id: "test1"
            - title: "title test2"
              url: "/test-url2"
              id: "test2-custom"
              parent: "test1"
        footer:
            - title: "title footer"
              url: "/test-url-footer"
              id: "test-footer"

    languages:
        en:
        es:
            menus:
                footer:
                    - title: "title footer"
                      url: "/test-url-footer"
                      id: "test-footer"

En este último ejemplo se pueden ver distintas configuraciones, como la configuración de menús o
idiomas, de las que hablaremos mas en detalle en las siguientes secciones.
