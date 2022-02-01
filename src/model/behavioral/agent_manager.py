import csv
from .attribute.generator_attribute import GeneratorAttribute

def load_attributes_generator(file_names,rng):
	return GeneratorAttribute(file_names,rng)

def test():
	print("test")