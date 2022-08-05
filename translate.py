from googletrans import Translator

# function that translate some text from any language to english
def translate(toTranslate):
    translator = Translator() # create an instance of translator
    translations = translator.translate(toTranslate, dest = "en") 
    return translations.text  

# print(translate("hola mundo"))


