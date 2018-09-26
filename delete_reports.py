import os, time

def delete_reports(days):
    now = time.time()
    cutoff = now - (days * 86400)

    files = os.listdir('static/reports')

    for xfile in files:
        if os.path.isfile( 'static/reports/'+ xfile ):
            t = os.stat( 'static/reports/'+ xfile)
            c = t.st_ctime

            # delete file if older than a week
            ext = xfile.split('.')[1]
            if ext == 'pdf' or ext == 'csv':
                if c < cutoff:
                    os.remove('static/reports/'+ xfile)
