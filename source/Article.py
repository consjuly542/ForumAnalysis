# coding: utf-8

class Article:

    def __init__(self):
        self.law = None                 #без кавычек
        self.article = None             #без кавычек
        self.article_num = None
        self.law_num = None
        self.flaw_num = None
        self.chapter_num = None
        self.date = "0000.00.00"
        self.edit_date = "0000.00.00"
        self.law_ID = None
        self.article_ID = None           #law_ID + '_' + article_num
        self.article_link = None

    def to_dict(self):
        return self.__dict__

    # def __hash__(self):
    #     return hash(self.article_ID)