import os
from links_searcher import *
from link_to_article import Link2Article
import sys
import _pickle as cPickle
import pickle

class Guide(object):
	"""
	For guides from ConsultantPlus
	self.articles_link = {article_ID:link to guide}
	"""
	def __init__(self, filename, guide_name):
		self.name = guide_name
		self.articles_link = {}

		cnt_not_match_links = 0
		links_cnt = 0
		l2a = Link2Article()

		with open("../data/guide_articles/" + filename, "r", encoding = 'utf-8') as f:
			for line in f:
				# print (line)
				links = LinksSearcher(line).get_simple_links()
				for link in links:
					article = l2a.link2article(link)
					if article:
						links_cnt += 1
						if article.article_ID not in self.articles_link:
							self.articles_link[article.article_ID] = line.strip().split("\t")[-1]
					else:
						cnt_not_match_links += 1

				sys.stderr.write("\r\t\t\t\t\tALL LINKS: %d; CAN't MATCH: %d" % (links_cnt, cnt_not_match_links))

	def get_link(self, article_ID):
		if article_ID in self.articles_link:
			return self.articles_link[article_ID]
		else:
			return None

# g1= Guide("PPN.txt", "Путеводитель по налогам")
# g2= Guide("PPVS.txt", "Перечень позиций высших судов")
# g3= Guide("PSP.txt", "Путеводитель по судебной практике")
# g4= Guide("PTS.txt", "Путеводитель по трудовым спорам")

# guides_list = [g1, g2, g3, g4]

# # print (g.name, g.articles_link.values(), len(g.articles_link))
# with open("../data/guide_articles/guides_list", "wb") as f:
# 	cPickle.dump(guides_list, f, protocol=pickle.HIGHEST_PROTOCOL)