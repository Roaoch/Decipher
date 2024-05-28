import nltk
import re
import wordsegment

import numpy as np

from src.test import probablyties

from collections import Counter
from functools import reduce
from typing import List, Dict, Optional, Tuple
from langdetect import detect

class Decipher():
    def __init__(self) -> None:
        self.key = None
        self.first_char = ord('А')
        self.last_char = ord('Я')
        self.probablyties = probablyties
        self.alphabet_chars = np.arange(self.first_char, self.last_char + 1, 1)
        self.crypt_matrix = self._get_crypt_matrix()

    def _get_factor_of_int(self, number: int) -> List[int]:
        return [num for num in range(2, number + 1) if number % num == 0]
    
    def _get_prob_dist(self, text: str | List[str]) -> Dict[str, float]:
        counter = Counter(text)
        total = len(text)
        return dict([
            (key, count / total)
            for key, count in counter.items()
        ])
    
    def _get_crypt_matrix(self) -> np.ndarray:
        matrix = []
        matrix_alphabet = self.alphabet_chars.copy()
        for _ in self.alphabet_chars:
            matrix.append(matrix_alphabet.tolist())
            matrix_alphabet = np.roll(matrix_alphabet, -1)
        return np.array(matrix)

    def _get_prob_difference(self, sample: List[str]) -> float:
        sample_prob = self._get_prob_dist(sample)
        res = 0
        for k, v in sample_prob.items():
            res += (self.probablyties[k] - v)**2
        return res

    def _preprocess(self, text: str) -> str:
        text = text.upper()
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

    def break_in(self, cipher_text: str) -> Tuple[str, str]:
        cipher_text = self._preprocess(cipher_text)

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
        
        min_dispersion = float('inf')
        most_expected_key = None
        most_expected_dechipher = None
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
                for key_char in self.alphabet_chars:
                    key_char = int(key_char)
                    translated_split = [
                        chr(((ord(symbol) - key_char) % len(self.alphabet_chars)) + self.first_char) 
                        for symbol in expected_split
                    ]
                    difference = self._get_prob_difference(translated_split)
                    if difference < min_difference:
                        min_difference = difference
                        most_expected_symbol = chr(key_char)
                key.append(most_expected_symbol)

            trie_decipher = self.dechiper(cipher_text=cipher_text, key=''.join(key))
            trie_decipher_dispersion = self._get_prob_difference(trie_decipher)
            if trie_decipher_dispersion <= min_dispersion and (most_expected_key is None or len(key) < len(most_expected_key)):
                min_dispersion = trie_decipher_dispersion
                most_expected_key = key
                most_expected_dechipher = trie_decipher
        return (most_expected_dechipher, ''.join(most_expected_key))
    
    def dechiper(self, cipher_text: str, key: Optional[str]=None) -> str:
        if key is None:
            key = self.key

        res = []
        for i, symbol in enumerate(cipher_text):
            res.append(chr(
                ((ord(symbol) - ord(key[i % len(key)])) % 32) + self.first_char
            ))
        return ''.join(res)