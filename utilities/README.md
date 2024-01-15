# Utilities

Various utilities and scripts to make life easier

## Headless Google Chrome:

```
#
# Install google chrome on Ubuntu
#
apt-get install fonts-liberation libu2f-udev
dpkg -i google-chrome-stable_current_amd64.deb
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

#
# Command to use google chrome to get a URL and dump it to STDOUT
#
google-chrome --no-sandbox \
--crash-dumps-dir=/tmp/www \
--disable-crash-reporter \
--headless --disable-gpu \
--enable-javascript \
--dump-dom https://seifried.org/ \
2>/dev/null 
```
