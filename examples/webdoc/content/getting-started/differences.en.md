+++
weight=2
title='Difference with dynamic generators'
+++

Web site generators generate content in HTML files. Most of them are "dynamic generators".
This means that the HTTP server (which is the program running on your website with which the browser of the
user speaks) runs the generator to create a new HTML file each time a user wants to view a page.

Dynamically creating the page means that the machine hosting the HTTP server has to have enough
CPU and memory to run the generator efficiently all day long. If not, then the user has to
wait for the page to be generated.

No one wants users to expect more than necessary, so dynamic site generators programmed
their systems to cache HTML files. When a file is cached, a copy is copied to
stores temporarily in the equipment. It's much faster for the server to send that copy the next time it's sent
the page is requested instead of being generated from scratch.

Sitic tries to take caching one step further. All HTML files are represented on your machine.
You can check the files before you copy them to the host on the HTTP server. Given that the HTML files
are not generated dynamically, we say that Sitic is a "static generator".

Not having to run HTML generation every time a request is received has several advantages. Among them,
the most notable is the performance, HTTP servers are very good at sending files. So good that he can
Efficiently serve the same number of pages with a fraction of memory and CPU required for a dynamic site.

Sitic has two components to help you build and test your website. The one you will probably use most often is the
HTTP server built in. When you run the server, Sitic processes all its content into HTML files and then runs
an HTTP server on your machine so you can see what the pages look like.

The second component is used once the site is ready to be published.
Running Sitic without any action will rebuild your entire website using the `base_url` configuration
from your site's configuration file. This is necessary for your page links to work properly 
with most lodging companies.
