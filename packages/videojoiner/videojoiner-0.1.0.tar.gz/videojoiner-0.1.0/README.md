# VideoJoiner

Videojoiner is a simple python script to help joining video parts together.  It's designed to run in windows only, will download ffmpeg builds from https://www.gyan.dev/ffmpeg/builds/, then use it to concatenate video files.

The ffmpeg binaries are stored in `%APPDATA%/videojoiner/ffmpeg` and will only be downloaded if missing or the '-d/--force-download' flag is passed.

The output filename can be specified, or it will autogenerate a video file formatted `merged_video_YYMMDD_HHMMSS.EXT` where the extension is copied from the first file in the input list.

## Example:

```
videojoiner.py source1.mp4 source2.mp4 source3.mp4
```

## Usage

```
videojoiner.py -h
usage: videojoiner.py [-h] [-v] [-q] [-d] [-o OUTPUT_FILE] inputvideos [inputvideos ...]

positional arguments:
  inputvideos           space separated input files

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose output for troubleshooting
  -q, --quiet           be more quiet, only fatal messages
  -d, --force-download  force ffmpeg download
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        specify output filename
```
