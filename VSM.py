from vocabUtil import VocabAgent as VA
from collections import defaultdict
from math import sqrt, log

class BlogVSM(object):
	# constructor
	def __init__(self, blog_name):
		self.blog_name = blog_name
		self.blog_length = float(0)
		self.relativity = float(0)
		self.TF = defaultdict(float)
		self.vector = defaultdict(float)
		self.vector_d = float(0);

class VSM(object):
	# constructor
	def __init__(self, ta=None, va=None, pb=0.75, pk=2.5, topK=10):
		self.ta = ta
                self.va = va
		self.pb = pb
		self.pk = pk
		self.topK = topK
		self.Blogs = []
		self.BlogFre = defaultdict(float)
		self.totallength = float(0)
		self.avglength = float(0)
		# initial run through
		self.__goThroughAllPost()
	# go through all blog's post
	def __goThroughAllPost(self):
		bn = self.ta.getAllBlogs()
		for index in range(len(bn)):
			self.Blogs.append(BlogVSM(bn[index]))
			b = self.ta.getBlogByName(bn[index])
			pid_list = b.getAllPosts()
			termlist = []
			for pid in pid_list:
				p = self.ta.getPostById(bn[index], pid)
				terms = VA.extractTermsFromPost(p)
                                terms += self.va.extractTermsFromPhoto(p)
				termlist += terms
				for term in terms:
					self.Blogs[index].TF[term] += 1
					self.Blogs[index].blog_length += 1
					self.totallength += 1
			for term in list(set(termlist)):
				self.BlogFre[term] += 1
		self.__countVectorWeight()
	# count blog's vector weight
	def __countVectorWeight(self):
		self.avglength = self.totallength/len(self.Blogs)
		# trans RawTF into NormTF*IDF
		for bs in self.Blogs:
			tempd = float(0)
			for key,value in bs.TF.iteritems():
				bs.vector[key] = (self.pk+1)*value / (value+self.pk*(1-self.pb+self.pb*bs.blog_length/self.avglength)) * log(len(self.Blogs)/self.BlogFre[key])
				tempd += bs.vector[key] * bs.vector[key]
			bs.vector_d = sqrt(tempd)
	# query by blog name and return relative blogs
	def queryByBlogName(self, queryBlog):
		# blog already in Blogs
		if queryBlog in self.ta.getAllBlogs():
			for index in range(len(self.Blogs)):
				if self.Blogs[index].blog_name == queryBlog:
					Query = self.Blogs[index]
					break
		# blog not in Blogs
		else:
			Query = BlogVSM(queryBlog)
			b = self.ta.getBlogByName(queryBlog)
			pid_list = b.getAllPosts()
			termlist = []
			for pid in pid_list:
				p = self.ta.getPostById(queryBlog, pid)
				terms = VA.extractTermsFromPost(p)
                                terms += self.va.extractTermsFromPhoto(p)
				termlist += terms
				for term in terms:
					Query.TF[term] += 1
					Query.blog_length += 1
					self.totallength += 1
			# append to Blogs
			self.Blogs.append(Query)
			for term in list(set(termlist)):
				self.BlogFre[term] += 1
			# recount vector weight 
			self.__countVectorWeight()
			Query = self.Blogs[len(self.Blogs)-1]

		for bs in self.Blogs:
			temprel = float(0)
			for key,value in bs.vector.iteritems():
				temprel += value * Query.vector[key]

			denominator = bs.vector_d * Query.vector_d
			if denominator == 0:
				bs.relativity = float("-INF")
			else:
				bs.relativity = temprel / denominator

		self.Blogs.sort(key=lambda x: x.relativity,reverse=True)

		ret = [(b.blog_name, b.relativity) for b in self.Blogs[1:self.topK+1]] # skipping the blog itself
		return ret




