#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import subprocess as sp
import json
import os
import logging

logging.basicConfig(filename='hls.log', level=logging.WARNING)


def findvideofile():
    videoformat = (".mp4", ".ts", ".flv", ".mov")  # 可以添加各种ffmpeg支持的视频格式
    w = os.walk("./")
    for root, dirs, files in w:
        for name in files:
            if name.endswith(videoformat):
                with open('videolist', 'a') as f:
                    f.write(os.path.join(root, name))
                    f.write("\n")


def transcode(filepath, outputdir):
    outputdir = os.path.join(outputdir, "playlist.m3u8")
    command = ["ffmpeg", "-y", "-i", filepath,
               "-loglevel", "error",
               "-metadata", "service_name='Push Media'",
               "-metadata", "service_provider='Push Media'",
               "-c:v", "h264",
               # "-profile:v", "high", "-level:v", "4.1",
               "-b:v", "4M",
               # "-preset", "faster"",
               #"-s", "1920x1080",
               #"-aspect", "16:9",
               #"-r", "25",
               "-c:a", "aac",
               "-b:a", "150K", "-ar", "48000",
               "-f", "hls", "-hls_time", "10", "-hls_list_size", "0",
               outputdir
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
    findvideofile()
    openvideofile()


def openvideofile():
    with open('videolist', 'r') as f:
        line = f.readline()
    # 逐行读取文件，并新建输出路径
        while line:
            # 输出入文件路径
            filepath = line.strip()  # 去除行尾的"\n"
            # 去除文件扩展名，获得一个list
            filedir = os.path.splitext(filepath)
            # 去除文件扩展名后的路径作为输出的路径
            outputdir = filedir[0]
            # 文件扩展名
            # filesuffix = filedir[1]
            # raise SystemExit('Debug and Exit!')
            outputdir = os.path.join(
                os.path.abspath('.'), 'hlsvideodir', outputdir)
            # 标准化路径名，合并多余的分隔符和上层引
            outputdir = os.path.normpath(outputdir)
            outputdir = outputdir.replace(" ", "_")
            if os.path.exists(outputdir):
                logging.warning(outputdir + ", the dir already exist.")
            else:
                logging.info(outputdir + ", the dir create success.")
                os.makedirs(outputdir)
            logging.warning(filepath)  # 记录进度
            transcode(filepath, outputdir)
            line = f.readline()


if __name__ == '__main__':
    main()
