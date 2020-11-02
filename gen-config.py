import os
import yaml
dictionary = dict()
env_vars = os.environ
for var in env_vars:
    dictionary[var] = os.getenv(var).replace('"', '')
file = open("configuration.yml", 'w')
yaml.dump(dictionary, file)
