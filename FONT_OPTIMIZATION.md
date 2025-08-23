# 字体优化使用说明

现在 GitHubPoster 支持字体子集化功能，可以大幅减小 SVG 文件的大小。

## 什么是字体子集化？

字体子集化是指只保留字体文件中实际需要的字符，删除不需要的字符，从而大幅减小文件大小。

例如，完整的 LXGW WenKai Mono 字体文件可能有几MB，但如果只保留数字、英文字母和几个中文字符，文件大小可以减小到几十KB。

## 如何使用

### 1. 安装依赖（可选）

```bash
pip install fonttools
```

如果不安装 fonttools，系统会使用完整的字体文件，但仍然能正常工作。

### 2. 配置自定义字符

编辑 `github_poster/font_config.py` 文件：

```python
# 添加你的用户名中的中文字符
CUSTOM_CHARS = "胡启航"

# 添加额外的英文单词
ADDITIONAL_WORDS = ["MyProject", "CustomName"]
```

### 3. 生成 poster

正常使用命令生成 poster，系统会自动创建优化的字体文件。

## 优化效果

- **原始字体**：通常 2-5MB
- **优化后字体**：通常 10-50KB
- **文件大小减少**：90%+ 的减少

## 包含的字符

默认情况下，优化后的字体包含：

- 数字：0-9
- 英文字母：a-z, A-Z
- 常用符号：空格, 逗号, 点, 冒号, 连字符, 斜杠
- 月份缩写：Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
- 常用单位：km, hours, mins, miles, minutes
- 配置文件中指定的自定义字符

## 注意事项

1. 首次生成时会创建字体子集文件，可能需要几秒钟时间
2. 字体子集文件会保存在 `github_poster/font/LXGWWenKaiMono-Subset.ttf`
3. 如果需要添加新的字符，修改配置文件后删除子集文件即可重新生成
4. 如果 fonttools 未安装，会自动回退到使用完整字体文件

## 故障排除

如果遇到字符显示问题：

1. 检查是否在 `font_config.py` 中添加了相应字符
2. 删除 `github_poster/font/LXGWWenKaiMono-Subset.ttf` 文件重新生成
3. 如果问题持续，可以卸载 fonttools 使用完整字体文件

```bash
pip uninstall fonttools
```