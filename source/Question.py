class Question:
    
    def __init__(self):
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
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('utf8')

    def to_dict(self):
        return self.__dict__
    
    def get_all_text(self):
        all_text = self.question_title + " " + self.question_full + " "
        all_text += " ".join(self.question_href_txt) + " "
        all_text += " ".join(self.answers_href_txt) + " "
        all_text += " ".join(self.answers)
        return all_text

class Question9111(Question):
    def __init__(self):
        self.questionID = ""
        super().__init__()

class QuestionKlerk(Question):
    def __init__(self):
        self.idx = ""
        super().__init__()

