import os, time

def delete_images(days):
    now = time.time()
    cutoff = now - (days * 86400)

    files = os.listdir('static/images')
    print (files)
    for xfile in files:
        print (os.path.isfile( 'static/images/'+ xfile ))
        if os.path.isfile( 'static/images/'+ xfile ):
            t = os.stat( 'static/images/'+ xfile)
            c = t.st_ctime
            print (c)

            # delete file if older than a week
            ext = xfile.split('.')[1]
            print (ext)
            if ext == 'png':
                if c < cutoff:
                    os.remove('static/images/'+ xfile)
