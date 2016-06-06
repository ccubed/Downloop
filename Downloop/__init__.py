import os
import io
import sys
from bundler import *
from cacher import *
from flask import *

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.rsplit(".", 1)[1] in ['jpg', 'jpeg', 'bmp', 'gif', 'png']:
            final = file.filename.split("/")[-1:]
            if final.count(".") > 1:
                ext = final.rsplit(".", 1)[1]
                final = final.rsplit(".", 1)[0].replace(".", "_")
                final = final + ext
            hid = create_hash()
            final = "".join(final)
            file.save(final)
            cacher_store_image(final, hid, app.config['SHARD'])
            bundler_store_image(app.config['SHARD'], final)
            return '<!doctype html><title>Success</title><h1>Image ID is {}</h1>'.format(hid)
        else:
            return '<!doctype html><title>Invalid Extension</title><h1>Invalid File Extension</h1>'
    else:
        return '<!doctype html><title>Upload new File</title><h1>Upload new File</h1><form action="" method=post enctype=multipart/form-data><p><input type=file name=file><input type=submit value=Upload></form>'


@app.route("/img/<hash>", methods=['GET'])
def get_data(hash):
    info = cacher_get_image(hash)
    if info is None:
        return '<!doctype html><title>Not Found</title><h1>Hash not found</h1>'
    else:
        data = bundler_get_image(info['shard'], info['filename'])
        return send_file(io.BytesIO(data), mimetype="image/jpeg")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Need a shard.")
    else:
        app.config['SHARD'] = sys.argv[1].split("=")[1]
        app.debug = True
        app.run()