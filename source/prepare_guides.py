import os 
import load_file_article
from links_searcher import *
from link_to_article import Link2Article
import sys
import _pickle as cPickle
import pickle

files = os.listdir("../data/processed_articles/")
files.remove("guide_article_ID")
articles = load_file_article.load_data()
cnt_not_match_links = 0
links_cnt = 0
l2a = Link2Article()
for filename in files:
	processed_articles = []
	with open("../data/processed_articles/" + filename, encoding = 'utf-8') as f:
		for line in f:
			# print (line)
			links = LinksSearcher(line).get_simple_links()
			for link in links:
                # function from Alexandrina
				article = l2a.link2article(link)
				if article:
					links_cnt += 1
					if article.article_ID not in processed_articles:
						processed_articles.append(article.article_ID)
				else:
					cnt_not_match_links += 1

			sys.stderr.write("\r\t\t\t\t\tALL LINKS: %d; CAN't MATCH: %d" % (links_cnt, cnt_not_match_links))

	cPickle.dump(processed_articles, open("../data/processed_articles/article_ID_" + filename[:-4], "wb"))