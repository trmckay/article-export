from newspaper import Article

def match_source(article, sources):
    for source in sources:
        if source.lower() in article.url.lower():
            return True
    return False


def match_keyword(article, keywords):
    for keyword in keywords:
        if keyword.lower() in article.url.lower():
            return True

        for keyword in keywords:
            if keyword.lower() in article.title.lower():
                return True
        return False


class article_archive:

    def __init__(self, urls):
        self.articles = []
        unique_urls = set(urls)

        for url in unique_urls:
            article = Article(url)
            self.articles.append(article)


    def filter(self, sources_path, keywords_path):
        sources = []
        keywords = []
        filtered_articles = []

        try:
            sources = open(sources_path, 'r').read().splitlines()
            keywords = open(keywords_path, 'r').read().splitlines()
        except:
            print("Could not open required sources.txt or keywords.txt!")
            exit()

        print("Accepted sources:")
        for source in sources:
            print("\t"+source)
        print("\nAccepted keywords:")
        for keyword in keywords:
            print("\t"+keyword)
        print('')

        i = 0
        s = 0
        d = 0
        f = 0
        for article in self.articles:
            print('Progress: {:.1%}'.format(i/len(self.articles)), end='\r')
            i += 1
            try:
                article.download()
                article.parse()
            except:
                s += 1
                continue
            if match_source(article, sources) or match_keyword(article, keywords):
                filtered_articles.append(article)
                f += 1
            else:
                d += 1

        print("{} saved, {} discarded, and {} skipped.".format(f, d, s))
        return filtered_articles


def to_csv(articles, filename):
    with open(filename, 'w') as f:

        f.write("title,date,authors,url\n")

        for article in articles:
            f.write("\"" + article.title + "\",")

            if article.publish_date is not None:
                f.write(\
                    str(article.publish_date.month) + "/" +\
                    str(article.publish_date.day) + "/" +\
                    str(article.publish_date.year) + ",\"")
            else:
                f.write(",\"")

            for j in range(0, len(article.authors)):
                f.write(article.authors[j])
                if len(article.authors) > 1 and j < len(article.authors)-1:
                    f.write(", ")
            f.write("\",")

            f.write(article.url + "\n")
        print("Output saved to " + filename + ".")

