# Hashmap Implementation in Python - README 🔢

## Table of Contents
1. [Overview](#Overview)
1. [Chaining](#Chaining)
1. [Open-Addressing](#Open-Addressing)
1. [Reflection](#Reflection)

## Overview
### Description
This project is a hashmap implementation using chaining and open addressing using Python 3.
The purpose of this project is to create a hasmap implementation without using Python's built-in
methods or data structures. 

## Chaining

### Specification
A dynamic array stores the hash table and chaining is implemented for collision resolution with a singly linked list. The chains of key/value pairs are stored in linked list nodes. Separate DynamicArray and LinkedList classes are used to assist in the implementation of the chaining hash map. Note that variables in the SLNode class are not private.
### Implementation
- **put(self, key: str, value: object) -> None**: this method updates key/value pair in the hash map. 
If the given key already exists in the hashmap, then its associated value must be replaced with the
new value. If the given key is not in the hash map, a new key/value pair is added. For the hashmap,
the table is resized to double its capacity when this method is called and the current load factor
of the table is greater than or equal to 1.0.
- **empty_buckets(self) -> int**: This method returns the number of empty buckets in the hash table.
- **table_load(self) -> float**: This method returns the current hash table load factor.
- **clear(self) -> None**: This method clears the contents of the hash map. It does not change the
underlying table capacity.
- **resize_table(self, new_capacity: int) -> None**: This method changes the capacity of the internal
hash table. All existing key/value reamins in the new hash map, and all hash table linkes are rehashed
through their corresponding hash function. First checks that new_capacity is not less than 1 and that
if it is then does nothing. If new_capacity is > 0, it makes sure that it is a prime number (to help
reduce collisions). If not, then it changes it to its next highest prime number. The methods _is_prime()
and _next_prime() are used to assist with this.
- **get(self, key: str) -> object**: This method returns the value associated with the given key. If the key is not in the map, the method returns None
- **contains_key(self, key:str) -> bool**: This method returns True if the given key is in the hash map, otherwise it returns False. An empty hashmap does not contain any keys.
- **return(self, key: str) -> None**: This method removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exceptions are raised).
- **get_keys_and_values(self) -> DynamicArray**: This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of they keys in the dynamic array does not matter.
- **find_mode(arr: DynamicArray) -> (DynamicArray, int)**: A standalone function outside of the HashMap class that receieves a dynamic array. This function returns a tuple containing, in this order, a dynamic array comprising the mode value/s of the array, and an integer that represents the highest frequenncy. If there is more than one value with the highest frequency, all values at that frequency is included in the array being returned (order does not matter). If there is only one mode, the dynamic array will only contain that value. The input array must contain at least one element and all values in the array are strings. Implemented with O(N) time complexity. A separate chaining hash map isused.

## Open-Addressing

### Specification
A dynamic array is used to store the hash table and uses open addressing with **quadratic probing** for collision resolution inside the dyanamic array. Key/value pairs are stored in the array.
### Implementation
- **put(self, key: str, value: object) -> None**: This method updates the key/value pair in the hash map. If the given key already exists in the hash map, then its associated value must be replaced with the new value. If the given key is not in the hash map, a new key/value pair must be added. For this hashmap implementation, the table is resized to double its current capacity when this method is called and the current load factor of the table is greater or equal to 0.5.
- **table_load(self) -> float**: This method returns the current hash table load factor.
- **empty_buckets(self) -> int**: This method returns the number of empty buckets in the hash table.
- **resize_table(self, new_capacity: int) -> None**: This method changes the capacity of the internal hash table. All existing key/value pairs remain in the new hash map, and all hash table linkes are rehashed through the corresponding hash function. Checks if new_capacity is not less than the current number of elements in the hash map and if so, then the method does nothing. If new_capacity is valid, it makes sure that it is a prime number to help avoid collisions. If not, uses _is_prime() and _next_prime() to find the next highest prime number.
- **get(self, key: str) -> object**: This method returns the value associated with the given key. If they key is not in the hash map, the method returns None.
- **contains_key(selff, key: str) -> bool**: This method returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys.
- **remove(self, key:str) -> None**: This method removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exceptions are raised).
- **clear(self) -> None**: This method clears the contents of the hash map. It does not change the underlying hash table capacity.
- **get_keys_and_values(self) -> DynamicArray**: This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter.
- **__iter__()**: This method enables iteration of the hash map. A variable is initialized to track the iterator's progress through the hash map's contents.
- **__next__()**: This method returns the next item in the hash map, based on current location of the iterator.

## Reflection
This was my first data structures project involving hash map implementation with Python 3. I learned that there are various ways to handle collisions, such as open addressing and chaining. Furthermore, with open addressing, I can use different probing methods to handle collisions. I learned that I can also use linear probing or double hashing. What could be improved here is that quadratic probing can also be used to iterate across the hash map, rather than iterating through linearly. Tombstones are used as a way to label removed values to prevent a search for an elemment from haulting due to an empty space. Quadratic probing is preferred over linear probing to reduce likelihood of clustering. A low load factor is achieved to avoid collisions, however, too low of a load factor can lead to unfavorable space usage so there needs to be balance.
