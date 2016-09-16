import csv
import sys
import random
import string
from gtts import gTTS
import os

args = sys.argv
acro = args[1]

combos = {3: ['verb|prep|noun', 'verb|noun|adv', 'noun|verb|adv', 'noun|verb|noun', 'adj|noun|verb', 'adj|noun|noun'],
          4: ['noun|adv|verb|noun', 'noun|verb|noun|adv', 'adj|noun|adv|verb',
              'adj|noun|prep|noun', 'noun|verb|prep|noun'],
          5: ['adj|noun|adv|verb|noun', 'adj|noun|verb|noun|adv'],
          6: ['adv|adj|noun|verb|adj|noun'],
          7: ['adj|noun|verb|adj|adj|noun|adv', 'adv|adj|noun|verb|adj|noun|adv']
}

words = {}

def generate_word_dict():
	for type in ['noun', 'verb', 'adv', 'adj', 'prep']:
		words[type] = {}
		for letter in list(string.ascii_lowercase):
			words[type][letter] = []

		with open(type + '.short', 'r') as f:
			reader = csv.reader(f)
			type_words = list(reader)
			type_words_flat = [item for sublist in type_words for item in
			                   sublist]
			for word in type_words_flat:
				first_letter = word[0].lower()
				words[type][first_letter].append(word)

def generate_acro(acro):
	length = len(str(acro))
	combo = random.choice(combos[length])
	poses = combo.split('|')

	final_acro = []
	for idx, pos in enumerate(poses):
		letter = str(acro[idx]).lower()

		words_to_choose = []
		if letter in string.ascii_lowercase:
			words_to_choose = words[pos][letter]
		elif letter == '*':
			letter = random.choice(list(string.ascii_lowercase))
			words_to_choose = words[pos][letter]

		try:
			final_acro.append(random.choice(words_to_choose))
		except IndexError:
			final_acro.append(letter+'-'+pos)
			pass

	la_acro = " ".join(final_acro)
	return la_acro

def speak(la_acro):
	tts = gTTS(text=la_acro, lang='en')
	tts.save('acro.mp3')
	os.system('cvlc acro.mp3 --play-and-exit 2> /dev/null')

generate_word_dict()
fa = generate_acro(acro)
print(fa)
speak(fa)
