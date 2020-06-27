import sys
import os
from pocket import Pocket, PocketException
from url_archive import archive


def init_kf():
    """initialize a keyfile"""
    try:
        os.remove('.keys')
    except:
        pass

    with open('.keys', 'w') as kf:
        ck = input("Consumer key: ")
        at = input("Access token: ")
        kf.write("{}\n{}\n".format(ck, at))


def authenticate():
    """attempt to log into Pocket servers using the key-pair in ./.keys"""

    kf_exists = False

    try:
        kf = open('.keys', 'r')
    except:
        print('Unable to find or access keyfile.')
        a = input('Initialize keyfile? [y/n]: ')
        if a == 'y' or a == 'Y':
            init_kf()
            return None
        else:
            exit()

    keys = kf.readlines()

    try:
        p = Pocket(keys[0][:-1], keys[1][:-1])
        print("Authentification success!")
        return p

    except PocketException:
        print('Authentification failed.')
        a = input('(T)ry again,\n(r)e-initialize keyfile,\nor (q)uit?\n[t/r/q]: ')
        if a == 'r' or a == 'r':
            init_kf()
            return None
        if a == 't' or a == 'T':
            return None
        else:
            print("Aborted.")
            exit()

    except IndexError:
        print('Invalid keyfile.')
        a = input('Re-initialize keyfile? [y/n]: ')
        if a == 'y' or a == 'Y':
            init_kf()
            return None
        else:
            print("Aborted.")
            exit()

    except Exception as e:
        print('Error: Unhandled exception: ', end='')
        print(e)
        exit()


def pocket_to_csv(flags):
    """get a list of articles from Pocket servers and output a csv catalog"""

    # print settings
    print("Settings:")
    print("  State: " + flags['state'])
    print("  Content type: " + flags['content_type'])
    print("  Maximum number of articles: " + str(flags['num']))
    print("  Output path: " + flags['dest'])
    print("  Filter by keyword: " + str(flags['do_keywords']))
    print("  Filter by source: " + str(flags['do_sources']))
    print("  Scan full article text: " + str(flags['scan_text']))

    # authenticate with Pocket
    p = None
    while p is None:
        p = authenticate()

    # get list of urls
    urls = []
    print("Getting list from Pocket... ", end='')
    lst = p.retrieve(state=flags['state'], contentType=flags['content_type'], offset=0, count=flags['num'])['list'].items()
    print("Done!")
    for i in lst:
        urls.append(i[1]['resolved_url'])

    # create and filter archive
    articles = archive(urls)
    articles.filter(\
        do_sources=flags['do_sources'],\
        sources_path=flags['sources_path'],\
        do_keywords=flags['do_keywords'],\
        keywords_path=flags['keywords_path'],\
        scan_text=flags['scan_text']
        )
    # output csv
    articles.to_csv(flags['dest'])


def usage(error_msg=''):
    """print usage message present in ./.usage"""

    print(error_msg, end='')
    try:
        umsg = open('.usage', 'r').read()
        print(umsg)
        exit()
    except Exception as e:
        print("Could not print usage message: " + str(e))
        exit()


def parse_flags():
    """parse cli for flags"""

    flags = {\
             'state': 'all',\
             'num': 1000,\
             'dest': 'pocket.csv',\
             'do_sources': False,\
             'sources_path': 'sources.txt',\
             'do_keywords': False,\
             'keywords_path': 'keywords.txt',\
             'scan_text': False,\
             'content_type': None \
            }
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]

        if arg == '--help': usage()

        elif arg == '--filter-keywords': flags['do_keywords'] = True
        elif arg == '--filter-sources': flags['do_sources'] = True
        elif arg == '--scan-text' : flags['scan_text'] = True

        elif arg == '-s':
            if i == len(sys.argv): usage("Error: Provide state following -s flag.\n")
            else:
                state = sys.argv[i+1]
                if state != 'all' and state != 'archive' and state != 'unread':
                    usage("Error: Not a valid state: {}.\n".format(state))
                flags['state'] = state

        elif arg == '-m':
            if i == len(sys.argv): usage()
            else:
                try:
                    num = int(sys.argv[i+1])
                except:
                    usage("Error: Not valid number: {}.\n".format(sys.argv[i+1]))
                if num < 1:
                    usage("Error: Max articles must be greater than 1.\n")
                flags['num'] = num

        elif arg == '-p':
            if i == len(sys.argv): usage("Error: Provide destination file following -f flag.\n")
            else:
                flags['dest'] = sys.argv[i+1]

        elif arg == '-c':
            if i == len(sys.argv): usage("Error: Provide content type following -f flag.\n")
            else:
                content_type = sys.argv[i+1]
                if content_type != 'all' and content_type != 'video' and content_type != 'article':
                    usage("Error: Provide a valid content type follow -c flag.\n")
                if content_type == 'all':
                    content_type = None
                flags['content_type'] = content_type

        elif sys.argv[i-1] != '-s' and sys.argv[i-1] != '-m' and sys.argv[i-1] != '-p' and sys.argv[i-1] != '-c':
            usage("Unrecognized flag: {}.\n".format(arg))
    return flags


def main():
    pocket_to_csv(parse_flags())

if __name__ == "__main__":
    main()
