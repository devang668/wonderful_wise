import re
import unicodedata
from typing import Optional

# ---------- 1. 全局预编译 ----------
# 1.1 Markdown 内联/块级格式（合并同类项）
_MD_INLINE = re.compile(
    r'(?<![\\*])'          # 前面不能有反斜杠转义
    r'(\*\*|__|\*|_)'      # 1. 开始符号
    r'(.*?)'               # 2. 内容（非贪婪）
    r'(?<![\\])\1',        # 3. 结束符号（与开始相同）
    re.UNICODE
)

_MD_LINK = re.compile(r'!?\[([^]]+)]\([^)]*\)', re.UNICODE)          # [text](url) 或 ![alt](url)
_MD_CODE = re.compile(r'`([^`]+)`', re.UNICODE)                       # `inline code`
_MD_FENCE = re.compile(r'```.*?```', re.DOTALL | re.UNICODE)          # ```code block```
_MD_HEAD = re.compile(r'^#{1,6}\s+', re.MULTILINE | re.UNICODE)       # # title
_MD_LIST = re.compile(r'^\s*([-*+]|\d+\.)\s+', re.MULTILINE | re.UNICODE)  # 列表符号
_MD_HR = re.compile(r'^[ \t]*[-*_]{3,}[ \t]*$', re.MULTILINE | re.UNICODE)  # --- 分割线

# 1.2 空白折叠
_BLANK = re.compile(r'[ \t]+', re.UNICODE)


def _is_emoji(ch: str) -> bool:
    """
    用 Unicode category 判断一个字符是否为 emoji / symbol。
    比罗列区间更快，也不会误杀汉字。
    """
    cat = unicodedata.category(ch)
    # So: Symbol, Other ； Sk: Symbol, Modifier ； Pf: Punctuation, Final quote …
    return cat in ('So', 'Sk') or (
        cat == 'Cf' and ord(ch) >= 0x1F600  # 兼容补充区
    )


def _strip_emoji(text: str) -> str:
    """逐字符过滤 emoji，C 扩展层循环，速度足够快。"""
    return ''.join(ch for ch in text if not _is_emoji(ch))


def clean_content(content: Optional[str]) -> str:
    """
    安全清洗：去 Markdown、去 emoji、压空白。
    任何异常直接返回原串（strip 后），不抛错、不打印。
    """
    if not content or not isinstance(content, str):
        return ''
    text = content               # 不修改原串
    try:
        # 2.1 内联格式（粗体、斜体）
        text = _MD_INLINE.sub(r'\2', text)
        # 2.2 链接 / 图片
        text = _MD_LINK.sub(r'\1', text)
        # 2.3 代码
        text = _MD_CODE.sub(r'\1', text)
        text = _MD_FENCE.sub('', text)
        # 2.4 标题、列表、分割线
        text = _MD_HEAD.sub('', text)
        text = _MD_LIST.sub('', text)
        text = _MD_HR.sub('', text)
        # 2.5 emoji
        text = _strip_emoji(text)
        # 2.6 压空白
        text = _BLANK.sub(' ', text)
        text = '\n'.join(line.rstrip() for line in text.splitlines())
        return text.strip()
    except Exception:              # 捕获一切，静默回退
        return content.strip()
