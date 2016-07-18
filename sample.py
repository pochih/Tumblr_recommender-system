import sys, os
import pytumblr
import json


# api key
TUMBLR_CONSUMER_KEY = "ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk"
TUMBLR_CONSUMER_SECRET = "PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs"

# OAuth
# ACCESS_TOKEN = 'sSG3qISDXvahdO3qr8LbWy5SXXg3Ts0BBNRHCHDaksN9MSlbsy',
# ACCESS_SECRET = 'VCOF3mVfSQ7dHufNw3nCi5kW10bu5BrhGfgu8hlVU0Prvekr0R'
ACCESS_TOKEN = "v5e5U3tEOgZL37TGNbuhlUF3nMzaQV2zCVumRfd7wjkyN7ht4x"
ACCESS_SECRET = "FvHzFRwhZQLumDnrjXhvsiEDZ0mPSbbDtoFG15kX1x70MaFw8V"

if __name__ == "__main__":
	# create client
	client = pytumblr.TumblrRestClient(
		TUMBLR_CONSUMER_KEY,
		TUMBLR_CONSUMER_SECRET,
		ACCESS_TOKEN,
		ACCESS_SECRET
	)
	# client = pytumblr.TumblrRestClient(
	#   	'ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk',
	#   	'PpHRSKUKqBMNp4bjchW8EkxQNcQvyVyDYDWiz7gROzVERsOYAs',
	#   	'sSG3qISDXvahdO3qr8LbWy5SXXg3Ts0BBNRHCHDaksN9MSlbsy',
	#   	'VCOF3mVfSQ7dHufNw3nCi5kW10bu5BrhGfgu8hlVU0Prvekr0R'
	# )
	# get the client information
	client_info = client.info()
	client_dashboard = client.dashboard()
	client_likes = client.likes()
	tag_Data = client.tagged('lol')

	# Authenticate via API Key
	_client = pytumblr.TumblrRestClient('ytrXGiUjY2pZ9zggTPomZbXAwQD5xfveSj73h3bI76LwUkhYRk')
	_client_blog_info = _client.blog_info('superbc28blog.tumblr.com')
	_client_avatar = _client.avatar('brianhuang1019.tumblr.com')
	client_queue = client.queue('brianhuang1019.tumblr.com')
	client_drafts = client.drafts('brianhuang1019.tumblr.com')
	client_submission = client.submission('brianhuang1019.tumblr.com')
	client_reblog = client.reblog('brianhuang1019.tumblr.com')
	_client_posts = _client.posts('brianhuang1019.tumblr.com')

	print json.dumps(client_dashboard, indent=4)
