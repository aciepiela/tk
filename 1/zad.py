import os
import sys
import re
import codecs

author_pattern = re.compile(r'(META NAME="AUTOR" CONTENT=")(.+?)(">)')


def find_author(content):
    return re.search(author_pattern, content).group(2)


category_pattern = re.compile(r'(META NAME="DZIAL" CONTENT=")(.+?)(">)')


def find_category(content):
    return re.search(category_pattern, content).group(2)


key_words_pattern = re.compile(r'(META NAME="KLUCZOWE_(\d+?)" CONTENT=")(.+?)(">)')


def find_key_words(content):
    key = re.findall(key_words_pattern, content)
    if key:
        to_return = key[0][2]
        for tuple in key[1:]:
            to_return = to_return + ", " + tuple[2]
    else:
        to_return = ""
    return to_return


emails_string = r'([\w\-]+(\.[\w\-]+)*@([\w\-]+\.)+[a-zA-Z]{1,4})'
emails_pattern = re.compile(emails_string, re.I)


def find_emails(content):
    return len(set(re.findall(emails_pattern, content, )))


abbreviations_string = r'(?<=\s)([A-Za-z]{1,3}\.)(?=\s|$)'
abbreviations_pattern = re.compile(abbreviations_string, re.MULTILINE)


def find_abbreviations(content):
    a = re.findall(abbreviations_pattern, content)

    unique = set()

    for tuple in a:
        unique.add(tuple[0])

    return len(unique)


integers_pattern = re.compile(r'(?<=\D)(-32768|-?[0-9]|-?[1-9][0-9]|-?[1-9][0-9][0-9]|-?[1-9][0-9][0-9][0-9]|'
                              r'-?[1-2][0-9][0-9][0-9][0-9]|-?3[0-1][0-9][0-9][0-9]|'
                              r'-?32[1-6][0-9][0-9]|-?327[0-5][0-9]|-?3276[0-7])(?=\D|$)')


def find_integers(content):
    return len(set(re.findall(integers_pattern, content)))


dates_string = r'((((?P<twentynine>(0[1-9]|[1-2][0-9]))|(?P<thirty>30)|(?P<thirtyone>31))' + \
               r'(?P<delimiter>[-///.])' + \
               r'(?(twentynine)(0[1-9]|1[0-2]))(?(thirty)(0[13456789]|1[0-2]))(?(thirtyone)(0[13578]|1[02]))' + \
               r'(?P=delimiter)' + \
               r'(\d{4}))' + \
               r'|' + \
               r'((\d{4})' + \
               r'(?P<delimiterr>[-///.])' + \
               r'((?P<twentyninee>(0[1-9]|[1-2][0-9]))|(?P<thirtyy>30)|(?P<thirtyonee>31))' + \
               r'(?P=delimiterr)' + \
               r'(?(twentyninee)(0[1-9]|1[0-2]))(?(thirtyy)(0[13456789]|1[0-2]))(?(thirtyonee)(0[13578]|1[02]))))'
dates_pattern = re.compile(dates_string)


def find_dates(content):
    f = re.findall(dates_pattern, content)
    unique = set()
    for match in f:
        split = re.split(r'[-\/\.]', match[0])
        if len(split[0]) == 4:
            unique.add(split[0] + split[1] + split[2])
        else:
            unique.add(split[2] + split[0] + split[1])
    return len(unique)


float_string = r'(^|\s)([+-]?(\d+\.(\d*)?|\.\d+)([eE][+-]?\d+)?)(?=[\.,]?(?=$|\s))'
float_pattern = re.compile(float_string)


def find_floats(content):
    f = re.findall(float_pattern, content)
    unique = set()
    for num in f:
        unique.add(float(num[1]))
    return len(unique)


sentences_string = r'((^|\s)(((?<=\s)(([a-zA-Z0-9_]\.?)+(?<![\.])@([a-zA-Z]\.?)+(?<=[\.])[a-zA-Z]+)(?=\s))' \
                   r'|((?<=\s)[+-]?((\d*[\.\,]\d+([eE][+-]\d+)?)' \
                   r'|(\d+[\.\,]))(?=\s))|\s[A-Za-z]{1,3}\.\s|[^.])+[\?\.\!\n]+)'
sentences_pattern = re.compile(sentences_string, re.MULTILINE)


def find_sentences(content):
    return len(re.findall(sentences_pattern, content))


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

    author = find_author(content)
    category = find_category(content)
    keyWords = find_key_words(content)

    text = re.search(r'(<P)(.*?)(<META)', content, re.S).group()
    emails = find_emails(text)
    abbr = find_abbreviations(text)
    integers = find_integers(text)
    dates = find_dates(text)
    floats = find_floats(text)
    sentences = find_sentences(text)

    fp.close()
    print "nazwa pliku: " + filepath
    print "autor: " + author
    print "dzial: " + category
    print "slowa kluczowe: " + keyWords
    print "liczba zdan:" + str(sentences)
    print "liczba skrotow: " + str(abbr)
    print "liczba liczb calkowitych z zakresu int: " + str(integers)
    print "liczba liczb zmiennoprzecinkowych: " + str(floats)
    print "liczba dat:" + str(dates)
    print "liczba adresow email:" + str(emails)
    print("\n")


try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)

tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)
