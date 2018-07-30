import os, time

def delete_images(days):
    now = time.time()
    cutoff = now - (days * 86400)

    files = os.listdir('static/images')

    for xfile in files:
        if os.path.isfile( 'static/images/'+ xfile ):
            t = os.stat( 'static/images/'+ xfile)
            c = t.st_ctime

            # delete file if older than a week
            ext = xfile.split('.')[1]
            if ext == 'png':
                if c < cutoff:
                    os.remove('static/images/'+ xfile)
