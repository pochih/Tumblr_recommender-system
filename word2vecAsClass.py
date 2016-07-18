from tumblrUtil import TumblrAgent as TA 
from vocabUtil import VocabAgent as VA
import sys
import numpy as np
import math

class W2V(object):

    ### numWords   : vocab size of word2vec
    ### topK       : how many recommendations
    ### enablePhoto: use photo to text information or not
    
    def __init__(self, ta=None, va=None, enablePhoto=True, numWords=200000, topK=10):
        self.ta = ta
        self.va = va
        self.enablePhoto = enablePhoto
        self.model = self.loadWordVecs(numWords)
        self.vecs = self.initialW2VModel()
        self.topK = topK

    def loadWordVecs(self, numWords):
        model = {}
        f = open('data/small-GN-300-neg.txt','r')
        # tmp = f.readline()
        # tmp = f.readline()
        ### Take only the first @number of words ###
        for i in range(numWords):
            line = f.readline()
            tmp = line.split()
            vec = []
            if i % 10000 == 0:
                print >> sys.stderr, i, tmp[0]
            for j in range(1, 301):
                vec.append(float(tmp[j]))
            model[tmp[0]] = np.array(vec)
        return model

    def cosineDistance(self, v1, v2):
        eucV1 = math.sqrt(sum(x**2 for x in v1))
        eucV2 = math.sqrt(sum(x**2 for x in v2))
        if eucV1 == 0 or eucV2 == 0:
            return float('-inf')
        return np.dot(v1, v2) / (eucV1 * eucV2) 

    def computeVecFromBlog(self, blog):
        # blog = ta.getBlogByName(name)
        # print blog.getName()
        postIds = blog.getAllPosts()
        count = 0
        v = np.zeros(300)
        imageTerms = []
        
        for postId in postIds:
            post = self.ta.getPostById(blog.getName(), postId)
            ### tags ###
            tags = post.getTags()
            ### Image terms ###
            if self.enablePhoto:
                imageTerms = self.va.extractTermsFromPhoto(post)
            ### other terms ###
            otherTerms = VA.extractTermsFromPost(post)

            allTerms = tags + imageTerms + otherTerms
            
            for term in allTerms:
                if term in self.model:
                    v += self.model[term]

        return v

    def initialW2VModel(self):
        vecs = []
        blognames = self.ta.getAllBlogs()
        for name in blognames:
            blog = self.ta.getBlogByName(name)
            v = self.computeVecFromBlog(blog)
            vecs.append((name, v))
        return vecs

    def queryByBlogName(self, queryName):
        try:
            if queryName not in self.ta.getAllBlogs():
                blog = self.ta.getBlogByName(queryName)
                ### calculate the vector for query blog ###
                newV = self.computeVecFromBlog(blog)
                self.vecs.append((queryName, newV))
            else:
                blog = self.ta.getBlogByName(queryName)
        except:
            print >> sys.stderr, 'No such blog name'
            return

        v = self.computeVecFromBlog(self.ta.getBlogByName(queryName))
        # Now I have the vector
        dists = []
        for bv in self.vecs:
            tmp = self.cosineDistance(bv[1], v)
            dists.append((bv[0], tmp))
        dists.sort(key=lambda tup: tup[1], reverse=True)
        
        return dists[1 : self.topK + 1]




