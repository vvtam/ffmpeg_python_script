#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import subprocess as sp
import os
import logging

logging.basicConfig(filename='info.log', level=logging.WARNING)

def findfile():
    videoformat=(".mp4", ".ts", ".flv", ".mov")  #添加视频格式
    w = os.walk("./")
    for root, dirs, files in w:
        for name in files:
            if name.endswith(videoformat):
                with open('list', 'a') as f:
                    f.write(os.path.join(root, name))
                    f.write("\n")
                    
def transcode(filepath, outputdir):
    command = ["ffmpeg", "-y", "-i", filepath,
               "-loglevel",  "error",
               "-metadata", "service_name='Push Media'",
               "-metadata", "service_provider='Push Media'",
               "-c:v", "h264", #视频编码
               "-profile:v", "high", "-level:v", "4.0",
               "-x264-params", "nal-hrd=cbr",
               "-b:v", "4M", "-minrate", "4M", "-maxrate", "4M", "-bufsize", "2M", #cbr视频码率
               "-preset", "ultrafast",
               "-bf", "2", #B帧
               "-keyint_min", "25", "-g", "25", "-sc_threshold", "0",
               "-s", "1920x1080", #分辨率
               "-aspect", "16:9",
               "-r", "25",
               "-c:a", "aac", #音频编码
               "-b:a", "192K", "-ar", "48000", #音频码率
               "-f", "mpegts", "-muxrate", "5M", #cbr文件最大码率
               outputdir + ".ts"
               ]
    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    if pipe.returncode == 0:
        logging.info("command '%s' succeeded, returned: %s"
                     % (command, str(out)))
    else:
        logging.error("command '%s' failed, exit-code=%d error = %s"
                      % (command, pipe.returncode, str(err)))


def main():
    findfile()
    with open('list', 'r') as f:
        line = f.readline()
        while line:
            filepath = line.strip()
            filedir = os.path.splitext(filepath)
            outputdir = filedir[0]
            # 输出目录
            output_basedir = '.'
            outputdir = os.path.join(output_basedir, 'ts8M1080P', outputdir)
            # 输出目录
            outputdir = os.path.normpath(outputdir)
            output_basedir = os.path.dirname(outputdir)
            if os.path.exists(output_basedir):
                logging.info(output_basedir + ", the dir already exist.")
            else:
                logging.info(output_basedir + ", the dir create success.")
                os.makedirs(output_basedir)
            logging.warning(filepath)
            transcode(filepath, outputdir)
            line = f.readline()

if __name__ == '__main__':
    main()
