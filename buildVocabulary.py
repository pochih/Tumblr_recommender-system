import os, sys
from tumblrUtil import TumblrAgent as TA
from vocabUtil import VocabAgent as VA
import logging
from collections import defaultdict


# global variables
isDebug = True
VOCAB = defaultdict(int)

def print_usage():
	print >> sys.stderr, "Usage:\n\t%s <outputPath>" % (sys.argv[0])

def main(outputPath):
	global isDebug, VOCAB

	# enable / disable debug logging
	if isDebug:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)
	
	logging.debug('initializing TumblrAgent')
	ta = TA()

	# loop over all posts
	logging.debug('iterate through every post in cache')
	debug_blog_counter = 0
	for bn in ta.getAllBlogs():
		b = ta.getBlogByName(bn)
		pid_list = b.getAllPosts()
		for pid in pid_list:
			p = ta.getPostById(bn, pid)
			# use VA to extract terms
			terms = VA.extractTermsFromPost(p)
			# add to VOCAB
			for term in terms:
				VOCAB[term] += 1
		debug_blog_counter += 1
		if debug_blog_counter % 10 == 0:
			logging.debug('processed %d blogs' % (debug_blog_counter))
	logging.debug('processed %d blogs' % (debug_blog_counter))

	# output VOCAB
	logging.debug('writing results to file... (%s)' % (outputPath))
	with open(outputPath, "w") as f:
		for k, v in VOCAB.iteritems():
			if v > 0:
				f.write("%s\t%d\n" % (k, v))
	logging.debug('finish writing file. (%s)' % (outputPath))



if __name__ == "__main__":
	# check argument count
	if len(sys.argv) != 2:
		print_usage()
		sys.exit(-1)

	# check argument: outputPath
	if os.path.exists(sys.argv[1]):
		print >> sys.stderr, "the file %s already exists." % (sys.argv[1])
		print_usage()
		sys.exit(-1)
		
	# calling main() function
	main(sys.argv[1])

