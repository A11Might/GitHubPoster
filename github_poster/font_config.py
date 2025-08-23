"""
字体优化配置文件
用户可以在这里添加需要包含在字体中的自定义字符，比如用户名中的中文字符
"""

# 在这里添加你的自定义字符（比如用户名中的中文）
# 例如：CUSTOM_CHARS = "张三李四"
CUSTOM_CHARS = ""

# 如果你知道确切需要的字符，可以在这里列出
# 这将进一步减小字体文件大小
EXACT_CHARS_ONLY = False

# 额外的英文单词（比如特殊的项目名称）
ADDITIONAL_WORDS = []

def get_custom_characters():
    """获取所有自定义字符"""
    chars = set(CUSTOM_CHARS)
    
    for word in ADDITIONAL_WORDS:
        chars.update(word)
    
    return chars