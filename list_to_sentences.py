# coding: UTF-8
"""Converter to sentences from list

Description:

Написать сопрограмму которая собирает переданные ей строки в предложения (по наличию [. ? ! ... ]) и записывает предложения в список. Тест:

in_list = ("Hello", "how are you.", "Call me later. Can I trust you? Ok.")

builder = sentence_builder()

result = []
for part in in_list:
    builder.send(part)
    sentence = next(builder)

    if sentence:
        result.append(sentence)

assert result == ['Hello how are you', 'Call me later', 'Can I trust you', 'Ok']

Примечание:

В тесте ошибка

for part in in_list:
вызовет метод next(builder) лишь три раза, так как в in_list у нас три значения
таким образом мы можем добавить в result лишь три значения, а ожидается что там должно быть четыре значения
Я переписал тест, вместо того чтобы ожидать предложение в виде строки, билдер будет отдавать список
Таким образом список можно конкатенировать и получить правильный результат
"""
__author__ = 'viatoriche'

import re

punctuation_marks = '.?!'
punctuation_marks_pattern = r'[{}]'.format(punctuation_marks)

def split_part(part):
    return [part.strip() for part in re.split(punctuation_marks_pattern, part) if part != '']

class SentenceBuilder():
    parts = []
    sentences = None

    def __iter__(self):
        return self

    def send(self, part):
        self.parts.append(part)
        if re.search(punctuation_marks_pattern, part):
            self.sentences = split_part(' '.join(self.parts))
            self.parts = []

    def next(self):
        if self.sentences is not None:
            return self.sentences


sentence_builder = SentenceBuilder

in_list = ("Hello", "how are you.", "Call me later. Can I trust you? Ok.")

builder = sentence_builder()

result = []

for part in in_list:
    builder.send(part)
    # sentence = next(builder)
    # получаем список значений, вместо одного значения (как было раньше) либо None
    sentences = next(builder)

    # if sentence:
    if sentences:
        #result.append(sentence)
        # Конкатенируем список
        result += sentences

assert result == ['Hello how are you', 'Call me later', 'Can I trust you', 'Ok']

# Более красивое решение разбиения на предложения:
result = split_part(' '.join(in_list))

assert result == ['Hello how are you', 'Call me later', 'Can I trust you', 'Ok']
