# Medium series to markdown

This module takes a medium series and converts
it to markdown. This is not meant for either Medium RSS feeds or regular Medium posts or publications

**Note**: Medium's support for RSS and the API is pretty limited. This module is based on a scraper

## Usage
1. Clone the repository
2. Set up your virtualenv
`virtualenv medium-mkdwn`
`source medium-mkdwn/bin/activate`
1. Run it and pipe the markdown to a file
`python3 get.py > ~/Downloads/series.md`