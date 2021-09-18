import os
import yaml
env_vars = os.environ
dictionary = {}

for var in env_vars:
	if vara := os.getenv(var):
		dictionary[var] = vara

file = open("configuration.yml", 'w')
yaml.dump(dictionary, file)
