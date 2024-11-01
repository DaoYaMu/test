##题目000：找出字符串s=”aaabbbccceeefff111144444″中，字符出现次数最多的字符
s = "aaaaaabbbccceeefff111144444"

# 使用字典来存储字符出现的次数
char_count = {}

# 统计字符出现的次数
for char in s:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1

# 找到出现次数最多的字符
max_char = max(char_count, key=char_count.get)
max_count = char_count[max_char]

print(f"字符 '{max_char}' 出现最多，出现次数为 {max_count} 次")
print(char_count)

