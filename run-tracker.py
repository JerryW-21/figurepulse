#!/usr/bin/env python3
"""
FigurePulse — 人物动态追踪器（独立脚本）
==========================================
可在 WorkBuddy、Cursor、Codex、或本地命令行中运行。

用法:
  python run-tracker.py              # 追踪马斯克（默认）
  python run-tracker.py --figure elon-musk  # 指定人物
  python run-tracker.py --output report.md  # 输出到文件

依赖: requests（如未安装会自动尝试 pip install）
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# 人物配置（未来扩展在此添加）
# ============================================================
FIGURES = {
    "elon-musk": {
        "name": "埃隆·马斯克",
        "name_en": "Elon Musk",
        "companies": ["Tesla", "SpaceX", "xAI", "Neuralink", "The Boring Company", "X (Twitter)"],
        "role": "DOGE 政府效率部负责人",
        "stock_tickers": ["TSLA", "SPCX"],
        "search_terms": {
            "tweets": "Elon Musk X twitter tweet today {date}",
            "companies": "Tesla SpaceX xAI Neuralink news today {date}",
            "appearances": "Elon Musk appearance event interview {date}",
            "market": "TSLA Tesla stock SpaceX SPCX price {date}",
            "china": "马斯克 埃隆·马斯克 最新动态 {date}"
        }
    },
    # 未来扩展：
    # "jensen-huang": {
    #     "name": "黄仁勋", "name_en": "Jensen Huang",
    #     "companies": ["NVIDIA"],
    #     "stock_tickers": ["NVDA"],
    #     "search_terms": { ... }
    # }
}

# ============================================================
# HTML 报告模板
# ============================================================
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FigurePulse · {figure_name}24H动态追踪</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f4ef; color: #2c2c2a; max-width: 720px; margin: 0 auto; padding: 16px; }}
  .header {{ text-align:center; padding: 24px 0; }}
  .header h1 {{ font-size: 24px; color: #0f172a; }}
  .header p {{ color: #5f5e5a; font-size: 14px; margin-top: 4px; }}
  .card {{ background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .card h3 {{ font-size: 16px; color: #0f172a; margin-bottom: 8px; }}
  .card p {{ font-size: 14px; color: #5f5e5a; line-height: 1.6; }}
  .tag {{ display:inline-block; padding:2px 8px; border-radius:4px; font-size:12px; margin-right:4px; }}
  .tag-red {{ background:#fee2e2; color:#dc2626; }}
  .tag-green {{ background:#dcfce7; color:#16a34a; }}
  .tag-blue {{ background:#dbeafe; color:#2563eb; }}
  .metrics {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:12px; margin-bottom: 16px; }}
  .metric {{ background:#fff; border-radius:12px; padding:14px; text-align:center; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .metric .val {{ font-size:22px; font-weight:700; }}
  .metric .lbl {{ font-size:12px; color:#5f5e5a; }}
  .up {{ color:#dc2626; }} .down {{ color:#16a34a; }}
  .footer {{ text-align:center; padding:16px; font-size:12px; color:#9ca3af; }}
  .footer a {{ color:#2563eb; }}
</style>
</head>
<body>
<div class="header">
  <h1>⚡ FigurePulse</h1>
  <p>{figure_name} · 24H动态追踪 · 生成时间 {gen_time}</p>
</div>
<div class="metrics">
  {metrics_html}
</div>
{content_html}
<div class="footer">
  <p>FigurePulse — 人物动态脉搏 | <a href="https://github.com">GitHub</a></p>
  <p>数据来源：公开信息聚合 · 仅供参考，不构成投资建议</p>
</div>
</body>
</html>
'''

# ============================================================
# 搜索函数（在没有 API 的情况下，输出搜索链接和模板）
# ============================================================
def generate_search_queries(figure_id, date_str):
    """生成搜索查询列表"""
    figure = FIGURES.get(figure_id, FIGURES["elon-musk"])
    queries = []
    for category, template in figure["search_terms"].items():
        queries.append({
            "category": category,
            "query": template.format(date=date_str)
        })
    return queries

def generate_report(figure_id, date_str, output_path=None):
    """生成 HTML 报告"""
    figure = FIGURES.get(figure_id, FIGURES["elon-musk"])
    gen_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 搜索查询
    queries = generate_search_queries(figure_id, date_str)
    
    # 按类别组织
    from collections import defaultdict
    by_cat = defaultdict(list)
    for q in queries:
        by_cat[q["category"]].append(q["query"])
    
    # 构建内容
    cat_labels = {
        "tweets": "📱 X平台推文",
        "companies": "🏢 公司动态",
        "appearances": "🎤 出席活动",
        "market": "📈 市场影响",
        "china": "🇨🇳 中国相关"
    }
    
    content_blocks = []
    for cat, qs in by_cat.items():
        label = cat_labels.get(cat, cat)
        qs_html = "".join(f'<li>{q}</li>' for q in qs)
        content_blocks.append(f'''
<div class="card">
  <h3>{label}</h3>
  <p>搜索关键词:</p>
  <ul style="font-size:13px;color:#6b7280;padding-left:20px;">
    {qs_html}
  </ul>
  <p style="margin-top:12px;color:#9ca3af;font-style:italic;">
    ⚠ 本脚本为离线搜索模板。在 WorkBuddy 或 Cursor 中运行时，AI 将使用这些关键词执行 WebSearch。
    手动运行请复制关键词到搜索引擎。
  </p>
</div>''')
    
    metrics_html = f'''
<div class="metric"><div class="lbl">{figure['name_en']} 动态</div><div class="val">{len(queries)}项</div></div>
<div class="metric"><div class="lbl">覆盖公司</div><div class="val">{len(figure['companies'])}家</div></div>
<div class="metric"><div class="lbl">追踪股票</div><div class="val">{','.join(figure['stock_tickers'])}</div></div>
'''
    
    html = HTML_TEMPLATE.format(
        figure_name=figure['name'],
        gen_time=gen_time,
        metrics_html=metrics_html,
        content_html="\n".join(content_blocks)
    )
    
    if output_path:
        Path(output_path).write_text(html, encoding='utf-8')
        print(f"✅ 报告已生成: {output_path}")
    else:
        out = Path(f"figurepulse-{figure_id}-{date_str}.html")
        out.write_text(html, encoding='utf-8')
        print(f"✅ 报告已生成: {out}")
    
    return html

# ============================================================
# CLI 入口
# ============================================================
def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="FigurePulse — 人物动态追踪器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run-tracker.py                        # 追踪马斯克
  python run-tracker.py --figure elon-musk     # 指定人物
  python run-tracker.py --output report.md     # 输出到文件
  python run-tracker.py --json                 # JSON 格式输出（供 AI 管道使用）
        """
    )
    parser.add_argument("--figure", default="elon-musk", 
                        choices=list(FIGURES.keys()),
                        help="追踪的人物ID")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--date", help="日期 (YYYY.MM.DD)，默认今天")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    date_str = args.date or datetime.now().strftime("%Y.%m.%d")
    
    if args.json:
        figure = FIGURES.get(args.figure, FIGURES["elon-musk"])
        output = {
            "figure": figure,
            "date": date_str,
            "queries": generate_search_queries(args.figure, date_str),
            "generated_at": datetime.now().isoformat()
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        generate_report(args.figure, date_str, args.output)

if __name__ == "__main__":
    main()
