import csv
from .attribute import generator_attribute as ga

def load_attributes_generator(file_names):
	ga.GeneratorAttribute(file_names)

def test():
	print("test")