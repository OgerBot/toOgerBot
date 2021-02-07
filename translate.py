import translations
import random

class OgerTranslator():

    @classmethod
    def translate(cls, message: str):
        words = message.split(" ")
        translated = ""

        for word in words:
            if word[0:4] == "http":
                translated += " "+word if translated else word
                continue

            punctuations = translations.punctuations.keys()

            linebreak = ""
            while (word[0] in "\r\n"):
                linebreak += word[0]
                word = word[1:]

            quotation = ""
            if word[0] == '"':
                quotation = "start"
                word = word[1:]

            if word[-1] == '"':
                quotation = "end"
                word = word[0:-1]          

            punctuation = ""
            if (word[-1] in punctuations):
                punctuation = word[-1]
                word = word[0:-1]

            # translate whole words if translation available
            if (translations.translations.__contains__(word)):
                word = translations.translations[word][random.randint(0, len(translations.translations[word])-1)]
            # translate chars otherwise
            else:
                for twist in translations.twistedChars:
                    word = ("^"+word+"$").replace(twist, translations.twistedChars[twist][random.randint(0, len(translations.twistedChars[twist])-1)])[1:-1]

            if (punctuation):
                if (translations.punctuations.__contains__(punctuation)):
                    punctuation = translations.punctuations[punctuation][random.randint(0, len(translations.punctuations[punctuation])-1)]
                word += punctuation

            if quotation == "start":
                word = translations.quotationMark[random.randint(0, len(translations.quotationMark)-1)] + word
            elif quotation == "end":
                word += '"'

            translated += " " + linebreak + word if translated else linebreak + word

        return translated

#print(OgerTranslator.translate('"Rainer stinkt!"'))
