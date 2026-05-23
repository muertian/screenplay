#!/usr/bin/env python3
"""Build a static browser page for the ai-comic-drama user manual."""

from __future__ import annotations

import argparse
import html
from datetime import datetime
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = SKILL_ROOT / "references" / "user-manual-prompts.md"
DEFAULT_OUTPUT = SKILL_ROOT / "references" / "user-manual-browser.html"


HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI漫剧 Skill 用户推进手册</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f8f7f3;
      --panel: #ffffff;
      --panel-soft: #fbfaf7;
      --ink: #24313a;
      --muted: #64717b;
      --line: #ddd8cc;
      --teal: #0f766e;
      --teal-dark: #115e59;
      --amber: #b45309;
      --code-bg: #172126;
      --code-ink: #e8f0ed;
      --shadow: 0 18px 45px rgba(36, 49, 58, 0.12);
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", Arial, sans-serif;
      line-height: 1.65;
    }}

    a {{
      color: inherit;
      text-decoration: none;
    }}

    .app-shell {{
      display: grid;
      grid-template-columns: 292px minmax(0, 1fr);
      min-height: 100vh;
    }}

    .sidebar {{
      position: sticky;
      top: 0;
      align-self: start;
      height: 100vh;
      padding: 24px 18px;
      border-right: 1px solid var(--line);
      background: #f0eee7;
      overflow: auto;
    }}

    .brand {{
      display: grid;
      gap: 8px;
      margin-bottom: 18px;
    }}

    .brand-mark {{
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      background: var(--ink);
      color: #fff7ed;
      font-weight: 800;
      letter-spacing: 0;
    }}

    .brand h1 {{
      margin: 0;
      font-size: 1.15rem;
      line-height: 1.3;
    }}

    .brand p {{
      margin: 0;
      color: var(--muted);
      font-size: 0.88rem;
    }}

    .search {{
      position: relative;
      margin: 18px 0;
    }}

    .search input {{
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 9px 12px;
      background: #fffdfa;
      color: var(--ink);
      font: inherit;
      outline: none;
    }}

    .search input:focus {{
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.14);
    }}

    .toc {{
      display: grid;
      gap: 4px;
      margin: 0;
      padding: 0;
      list-style: none;
    }}

    .toc a {{
      display: block;
      padding: 8px 10px;
      border-radius: 8px;
      color: #3e4b54;
      font-size: 0.92rem;
    }}

    .toc a:hover,
    .toc a.active {{
      background: #fffdfa;
      color: var(--teal-dark);
    }}

    .main {{
      min-width: 0;
      padding: 34px clamp(22px, 5vw, 72px) 70px;
    }}

    .toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      margin-bottom: 22px;
      color: var(--muted);
      font-size: 0.9rem;
    }}

    .source-link {{
      color: var(--teal-dark);
      font-weight: 700;
    }}

    .hero {{
      max-width: 980px;
      margin-bottom: 26px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--line);
    }}

    .hero h1 {{
      margin: 0 0 12px;
      font-size: 2rem;
      line-height: 1.2;
      letter-spacing: 0;
    }}

    .hero p {{
      margin: 0;
      max-width: 820px;
      color: var(--muted);
      font-size: 1rem;
    }}

    .stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 18px 0 0;
    }}

    .chip {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 5px 9px;
      background: #fffdfa;
      color: #4b5962;
      font-size: 0.84rem;
      line-height: 1.4;
    }}

    .manual-section {{
      max-width: 980px;
      padding: 26px 0;
      border-bottom: 1px solid var(--line);
    }}

    .manual-section[hidden] {{
      display: none;
    }}

    .manual-section h2 {{
      margin: 0 0 16px;
      color: var(--ink);
      font-size: 1.45rem;
      line-height: 1.3;
      letter-spacing: 0;
    }}

    .manual-section h3 {{
      margin: 24px 0 10px;
      color: #2e3b44;
      font-size: 1.06rem;
      line-height: 1.35;
      letter-spacing: 0;
    }}

    .manual-section p {{
      margin: 10px 0;
    }}

    .manual-section ul {{
      margin: 10px 0 14px;
      padding-left: 1.2rem;
    }}

    .manual-section li {{
      margin: 5px 0;
    }}

    code:not(pre code) {{
      border: 1px solid #e2ded5;
      border-radius: 6px;
      padding: 0.08rem 0.32rem;
      background: #fffdfa;
      color: #8a3c08;
      font-family: "Cascadia Mono", Consolas, monospace;
      font-size: 0.92em;
    }}

    .table-wrap {{
      width: 100%;
      overflow-x: auto;
      margin: 12px 0 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }}

    table {{
      width: 100%;
      min-width: 680px;
      border-collapse: collapse;
      font-size: 0.92rem;
    }}

    th,
    td {{
      padding: 10px 12px;
      border-bottom: 1px solid #ece7db;
      text-align: left;
      vertical-align: top;
    }}

    th {{
      background: #f3f0e7;
      color: #26333b;
      font-weight: 800;
    }}

    tr:last-child td {{
      border-bottom: 0;
    }}

    .prompt {{
      position: relative;
      margin: 12px 0 20px;
      border-radius: 8px;
      background: var(--code-bg);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}

    .prompt pre {{
      margin: 0;
      padding: 44px 18px 18px;
      overflow-x: auto;
      color: var(--code-ink);
      font-family: "Cascadia Mono", Consolas, monospace;
      font-size: 0.92rem;
      line-height: 1.6;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }}

    .copy-button {{
      position: absolute;
      top: 8px;
      right: 8px;
      min-height: 30px;
      border: 1px solid rgba(255, 255, 255, 0.22);
      border-radius: 8px;
      padding: 4px 10px;
      background: rgba(255, 255, 255, 0.08);
      color: #f8faf9;
      font: inherit;
      font-size: 0.82rem;
      cursor: pointer;
    }}

    .copy-button:hover {{
      background: rgba(255, 255, 255, 0.16);
    }}

    .empty-state {{
      max-width: 980px;
      padding: 22px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--muted);
    }}

    @media (max-width: 900px) {{
      .app-shell {{
        grid-template-columns: 1fr;
      }}

      .sidebar {{
        position: static;
        height: auto;
        max-height: none;
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }}

      .toc {{
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      }}

      .main {{
        padding: 24px 18px 52px;
      }}
    }}
  </style>
