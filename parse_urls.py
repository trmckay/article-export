def first_non_url_char(word, start):
    """takes a string a returns the index of the first non-url character after the url begins"""

    delimiters = [" ", "\n", "\t", "]", ")", "}", ">", "<", "\"", ",", "|"]
    for i in range(start, len(word)):
        if word[i] in delimiters:
            return i
    return -1

def parse_urls(path):
    """takes a file as input and returns a list of all urls"""

    with open(path) as f:
        lines = f.readlines()
        words = []
        for line in lines:
            for word in line.split(" "):
                words.append(word)
        filtered_words = []
        for word in words:
            if word != '':
                filtered_words.append(word)
        words = filtered_words

        urls = []
        for word in words:
            if "http://" in word:
                urls.append(word[word.find("http://"):first_non_url_char(word, word.find("http://"))])
            if "https://" in word:
                urls.append(word[word.find("https://"):first_non_url_char(word, word.find("https://"))])
        return urls
