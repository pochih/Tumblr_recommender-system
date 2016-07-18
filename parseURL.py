import sys, os
import pytumblr
import json
from tumblrUtil import TumblrAgent as TA
from vocabUtil import VocabAgent as VA
from imageUtil import parser, OCR

def legalImageType(url):
	path = url.split('.')
	iType = path[len(path)-1]
	if iType == 'jpg' or iType == 'png':
		return True;
	return False;

if __name__ == "__main__":

	# blogsFile = open('../DB_blogs', 'a')
	# postsFile = open('../DB_posts', 'a')
	# tagsFile = open('../DB_tags', 'a')
	urlFile = open('../DB_urls', 'a')

	# use TumblrAgent
	ta = TA()
	print "TA OK"
	for bn in ta.getAllBlogs():
		print "bn:", bn
		b = ta.getBlogByName(bn)
		pid_list = b.getAllPosts()
		terms = []
		for pid in pid_list:
			p = ta.getPostById(bn, pid)
			if p.getType() == 'photo':
				for photo in p.photos:
					photoUrl = photo['original_size']['url']
					if legalImageType(photoUrl):
						urlFile.write(str(bn) + ' ' + str(pid) + ' ' + str(photoUrl) + '\n')

	urlFile.close()
	sys.exit(0)
