# Utilities

Various utilities and scripts to make life easier

## Lessons learned:

JSON isn't much bulkier than markdown, but converting everything to markdown makes it easier to feed into AI prompts.

HTML is 2-3x bulkier than markdown, so definitely convert things to markdown.

PDF is much larger than markdown text.

Excel has a 32k character/cell size limit and Google sheets has a 50k chartacter/cell limit. This means we can't reliably put the data from files into the sheet. You will need to get the markdown files from Google Drive or run the downloader yourself.

