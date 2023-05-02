from django import template

register = template.Library()

@register.filter(name='Censor')
def Censor(value):
    Stoplist = ['идиот', 'хуйня', 'пидорас', 'титьками']
    sentence = value.split()
    for i in Stoplist:
        for words in sentence:
            if i in words:
                pos = sentence.index(words)
                sentence.remove(words)
                sentence.insert(pos, '*' * len(i))
    return " ".join(sentence)