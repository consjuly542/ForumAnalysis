'''Classes initialization'''

class Question:
    
    def __init__(self):
	    '''
		Methods
		----------
		date: date of question
		answers_count: number of repeats
		views_count: number of views
		region: user's region
		themes_list: list of question's themes
		question_title: question's title on a forum
		question_full: text of question
        question_href_ref: link for question in html
		question_href_txt: text of question in html
		answers_href_ref: link for answers in html
		answers_href_txt: text of answers in html
		answers: list of answers
		'''
        #year, month, day
        self.date = "0000.00.00"
        self.answers_count = -1
        self.views_count = -1
        self.region = "Not stated"
        self.themes_list = []

        self.question_title = "No text"
        self.question_full = "No text"
        self.question_href_ref = []
        self.question_href_txt = []

        self.answers_href_ref = []
        self.answers_href_txt = []
        self.answers = []

    def to_json_dump(self):
	    '''
		Coding in json
		'''
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('utf8')

    def to_dict(self):
	    '''
		Converts from Question to dictionary
		'''
        return self.__dict__
    
    def get_all_text(self):
	    '''
		Makes full text of question
		'''
        all_text = self.question_title + " " + self.question_full + " "
        all_text += " ".join(self.question_href_txt) + " "
        all_text += " ".join(self.answers_href_txt) + " "
        all_text += " ".join(self.answers)
        return all_text

class Question9111(Question):
    '''
	class Question9111
	'''
    def __init__(self):
	    '''
		Methods
		--------
		Inherits Question methods
		questionID: ID of question
		'''
        self.questionID = ""
        super().__init__()

class QuestionKlerk(Question):
    '''
	class QuestionKlerk
	'''
    def __init__(self):
	    '''
		Methods
		--------
		Inherits Question methods
		idx: ID of question
		'''
        self.idx = ""
        super().__init__()

