import tarfile
import os.path
import os


def bundler_get_image(shard, filename):
    """
    This function accepts the shard in question and filename. It then returns the image file in bytes.

    :param shard: The shard whose files we are accessing. Starts at 0.
    :param filename: The filename we need data for.
    """
    image = 0
    with tarfile.open("shard{}".format(shard), "r:xz") as files:
        for tarinfo in files.getmembers():
            if tarinfo.name == filename:
                image = files.extractfile(tarinfo).read()
                break
    return image


def bundler_store_image(shard, filename):
    """
    Store an image into a shard's bundle tar and then removes the temp copy.

    :param shard:  The shard bundle we are accessing. Starts at 0.
    :param filename:  The file we are pushing into the tar archive.
    """
    if os.path.isfile("shard{}".format(shard)):
        existing = []
        with tarfile.open("shard{}".format(shard), "r:xz") as newtar:
            for x in newtar.getmembers():
                existing.append(x.name)
            newtar.extractall()
        os.remove("shard{}".format(shard))
        with tarfile.open("shard{}".format(shard), "w:xz") as newtar:
            for x in existing:
                newtar.add(x)
            newtar.add(filename)
        for x in existing:
            os.remove(x)
    else:
        with tarfile.open("shard{}".format(shard), "w:xz") as newtar:
            newtar.add(filename)
    os.remove(filename)


