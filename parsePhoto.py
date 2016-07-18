import sys, os
import pytumblr
import json
from tumblrUtil import TumblrAgent as TA
# from vocabUtil import VocabAgent as VA
from imageUtil import parser, OCR

def legalImageType(url):
	path = url.split('.')
	iType = path[len(path)-1]
	if iType == 'jpg' or iType == 'png':
		return True;
	return False;

def unuseBlogName(bn):
	usedBlogNames = ['ayee-erbear', 'afinefashionfrenzy', 'hipsterizeddolls', 'sexy-animegirls', 'hipsterizeddolls', 'thehundreds', 'stfuconservatives','']
	for blogname in usedBlogNames:
		if bn == blogname:
			return False
	return True

if __name__ == "__main__":

	output_file = open('photoText', 'a')

	# use TumblrAgent
	ta = TA()
	for bn in ta.getAllBlogs()[int(sys.argv[1]):int(sys.argv[2])]:
		# if not unuseBlogName(bn):
		# 	continue
		b = ta.getBlogByName(bn)
		pid_list = b.getAllPosts()
		count = 0
		for pid in pid_list:
			p = ta.getPostById(bn, pid)
			if p.getType() == 'photo':
				count += 1
				if count < int(sys.argv[3]) or count > int(sys.argv[4]):
					break
				# if bn == 'skypestripper' and int(pid) >= 145286179484:
				# 	continue
				output_file.write('b=' + str(bn) + '\n')
				output_file.write('p=' + str(pid) + '\n')
				# ocrData = []
				parserData = []
				for photo in p.photos:
					photoUrl = photo['original_size']['url']
					if legalImageType(photoUrl):
						# ocrData += OCR(photoUrl)
						parserData += parser(photoUrl)
				print bn, pid
				# print str(ocrData)
				print str(parserData)
				print '\n'
				# output_file.write('OCR=' + str(ocrData) + '\n')
				output_file.write('caffe=' + str(parserData) + '\n')

	output_file.close()
	sys.exit(0)
