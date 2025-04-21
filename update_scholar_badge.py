# update_scholar_badge.py

import os
import sys
import requests
from serpapi import GoogleSearch


def fetch_citations(author_id: str, api_key: str) -> int:
    """
    调用 SerpApi 的 Google Scholar Author API（engine=google_scholar_author）,
    返回该作者的总引用数（all）。

    JSON 中结构示例：
    {
      ...,
      "cited_by": {
        "table": [
          { "citations": { "all": 21934, "since_2016": 12302 } },
          { "h_index": { "all": 45, "since_2016": 36 } },
          { "i10_index": { "all": 59, "since_2016": 51 } }
        ],
        "graph": [ … ]
      },
      …
    }
    :contentReference[oaicite:0]{index=0}
    """
    params = {
        "engine": "google_scholar_author",
        "author_id": author_id,
        "api_key": api_key,
        "hl": "en",
        "no_cache": True
    }
    search = GoogleSearch(params)
    data = search.get_dict()

    # 检查 SerpApi 层面错误
    if "error" in data:
        raise RuntimeError(f"SerpApi 返回错误: {data['error']}")
    # 检查是否包含 cited_by
    if "cited_by" not in data or "table" not in data["cited_by"]:
        available = ", ".join(data.keys())
        raise RuntimeError(
            f"'cited_by' 未在响应中找到，现有字段: {available}\n完整响应: {data}"
        )
    # 提取总引用数
    try:
        return int(data["cited_by"]["table"][0]["citations"]["all"])
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"解析引用数失败: {e}\n字段内容: {data['cited_by']['table']}")


def main():
    author_id = "yuiXa5EAAAAJ"
    # api_key = os.getenv("SERPAPI_API_KEY")
    api_key = '5ec1d1ba2f6e6afcd8b1b981ba66916005750d4e4930626f95862d17729ee97b'
    if not api_key:
        print("错误：环境变量 SERPAPI_API_KEY 未设置", file=sys.stderr)
        sys.exit(1)

    citations = fetch_citations(author_id, api_key)
    print(f"当前引用数: {citations}")

    # 利用 shields.io 的动态 badge URL
    # 新版：左侧是蓝底白字的 Google Scholar icon，右侧是灰底黑字的引用数
    badge_link = {
        'gs_pymk_cite': (
            "https://img.shields.io/badge/"
            "Citations-{cite}-_"
            ".svg"
            "?logo=google-scholar"
            "&labelColor=4f4f4f"
            "&color=3388ee"
        ).format(cite=citations),
    }

    # 取出 Google Scholar 的那个：
    badge_url = badge_link['gs_pymk_cite']

    # 下载并写文件
    import requests
    r = requests.get(badge_url)
    r.raise_for_status()
    with open("scholar_badge.svg", "wb") as f:
        f.write(r.content)


if __name__ == "__main__":
    main()
