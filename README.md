# Medium series to markdown

This module takes a medium RSS feed and converts 
it to markdown

**Note**: Medium's support for RSS and the API is pretty limited. This module is based on a scraper and is pretty fragile itself. Contact me if something is broken and I will address it in a reasonable time

## Usage
1. Clone the repository
2. Set up your virtualenv
`virtualenv medium-mkdwn`
`source medium-mkdwn/bin/activate`
1. Run it and pipe the markdown to a file
`python3 get.py > ~/Downloads/series.md`