# Medium series to markdown

This module takes a medium series or a medium post and converts
it to markdown. This is not meant for either Medium RSS feeds or regular Medium posts or publications.
A sample medium series is https://medium.com/series/sample-3d219d98b481 

This module takes a medium URL and can emit either markdown or JSON. Support for selenium based auto scrolling of content is under progress

**Note**: Medium's support for RSS and the API is pretty limited. This module is based on a scraper  

## Setup 
1. Clone the repository
2. Set up your virtualenv
`virtualenv medium-mkdwn`
`source medium-mkdwn/bin/activate`
1. Run it and pipe the markdown to a file
`python3 get.py https://medium.com/series/sample-3d219d98b481`




## Setting up selenium 
1. Download chromedriver following instructions on selenium's page 
2. Move chromedriver to /usr/local/bin (on Mac)
3. Add to path `export PATH=$PATH:/usr/local/bin >> ~/.profile`
4. Remove from MacOS quarantine (thing that throws a message saying Apple cannot verify this application): `xattr -d com.apple.quarantine chromedriver`
5. Run `chromedriver`. If you get driver output to the console, it has been installed correctly