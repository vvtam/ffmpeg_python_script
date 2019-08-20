"""根据大小查找文件"""
import os,sys  
  
def comparefilesize(file_path):  
    """断判文件是否大于sizefilter，大于返回文件大小，小于返回false"""  
    sizefilter = 1*1024*1024 #1MB
    filesize = os.path.getsize(file_path)  
    if os.path.isfile(file_path) == False:  
        raise os.error("没有该文件")  
    if(filesize > sizefilter):  
        return filesize  
    else:  
        return 0  
  
def getvideofile(dir_path):  
    """查找录目下大于sizefilter的文件，写到文件。"""  
    for videoname in os.listdir(dir_path):  
        full_path = os.path.join(dir_path, videoname)  
        if os.path.isfile(full_path):  
            filesize=comparefilesize(full_path)              
            if filesize > 0:  
                open('videolist', 'a+').write(full_path + '\n')
                #print("路径%s 大小%d" % (full_path,filesize))                
        if os.path.isdir(full_path):  
            getvideofile(full_path)  

#def main():  
#    dir_path = os.path.abspath('.')
#    getvideofile(dir_path)  
    #print("Search End")  

#if __name__ == '__main__':
#    main()
