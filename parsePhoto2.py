import sys, os
import pytumblr
import json
from tumblrUtil import TumblrAgent as TA
# from vocabUtil import VocabAgent as VA
from imageUtil import parser, OCR

if __name__ == "__main__":

	output_file = open('photoText', 'a')

	DB_urls = {}
	f = open('data/DB_urls', 'r')
	for line in f:
		tmp = line.strip().split()
		if tmp[0] not in DB_urls:
			print tmp[0]
			DB_urls[tmp[0]] = [(tmp[1], tmp[2])]
		else:
			DB_urls[tmp[0]].append((tmp[1], tmp[2]))

	f.close()

	### argument1: blogList ###
	queryF = open(sys.argv[1], 'r')
	limit = int(sys.argv[2])

	for blogName in queryF:
		if blogName.strip() not in DB_urls:
			continue
		photoList = DB_urls[blogName.strip()]
		convertList = photoList[:min(limit, len(photoList))]
		for post in convertList:
			pid = post[0]
			photoUrl = post[1]
			print blogName.strip(), pid, photoUrl
			output_file.write('b=' + str(blogName))
			output_file.write('p=' + str(pid) + '\n')
			# ocrData = []
			parserData = []
			parserData = parser(photoUrl)

			# print blogName, pid
			# print str(ocrData)
			print str(parserData)
			print '\n'
			# output_file.write('OCR=' + str(ocrData) + '\n')
			output_file.write('caffe=' + str(parserData) + '\n')

	output_file.close()



