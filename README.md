# serve_file

A very simple python script to serve a single file locally through HTTP, by using the SimpleHTTPRequestHandler.

I built this for using gradle, because it tries to download the latest gradle package from gradle.org, which is extremely slow to access from China. Now I can download it separately and serve it locally by modifying gradle-wrapper.properties.

Obviously it can be used in other situations. Usable is straight forward with only parameter being the file to serve. Access from non-localhost will be denied with 404 error.
