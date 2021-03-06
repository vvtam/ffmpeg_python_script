#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import subprocess as sp
import os
import logging

logging.basicConfig(filename='error.log', level=logging.WARNING)
# logging.basicConfig(filename='tcTS.log', level=logging.INFO)


def transcode(filepath, outputdir):
    command = ["ffmpeg", "-y", "-i", filepath,
               "-r", "25", #帧率25
               "-vsync", "cfr", #恒定帧率
               "-loglevel",  "error",
               "-metadata", "service_name='Push Media'",
               "-metadata", "service_provider='Push Media'",
               "-c:v", "libx264",
               #"-preset", "ultrafast", "-tune", "animation",
               #用ultrafast,profile 变成main,官方文档说的有冲突
               "-preset", "fast",
               #"-profile:v", "high", "-level:v", "4.0",
               "-flags", "+ildct+ilme", #Interlaced video,隔行扫描
               "-top", "1", #隔行扫描前场/后场优先模式 ，1是前场（顶场），0是后场（底场）
               "-keyint_min", "25", "-g", "25", "-bf", "2", "-sc_threshold", "0", #GOP长度
               #b_adapt=0 连续B帧force-cfr 恒定帧率
               "-x264-params", "profile:v=high:level=4.0:force-cfr=1:bitrate=8000:vbv-maxrate=8000:vbv-minrate=8000:vbv-bufsize=8000:cabac=1:ref=3:b-pyramid=0:b_adapt=0",
               "-s", "1920x1080", #hd1080
               "-aspect", "16:9",
               "-c:a", "aac",
               "-b:a", "128K", "-ar", "48000",
               "-muxrate", "9M",
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
            outputdir = os.path.join(os.path.abspath('.'), '8m1080its', outputdir)
            # ===输出不在当前目录===
            #output_basedir = '/mnt/nfs/transcode'
            #outputdir = os.path.join(output_basedir, 'ts8M1080P', outputdir)
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
