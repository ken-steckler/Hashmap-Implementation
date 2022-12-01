# Name: Ken Steckler
# OSU Email: stecklek@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: December 2, 2022
# Description: Hash Map Open Addressing Implementation

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        If the given key exists in the hash map, its associated value
        is replaced with the new value.
        If the given key is not in the hash map, new key/value pair is added.
        Table is resized to double its current capacity when the method is called
        and the current load factor of the table is >= 0.5
        """
        # If table load is greater than or equal to 0.5 then resize table
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash_key = self._hash_function(key) % self._capacity

        # if the bucket does not contain a key and value then simply insert the key value pair and increment size
        if self._buckets.get_at_index(hash_key) is None:
            self._buckets.set_at_index(hash_key, HashEntry(key, value))
            self._size += 1

        else:
            j = 1
            quad_key = hash_key
            while self._buckets.get_at_index(quad_key):
                # if the key is found in the hash, then replace without incrementing size and return
                # if it was previously a tombstone then do increment size
                if self._buckets.get_at_index(quad_key).key == key:
                    if self._buckets.get_at_index(quad_key).is_tombstone:
                        self._buckets.set_at_index(quad_key, HashEntry(key, value))
                        self._size += 1
                        self._buckets.get_at_index(quad_key).is_tombstone = False
                    else:
                        self._buckets.set_at_index(quad_key, HashEntry(key, value))
                    return
                quad_key = (hash_key + j**2) % self._capacity
                j += 1

            self._buckets.set_at_index(quad_key, HashEntry(key, value))
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key/value pairs remain in the new hash map and all hash table links are rehashed.
        new_capacity must be > current number of elements in the hash map. If not, the method does nothing.
        Checks if new_capacity is a prime number. If not, it rounds up to the nearest prime number.
        """
        if new_capacity <= self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_table = HashMap(new_capacity, self._hash_function)

        # this is to prevent next_prime from going to 3, when it should stay at 2 (since 2 is prime)
        if new_capacity == 2:
            new_table._capacity = 2

        # be sure to not add size + 1 if rehashing tombstone values
        for i in range(self._capacity):
            if self._buckets.get_at_index(i):
                pair = self._buckets.get_at_index(i)
                new_table.put(pair.key, pair.value)

        # Reassigning new values to self
        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table.get_capacity()

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash
        map, then the method returns None.
        """

        for item in self:
            if item:
                if item.key == key and not item.is_tombstone:
                    return item.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map, otherwise returns False.
        An empty hash map does not contain any keys.
        """
        for item in self:
            if item:
                if item.key == key and not item.is_tombstone:
                    return True
        return False

        # for i in range(self._capacity):
        #     if self._buckets.get_at_index(i):
        #         if self._buckets.get_at_index(i).key == key and not self._buckets.get_at_index(i).is_tombstone:
        #             return True

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing (no exceptions
        is raised)
        """

        for i in range(self._capacity):
            if self._buckets.get_at_index(i):
                if self._buckets.get_at_index(i).key == key:
                    # only set tombstone to true if it is not already
                    if not self._buckets.get_at_index(i).is_tombstone:
                        self._buckets.get_at_index(i).is_tombstone = True
                        self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying
        hash table capacity.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value
        pair stored in the hash map. The order of the keys in the dynamic array
        does not matter.
        """
        arr = DynamicArray()

        for i in range(self._capacity):
            if self._buckets.get_at_index(i) and not self._buckets.get_at_index(i).is_tombstone:
                arr.append((self._buckets.get_at_index(i).key, self._buckets.get_at_index(i).value))

        return arr

    def __iter__(self):
        """
        Enables the hash map to iterate across itself.
        A variable is initialized to track the iterator's progress
        through the hash map's contents.
        """
        self.index = 0
        return self

    def __next__(self):
        """
        This method returns item n the hash map, based on the current location of
        the iterator.
        """
        try:
            value = None
            while value is None or value.is_tombstone is True:
                value = self._buckets.get_at_index(self.index)
                self.index += 1
        except DynamicArrayException:
            raise StopIteration

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)

    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
