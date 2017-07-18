import re

class Link(object):
    """
    Class for Link.
    Very stupid initialization for fast execution.
    Три поля: 0 - часть/пункт, 1 - статья, 2 - название фз. 
    Для каждого поля предусмотрено по 4 группы в regexp - ах.
    В зависимости от порядка частей, присваиваются поля.
    """
    def __init__(self, matches, re_type = [0, 1, 2]):
        # print (matches, len(matches))
        # print (re_type)
        #полный текст ссылки
        self.link_text = matches[0].strip().strip(".")
        #часть или пункт
        self.part_name = None
        #номер части или пункта
        self.part_num = None
        #номер статьи
        self.article_num = None
        #название кодекса или название конкретного ФЗ, если есть.
        self.law_name = "фз"
        #номер ФЗ, если есть.
        self.law_num = None

        for idx, re_part in enumerate(re_type):
            cur_idx = idx * 4 + 1

            # print(idx, cur_idx  + 3)
            # part for point
            if re_part == 0:
                if (matches[cur_idx + 0].startswith("п") or matches[cur_idx + 3].startswith("п")):
                    self.part_name == "пункт"
                elif (matches[cur_idx + 0].startswith("ч") or matches[cur_idx + 3].startswith("ч")):
                    self.part_name == "часть"
                if matches[cur_idx + 1]:
                    self.part_num = matches[cur_idx + 1]
                elif matches[cur_idx + 2]:
                    self.part_num = matches[cur_idx + 2]

            #part for article
            if re_part == 1:
                if matches[cur_idx + 1]:
                    self.article_num = matches[cur_idx + 1]
                else:
                    self.article_num = matches[cur_idx + 2]

            #part for law
            if re_part == 2:
                if matches[cur_idx + 0]:
                    self.law_name = matches[cur_idx + 0]
                if matches[cur_idx + 3].startswith("\""):
                    self.law_name = matches[cur_idx + 3][1:-1]
                if matches[cur_idx + 3].isdigit():
                    self.law_num = matches[cur_idx + 3]

    def print_link(self):
        print (self.__dict__)

    #compare links
    def is_equal(self, link, compare_type='hard'):
        if compare_type == 'hard':
            if self.part_name == link.part_name and self.part_num == link.part_num \
                and self.law_name == link.law_name and self.law_num == link.law_num \
                and self.article_num == link.article_num:
                return True
            else:
                return False
        elif compare_type == 'soft':
            if self.law_name == link.law_name and self.law_num == link.law_num \
                and self.article_num == link.article_num:
                return True
            else:
                return False  



#TODO: включить в регулярки поные названия кодексов
class LinksSearcher(object):
    """
    Class for search simple article links in text.
    method get_simple_links for find all links in text.
    """
    def __init__(self, text):
        self.text = text
        self.cnr_links = 0
        
    def get_simple_links(self):
        re_point = r'(?:(?:\b(пункт|часть|п|ч)\s*\.?\s*(\d+)(?:\s*\.)?)|(?:(\d+)\s*\.?\s*(пункт|часть|п|ч)(?:\s*\.)?))?'
        re_article = r'(?:\b(?:(статья|ст|c)\s*\.?\s*(\d+(?:\.\d+)*)(?:\s*\.)?)|(?:(\d+)\s*\.?\s*(статья|ст|c)(?:\s*\.)?))'
        re_name = r'(?:\b([а-я]к)(?:\s?(рф|российск[а-я]{2} федераци[а-я])?)|(фз|федеральн[а-я]{2-3} закона?)\s?(?:"[\w\s]+"|(?:N|№)?\s?(\d+)))'
        re_delimeter = r'\s{,3}'
        re_parts = [re_point, re_article, re_name]
        links_list = []
        for i, r_1 in enumerate(re_parts):
            for j, r_2 in enumerate(re_parts):
                for k, r_3 in enumerate(re_parts):
                    if i != j and i != k and j != k:
                        # print ("dlfjgnskdjfnakldfnkladb", i, j, k)
                        re_all = re.compile('(' + r_1 + re_delimeter + r_2 +  re_delimeter + r_3 + ')')
#                         print ('(' + r_1 + re_delimeter + r_2 +  re_delimeter + r_3 + ')')
                        all_matches = re.findall(re_all, self.text.lower())
                        # print (all_matches)
                        # link = Link(all_matches[0], [i, j, k])
                        # link.print_link()
                        # if all_matches:
                        # print(all_matches[0])
                        # print ("sgsyLDJSHNLKJSENILEGBJNILSEGBNILES")
                        # for matches in all_matches:
                            # print (matches)
                        links_list += [Link(matches, [i, j, k]) for matches in all_matches if isinstance(matches,tuple)]
    
        uniq_links = [links_list[0]]
        for i_1, l_1 in enumerate(links_list[1:]):
            is_uniq = True
            for j_1, l_2 in enumerate(uniq_links):
                if l_2.is_equal(l_1, 'soft'):
                    # print (l_1, l_2)
                    is_uniq = False
                    break
            if is_uniq:
                uniq_links.append(l_1)
                                
        # for l in uniq_links:
        #     print (l.print_link())
            
        return uniq_links