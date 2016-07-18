import os, sys
import re


def isActuallyFloat(term):
	try:
		tmp = float(term)
		return True
	except:
		return False

def parse_this_line(line):
	line = line[8:] # skip the beginning: caffe=[(
	line = re.sub(r'[^a-zA-Z0-9._-]',' ', line)
	ret = [t for t in line.split() if t != "u" and not isActuallyFloat(t)]
	return ret


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print >> sys.stderr, "wrong argument count!"
		sys.exit(-1)
	if not os.path.isfile(sys.argv[1]):
		print >> sys.stderr, "illegal argument: %s" % (sys.argv[1])
		sys.exit(-1)
	if os.path.exists(sys.argv[2]):
		print >> sys.stderr, "illegal argument: %s" % (sys.argv[2])
		sys.exit(-1)
	outputFile = open(sys.argv[2], "w")
	with open(sys.argv[1], "r") as f:
		bn = ""
		pid = ""
		for line in f:
			line = line.strip()
			if line.startswith("b="):
				bn = line.split("=")[1]
			if line.startswith("p="):
				pid = line.split("=")[1]
			if line.startswith("caffe=[(") and line.endswith(")]"):
				terms = parse_this_line(line)
				s = "%s %s " % (bn, pid)
				for term in terms:
					s += "%s " % (term)
				outputFile.write(s + "\n")
	outputFile.close()
