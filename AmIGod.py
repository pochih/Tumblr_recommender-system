from flask import Flask, render_template, redirect, request
from tumblrUtil import TumblrAgent as TA
from vocabUtil import VocabAgent as VA
import logging
from word2vecAsClass import W2V
from VSM import VSM
from LMAsClass import LanguageModel

# global variables
ta = None
va = None
w2v = None
vsm = None
lm = None
app = Flask(__name__)

def initializeGlobalVariables():
	global ta, va, w2v, vsm, lm
	logging.debug('initializing TumblrAgent ...')
	ta = TA()
	logging.debug('initializing VocabAgent ...')
	va = VA()
	va.load('data/VocabAgentCache.new')
	logging.debug('initializing W2V ...')
	w2v = W2V(ta=ta, va=va)
	logging.debug('initializing VSM ...')
	vsm = VSM(ta=ta, va=va)
	logging.debug('initializing LM ...')
	lm = LanguageModel(ta=ta, va=va)

@app.route("/")
def index():
	return render_template('index.html'), 200

@app.route("/search", methods=['POST'])
def search():
	global w2v, vsm, lm
	blogName = request.form['blogName']
	vsmResult = vsm.queryByBlogName(blogName)
	lmResult = lm.query(blogName)
	w2vResult = w2v.queryByBlogName(blogName)
	return render_template('search.html', blogName=blogName, w2vResult=w2vResult, vsmResult=vsmResult, lmResult=lmResult), 200

if __name__ == "__main__":
	app.debug = False
	logging.basicConfig(level=logging.DEBUG)
	
	logging.debug('initializing global variables...')
	initializeGlobalVariables()

	logging.debug('running on port 8080 ...')
	app.run(port=8080)

