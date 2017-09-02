## Get ngrams from a source document

Getting every ngram would be pretty expensive, the max length is around
the length of `/usr/bin/share/dict` minus the number of lines.

The max number of n-grams in a word is the sum of:

bigrams: (len-1)+1
trigrams: (len-2)+1
4-grams: (len-3)+1
n-grams: (len-n)+1 where len==n, this represents the full word

### Working backwards:

```
A word of length 2 has one n-gram, itself: (2-2)+1 = 0
A word of length 3 has three n-grams: (3-3)+1 + (3-2)+1 = 1 + 2 = 2! = 3
A word of length 4 has 6 n-grams: (4-4)+1 + (4-3)+1 + (4-2)+1 = 1 + 2 + 3 = 3! = 6
A word of length 5 has _ n-grams: (5-5)+1 + (5-4)+1 + (5-3)+1 + (5-2)+1 = 1 + 2 + 3 + 4 = 4! + 10

So, the number of bigrams in the word dictionary is the factorial of the average length of the word in `/usr/bin/share/dict`.
I don't know how to do decimal factorials so hopefully it is a whole number...
The average word length in `/usr/bin/share/dict` is: 9.56908604544
Using an upper bound of 10, we expect 55 n-grams per word.
We have 235886 lines in `/usr/bin/share/words`
This means `235886 * 55 == 12,973,730` is the upper bound for ngrams. 
The size of this set would probably have an average length of 5 bytes.
The max size of the ngram dictionary would be ~13 * ~5 = 65 megabytes
The size will be lower due to duplicates, perhaps 50-80% of upper bound. 
Also allocate an int for each ngram to measure quantity of ngrams.
```

### README from `/usr/share/dict/words`

```
#	@(#)README	8.1 (Berkeley) 6/5/93
# $FreeBSD$

WEB ---- (introduction provided by jaw@riacs) -------------------------

Welcome to web2 (Webster's Second International) all 234,936 words worth.
The 1934 copyright has lapsed, according to the supplier.  The
supplemental 'web2a' list contains hyphenated terms as well as assorted
noun and adverbial phrases.  The wordlist makes a dandy 'grep' victim.

     -- James A. Woods    {ihnp4,hplabs}!ames!jaw    (or jaw@riacs)

Country names are stored in the file /usr/share/misc/iso3166.


FreeBSD Maintenance Notes ---------------------------------------------

Note that FreeBSD is not maintaining a historical document, we're
maintaining a list of current [American] English spellings.

A few words have been removed because their spellings have depreciated.
This list of words includes:
    corelation (and its derivatives)	"correlation" is the preferred spelling
    freen				typographical error in original file
    freend				archaic spelling no longer in use;
					masks common typo in modern text

--

A list of technical terms has been added in the file 'freebsd'.  This
word list contains FreeBSD/Unix lexicon that is used by the system
documentation.  It makes a great ispell(1) personal dictionary to
supplement the standard English language dictionary.
```
