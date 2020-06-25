import sys
from articles import article_archive
from articles import to_csv
from parse_urls import parse_urls

def pexport_to_csv(pexport, csv_out, sources, keywords):
    urls = parse_urls(pexport)
    articles = article_archive(urls)
    to_csv(articles.filter(sources, keywords), csv_out)

if __name__ == "__main__":
    pexport = sys.argv[1]
    csv_out = sys.argv[2]
    sources = "sources.txt"
    keywords = "keywords.txt"
    pexport_to_csv(pexport, csv_out, sources, keywords)
