# tmp = raw_input()
from tumblrUtil import TumblrAgent as TA
# from vocabUtil import VocabAgent as VA
import numpy as np
import sys

def loadModel(number):
    model = {}
    f = open('GN-300-neg.txt','r')
    tmp = f.readline()
    tmp = f.readline()
    ### Take only the first @number of words ###
    for i in range(number):
        line = f.readline()
        tmp = line.split()
        vec = []
        if i % 10000 == 0:
            print >> sys.stderr, i, tmp[0]
        for j in range(1, 301):
            vec.append(float(tmp[j]))
        model[tmp[0]] = np.array(vec)

def cosineDistance(v1, v2):
    return np.cosine(v1, v2)

def loadVecs(names):
    vecs = []
    f = open('w2v_for_blogs.txt','r')
    for i, line in enumerate(f):
        v = line.strip().split()
        v = [float(x) for x in v]
        vecs.append((names[i], v))
    return vecs

ta = TA()
model = loadModel(300000)
blogVecs = loadVecs(ta.getAllBlogs())
topK = 10

while True:
    queryName = raw_input()
    blog = ta.getBlogByName(queryName)
    postIds = blog.getAllPosts()
    v = np.zeros(300)
    for Id in postIds:
        post = ta.getPostById(blog.getName(), Id)
        for tag in post.getTags():
            if tag in model:
                v += model[tag]

    # Now I have the vector
    dists = []
    for bv in blogVecs:
        dists.append((bv[0], cosineDistance(bv[1], v)))
    dists.sort(key=lambda tup: tup[1])
    for i in range(topK):
        print dist[i][0]
        
        
        # lst = va.extractTermsFromPost(post)
