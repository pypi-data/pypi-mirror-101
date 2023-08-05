import argparse
import datetime
import hashlib
import logging
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile

import requests

class VideoJoiner:

    ffmpeg_release_archive = "ffmpeg-release-essentials.zip"
    ffmpeg_release_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    ffmpeg_sha256_url = "https://www.gyan.dev/ffmpeg/builds/sha256-release-essentials-zip"
    ffmpeg_version_url = "https://www.gyan.dev/ffmpeg/builds/release-version"

    ffmpeg_executables = (
        'ffmpeg.exe',
        'ffprobe.exe',
        'ffplay.exe',
    )

    homedir = os.path.join(
        os.getenv('APPDATA'),
        "videojoiner",
    )
    
    ffmpegdir = os.path.join(homedir, "ffmpeg")


    def __init__(self):
    
        if platform.system().lower() != "windows":
            self.log.critical("Invalid platform. Script is designed to run on Windows only.")
            sys.exit(1)
    
        self.log = logging.getLogger("VideoJoiner")
    
        os.makedirs(self.homedir, exist_ok=True)
        os.makedirs(self.ffmpegdir, exist_ok=True)

    def __download_ffmpeg(self):
        """ will download ffmpeg and store in APPDATA """
    
        # get expected ffmpeg version
        version_req = requests.get(self.ffmpeg_version_url)
        version_req.raise_for_status()
        ffmpeg_version = version_req.text
        self.log.debug(f"Expecting ffmpeg version {ffmpeg_version}")
    
        # get expected hash from url
        hash_req = requests.get(self.ffmpeg_sha256_url)
        hash_req.raise_for_status()
        
        expected_sha256 = hash_req.text
        self.log.debug(f"Expecting ffmpeg hash: {expected_sha256}")
    
        # open tempdir to download the file
        with tempfile.TemporaryDirectory(dir=self.homedir) as tempdir:

            temp_archive = os.path.join(tempdir, self.ffmpeg_release_archive)
            
            file_req = requests.get(self.ffmpeg_release_url, stream=True, allow_redirects=True)
            with open(temp_archive, "wb") as dlfile:
                for chunk in file_req.iter_content(chunk_size=16*1024):
                    dlfile.write(chunk)
                    
            # get hash of file
            sha256_hash = hashlib.sha256()
            with open(temp_archive, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
                checksum_sha256 = sha256_hash.hexdigest()
            del sha256_hash
            self.log.debug(f"Actual ffmpeg hash: {checksum_sha256}")
            
            # check hash, exit if does not match
            if checksum_sha256 != expected_sha256:
                self.log.critical("Downloaded archive does not match the expected checksum. Exiting")
                sys.exit(1)
                
            with zipfile.ZipFile(temp_archive, 'r') as ffmpeg_zip:
                
                extracted_bin_dir = os.path.join(
                    tempdir,
                    "extracted",
                    f"ffmpeg-{ffmpeg_version}-essentials_build",
                    "bin",
                )
                for x in self.ffmpeg_executables:
                    
                    ffmpeg_zip.extract(
                        f"ffmpeg-{ffmpeg_version}-essentials_build/bin/{x}",
                        path=os.path.join(tempdir, "extracted"),
                    )
                    
                    shutil.move(
                        os.path.join(extracted_bin_dir, x),
                        os.path.join(self.ffmpegdir, x),
                    )

    def ensure_ffmpeg(self, force=False):
        """ logical method to determine if ffmpeg needs to be downloaded or not """
        if force or not os.path.isfile(os.path.join(self.ffmpegdir, "ffmpeg.exe")):
            self.__download_ffmpeg()

    def run(self, input_vids, output_vid, ffmpeg_loglevel="info"):
        """ merge the video files """

        formatted_sources = map(
            lambda x: f"file '{x}'{os.linesep}",
            input_vids,
        )
        
        if not output_vid:
            output_vid = "merged_video_{date}{ext}".format(
                date=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                ext=os.path.splitext(input_vids[0])[1],
            )

        with tempfile.TemporaryDirectory(dir=self.homedir) as tempdir:
            sources_file = os.path.join(tempdir, "sources.txt")
            
            with open(sources_file, "w") as source_fd:
                source_fd.writelines(formatted_sources)
        
            cmd = [
                os.path.join(self.ffmpegdir, "ffmpeg.exe"),
                "-loglevel", ffmpeg_loglevel,
                "-f", "concat",
                "-i", sources_file,
                "-c", "copy",
                output_vid,
            ]
            
            subprocess.Popen(cmd).wait()
            
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", default=False,
        help="verbose output for troubleshooting",
    )
    
    parser.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", default=False,
        help="be more quiet, only fatal messages",
    )
    
    parser.add_argument(
        "-d", "--force-download", dest="force_download", action="store_true", default=False,
        help="force ffmpeg download",
    )
    
    parser.add_argument(
        "-o", "--output", dest="output_file", default="",
        help="specify output filename",
    )
    
    parser.add_argument(
        "inputvideos", nargs="+",
        help="space separated input files"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        script_loglevel = logging.DEBUG
        ffmpeg_loglevel = "verbose"
    elif args.quiet:
        script_loglevel = logging.WARNING
        ffmpeg_loglevel = "warning"
    else:
        script_loglevel = logging.INFO
        ffmpeg_loglevel = "info"

    logging.basicConfig(
        format="[%(levelname)s] [%(asctime)s] %(message)s",
        datefmt="%H:%M:%S",
        level=script_loglevel,
    )
    
    joiner = VideoJoiner()
    joiner.ensure_ffmpeg(force=args.force_download)
    joiner.run(args.inputvideos, args.output_file, ffmpeg_loglevel=ffmpeg_loglevel)
    
