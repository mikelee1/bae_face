import os  
import subprocess  
  
def amr2mp3(amr_path,mp3_path=None):  
    path, name = os.path.split(amr_path)  
    if name.split('.')[-1]!='amr':  
        print 'not a amr file'  
        return 0  
    if mp3_path is None or mp3_path.split('.')[-1]!='mp3':  
        mp3_path = os.path.join(path, name.split('.')[0] +'.mp3')  
    print(mp3_path)
    error = subprocess.call(['ffmpeg','-i',amr_path,mp3_path])  
    print error  
    if error:  
        return 0  
    print 'success'  
    return mp3_path  
  
if __name__ == '__main__':  
    amr_path = '20180227_170656.amr'  
    amr2mp3(amr_path)  
