// Печатный чёрно-белый docx-двойник конспекта из .md (стиль — как build_Zanyatie_04_Konspekt.js).
// Запуск: NODE_PATH=<scratchpad>/node_modules node tools/docx-konspekt/md_to_docx.js <in.md> <out.docx>
// Понимает: «# », «## », «### », абзацы с **жирным**, *курсивом* и `кодом`, списки «- » и «1. »,
// таблицы-«трубы», цитаты «> », абзацы-плашки «**Определение.** …» / «**Пример.** …».
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
} = require("docx");
const fs = require("fs");

const FONT = "Arial", INK = "1A1A1A", MUTE = "5B6B7D", FILL = "E8E8E8", BORDER = "B3B3B3", RULE = "999999";
const thin = { style: BorderStyle.SINGLE, size: 4, color: BORDER };
const cellBorders = { top: thin, bottom: thin, left: thin, right: thin };

const run = (text, o = {}) => new TextRun({
  text, font: o.code ? "Courier New" : FONT, color: o.color || INK, size: o.size || 20, bold: !!o.bold, italics: !!o.italic,
});
// инлайн-разметка -> массив TextRun
function inline(text, base = {}) {
  const out = [];
  for (const part of text.split(/(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`)/g)) {
    if (!part) continue;
    if (part.startsWith("**")) out.push(run(part.slice(2, -2), { ...base, bold: true }));
    else if (part.startsWith("`")) out.push(run(part.slice(1, -1), { ...base, code: true }));
    else if (part.startsWith("*")) out.push(run(part.slice(1, -1), { ...base, italic: true }));
    else out.push(run(part, base));
  }
  return out;
}
const para = (children, o = {}) => new Paragraph({
  children, spacing: { before: o.before ?? 0, after: o.after ?? 140, line: 276 }, indent: o.indent,
});
const callout = (children) => new Paragraph({
  children, spacing: { before: 80, after: 160, line: 276 },
  shading: { type: ShadingType.CLEAR, fill: FILL, color: "auto" },
  border: ["top", "bottom", "left", "right"].reduce((a, k) => ({ ...a, [k]: { style: BorderStyle.SINGLE, size: 4, color: BORDER, space: k === "left" || k === "right" ? 8 : 4 } }), {}),
});
const h1 = (t) => new Paragraph({
  children: [run(t, { bold: true, size: 32 })], spacing: { before: 0, after: 160 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: RULE, space: 6 } },
});
const h2 = (t) => new Paragraph({
  children: [run(t, { bold: true, size: 26 })], spacing: { before: 320, after: 140 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE, space: 4 } },
});
const h3 = (t) => new Paragraph({ children: [run(t, { bold: true, size: 22 })], spacing: { before: 220, after: 90 } });

function mdTable(lines) {
  const split = (l) => l.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
  const head = split(lines[0]);
  const rows = lines.slice(2).map(split);
  const weight = head.map((_, i) => Math.max(6, Math.min(60, Math.max(head[i].length, ...rows.map((r) => (r[i] || "").length)))));
  const sum = weight.reduce((a, b) => a + b, 0);
  const widths = weight.map((w) => Math.round((w / sum) * 100));
  const mk = (txt, i, header) => new TableCell({
    width: { size: widths[i], type: WidthType.PERCENTAGE },
    shading: header ? { type: ShadingType.CLEAR, fill: FILL, color: "auto" } : undefined,
    borders: cellBorders, verticalAlign: "center", margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: inline(txt, { size: 18, bold: header }), spacing: { after: 0, line: 250 } })],
  });
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({ children: head.map((h, i) => mk(h, i, true)) }),
      ...rows.map((r) => new TableRow({ children: head.map((_, i) => mk(r[i] || "", i, false)) })),
    ],
  });
}

function convert(md) {
  const L = md.split("\n");
  const kids = [];
  let i = 0, first = true;
  while (i < L.length) {
    const line = L[i];
    if (!line.trim() || line.trim() === "---") { i++; continue; }
    if (line.startsWith("|")) {
      const buf = [];
      while (i < L.length && L[i].startsWith("|")) buf.push(L[i++]);
      kids.push(mdTable(buf), new Paragraph({ spacing: { after: 140 } }));
      continue;
    }
    if (line.startsWith("### ")) kids.push(h3(line.slice(4)));
    else if (line.startsWith("## ")) kids.push(h2(line.slice(3)));
    else if (line.startsWith("# ")) kids.push(h1(line.slice(2)));
    else if (/^- /.test(line)) kids.push(para(inline("•  " + line.slice(2)), { indent: { left: 360, hanging: 240 }, after: 80 }));
    else if (/^\d+\. /.test(line)) kids.push(para(inline(line), { indent: { left: 360, hanging: 300 }, after: 80 }));
    else if (line.startsWith("> ")) kids.push(callout(inline(line.slice(2), { italic: false })));
    else if (first) kids.push(para(inline(line, { size: 16, color: MUTE }), { after: 60 }));
    else if (/^\*[^*].*\*$/.test(line.trim()) && !line.startsWith("**")) kids.push(para(inline(line, { size: 16, color: MUTE }), { after: 200 }));
    else if (/^\*\*(Определение|Пример|Одной фразой|Источник)/.test(line)) kids.push(callout(inline(line)));
    else kids.push(para(inline(line)));
    first = false;
    i++;
  }
  return kids;
}

const [, , inp, out] = process.argv;
const doc = new Document({
  creator: "ГУАП · Кафедра № 3", title: out,
  sections: [{ properties: { page: { margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } }, children: convert(fs.readFileSync(inp, "utf8")) }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(out, b); console.log("OK", out, b.length); });
