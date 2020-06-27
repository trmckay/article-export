### PURPOSE ###
Export your Pocket reading list as a CSV file.

### PREREQUESITES ###
- python3
- pip

### SET-UP ###
- Run ./setup.sh to install dependencies.
- Consider adding ./article-export to your PATH and alias article-export="python3 export.py" so you can use 'article-export' as a bash command.
- Generate a new consumer ID at https://getpocket.com/developer/
    - Create new app.
    - Give it a name (i.e. article-archiver).
    - Give it a description.
    - Under permissions, check 'Retrieve'.
    - Under platforms, check 'Desktop (other)
    - Accept the terms and continue.
    - Make a note of the consumer ID.
- Authorize the app. You can do this yourself, or use [this website](http://reader.fxneumann.de/plugins/oneclickpocket/auth.php) to do so. Make a note of the access token.

### USAGE ###

Run export.py with your desired flags and options. If no keys are found you will be prompted to input them. If you are filtering by source or keyword, make sure to add them to ./article-export/sources.txt and ./article-export/keywords.txt, respectively.

```
python3 export.py [-s state] [-c type] [-m number] [-p path] [OPTIONS]

FLAGS
    -s <state>: export only articles with the following state
        all: export all articles (default)
        unread: export only unread articles
        archive: export only archived articles

    -c <type>: export only articles with the following content type
        all: all items in list (default)
        article: only articles
        video: only videos (buggy)

    -m <number>: export a maximum of this many articles

    -p <path>: save the csv output to the provided path

OPTIONS
    --help: show this again
    --filter-keywords: only keep articles that contain keywords in keywords.txt (separated by newline)
    --filter-sources: only keep articles that come from sources in sources.txt (separated by newline)
    --scan-text: additionally parses full article text for keywords
```

### AKNOWLEDGEMENTS ###

## Newspaper ##
Lucas Ou-Yang : https://github.com/codelucas/newspaper/

## pocket-api ##
Rakan Alhneiti : https://github.com/rakanalh/pocket-api
