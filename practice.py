#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random, sys, os, subprocess

pairs = [
	('kuiamrisha', 'to strengthen'),
	('kuendea', 'to approach someone'),
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
