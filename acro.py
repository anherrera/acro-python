import csv
import sys
import random
import string
from gtts import gTTS
import os

args = sys.argv
acro = args[1]

combos = {3: ['noun|verb|noun', 'verb|noun|adv', 'noun|verb|adv', 'adv|verb|noun'], 
          4: ['noun|adv|verb|noun', 'noun|verb|noun|adv'],
          5: ['adj|noun|adv|verb|noun', 'adj|noun|verb|noun|adv']
}

words = {}
for type in ['noun', 'verb', 'adv', 'adj']:
	words[type] = {}
	for letter in list(string.ascii_lowercase):
		words[type][letter] = []

	with open(type + '.exc', 'r') as f:
		reader = csv.reader(f)
		type_words = list(reader)
		type_words_flat = [item for sublist in type_words for item in sublist]
		for word in type_words_flat:
			first_letter = word[0].lower()
			words[type][first_letter].append(word)

length = len(str(acro))
combo = random.choice(combos[length])
poses = combo.split('|')

final_acro = []
for idx, pos in enumerate(poses):
	letter = str(acro[idx]).lower()
	words_to_choose = words[pos][letter]
	final_acro.append(random.choice(words_to_choose))

la_acro = " ".join(final_acro)

print(la_acro)

tts = gTTS(text=la_acro, lang='en')
tts.save('acro.mp3')
os.system('vlc acro.mp3 --play-and-exit')
