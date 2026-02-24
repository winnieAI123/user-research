"""
analyze_kano.py
基于功能关键词，在合并文字稿中检索用户原话证据并统计提及频次。

用法:
  # 使用 JSON 功能定义文件
  python analyze_kano.py --features features.json --offline merged_offline.txt --online merged_online.txt --out ./

  # 仅使用单一合并文本（不区分线上/线下）
  python analyze_kano.py --features features.json --all merged_all.txt --out ./

功能定义 JSON 格式:
{
  "功能名A": {
    "desc": "功能描述",
    "keywords": ["关键词1", "关键词2", ...]
  },
  ...
}

输出:
  kano_evidence.json  — 结构化证据（每项功能含用户原话列表）
  summary.txt         — 频次排序汇总表
"""
import os, re, json, argparse

CONTEXT_CHARS = 120
MAX_QUOTES_PER_FEATURE = 15

def extract_context(text, keyword, ctx=CONTEXT_CHARS):
    matches = []
    for m in re.finditer(re.escape(keyword), text):
        start = max(0, m.start() - ctx)
        end = min(len(text), m.end() + ctx)
        context = text[start:end].replace('\n', ' ').strip()
        matches.append({"keyword": keyword, "context": f"...{context}..."})
    return matches

def analyze_feature(name, info, offline_text, online_text):
    res = {
        "feature": name, "description": info.get("desc", ""),
        "offline_mentions": [], "online_mentions": [],
        "offline_count": 0, "online_count": 0, "total_count": 0
    }
    seen_off, seen_on = set(), set()
    for kw in info.get("keywords", []):
        for m in extract_context(offline_text, kw):
            key = m["context"][:80]
            if key not in seen_off:
                seen_off.add(key)
                res["offline_mentions"].append(m)
        for m in extract_context(online_text, kw):
            key = m["context"][:80]
            if key not in seen_on:
                seen_on.add(key)
                res["online_mentions"].append(m)
    res["offline_count"] = len(res["offline_mentions"])
    res["online_count"]  = len(res["online_mentions"])
    res["total_count"]   = res["offline_count"] + res["online_count"]
    res["offline_mentions"] = res["offline_mentions"][:MAX_QUOTES_PER_FEATURE]
    res["online_mentions"]  = res["online_mentions"][:MAX_QUOTES_PER_FEATURE]
    return res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", required=True, help="功能定义 JSON 文件路径")
    parser.add_argument("--offline", default="", help="merged_offline.txt 路径")
    parser.add_argument("--online",  default="", help="merged_online.txt 路径")
    parser.add_argument("--all",     default="", help="merged_all.txt 路径（替代 offline/online）")
    parser.add_argument("--out",     required=True, help="输出目录")
    args = parser.parse_args()

    with open(args.features, "r", encoding="utf-8") as f:
        features = json.load(f)

    def read(path):
        if path and os.path.exists(path):
            return open(path, "r", encoding="utf-8").read()
        return ""

    if args.all:
        offline_text = online_text = read(args.all)
    else:
        offline_text = read(args.offline)
        online_text  = read(args.online)

    print(f"Offline: {len(offline_text)} chars | Online: {len(online_text)} chars\n")

    results = []
    for name, info in features.items():
        r = analyze_feature(name, info, offline_text, online_text)
        results.append(r)
        print(f"  [{name}] off={r['offline_count']} on={r['online_count']} total={r['total_count']}")

    os.makedirs(args.out, exist_ok=True)

    evidence_path = os.path.join(args.out, "kano_evidence.json")
    with open(evidence_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[完成] 证据保存: {evidence_path}")

    summary_path = os.path.join(args.out, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        for r in sorted(results, key=lambda x: x["total_count"], reverse=True):
            line = f"{r['feature']:14s}  off={r['offline_count']:4d}  on={r['online_count']:4d}  total={r['total_count']:4d}\n"
            f.write(line)
            print(" ", line.strip())
    print(f"[完成] 频次汇总: {summary_path}")

if __name__ == "__main__":
    main()
