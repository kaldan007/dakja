import random
import pyewts

from botok.tokenizers.wordtokenizer import WordTokenizer


converter = pyewts.pyewts()


class Questions:

    def __init__(self, sentence = ""):
        self.sentence = sentence
        self.question = ""
        self.options = []

    def get_word_token(self):
        word_tokenizer = WordTokenizer()
        word_tokens = word_tokenizer.tokenize(self.sentence)
        return word_tokens

    def is_invalid_choice(self, token):
        if token.pos:
            if token.pos == "PART" or len(token.text)<3:
                return True
            else:
                return False
        else:
            return True

    def choose_word_tobe_rm(self, word_tokens):
        token_tobe_rm = random.choice(word_tokens)
        while self.is_invalid_choice(token_tobe_rm):
            token_tobe_rm = random.choice(word_tokens)
        return token_tobe_rm.text

    def set_options(self, word_tobe_rm):
        word_tobe_rm_wylie = converter.toWylie(word_tobe_rm)
        if len(word_tobe_rm_wylie) > 3:
            self.options.append(converter.toUnicode(word_tobe_rm_wylie[:-2]))
            self.options.append(converter.toUnicode(word_tobe_rm_wylie[1:]))
            self.options.append(converter.toUnicode(word_tobe_rm_wylie[:2]+word_tobe_rm_wylie[2+1:]))
        self.options.append(word_tobe_rm)

    def set_question(self, word_tokens):
        question = ""
        word_tobe_rm = self.choose_word_tobe_rm(word_tokens)
        for word_token in word_tokens:
            if word_token.text == word_tobe_rm:
                question += "_"*len(word_tobe_rm)
            else:
                question += word_token.text
        self.set_options(word_tobe_rm)
        self.question = question
        

if __name__ == "__main__":
    sentence = "མི་དེ་ལྕགས་སྒང་ལ་རྩེད་མོ་རྩེ་བསྡད་ཡོད་རེད་ད་རྐུན་མ་བརྒྱབ་པའི་རྗེས་ལ།"
    que = Questions(sentence)
    word_token = que.get_word_token()
    que.set_question(word_token)
    print(que.question)
    print(que.options)



    