</head>
<body>
  <div class="app-shell">
    <aside class="sidebar" aria-label="手册导航">
      <div class="brand">
        <div class="brand-mark">AI</div>
        <h1>AI漫剧 Skill 手册</h1>
        <p>阶段路由、提示词、验收门禁</p>
      </div>
      <label class="search">
        <input id="searchInput" type="search" placeholder="搜索阶段、提示词、关键词" autocomplete="off" />
      </label>
      <nav>
        <ul class="toc" id="toc"></ul>
      </nav>
    </aside>

    <main class="main">
      <div class="toolbar">
        <span>生成时间：{generated_at}</span>
        <a class="source-link" href="user-manual-prompts.md">查看 Markdown 源文件</a>
      </div>
      <article id="content"></article>
      <div id="emptyState" class="empty-state" hidden>没有找到匹配内容。</div>
    </main>
  </div>

  <textarea id="manualSource" hidden>{manual_markdown}</textarea>

  <script>
    const source = document.getElementById("manualSource").value.replace(/\\r\\n/g, "\\n");
    const content = document.getElementById("content");
    const toc = document.getElementById("toc");
    const searchInput = document.getElementById("searchInput");
    const emptyState = document.getElementById("emptyState");

    function escapeHtml(value) {{
      return value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }}

    function inlineFormat(value) {{
      return escapeHtml(value).replace(/`([^`]+)`/g, "<code>$1</code>");
    }}

    function slugFor(title, index) {{
      const ascii = title
        .toLowerCase()
        .replace(/[^a-z0-9\\u4e00-\\u9fa5]+/g, "-")
        .replace(/^-+|-+$/g, "");
      return ascii || `section-${{index}}`;
    }}

    function parseTable(lines) {{
      const rows = lines
        .map(line => line.trim().replace(/^\\|/, "").replace(/\\|$/, "").split("|").map(cell => cell.trim()))
        .filter(row => row.length > 1);
      if (rows.length < 2) return "";
      const header = rows[0];
      const body = rows.slice(2);
      return `<div class="table-wrap"><table><thead><tr>${{header.map(cell => `<th>${{inlineFormat(cell)}}</th>`).join("")}}</tr></thead><tbody>${{body.map(row => `<tr>${{row.map(cell => `<td>${{inlineFormat(cell)}}</td>`).join("")}}</tr>`).join("")}}</tbody></table></div>`;
    }}

    function renderMarkdown(markdown) {{
      const lines = markdown.split("\\n");
      let html = "";
      let index = 0;
      let sectionOpen = false;
      let sectionIndex = 0;

      function openSection(title) {{
        if (sectionOpen) html += "</section>";
        const id = slugFor(title, sectionIndex++);
        html += `<section class="manual-section" id="${{id}}" data-title="${{escapeHtml(title)}}"><h2>${{inlineFormat(title)}}</h2>`;
        sectionOpen = true;
      }}

      while (index < lines.length) {{
        const line = lines[index];
        const trimmed = line.trim();

        if (!trimmed) {{
          index++;
          continue;
        }}

        if (trimmed.startsWith("# ")) {{
          const title = trimmed.replace(/^#\\s+/, "");
          html += `<header class="hero"><h1>${{inlineFormat(title)}}</h1>`;
          index++;
          const intro = [];
          while (index < lines.length && !lines[index].startsWith("## ")) {{
            if (lines[index].trim()) intro.push(lines[index].trim());
            index++;
          }}
          if (intro.length) html += `<p>${{inlineFormat(intro.join(" "))}}</p>`;
          html += `<div class="stats" id="stats"></div></header>`;
          continue;
        }}

        if (trimmed.startsWith("## ")) {{
          openSection(trimmed.replace(/^##\\s+/, ""));
          index++;
          continue;
        }}

        if (trimmed.startsWith("### ")) {{
          if (!sectionOpen) openSection("快速开始");
          html += `<h3>${{inlineFormat(trimmed.replace(/^###\\s+/, ""))}}</h3>`;
          index++;
          continue;
        }}

        if (trimmed.startsWith("```")) {{
          const lang = trimmed.replace(/^```/, "").trim();
          index++;
          const code = [];
          while (index < lines.length && !lines[index].trim().startsWith("```")) {{
            code.push(lines[index]);
            index++;
          }}
          index++;
          if (!sectionOpen) openSection("提示词");
          html += `<div class="prompt" data-lang="${{escapeHtml(lang)}}"><button class="copy-button" type="button">复制</button><pre><code>${{escapeHtml(code.join("\\n"))}}</code></pre></div>`;
          continue;
        }}

        if (trimmed.startsWith("|") && index + 1 < lines.length && /^\\|?\\s*:?-{{3,}}/.test(lines[index + 1].trim())) {{
          const tableLines = [];
          while (index < lines.length && lines[index].trim().startsWith("|")) {{
            tableLines.push(lines[index]);
            index++;
          }}
          if (!sectionOpen) openSection("表格");
          html += parseTable(tableLines);
          continue;
        }}

        if (trimmed.startsWith("- ")) {{
          const items = [];
          while (index < lines.length && lines[index].trim().startsWith("- ")) {{
            items.push(lines[index].trim().replace(/^-\\s+/, ""));
            index++;
          }}
          if (!sectionOpen) openSection("要点");
          html += `<ul>${{items.map(item => `<li>${{inlineFormat(item)}}</li>`).join("")}}</ul>`;
          continue;
        }}

        const paragraph = [];
        while (
          index < lines.length &&
          lines[index].trim() &&
          !lines[index].startsWith("#") &&
          !lines[index].trim().startsWith("- ") &&
          !lines[index].trim().startsWith("|") &&
          !lines[index].trim().startsWith("```")
        ) {{
          paragraph.push(lines[index].trim());
          index++;
        }}
        if (!sectionOpen) openSection("说明");
        html += `<p>${{inlineFormat(paragraph.join(" "))}}</p>`;
      }}

      if (sectionOpen) html += "</section>";
      return html;
    }}

    function setupToc() {{
      toc.innerHTML = "";
      document.querySelectorAll(".manual-section").forEach(section => {{
        const title = section.dataset.title || section.querySelector("h2")?.textContent || "";
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.href = `#${{section.id}}`;
        link.textContent = title;
        item.appendChild(link);
        toc.appendChild(item);
      }});
    }}

    function setupCopyButtons() {{
      document.querySelectorAll(".copy-button").forEach(button => {{
        button.addEventListener("click", async () => {{
          const code = button.nextElementSibling?.innerText || "";
          try {{
            await navigator.clipboard.writeText(code);
            button.textContent = "已复制";
          }} catch {{
            const holder = document.createElement("textarea");
            holder.value = code;
            document.body.appendChild(holder);
            holder.select();
            document.execCommand("copy");
            holder.remove();
            button.textContent = "已复制";
          }}
          window.setTimeout(() => (button.textContent = "复制"), 1200);
        }});
      }});
    }}

    function setupSearch() {{
      searchInput.addEventListener("input", () => {{
        const query = searchInput.value.trim().toLowerCase();
        let visible = 0;
        document.querySelectorAll(".manual-section").forEach(section => {{
          const hit = !query || section.textContent.toLowerCase().includes(query);
          section.hidden = !hit;
          if (hit) visible++;
        }});
        emptyState.hidden = visible !== 0;
      }});
    }}

    function setupStats() {{
      const stats = document.getElementById("stats");
      const sectionCount = document.querySelectorAll(".manual-section").length;
      const promptCount = document.querySelectorAll(".prompt").length;
      const tableCount = document.querySelectorAll("table").length;
      stats.innerHTML = `
        <span class="chip">${{sectionCount}} 个章节</span>
        <span class="chip">${{promptCount}} 条可复制提示词</span>
        <span class="chip">${{tableCount}} 张速查表</span>
      `;
    }}

    content.innerHTML = renderMarkdown(source);
    setupToc();
    setupCopyButtons();
    setupSearch();
    setupStats();
  </script>
</body>
</html>
"""


def build(input_path: Path, output_path: Path) -> None:
    manual = input_path.read_text(encoding="utf-8")
    html_text = HTML_TEMPLATE.format(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        manual_markdown=html.escape(manual),
    )
    output_path.write_text(html_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    build(args.input, args.output)
    print(args.output)
    print(args.output.resolve().as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
