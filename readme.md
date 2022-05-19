How to use the Tool
---

1. download the zip file
2. unzip the zip file in an empty folder or just pull the folder in the zip file in an foleder.
3. open settings.json
   1. ``["https://www.elle.de/", "elle", false],``
      1. ``https://www.elle.de`` url to root site
      2. ``elle`` name of the site (you decide)
      3. ``false`` if it should use selenium ``true`` else ``false`` only use selenium if necessary
   2. ``"browser": "chrome"`` browser
      1. if you use chrome: ``"browser": "chrome"``
      2. if you use firefox: ``"browser": "firefox"``
   3. put it (if needed in the autostart)

If you run into any issues, open an issue in this github page or write me a mail: Lars.Noack@outlook.de

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

The data is saved in a folder, where every subfolder is named a date. In the subfolder there are every data from a day. For every available magazine one json file.

I am only reading the data of the above mentioned magazines. I am returning this number with a custom iterator. Every iteration it returns a dictionary, where the keys are the names of the magazines and the value being the according content. It also returns the date in utc.