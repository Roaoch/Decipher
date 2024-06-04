import nltk
import re
import wordsegment
import math

import numpy as np

from src.test import probablyties_ru, probablyties_en

from collections import Counter
from functools import reduce
from typing import List, Dict, Optional, Tuple

class Decipher():
    def __init__(self) -> None:
        self.key = None
        self.current_lang = None
        self.avilable_lang = [
            "en",
            "ru"
        ]
        self.first_char = {
            "ru": ord('А'),
            "en": ord('A')
        }
        self.last_char = {
            "ru": ord('Я'),
            "en": ord('Z')
        }
        self.probablyties = {
            "ru": probablyties_ru,
            "en": probablyties_en
        }
        self.alphabet_chars = dict([
            (langs, np.arange(self.first_char[langs], self.last_char[langs] + 1, 1))
            for langs in self.avilable_lang
        ])

    def _get_factor_of_int(self, number: int) -> List[int]:
        return [num for num in range(2, number + 1) if number % num == 0]
    
    def _get_prob_dist(self, text: str | List[str]) -> Dict[str, float]:
        counter = Counter(text)
        total = len(text)
        return dict([
            (key, count / total)
            for key, count in counter.items()
        ])

    def _get_prob_difference(self, sample: List[str]) -> float:
        sample_prob = self._get_prob_dist(sample)
        res = 0
        for k, v in sample_prob.items():
            res += (self.probablyties[self.current_lang][k] - v)**2
        return res

    def _preprocess(self, text: str) -> str:
        text = text.upper()
        text = text.replace("Ё", "Е")
        regex = re.compile('[^A-ZА-Я]')
        return regex.sub('', text)

    def _segment_text(self, text: str) -> List[str]:
        return wordsegment.segment(text=text)
        # WORDS = nltk.corpus.brown.words()
        # COUNTS = Counter(WORDS)

        # def pdist(counter: Counter):
        #     N = sum(counter.values())
        #     return lambda x: counter[x]/N

        # P = pdist(COUNTS)

        # def Pwords(words):
        #     return product(P(w) for w in words)

        # def product(nums):
        #     result = 1
        #     for x in nums:
        #         result *= x
        #     return result

        # def splits(text, start=0, L=20):
        #     return [(text[:i], text[i:]) 
        #             for i in range(start, min(len(text), L)+1)]

        # if not text: 
        #     return []
        # else:
        #     candidates = ([first] + self._segment_text(rest) 
        #                 for (first, rest) in splits(text, 1))
        #     return max(candidates, key=Pwords)

    def _get_lang(self, text: str) -> str:
        if bool(re.search('[А-Я]', text)):
            return 'ru'
        elif bool(re.search('[A-Z]', text)):
            return 'en'
        else:
            raise ValueError('Язык не поддерживается')

    def break_in(self, cipher_text: str) -> Tuple[str, str]:
        cipher_text = self._preprocess(cipher_text)
        if self._get_lang(cipher_text) != 'ru':
            raise ValueError()
        self.current_lang = 'ru'

        threegrams = nltk.ngrams(cipher_text, 3)

        threegrams_freq = nltk.FreqDist(threegrams)
        most_comon = threegrams_freq.most_common(10)

        distance = []
        for symbols, _ in most_comon:
            iter = re.finditer(''.join(symbols), cipher_text)
            last = next(iter)
            for current in iter:
                distance.append(current.start() - last.start())
                last = current
        distance = reduce(lambda prev, e: prev + self._get_factor_of_int(e), distance, [])
        candidate = Counter(distance)
        candidate = candidate.most_common(int(len(candidate) * 0.1))
        
        possible_cryptos = {}
        for expected_len, _ in candidate:
            text_split = [
                [
                    cipher_text[symbol_i]
                    for symbol_i in range(i, len(cipher_text), expected_len)
                ] 
                for i in range(expected_len)
            ]

            key = []
            for expected_split in text_split:
                min_difference = float('inf')
                most_expected_symbol = None
                for key_char in self.alphabet_chars[self.current_lang]:
                    key_char = int(key_char)
                    translated_split = [
                        chr(((ord(symbol) - key_char) % len(self.alphabet_chars[self.current_lang])) + self.first_char[self.current_lang]) 
                        for symbol in expected_split
                    ]
                    difference = self._get_prob_difference(translated_split)
                    if difference < min_difference:
                        min_difference = difference
                        most_expected_symbol = chr(key_char)
                key.append(most_expected_symbol)

            trie_key = ''.join(key)
            trie_decipher = self.dechiper(cipher_text=cipher_text, key=trie_key)
            self.current_lang = "ru"
            trie_decipher_dispersion = self._get_prob_difference(trie_decipher)

            if trie_decipher_dispersion in possible_cryptos:
                possible_cryptos[trie_decipher_dispersion].append((
                    trie_key,
                    trie_decipher_dispersion,
                    trie_decipher
                ))
            else:
                possible_cryptos.update({trie_decipher_dispersion: [(
                    trie_key,
                    trie_decipher_dispersion,
                    trie_decipher
                )]})
        
        cryptos = {}
        for crypto_group in filter(lambda e: len(e) > 1, possible_cryptos.values()):
            minimum = (100000000000, ())
            for candidate in crypto_group:
                if minimum[0] > len(candidate[0]):
                    minimum = (
                        len(candidate[0]),
                        candidate
                    )
            cryptos.update({minimum[1][1]: minimum[1]})

        if len(cryptos) != 0:
            most_expected_disperssion = min(cryptos.keys())
            return (cryptos[most_expected_disperssion][2], cryptos[most_expected_disperssion][0], cryptos.values())
        
        cryptos = {}
        for crypto_group in possible_cryptos.values():
            minimum = (100000000000, ())
            for candidate in crypto_group:
                if minimum[0] > len(candidate[0]):
                    minimum = (
                        len(candidate[0]),
                        candidate
                    )
            cryptos.update({minimum[1][1]: minimum[1]})
        most_expected_disperssion = min(cryptos.keys())
        return (cryptos[most_expected_disperssion][2], cryptos[most_expected_disperssion][0], cryptos.values())

    
    def dechiper(self, cipher_text: str, key: Optional[str]=None) -> str:
        if self.current_lang is None:
            cipher_text = self._preprocess(cipher_text)
            key = self._preprocess(key)
            key_lang = self._get_lang(''.join(key))
            text_lang = self._get_lang(cipher_text)
            if key_lang != text_lang:
                raise ValueError()
            self.current_lang = text_lang

        if key is None:
            key = self.key

        res = []
        for i, symbol in enumerate(cipher_text):
            res.append(chr(
                ((ord(symbol) - ord(key[i % len(key)])) % len(self.alphabet_chars[self.current_lang])) + self.first_char[self.current_lang]
            ))
        
        self.current_lang = None
        return ''.join(res)
    
    def chiper(self, cipher_text: str, key: Optional[str]=None) -> str:
        if self.current_lang is None:
            cipher_text = self._preprocess(cipher_text)
            key = self._preprocess(key)
            key_lang = self._get_lang(''.join(key))
            text_lang = self._get_lang(cipher_text)
            if key_lang != text_lang:
                raise ValueError()
            self.current_lang = self._get_lang(cipher_text)

        if key is None:
            key = self.key

        res = []
        for i, symbol in enumerate(cipher_text):
            res.append(chr(
                ((ord(symbol) + ord(key[i % len(key)])) % len(self.alphabet_chars[self.current_lang])) + self.first_char[self.current_lang]
            ))
        
        self.current_lang = None
        return ''.join(res)