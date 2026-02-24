"""
extract_transcripts.py
从 .doc/.docx 访谈文字稿文件夹提取纯文本并合并。

用法:
  python extract_transcripts.py --offline <线下文件夹> --online <线上文件夹> --out <输出目录>
  python extract_transcripts.py --all <单文件夹> --out <输出目录>

依赖: python-docx, pywin32 (Windows only for .doc)
"""
import os, sys, argparse

def read_docx(path):
    from docx import Document
    try:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        print(f"  [WARN] docx failed {path}: {e}")
        return ""

def read_doc(path):
    """Windows only: use Word COM for .doc files"""
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(path))
        text = doc.Content.Text
        doc.Close(False)
        word.Quit()
        return text
    except Exception as e:
        print(f"  [WARN] doc COM failed {path}: {e}")
        return ""

def extract_folder(folder):
    """Extract and concatenate all .doc/.docx files in folder (recursive)"""
    texts = []
    if not os.path.exists(folder):
        print(f"[ERROR] Folder not found: {folder}")
        return ""
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            fp = os.path.join(root, fn)
            if fn.lower().endswith(".docx"):
                print(f"  Reading: {fn}")
                texts.append(read_docx(fp))
            elif fn.lower().endswith(".doc"):
                print(f"  Reading: {fn}")
                texts.append(read_doc(fp))
    return "\n\n".join(texts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", help="线下访谈文件夹路径")
    parser.add_argument("--online",  help="线上访谈文件夹路径")
    parser.add_argument("--all",     help="不区分线上/线下，单一文件夹")
    parser.add_argument("--out",     required=True, help="输出目录")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    if args.all:
        print(f"[提取] 合并文件夹: {args.all}")
        text = extract_folder(args.all)
        out_path = os.path.join(args.out, "merged_all.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[完成] 输出: {out_path} ({len(text)} chars)")
    else:
        for mode, folder in [("offline", args.offline), ("online", args.online)]:
            if not folder:
                continue
            print(f"\n[提取] {mode}: {folder}")
            text = extract_folder(folder)
            out_path = os.path.join(args.out, f"merged_{mode}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[完成] {out_path} ({len(text)} chars)")

if __name__ == "__main__":
    main()
