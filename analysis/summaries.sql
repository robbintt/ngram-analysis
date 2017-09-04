select * from ngrams where frequency > 1000 and length(ngram) > 3 order by frequency;
