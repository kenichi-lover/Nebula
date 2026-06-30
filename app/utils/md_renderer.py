import bleach
import markdown
import re


def render_markdown(content: str) -> str:
    """
    Markdown -> Safe HTML
    """

    html = markdown.markdown(
        content,
        extensions=[
            "fenced_code",
            "tables",
            "nl2br",
        ]
    )
    allowed_tags = [
    # 基础排版
    "p", "br", "hr", "div", "span",
    # 标题
    "h1", "h2", "h3", "h4", "h5", "h6",
    # 文本格式
    "strong", "em", "a", "blockquote",
    # 列表
    "ul", "ol", "li",
    # 代码
    "code", "pre",
    # 表格
    "table", "thead", "tbody", "tr", "th", "td",
]
    # 3. 定义允许的属性
    allowed_attributes = {
        "a": ["href", "title"],
        "code": ["class"],
        "pre": ["class"],
    }
    return bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )

def strip_markdown(content: str, max_length: int = 150) -> str:
    html = markdown.markdown(content, extensions=["fenced_code", "tables", "nl2br"])
    # 移除 HTML 标签
    text = re.sub(r"<[^>]+>", "", html)
    text = re.sub(r"\s+", " ", text).strip()  # 移除多余的空白字符
    # 限制长度
    return text[:max_length].rsplit(' ', 1)[0] + "..." if len(text) > max_length else text
