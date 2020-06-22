import sys
from articles import article_archive
from parse_urls import parse_urls

def pexport_to_csv(pexport, csv_out, allowed_sources_f):
    urls = parse_urls(pexport)
    articles = article_archive(urls)
    articles.filter_sources(allowed_sources_f)
    articles.to_csv(csv_out)

if __name__ == "__main__":
    pexport = sys.argv[1]
    csv_out = sys.argv[2]
    allowed_sources_f = "sources.txt"
    pexport_to_csv(pexport, csv_out, allowed_sources_f)
