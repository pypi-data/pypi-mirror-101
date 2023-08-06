# Paste it
Paste it is a python script that I made to upload files to pastebin using requests. it aims to be fast and light and hence doesn't support a large array of options. Currently paste_it reads from json.config in the directory its launched from, in the future it may support reading from appdata dirs using the `appdirs` python library. I don't intened for this to be used as a library but it can be used as one if you wish to, all functions do have docstrings incase you do decied to use this a library.
## Usage

```
usage: paste_it [-h] [--format FORMAT] [--private PRIVATE] [--title [TITLE]] path

positional arguments:
  path               file who's contents you want to paste on pastebin

optional arguments:
  -h, --help         show this help message and exit
  --format FORMAT    format of the file contents. you can find the avalible formats at https://pastebin.com/doc_api
  --private PRIVATE  if your file should be privte, 0 public, 1 unlisted, 2 Private (only allowed in combination with api_user_key, as you have to be logged into your account to
                     access the paste)
  --title [TITLE]    the title of your paste
  ```
  
