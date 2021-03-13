#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random, sys, os, subprocess

# TODO: add types, add fuzzy matching, require use in a sentence
# verbs: handle conjugations (see below)
# nouns: separate singular and plural
pairs = [
	('-imarisha', 'to strengthen'),
	('-endea', 'to approach someone'),
	('fursa', 'opportunity'),
	('-kimbiza', 'to chase'),
	('-amrisha', 'to command, to order'),
	('silaha', 'weapon'),
	('ujinga', 'stupidity, ignorance'),
	('hatua', 'steps, measures'),
	('-shambulia', 'to attack, to invade'),
	('alama', 'sign, signal, clue'),
	('tukio', 'event, happening'),
	('-kaza', 'to fasten, to make tight'),
	('(ma)pato', 'achievement(s), acquisition(s)'),
	('dhambi', 'sin, offense'),
	('(ma)dhara', 'damage(s), injury(s)'),
	('-sisimua', 'to excite, to thrill'),
	('(ma)bwawa', 'pool(s), dam(s)'),
	('-nafuu', 'improve, recover, make progress'),
	('(ma)lengo', 'goal, aim'),
	('shabaha', 'target, aim, intention, ambition'),
	('fimbo', 'stick'),
	('utulivu', 'peace, calmness'),
	('-vunja', 'break'),
	('gharama', 'cost'),
	('-sikitika', 'to be sad'),
	('uchi', 'naked'),
	('huruma', 'compassion'),
]

# 1) active 2) passive
# 3) applicative active 4) applicative passive
# 5) causative 6) stative 7) associative
# 8) negative infinitive
verbs = [
	(
	 ('-weka', 'to put'),
	 ('-wekwa', 'to be put'),
	 ('-wekea', 'to put for someone'),
	 ('-wekewa', 'to be put for someone'), # aliwekewa sumu
	 ('-wekesha', 'to cause to put'),
     ('-wekeka', 'to be placeable'),
     ('-wekana', 'to be placeable together'),
     ('kutoweka', 'to not put'),
	),
	(
	 ('-penda', 'to love'),
	 ('-pendwa', 'to be loved'),
	 ('-pendea', 'to attract someone (?)'),
	 (None, None),
	 ('-pendeza', 'to cause to love, to cause someone to be attracted'),
	 ('-pendeka', 'to be loveable'),
	 ('-pendana', 'to love each other'),
     ('kutopenda', 'to not love'),
	),
	(
	 ('-pata', 'to get'),
	 ('-patiwa', 'to be given'),
	 ('-patia', 'to get for'),
	 ('-patiwa', 'to be provided for'), # alipatiwa na mfalme mahitaji yake
	 (None, None),   # jumanne says "-patisha" isn't a word
	 (None, None), # not "-patika" because it adds "-na" suffix
	 ('-patikana', 'to be available'),
     ('kutopata', 'to not get'),
	),
	(
	 ('-pika', 'to cook'),
	 ('-pikwa', 'to be cooked'),
	 ('-pikia', 'to cook for'),
	 ('-pikiwa', 'to be cooked for'),
	 ('-pikisha', 'to cause to cook'), # alimpikisha chakula
	 ('-pikika', 'cookable'),
	 (None, None),
     ('kutopika', 'to not cook'),
	),
]

num_correct = 0
num_forfeits = 0
num_retries = 0

def prompt(to_show, to_reply):
	global num_retries
	response = input(to_show + ': ')
	if response == 'f':
		print(to_reply)
		# After a forfeit, the user may have entered
		# a response that isn't materially different
		# from the answer. If so, allow them to override
		# so as to reflect a more accurate correct/forfeit count.
		if prompt(to_show, to_reply) == 'OVERRIDE':
			return 'CORRECT'
		else:
			return 'FORFEIT'
	elif response == 'o':
		print("OVERRIDING; this will be marked as correct.")
		return 'OVERRIDE'
	elif response != to_reply:
		num_retries += 1
		print("INCORRECT, try again.")
		return prompt(to_show, to_reply)
	else:
		print("CORRECT")
		return 'CORRECT'

def print_status():
	global num_correct, num_forfeits, num_retries
	print("Correct: %d, Forfeits: %d (Total Retries: %d)" \
		% (num_correct, num_forfeits, num_retries))

# We want to run through the list of pairs twice,
# since we want to prompt for both the elements.
for run_count in range(2):
	# Shuffle the pairs in place.
	random.shuffle(pairs)
	for pair_idx in range(len(pairs)):
		print("\n====== RUN %d, PROMPT %d of %d" \
			% (run_count+1, pair_idx+1, len(pairs)))
		if run_count == 0:
			# On first run, randomly select either of the
			# elements to show to the user.
			prompt_idx = random.randint(0, 1)
		else:
			# On second run, show the pair element
			# that wasn't shown to the user on the first run.
			prompt_idx = (pairs[pair_idx][2] + 1) % 2
		result = prompt(pairs[pair_idx][prompt_idx], \
			pairs[pair_idx][(prompt_idx + 1) % 2])
		if result == 'CORRECT':
			num_correct += 1
		elif result == 'FORFEIT':
			num_forfeits += 1
		print_status()
		if run_count == 0:
			# We append the prompted pair element to the pair,
			# so that on the next run, we prompt for the other.
			pairs[pair_idx] = pairs[pair_idx] + (prompt_idx,)

print("\nCOMPLETE")
