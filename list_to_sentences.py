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
"""
__author__ = 'viatoriche'

import re

class SentenceBuilder():
    punctuation_marks = '.?!'
    punctuation_marks_pattern = r'[{}]'.format(punctuation_marks)
    parts = []
    sentences = []

    def __iter__(self):
        return self

    def get_sentences(self):
        self.sentences = self.parts

    @classmethod
    def split_part(cls, part):
        parts = [part.strip() for part in re.split(cls.punctuation_marks_pattern, part)]
        if

    def send(self, part):
        parts = self.split_part(part)
        self.parts += parts

    def next(self):
        self.get_sentences()
        return builder.sentences


sentence_builder = SentenceBuilder

in_list = ("Hello", "how are you.", "Call me later. Can I trust you? Ok.")

builder = sentence_builder()

result = []
for part in in_list:
    builder.send(part)
    sentence = next(builder)
    print sentence

    if sentence:
        result.append(sentence)

assert result == ['Hello how are you', 'Call me later', 'Can I trust you', 'Ok']
