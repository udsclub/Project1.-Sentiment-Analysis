# Datasets Summary

All datasets with their description – https://docs.google.com/spreadsheets/d/12WNfuql2WWcB7ufCvZy12u5bd3zhuJlVHdIu2p1ysQQ/edit

### Iherb Dataset
1. source – http://www.iherb.com , parser – iherb.py, topic – Vitamins, Supplements & Natural Health Products
2. n_reviews – 879747, mean label = 4.38, median = 5
3. average review length = 141.90, average number of words = 26.68
4. top-10 – I, and, the, '', a, to, it, is, for, this
5. <3 = 12.16%, 4-10 = 22.20%, 11-50 = 51.58%, >51 = 14.04%
6. number of duplicates = 112730

### iTunes App Store Dataset
1. source – https://itunes.apple.com/us/, topic – app reviews, iOS
2. n_reviews – 16115674, mean label = 4.16, median = 5
3. average review length = 130.50, average number of words = 25.73
4. top-10 – the, I, to, and, it, a, is, app, this, of
5. <3 = 4.75%, 4-10 = 30.25%, 11-50 = 52.36%, >51 = 12.64%
6. number of duplicates = 1539296, 9.55%

### RottenTomatoes DataSet
1. source – https://www.rottentomatoes.com , parser – rt_scraper.py, topic – Movies
2. n_reviews – 102610, mean label = 0.63, median = 1
3. average review length = 113.24, average number of words = 19.59
4. top-10 – the, of, a, and, to, is, in, that, as, it
5. <3 = 2.8%, 4-10 = 20.76%, 11-50 = 76.43%, >51 = 0.01%
6. number of duplicates = 307

### Expedia Dataset
1. source – http://www.expedia.com , parser – expedia.py, topic – Hotels, apartments
2. n_reviews = 2 731 949, n_hotels= 19 639, mean label = 3.86, median = 4.0, min = 1, max = 5
3. average review length = 286.46, average number of words = 52.79
4. top-10 – the, and, was, to, a, i, in, we, of, for
5. <4 = 0.45%, 4-10 = 7.07%, 11-50 = 55.78%, >51 = 36.68%
6. number of duplicates = 7 316

### Goodreads DataSet
1. source – https://www.goodreads.com , parser – goodreads.py, topic – Book
2. n_reviews – 459390, mean label = 3.81, median = 4
3. average review length = 1595.26, average number of words = 287.11
4. top-10 – the, and, to, a, I, of, is, in, that, was
5. <3 = 0.36%, 4-10 = 2.27%, 11-50 = 16.21%, >51 = 81.14%
6. number of duplicates = 1467

### Prom Dataset (1)
0. language – Russian
1. source – https://prom.ua , parser – coming soon..., topic – Opinions about companies/sellers
2. n_reviews – 201744, mean label = 3.0, min = 1, max = 5
3. average review length = 177.6, average number of words = 26.04
4. top-10 – что, товар, заказ, все, очень, спасибо, мне, так, как, товара
5. word count – <4 = 1.60%, 4-10 = 20.86%, 11-50 = 58.79%, >51 = 14.61%
6. number of duplicates = 0

### Prom Dataset (2)
0. language – Ukrainian
1. source – https://prom.ua , parser – coming soon..., topic – Opinions about companies/sellers
2. n_reviews – 17456, mean label = 3.0, min = 1, max = 5
3. average review length = 176.35, average number of words = 25.91
4. top-10 – товар, замовлення, все, дуже, рекомендую, але, дякую, так, мені, товару
5. word count – <4 = 1.46%, 4-10 = 20.91%, 11-50 = 58.82%, >51 = 14.36%
6. number of duplicates = 0

### Yelp Academic Dataset
1. source – https://www.yelp.com , topic – Local businesses
2. n_reviews – 4153150, mean label = 3.72, median = 4, min = 1, max = 5
3. average review length = 631.23, average number of words = 120.23
4. top-10 – the, and, '', I, a, to, was, of, is, for
5. <3 = 0.020%, 4-10 = 0.38%, 11-50 = 27.49%, >51 = 72.09%
6. number of duplicates = 2342

### Lovehoney Dataset
1. source - lovehoney.co.uk, lovehoney.py topic - sex-goods
2. n_reviews - 158089, mean label - 4.11, median - 4.0
3. average review length = 804.11, average number of words = 151.57
4. top-10 - the, and, a, to, I, it, is, of, for, this
5. word count – 3 = 0.005%, 4-10 = 0.05%, 11-50 = 4.66%, >51 = 95.28%
6. number of duplicates = 104

### TripAdvisor.com UK/GB Restaurants Dataset
0. language – en_GB
1. source – https://www.tripadvisor.com/ , parser – inner c# code, topic – Restaurants, Food
2. n_reviews – 1000000, mean label = 4.09, median = 5, min = 1, max = 5
3. average review length = 502.10, average number of words = 93.92
4. top-10 – the, and, a, to, was, '', of, for, I, .
5. word count – <4 = 0.005%, 4-10 = 0.02%, 11-50 = 32.15%, >51 = 67.83%
6. number of duplicates = 165
7. total n_reviews in other batch files - 10635553

### Amazon Books Dataset
0. language - English
1. source - amazon.com, topic - books. ranking varies from 1 to 5 stars
2. number of reviews ~63k, mean ranking - 5, median - 4.543
3. average review length - 40.6 words and 221.1 symbols
4. top 10 words - the, and, to, I, a, of, is, in, book, this
5. word count: 1-2 words - 9%; 3-9 words - 20%; 10-49 words - 50%; 50+ words - 21%
6. number of duplicates - 5427

### Airbnb USA Rooms/Flats Dataset
0. language - English
1. source - airbnb.com, topic - rooms/flats
2. number of reviews ~204k, mean ranking - 0.37, median - 0.33, max - 5, min-0
3. average review length - 52.1 words and 221.1 symbols
4. top 10 words - and, the, was, to, a, is, I, in, very, we
5. word count: <4 - 2%; 3-11 - 7%; 10-49 - 50.1%; 50> - 38.5%
6. number of duplicates - 0
