Web-scraper
---

# How to use

1. download the zip file
2. unzip the zip file in an empty folder or just pull the folder in the zip file in a folder.
3. open settings.json
   1. ``["https://www.elle.de/", "elle", false],``
      1. ``https://www.elle.de`` url to root site
      2. ``elle`` name of the site (you decide)
      3. ``false`` if it should use selenium ``true`` else ``false`` only use selenium if necessary
   2. ``"browser": "chrome"`` browser
      1. if you use chrome: ``"browser": "chrome"``
      2. if you use firefox: ``"browser": "firefox"``
   3. put it (if needed in the autostart)

If you run into any issues, open an issue in this GitHub page or write me a mail: Lars.Noack@outlook.de

Analysing the data
---

I use analyze the data from following sites (every other site is even more crap):
- bleib gesund
- cosmopolitan
- brigitte
- elle
- jolie

# data preparation for cluster analysis

## read raw data

The data is saved in a folder, where every sub folder is named a date. In the sub folder there are every data from a day. For every available magazine one json file.

I am only reading the data of the above-mentioned magazines. I am returning this number with a custom iterator. Every iteration it returns a dictionary, where the keys are the names of the magazines and the value being the according content. It also returns the date in utc.

## keyword analysis

I am using [yake](https://pypi.org/project/yake/) to analyze 20 keywords from the body and 1 from the header, and returning it as sorted list, by importance.

The function to do so takes in a dictionary of the read data of a day, and some constants. It returns a dictionary where the key being again the magazines, and the values beeing a list containing a list containing all extracted keywords with the importance. Per article the list is sorted by importance and contains `KEYWORDS_PER_ARTICLE = 10` keywords.

``Note: The closer the importance of the keywords are, the more important it is.``

Due to the headers being less accurate, because yake can only extract keywords from larger texts well, I just multiply the importance of the keywords in the header by a factor of `HEADER_IMPORTANCE_FACTOR = 1.5`.

### filter out "index site"

There are some sites, just linking to other articles. To filter those out, I count the number of chars in the text and divide those with the number of chars in all headers. If this value is greater than `MIN_TEXT_HEADER_RATIO = 2`, then it is a real article.
`
