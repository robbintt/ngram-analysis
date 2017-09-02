''' Make n-grams from /usr/share/dict/words

We can make an exhaustive list of ngrams here for this dataset.

This will not tell us about ngram frequency in composed english.

We can use ngsl as a basis for ngram frequency.
There should be an ngsl file in the PyClass repository.
'''
import sqlite3

WORD_FILE = "/usr/share/dict/words"
NGRAM_DATABASE = "ngrams.sqlite3"

# compose a whitelist to filter the WORD_FILE: `/usr/share/dict/words`
letters = "abcdefghijklmnopqrstuvwxyz"
letters += letters.upper()


def clean_the_dictionary(contents):
    ''' Remove any letter that isn't whitelisted.

    The `/usr/share/dict/words` file only has two hyphenated words that 
    are cleaned out and both are names.
    '''
    dictionary = list()
    for word in contents.split("\n"):
        word = word.strip().lower()
        for letter in word:
            if letter not in letters:
                continue
        dictionary.append(word)

    # de-duplicate and convert back to a list
    dictionary = list(set(dictionary))

    return dictionary
    

def get_average_word_length(dictionary):
    ''' Get the average word length of an input
    '''
    # get the total length of the dictionary for averaging
    total = sum([len(word.strip()) for word in dictionary])

    # average the dictionary
    return float(total) / len(dictionary)


def add_ngrams(input_string):
    ''' Take a string and add all the ngrams to the ngram list
    '''
    pass


if __name__ == '__main__':
    ''' This is the main area
    '''
    # get the dictionary words 
    with open(WORD_FILE) as f:
        contents = f.read()

    dictionary = clean_the_dictionary(contents)

    # used for db size calculations
    average_word_length = get_average_word_length(dictionary)

    # need to build dict of ngrams for sqlite storage

    conn = sqlite3.connect(NGRAM_DATABASE)
    c = conn.cursor()

    # table should take (ngram, freq)
    table = 'ngrams'
    INSERT_TEMPLATE = 'INSERT INTO  {table} VALUES (?,?)'
    INSERT_TEMPLATE = INSERT_TEMPLATE.format(table=table)

    c.executemany(INSERT_TEMPLATE, ngrams)





