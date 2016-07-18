import os, sys
import json
from tumblrUtil import TumblrBlog, TumblrPost

def writeData(data, path):
    # check path
    if os.path.exists(path):
        print >> sys.stderr, "writeData(): %s already exists..." % (path)
        sys.exit(-1)
    # transform data
    #     transform TumblrBlog objects into strings
    #     transform TumblrPost objects into strings
    for bn in data['blogs'].keys():
        tmp_object = json.loads(data['blogs'][bn].raw)
        tmp_object['posts'] = data['blogs'][bn].posts
        data['blogs'][bn] = json.dumps(tmp_object)
    for pid in data['posts'].keys():
        data['posts'][pid] = data['posts'][pid].raw
    # write to file
    with open(path, "w") as f:
        f.write(json.dumps(data))


def readData(path):
    # check path
    if not os.path.isfile(path):
        print >> sys.stderr, "readData(): %s not exists..." % (path)
        sys.exit(-1)
    # read file
    data = None
    with open(path, "r") as f:
        data = json.loads(f.read())
    # transform data
    #     transform json strings to TumblrBlog and TumblrPost objects
    if data:
        for bn in data['blogs'].keys():
            tmp_object = json.loads(data['blogs'][bn])
            data['blogs'][bn] = TumblrBlog(tmp_object)
            data['blogs'][bn].posts = tmp_object['posts']
        for pid in data['posts'].keys():
            data['posts'][pid] = TumblrPost(json.loads(data['posts'][pid]))
    return data


if __name__ == "__main__":
    pass

