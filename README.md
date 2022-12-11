Hashmap Implementation in Python - README

## Table of Contents
1. [Overview](#Overview)
1. [Chaining](#Chaining)
1. [Open Addressing](#Open Addressing)
1. [Results](#Results)

## Overview
### Description
This project is a hashmap implementation using chaining and open addressing using Python 3.
The purpose of this project is to create a hasmap implementation without using Python's built-in
methods or data structures. 

## Chaining

### Specification
A dynamic array stores the hash table and chaining is implemented for collision resolution with a singly
linked list. The chains of key/value pairs are stored in linked list nodes. Separate DynamicArray and
LinkedList classes are used to assist in the implementation of the chaining hash map. Note that
variables in the SLNode class are not private.
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

## Open Addressing


