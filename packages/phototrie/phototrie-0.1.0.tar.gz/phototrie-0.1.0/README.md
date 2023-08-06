# phototrie (and other helper scripts)

Phototrie is a minimalistic application for quickly sorting through your
photographs.

This repository also includes `batchrename` and `datename`, two commands useful
for organising photographs.


## Usage

### phototrie

Run `phototrie JPG` in a directory where you have unsorted `JPG` photos.

`CR2` photos in the same directory, or in a `CR2/` subdirectory,
with the same name will also be processed.

Wait a short while for thumbnails to be generated. Once this has completed,
a window will pop up, showing your photos.

Press `B` to mark a photo as *bad*, `G` for *good* and `P` for *pristine*
(future versions may allow custom names).

Phototrie will move them into directories with those labels as you go along.


### datename

`datename photo1.jpg photo2.jpg` (etc)

e.g. `datename *.JPG` to process all JPG files in a directory.

This will rename photos to have their date (as stored in EXIF) as their name.

`CR2` photos in the same directory, or in a `CR2/` subdirectory,
with the same name will also be processed.

Once you are ready to apply the changes for real, pass `--apply` (or `-y`).


### batchrename

`batchrename <regex> <replacement> photo1.jpg photo2.jpg` (etc)

e.g. `batchrename .JPG$ .jpg *.JPG`

Once you are ready to apply the changes for real, pass `--apply` (or `-y`).


## Installation

You will probably need to install (on Debian/Ubuntu):

`apt install python3-dev python3-pip python3-tk python3-pil python3-pil.imagetk`

Then you can use:

`pip3 install --user phototrie`

(or, install from this repository: `pip3 install --user git+https://bics.ga/reivilibre/phototrie`)
