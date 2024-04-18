def romanToInt(s: str) -> int:
        roman_to_integer = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000,
        }
        s = s.replace("IV", "IIII").replace("IX", "VIIII").replace("XL", "XXXX").replace("XC", "LXXXX").replace("CD", "CCCC").replace("CM", "DCCCC")
        print(list(map(lambda x: roman_to_integer[x], s)))
        return sum(map(lambda x: roman_to_integer[x], s))

# print(romanToInt("DXCIV"))

a=[1,4,9,3,20,30]
discarded = set()
house_values = {value:idx for idx,value in enumerate(a)}
a.sort(reverse=True)
print(a)
print(house_values)