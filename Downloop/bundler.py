import tarfile
import os.path


def get_image(shard, filename):
    """
    This function accepts the shard in question and filename. It then returns the image file in bytes.

    :param shard: The shard whose files we are accessing. Starts at 0.
    :param filename: The filename we need data for.
    """
    image = 0
    with tarfile.open("shard{}.tar".format(shard), "w:xz") as files:
        for tarinfo in files:
            if tarinfo.name == filename:
                image = files.extractfile(tarinfo).read()
                break
    return image


def store_image(shard, filename):
    """
    Store an image into a shard's bundle tar.

    :param shard:  The shard bundle we are accessing. Starts at 0.
    :param filename:  The file we are pushing into the tar archive.
    """
    if os.path.isfile("shard{}".format(shard)):
        files = tarfile.open("shard{}".format(shard), "r:xz").getmembers()
        with tarfile.open("shard{}".format(shard), "w:xz") as newtar:
            for x in files:
                newtar.addfile(x)
            newtar.add(filename)
    else:
        with tarfile.open("shard{}".format(shard), "w:xz") as newtar:
            newtar.add(filename)



