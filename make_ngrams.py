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
                print word
                continue

        # remove the word if the word is too short to contain length 2+ n-grams
        if len(word) < 2:
            print word
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


def get_some_ngrams(size, word):
    ''' get all the <size>-grams for <word>
    word => string
    size => int

    returns a list of ngrams
    '''
    some_ngrams = list()
    
    # the max range integer we should pass is len(word)+1
    for i in range(len(word)-size+1):
        some_ngrams.append(word[i:i+size])

    return some_ngrams


def make_ngrams(dictionary):
    ''' make the dict of ngrams from a word dictionary
    dictionary => list()

    return a list of strings
    '''
    ngrams = list()
    count = 0
    for word in dictionary:
        # get all the ngrams for the word
        for size in range(2,len(word)):
            ngrams.extend(get_some_ngrams(size, word))

        # a temporary clause to count word progress
        count += 1
        if count % 100:
            print "{} words or {}% of ~235886".format(count, float(count)/235886)

    return ngrams


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
    ngrams = make_ngrams(dictionary)

    # assemble the frequency dict from the expanded ngram list
    # this list is estimated to be 65 megabytes (the dict should be smaller by some amount)
    print("Assembling the ngram dictionary...")
    ngram_freq_dict = dict()
    for ngram in ngrams:
        ngram_freq_dict[ngram] = ngram_freq_dict.get(ngram, 0) + 1

    conn = sqlite3.connect(NGRAM_DATABASE)
    c = conn.cursor()

    # table should take (ngram, freq)
    table = 'ngrams'
    INSERT_TEMPLATE = 'INSERT INTO {table} VALUES (?,?)'
    INSERT_TEMPLATE = INSERT_TEMPLATE.format(table=table)

    print("Inserting ngrams into ngrams sqlite3 table.")
    for ngram, freq in ngram_freq_dict.items():
        # check it out!!
        if freq > 10:
            print ngram, freq
        c.execute(INSERT_TEMPLATE, (ngram, freq))

    print("Commit the database entries (many MBs)")
    conn.commit()
    conn.close()

