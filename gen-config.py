import os
import yaml
env_vars = os.environ
dictionary = {var: os.getenv(var).replace('"', '') for var in env_vars}
file = open("configuration.yml", 'w')
yaml.dump(dictionary, file)
