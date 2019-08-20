#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import subprocess as sp
import os
import logging

logging.basicConfig(filename='transcode.log', level=logging.WARNING)
# logging.basicConfig(filename='tcTS.log', level=logging.INFO)


def transcode(filepath, outputdir):
    command = ["ffmpeg", "-y", "-i", filepath,
               "-loglevel",  "error",
               "-metadata", "service_name='Push Media'",
               "-metadata", "service_provider='Push Media'",
               "-c:v", "h264",
               # "-profile:v", "high", "-level:v", "3.2",
               # "-muxrate", "4200K", #复用码率，设置之后整体码率模式是CBR
               # "-x264-params", "nal-hrd=vbr",
               "-b:v", "3800K", "-minrate", "3800K", "-maxrate", "7600K", "-bufsize", "2M",
               "-preset", "ultrafast", "-tune", "animation",
               # "-g", "24",
               "-keyint_min", "24", "-g", "24", "-sc_threshold", "0",
               "-flags", "+ildct+ilme", #Interlaced video,隔行扫描
               "-top", "1", #隔行扫描前场/后场优先模式 ，1是前场（顶场），0是后场（底场） 
               "-streamid", "0:481", #视频pid
               "-streamid", "1:482", #音频pid
               # "-video_format", "pal", # PAL
               "-s", "1920x1080",
               "-aspect", "16:9",
               "-r", "50",
               # "-framerate", "50",
               "-c:a", "mp2",
               "-b:a", "128K", "-ar", "48000",
               #"-f", "mpegts",
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
    # 打开视频列表文件
    with open('list', 'r') as f:
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
            # raise SystemExit('Debug and Exit!') #调试
            # 输出在当前目录
            outputdir = os.path.join(os.path.abspath('.'), '1080its', outputdir)
            # ===输出不在当前目录===
            #output_basedir = '/home/pm/transcode'
            #outputdir = os.path.join(output_basedir, 'transcode', outputdir)
            # ===输出不在当前目录===
            # 标准化路径名，合并多余的分隔符和上层引
            outputdir = os.path.normpath(outputdir)
            # 替换空格
            #outputdir = outputdir.replace(" ", "_")
            output_basedir = os.path.dirname(outputdir)
            if os.path.exists(output_basedir):
                logging.info(output_basedir + ", the dir already exist.")
            else:
                logging.info(output_basedir + ", the dir create success.")
                os.makedirs(output_basedir)
            logging.warning(filepath)  # 记录进度
            transcode(filepath, outputdir)
            line = f.readline()

if __name__ == '__main__':
    main()
