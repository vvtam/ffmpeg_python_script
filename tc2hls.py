#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import subprocess as sp
import json
import os
import logging

logging.basicConfig(filename='2hls.log',level=logging.WARNING)

def probe(filepath):
    ''' Give a json from ffprobe command line

    @filepath: The absolute (full) path of the video file, string.
    '''
    if type(filepath) != str:
        raise Exception('Gvie ffprobe a full file path of the video')

    prog = ["ffprobe",
            "-loglevel",  "error",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            filepath
            ]
    pipe = sp.Popen(prog, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()

    if pipe.returncode == 0:
       logging.info("command '%s' succeeded, returned: %s" \
               % (prog, str(out)))
    else:
        logging.error("command '%s' failed, exit-code=%d error = %s" \
               % (prog, pipe.returncode, str(err)))
    return json.loads(out)


def transcode(filepath, outputdir):
    ''' Video's duration in seconds, return a float number
    '''
    _json = probe(filepath)
    # 定义一个空的列表用来存音频视频编码
    codec = []
    # 定义hls输出地址
    outputdir = os.path.join(outputdir, "playlist.m3u8")
    # 定义转码参数
    try:
        if 'streams' in _json:
            for cc in _json['streams']:
                if 'codec_name' in cc:
                    codec.append(cc['codec_name'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    # raise Exception('I found no duration')
    # return 0
    # except OSError:
    #    print("Can't found duration")
    #    return 0

    finally:
        if 'h264' in codec and 'aac' in codec:
            command = ["ffmpeg", "-y",
                       "-i", filepath,
                       "-loglevel",  "error",
                       "-bsf:v", "h264_mp4toannexb",
                       "-c:a", "copy",
                       "-c:v", "copy",
                       "-f", "hls", "-hls_time", "10", "-hls_list_size", "0",
                       outputdir
                       ]
            pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
            out, err = pipe.communicate()
            if pipe.returncode == 0:
                logging.info("codec: '%s', command '%s' succeeded, returned: %s"
                             % (codec, command, str(out)))
            else:
                logging.error("codec: '%s', command '%s' failed, exit-code=%d error = %s"
                              % (codec, command, pipe.returncode, str(err)))
        elif 'h264' in codec and 'mp3' in codec:
            command = ["ffmpeg", "-y",
                       "-i", filepath,
                       "-loglevel",  "error",
                       "-c:a", "copy",
                       "-c:v", "copy",
                       "-f", "hls", "-hls_time", "10", "-hls_list_size", "0",
                       outputdir
                       ]
            pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
            out, err = pipe.communicate()
            if pipe.returncode == 0:
                logging.info("codec: '%s', command '%s' succeeded, returned: %s"
                             % (codec, command, str(out)))
            else:
                logging.error("codec: '%s', command '%s' failed, exit-code=%d error = %s"
                              % (codec, command, pipe.returncode, str(err)))
        else:
            command = ["ffmpeg", "-y",
                       "-i", filepath,
                       "-loglevel",  "error",
                       "-c:a", "aac",
                       "-c:v", "h264",
                       "-f", "hls", "-hls_time", "10", "-hls_list_size", "0",
                       outputdir
                       ]
            pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
            out, err = pipe.communicate()
            if pipe.returncode == 0:
                logging.info("codec: '%s', command '%s' succeeded, returned: %s"
                             % (codec, command, str(out)))
            else:
                logging.error("codec: '%s', command '%s' failed, exit-code=%d error = %s"
                              % (codec, command, pipe.returncode, str(err)))

# 创建目录函数，未使用


def mkdir(hlsdir):
    hlsdir = hlsdir.strip()
    hlsdir = hlsdir.rstrip("\\")

    ifExists = os.path.exists(hlsdir)

    if not ifExists:
        print(hlsdir + "dir create success")
        os.makedirs(hlsdir)
        return True
    else:
        print(hlsdir + "already exist")
        return False


# 打开文件
with open('videoList', 'r') as f:
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
        outputdir = os.path.join(os.path.abspath('.'), '2hls', outputdir)
        # 如果输出不在当前目录,需要重新定义
        #output_basedir = ''
        #outputdir = os.path.join(output_basedir, '2hls', outputdir)
        # 标准化路径名，合并多余的分隔符和上层引
        outputdir = os.path.normpath(outputdir)
        outputdir = outputdir.replace(" ", "_")
        if os.path.exists(outputdir):
            logging.warning(outputdir + ", the dir already exist.")
        else:
            logging.info(outputdir + ", the dir create success.")
            os.makedirs(outputdir)
        logging.warning(filepath) #记录进度
        transcode(filepath, outputdir)
        line = f.readline()
