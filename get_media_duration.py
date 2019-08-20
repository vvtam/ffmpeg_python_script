# _*_ coding:utf-8 _*_

import xlwt
# import xlrd
import subprocess as sp
import json


def probe(filepath):
    ''' Give a json from ffprobe command line

    @filepath: The absolute (full) path of the video file, string.
    '''
    if type(filepath) != str:
        raise Exception('Gvie ffprobe a full file path of the video')
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

def writexcel(dir, sec, row):
    try:
        sheet.write(row, 0, dir)
        sheet.write(row, 1, sec)
        xlsname.save("./list.xls")
    except OSError:
        print("Can't write the excel file")

with open("filelist", 'r') as f:
    line = f.readline()
    # 初始化行为0
    row = 0
    # 新建excel
    xlsname = xlwt.Workbook()
    # 修改sheet name
    sheet = xlsname.add_sheet("list")

    while line:
        filepath = line.strip()
        dua = (duration(filepath))
        writexcel(filepath, dua, row)
        line = f.readline()
        row += 1
