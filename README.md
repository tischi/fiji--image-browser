# fiji--image-browser

This repository conatins a Fiji script to browse all image sets in a folder (including sub-folders).
Images belong to the same image set if the share the same file- and foldernames before the last '--' in the filename.

For example:
```
- image set 1: ...pos1/aaa--bbb--c01.tif, ...pos1/aaa--bbb--c02.tif
- image set 2: ...pos2/ccc--bbb--c01.tif, ...pos2/ccc--bbb--c02.tif
```

For questions please contact: tischitischer@gmail.com

### installation and running

- install Fiji: https://fiji.sc/
  - you need a Fiji with java 1.8  
- download and extract this repository: https://github.com/tischi/fiji--image-browser/archive/master.zip
  - in the extracted repository you will find a file called: __AutoMic_JavaTools-1.1.0-SNAPSHOT-19072016.jar__; this file must be moved to your Fiji's plugin folder
  - you will also find a file called __fiji--image-browser.py__; this can be on any location on your computer; to run it simply drag onto Fiji and click __[Run]__ at the bottom of the automatically appearing script editor
  - now simply select the folder containing your data


### usage notes

- if you examine your images in a zoomed-in mode you have to check __Fit image to frame__ on the left of the table.
