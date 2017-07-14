class LinksSearcher(object):
    """
    Class for search simple article links in text.
    method get_simple_links for find all links in text.
    """
    def __init__(self, text):
        self.text = text
        self.cnr_links = 0
        
    def get_simple_links(self):
        re_point = r'((\b(пункт|п)\s*\.?\s*\d+(\s*\.)?)|(\d+\s*\.?\s*(пункт|п)(\s*\.)?)\b)?'
        re_article = r'(\b((статья|ст|c)\s*\.?\s*(\d+(\.\d+)*)(\s*\.)?)|(\d+\s*\.?\s*(статья|ст|c)(\s*\.)?)\b)'
        re_name = r'(\b([а-я]к|фз)(\s?рф)?\b)'
        re_delimeter = r'\s?'
        re_parts = [re_point, re_article, re_name]
        links_list = []
        for i, r_1 in enumerate(re_parts):
            for j, r_2 in enumerate(re_parts):
                for k, r_3 in enumerate(re_parts):
                    if i != j and i != k and j != k:
#                         print (i, j, k)
                        re_all = re.compile('(' + r_1 + re_delimeter + r_2 +  re_delimeter + r_3 + ')')
#                         print ('(' + r_1 + re_delimeter + r_2 +  re_delimeter + r_3 + ')')
                        all_matches = re.findall(re_all, self.text.lower())
#                         print(all_matches)
                        links_list += [m[0].strip() if isinstance(all_matches[0],tuple) and all_matches[0] != '' else m \
                                       for m in all_matches]
    
        uniq_links = []
        links_list = list(set(links_list))
        for i_1, l_1 in enumerate(links_list):
            is_uniq = True
            for j_1, l_2 in enumerate(links_list[:i_1] + links_list[i_1 + 1:]):
                if l_2.find(l_1) != -1:
                    print (l_1, l_2)
                    is_uniq = False
                    break
            if is_uniq:
                uniq_links.append(l_1)
                                
        for l in uniq_links:
            print(l)
            
        return uniq_links