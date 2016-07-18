names = open("blogname", "r").read().split('\n')

def checkName(name):
	if name == "":
		return False
	badChar = ['.', '<', '>', '@', ':', '(', ')', '"', ',', '_', '/', '\\', '^', '?', '[', ']', ';', '*', '|', '{', '}', '+', '=', '&', '%', '$', '#', '!', '~', '`']
	for i in range(0, len(badChar)):
		if badChar[i] in name:
			return False
	return True

def replceName(name):
	return name.replace("\xe2\x80\x93", '-');

blognames = []
for name in names:
	name = replceName(name)
	if checkName(name):
		if name not in blognames:
			blognames.append(name)
print blognames

names = open("blogname", "w")
for blogname in blognames:
	names.write(blogname + '\n')