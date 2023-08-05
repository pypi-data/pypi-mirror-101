import jaconv


vowel_map =\
    [
        ['ア', 'アカサタナハマヤラワガザダバパァ　ャヮ'],
        ['イ', 'イキシチニヒミ　リ　ギジヂビピィ　　　'],
        ['ウ', 'ウクスツヌフムユル　グズヅブプゥッュ　'],
        ['エ', 'エケセテネヘメ　レ　ゲゼデベペェ　　　'],
        ['オ', 'オコソトノホモヨロヲゴゾドボポォ　ョ　'],
    ]

consonant_map = \
    [
        ['k', 'カキクケコ'],
        ['s', 'サシスセソ'],
        ['t', 'タチツテト'],
        ['n', 'ナニヌネノ'],
        ['h', 'ハヒフヘホ'],
        ['m', 'マミムメモ'],
        ['y', 'ヤ　ユ　ヨ'],
        ['r', 'ラリルレロ'],
        ['w', 'ワ　　　ヲ'],
        ['g', 'ガギグゲゴ'],
        ['z', 'ザジズゼゾ'],
        ['d', 'ダヂヅデド'],
        ['b', 'バビブベボ'],
        ['p', 'パピプペポ'],
    ]

alphabets = {
    'a': 'エー',
    'b': 'ビー',
    'c': 'シー',
    'd': 'ディー',
    'e': 'イー',
    'f': 'エフ',
    'g': 'ジー',
    'h': 'エッチ',
    'i': 'アイ',
    'j': 'ジェー',
    'k': 'ケー',
    'l': 'エル',
    'm': 'エム',
    'n': 'エヌ',
    'o': 'オー',
    'p': 'ピー',
    'q': 'キュー',
    'r': 'アール',
    's': 'エス',
    't': 'ティー',
    'u': 'ユー',
    'v': 'ブイ',
    'w': 'ダブリュ',
    'x': 'エックス',
    'y': 'ワイ',
    'z': 'ゼット',
}


def text2boin(text, cv='katakana'):
    """ 母音に変換 """
    if not cv in ('katakana', 'hiragana'):
        raise ValueError("argument cv allows 'katakana' or 'hiragana'")

    ret = ''
    text = jaconv.hira2kata(text)

    # replace
    for i, c in enumerate(text):
        if c == '　':
            ret += '　'

        for pair in vowel_map:
            # match
            if c in pair[1]:
                ret += pair[0]
        # not match
        if len(ret) == i:
            ret += c

    if cv == 'hiragana':
        ret = jaconv.kata2hira(ret)
    return ret


def convert_vowel(char, vowel):
    """ 母音を変換 """
    char_romanize = ''
    vowel_list = ['ア', 'イ', 'ウ', 'エ', 'オ']

    # convert vowel
    for i in range(len(vowel_map)):
        for j in range(len(vowel_map[i][1])):
            if char == vowel_map[i][1][j]:
                char_romanize = vowel_map[vowel_list.index(vowel)][1][j]
                return char_romanize

    return char


def romanize(vowel, consonant):
    """ ローマ字変換 """
    result = ''

    for pattern in consonant_map:
        if consonant == pattern[0]:
            index = 'aiueo'.index(vowel)
            if pattern[1][index] != '　':
                result = pattern[1][index]

    return result


def alphabet_to_reading(text):
    result = ''

    text = text.lower()
    for ch in text:
        if ch in alphabets:
            result += alphabets[ch.lower()]

    return result
