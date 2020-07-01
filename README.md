### pre-release

# Harvest text data from posts

This module takes a URL ( https://medium.com/series/sample-3d219d98b481 ) and emits either JSON or markdown as specified in the module
options.

This includes support for dynamically loaded content e.g. by clicking and scrolling.

## Setup 
1. Clone the repository
2. Set up your virtualenv
- `python3 -m pip install --user virtualenv`
- `python3 -m venv env`
- `source env/bin/activate`
3. Install packages 
- `pip install -r requirements.txt`
4. Run it 
- `python3 harvester.py https://medium.com/series/sample-3d219d98b481` 




## Setting up selenium (optional if you don't want to follow the result sets al the way to the end)
1. Download chromedriver following instructions on selenium's page 
2. Move chromedriver to /usr/local/bin (on Mac)
3. Add to path 
- `export PATH=$PATH:/usr/local/bin >> ~/.profile`
4. Remove from MacOS quarantine (thing that throws a message saying Apple cannot verify this application): 
- `xattr -d com.apple.quarantine chromedriver`
5. Run 
- `chromedriver` 
If you get driver output to the console, it has been installed correctly
