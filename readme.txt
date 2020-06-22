This script uses Newspaper by Lucas Ou-Yang.

It is intended for use with Pocket, which allows you to export your articles as an html file. However, due to the way the URLs are parsed, it may work with other text files that contain URLs.

Requirements:
    Newspaper (pip3 install newspaper3k)

Usage:
    Add acceptable sources to 'sources.txt' separated by newline. Leave it empty to file all articles.
    Run the executable 'pexport' with the exported html from Pocket as the first argument and the destination file with '.csv' extension as the second argument.
