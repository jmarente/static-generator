+++
weight=1
title="Example"
+++

The following is the basic configuration file:

    base_url: "http://Sitic.example.com/"

Next, we can create a slightly more complete file with different elements:

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

In this last example you can see different configurations, such as menu settings
or languages, which we will discuss in more detail in the following sections.
