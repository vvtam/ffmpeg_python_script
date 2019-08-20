#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import subprocess as sp
import os
import logging
import random
import json

logging.basicConfig(filename='error.log', level=logging.WARNING)
# logging.basicConfig(filename='tcTS.log', level=logging.INFO)

def probe(filepath):
    ''' Give a json from ffprobe command line

    @filepath: the path of the video file, string.
    '''
    if type(filepath) != str:
        raise Exception('Gvie ffprobe a file path of the video')
        return

    prog = ["ffprobe",
            "-loglevel",  "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            filepath
            ]
    pipe = sp.Popen(prog, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()

#    if pipe.returncode == 0:
#        print ("command '%s' succeeded, returned: %s" \
#               % (prog, str(out)))
#    else:
#        print ("command '%s' failed, exit-code=%d error = %s" \
#               % (prog, pipe.returncode, str(err)))

    out = out.decode("utf-8")
    return json.loads(out)


def duration(filepath):
    ''' Video's duration in seconds, return a float number
    '''
    _json = probe(filepath)

    try:
        if 'format' in _json:
            if 'duration' in _json['format']:
                return float(_json['format']['duration'])

        if 'streams' in _json:
            # commonly stream 0 is the video
            for s in _json['streams']:
                if 'duration' in s:
                    return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    # raise Exception('I found no duration')
    # return 0
    except OSError:
        print("Can't found duration")
        return 0

def getpic(filepath, outputdir):
    dur = duration(filepath)
    if type(dur) != float:
        dur = random.randint(5, 60)
    else:
        dur = int(dur)
    randNumber = random.randint(1, dur)
    randNumber = str(randNumber)
    command = ["ffmpeg",
               "-ss", randNumber,
               "-i", filepath, "-y",
               "-f", "image2", "-vframes", "1",
               outputdir + ".jpg"
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
            outputdir = os.path.join(os.path.abspath('.'), 'capture', outputdir)
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
            getpic(filepath, outputdir)
            line = f.readline()

if __name__ == '__main__':
    main()
