+++
weight=0
title="Structure"
+++

Sitic takes a directory and uses it as an entry to create a complete website.

The highest level of the main directory will have the following elements:

    +--content/
    +--data/
    +--locales/
    +--templates/
    +--static/
    +--sitic.yml

The purpose for each file/directory is described below:

* **content**: This is where the contents of the website are stored, will be created
        subdirectories to create the different sections of the website. Suppose our website
        has four sections:"blog,""news,""about," and "contact,"
        then it will be necessary to create a folder for each of them.
* **data**: This directory contains different configuration files that can be used to
        be used while the web is being generated. The content of these files can be in format
        YAML, JSON or TOML.
* **locales**: Files with the translations of the strings used in the templates.
* **templates**: The contents within this directory specify how they will be converted
        the contents of a static website.
* **static**: Directory used to store all static content that the web
        you will need as images, CSS, Javascript or other static content.
* **sitic. yml**: Every project made with Sitic must have a file
        in the project root. This one must have the name sitic.yml,
        using the YAML format. This setting applies to the entire entire site,
        which includes the `base_url` and `title` of the website.
