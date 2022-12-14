# Description: Hash Map Chaining Implementation
# Uses a Dynamic Array and Linked List as underlying Data Structure


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        If the given key exists, then associated value is replaced by new value.
        If given key is not in the hash map, a new key/value pair must be added.
        The table is resized to double its current capacity when current load factor is >= 1.0.
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hash_key = self._hash_function(key) % self._capacity
        chain_key = self._buckets.get_at_index(hash_key)

        # If the key in the hash map does not yet exist, then simply add the key to the corresponding bucket
        # and its value, which will be a linked list node.
        if chain_key.length() == 0:
            chain_key.insert(key, value)
            self._size += 1
        else:
            # iterate through the linked list and check if the same key exists. If it does then do nothing
            for item in chain_key:
                if item.key == key:
                    chain_key.remove(key)
                    chain_key.insert(key, value)
                    return
            chain_key.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        c = 0
        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() == 0:
                c += 1
        return c

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        Load factor is the average number of elements stored in the bucket.
        Load factor = total number of elements stored in the table / number of buckets.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key/value pairs must remain in the new hash map, and all hash table links are rehashed.
        It first checks that new_capacity is not less than 1. If it is, then it does nothing.
        If new_capacity >= 1, it makes sure that it is a prime number. If not, then it will round up to the
        next highest prime number.
        """
        # First, check if new_capacity is less than 1. If it is then do nothing
        if new_capacity < 1:
            return

        # A check for a new capacity with a prime number size
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # First, create a new Hashmap with the new capacity
        new_table = HashMap(new_capacity, self._hash_function)

        # this is to prevent next_prime from going to 3, when it should stay at 2 (since 2 is prime)
        if new_capacity == 2:
            new_table._capacity = 2

        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                # chain_key = self._buckets.get_at_index(i).__iter__()
                for item in self._buckets.get_at_index(i):
                    new_table.put(item.key, item.value)
                # for _ in range(self._buckets.get_at_index(i).length()):
                #     node = chain_key.__next__()
                #     new_table.put(node.key, node.value)

        # Reassigning new values to self
        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table._capacity

    def get(self, key: str):
        """
        Returns the value associated with given key. If key is not in the hash map, return None.
        """
        # This passes the key through a hash function and spits out the corresponding key in the buckets.
        hash_key = self._hash_function(key) % self._capacity

        # Storing the corresponding bucket into a variable to be used later.
        chain_key = self._buckets.get_at_index(hash_key)

        if chain_key.length() == 0:
            return None
        else:
            for item in self._buckets.get_at_index(hash_key):
                if item.key == key:
                    return item.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map, otherwise returns False.
        An empty hash map does not contain any keys.
        """

        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                for item in self._buckets.get_at_index(i):
                    if item.key == key:
                        return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If key is not in the hash map,
        the method does nothing (no exception needs to be raised).
        """
        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                for item in self._buckets.get_at_index(i):
                    if item.key == key:
                        self._buckets.get_at_index(i).remove(key)
                        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        The order of the keys in the dynamic array does not matter.
        """
        da = DynamicArray()

        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                for item in self._buckets.get_at_index(i):
                    da.append((item.key, item.value))

        return da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    A standalone function outside of the HashMap class that receives a dynamic array (not guaranteed to be sorted).
    Returns a tuple containing, in this order, a dynamic array comprising the mode (most occurring) value/s of the
    array, and an integer that represents the highest frequency (how many times they appear).

    If more than one value has the highest frequency, all values at that frequency is included in the array
    being returned (order does not matter). If there is only one mode, the dynamic array will only contain that
    value.

    The input array must contain at least one element, and that all values stored in the array will be strings.

    Implemented in O(N) time complexity. A separate chaining hash map is recommended.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    for i in range(da.length()):
        if not map.contains_key(da.get_at_index(i)):
            map.put(da.get_at_index(i), 1)
        else:
            map.put(da.get_at_index(i), map.get(da.get_at_index(i)) + 1)

    frequency = 0
    arr = map.get_keys_and_values()
    mode_arr = DynamicArray()
    for i in range(arr.length()):
        if frequency < arr.get_at_index(i)[1]:
            frequency = arr.get_at_index(i)[1]

    for i in range(arr.length()):
        if arr.get_at_index(i)[1] == frequency:
            mode_arr.append(arr.get_at_index(i)[0])

    # a tuple containing a dynamic array of the most frequent values and the frequency
    return mode_arr, frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - put example 22")
    # print("-------------------")
    # m = HashMap(11, hash_function_2)
    # m.put('key' + str(271), 110)
    # m.put('key' + str(77), -155)
    # m.put('key' + str(654), -390)
    # m.put('key' + str(303), 851)
    # m.put('key' + str(380), 547)
    # m.put('key' + str(783), 813)
    # m.put('key' + str(167), 218)
    # m.put('key' + str(883), 142)
    # m.put('key' + str(990), -597)
    # m.put('key' + str(49), -408)
    # m.put('key' + str(328), 847)
    # m.put('key' + str(303), 146)

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    # print("\nGRADESCOPE - resize example 1")
    # print("----------------------")
    # m = HashMap(89, hash_function_2)
    # m.put('key403', 758)
    # m.put('key988', -720)
    # m.put('key49', 134)
    # m.put('key640', -298)
    # m.put('key504', 225)
    # m.put('key353', 570)
    # m.put('key670', 39)
    # m.put('key890', -127)
    # m.put('key504', 225)
    # m.put('key584', 246)
    # m.put('key984', -974)
    #
    # m.resize_table(2)
    # print(m)
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
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
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    # #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    # print("EXPECTED: ", [('2', '20'), ('3', '30'), ('20', '200'), ('4', '40'), ('5', '50')])

    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    #
    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )
    #
    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
