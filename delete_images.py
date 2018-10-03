import os, time

dir = os.path.dirname(__file__)
mypath = os.path.join(dir, 'static','images')

def delete_images(days):
    now = time.time()
    cutoff = now - (days * 86400)

    files = os.listdir(mypath)

    for xfile in files:
        if os.path.isfile( os.path.join(dir, 'static','images', xfile) ):
            t = os.stat( os.path.join(dir, 'static','images', xfile))
            c = t.st_ctime

            # delete file if older than a week
            ext = xfile.split('.')[1]
            if ext == 'png':
                if c < cutoff:
                    os.remove(os.path.join(dir, 'static','images', xfile))
