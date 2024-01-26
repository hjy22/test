# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10	#rehashing 10 times, return false

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[int]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		current_circle = 0
		current_tableID = 0
		while current_circle <= self.CYCLE_THRESHOLD:
			hash_value = self.hash_func(key, current_tableID)
			if self.tables[current_tableID][hash_value] is None:
				self.tables[current_tableID][hash_value] = key
				return True
			else:
				current_value = self.tables[current_tableID][hash_value]
				self.tables[current_tableID][hash_value] = key
				key = current_value
				current_tableID = (current_tableID + 1) % 2
				current_circle += 1	
		return False
	
	def lookup(self, key: int) -> bool:
		hash_value1 = self.hash_func(key, 0)
		hash_value2 = self.hash_func(key, 1)
		if self.tables[0][hash_value1] == key or self.tables[1][hash_value2] == key:
			return True
		else:
			return False

	def delete(self, key: int) -> None:
		hash1_value = self.hash_func(key, 0)
		hash2_value = self.hash_func(key, 1)
		if self.tables[0][hash1_value] == key:
			self.tables[0][hash1_value] = None
		elif self.tables[1][hash2_value] == key:
			self.tables[1][hash2_value] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		old_tables = self.tables.copy()
		self.tables = [[None]*self.table_size for _ in range(2)]
		for table in old_tables:
			for element in table:
				if element != None:
					self.insert(element)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define

