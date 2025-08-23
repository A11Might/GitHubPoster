#!/usr/bin/env python3
"""
字体子集化工具
只保留SVG中实际使用的字符，大幅减少字体文件大小
"""

import os
import re
try:
    from fontTools.ttLib import TTFont
    from fontTools import subset
    FONTTOOLS_AVAILABLE = True
except ImportError:
    FONTTOOLS_AVAILABLE = False
    print("Warning: fontTools not installed. Font subsetting disabled.")
    print("Install with: pip install fonttools")

try:
    from .font_config import get_custom_characters
except ImportError:
    def get_custom_characters():
        return set()


class FontSubsetter:
    def __init__(self):
        # SVG中可能用到的所有字符
        self.base_chars = set()
        
        # 数字 0-9
        self.base_chars.update('0123456789')
        
        # 英文字母 a-z A-Z
        self.base_chars.update('abcdefghijklmnopqrstuvwxyz')
        self.base_chars.update('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        # 常用符号
        self.base_chars.update(' .,:-/')
        
        # 月份缩写 (已包含在字母中，但明确列出)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for month in months:
            self.base_chars.update(month)
        
        # 单位
        units = ['km', 'hours', 'mins', 'miles', 'minutes']
        for unit in units:
            self.base_chars.update(unit)
    
    def add_custom_chars(self, additional_chars):
        """添加额外的字符（比如中文姓名）"""
        self.base_chars.update(additional_chars)
    
    def extract_chars_from_svg(self, svg_path):
        """从SVG文件中提取实际使用的字符"""
        if not os.path.exists(svg_path):
            return set()
        
        chars = set()
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取所有text元素的内容
        text_pattern = r'<text[^>]*>([^<]*)</text>'
        matches = re.findall(text_pattern, content)
        
        for match in matches:
            chars.update(match)
        
        return chars
    
    def create_subset_font(self, input_font_path, output_font_path, chars_to_keep=None):
        """创建字体子集"""
        if not FONTTOOLS_AVAILABLE:
            return False
            
        if chars_to_keep is None:
            chars_to_keep = self.base_chars
        
        if not os.path.exists(input_font_path):
            print(f"Font file not found: {input_font_path}")
            return False
        
        try:
            # 创建子集选项
            options = subset.Options()
            options.layout_features = ['*']  # 保留所有布局特性
            options.name_IDs = ['*']  # 保留字体名称
            options.glyph_names = True
            
            # 创建子集器
            subsetter = subset.Subsetter(options=options)
            
            # 指定要保留的字符
            subsetter.populate(text=''.join(chars_to_keep))
            
            # 加载原始字体
            font = TTFont(input_font_path)
            
            # 创建子集
            subsetter.subset(font)
            
            # 保存子集字体
            font.save(output_font_path)
            
            # 打印文件大小对比
            original_size = os.path.getsize(input_font_path)
            subset_size = os.path.getsize(output_font_path)
            reduction = (1 - subset_size / original_size) * 100
            
            print(f"Font optimization successful:")
            print(f"  Original: {original_size:,} bytes")
            print(f"  Optimized: {subset_size:,} bytes")
            print(f"  Reduction: {reduction:.1f}%")
            print(f"  Characters included: {len(chars_to_keep)}")
            
            return True
            
        except Exception as e:
            print(f"Error creating font subset: {e}")
            return False
    
    def get_poster_specific_chars(self, poster):
        """根据poster对象获取特定的字符集"""
        chars = set(self.base_chars)
        
        # 添加年份
        if hasattr(poster, 'years') and poster.years:
            for year in poster.years:
                chars.update(str(year))
        
        # 添加类型名称
        if hasattr(poster, 'type_list') and poster.type_list:
            for type_name in poster.type_list:
                chars.update(type_name)
        
        # 添加单位
        if hasattr(poster, 'units') and poster.units:
            chars.update(poster.units)
        
        return chars


def create_optimized_font_for_poster(poster=None, custom_chars=None):
    """为poster创建优化的字体文件"""
    input_font_path = os.path.join(os.path.dirname(__file__), 'font', 'LXGWWenKai-Regular.ttf')
    output_font_path = os.path.join(os.path.dirname(__file__), 'font', 'LXGWWenKai-Subset.ttf')
    
    # 如果fonttools不可用，直接返回原始字体
    if not FONTTOOLS_AVAILABLE:
        return input_font_path
    
    # 检查是否已经存在子集字体且比较新
    if os.path.exists(output_font_path) and os.path.exists(input_font_path):
        if os.path.getmtime(output_font_path) >= os.path.getmtime(input_font_path):
            return output_font_path
    
    subsetter = FontSubsetter()
    
    # 添加配置文件中的自定义字符
    config_chars = get_custom_characters()
    if config_chars:
        subsetter.add_custom_chars(config_chars)
    
    # 添加传入的自定义字符
    if custom_chars:
        subsetter.add_custom_chars(custom_chars)
    
    # 获取poster特定的字符
    if poster:
        chars_to_keep = subsetter.get_poster_specific_chars(poster)
    else:
        chars_to_keep = subsetter.base_chars
    
    # 创建字体子集
    success = subsetter.create_subset_font(input_font_path, output_font_path, chars_to_keep)
    
    if success:
        return output_font_path
    else:
        return input_font_path  # 回退到原始字体


if __name__ == "__main__":
    # 测试
    subsetter = FontSubsetter()
    
    # 添加示例中文字符
    subsetter.add_custom_chars("胡启航")
    
    input_font = os.path.join(os.path.dirname(__file__), 'font', 'LXGWWenKai-Regular.ttf')
    output_font = os.path.join(os.path.dirname(__file__), 'font', 'LXGWWenKai-Subset.ttf')
    
    subsetter.create_subset_font(input_font, output_font)