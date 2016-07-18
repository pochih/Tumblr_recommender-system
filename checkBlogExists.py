import sys
import pytumblr

client = pytumblr.TumblrRestClient(
    "ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk",
    "PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs",
    "sVF038jN4AjBN1sUJ9RiqE0PUKnQDcgVBCOvEkiblXwSROiEIO",
    "NXYoBsNQBW3b6yqNS1VuxKixMoktAADZfPGJ72wIZOSx62P5OO"
)


if __name__ == "__main__":
    b_list = []
    final_list = []
    with open(sys.argv[1], "r") as f:
        b_list = list(set([line.strip() for line in f]))
    for bn in b_list:
        res = client.blog_info(bn)
        if u'blog' not in res.keys():
            print >> sys.stderr, "%s not a blog." % (bn)
        else:
            final_list.append(bn)
    with open(sys.argv[1], "w") as f:
        f.write("\n".join(final_list))
