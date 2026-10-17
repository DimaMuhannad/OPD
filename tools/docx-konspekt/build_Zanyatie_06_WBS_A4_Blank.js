// Бланк к занятию 6: лицевая сторона — дерево WBS, обратная — таблица пакетов работ (вход для Ганта).
// Чёрно-белая печать, альбомная А4 (А3 нет), стиль — как Zanyatie_05_Derevo_A4_Blank. Запуск:
//   NODE_PATH=/opt/node-tools/node_modules node tools/docx-konspekt/build_Zanyatie_06_WBS_A4_Blank.js
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  AlignmentType, HeightRule, PageOrientation, PageBreak, TableLayoutType, VerticalAlign,
} = require("docx");
const fs = require("fs");

const FONT = "Arial", INK = "000000", MUTE = "666666";
const MARGIN_X = 700;
const PAGE_W = 16838 - 2 * MARGIN_X;
const GAP = 160;

const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: none, bottom: none, left: none, right: none };
const thick = { style: BorderStyle.SINGLE, size: 12, color: INK };
const thin = { style: BorderStyle.SINGLE, size: 6, color: INK };
const dashed = { style: BorderStyle.DASHED, size: 8, color: INK };
const box = (b) => ({ top: b, bottom: b, left: b, right: b });

const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 20, bold: !!o.bold, color: o.color || INK, italics: !!o.italic });
const para = (t, o = {}) => new Paragraph({
  alignment: o.align || AlignmentType.LEFT, spacing: { before: o.before || 0, after: o.after ?? 40 },
  children: Array.isArray(t) ? t : [run(t, o)],
});
const label = (t, hint) => para([run(t, { bold: true, size: 21 }), run(hint ? "  " + hint : "", { size: 18, color: MUTE, italic: true })], { before: 80, after: 30 });

function row(n, hints, height, borders, total = PAGE_W, center = false) {
  const w = Math.floor((total - (n - 1) * GAP) / n);
  const cells = [];
  for (let i = 0; i < n; i++) {
    if (i) cells.push(new TableCell({ width: { size: GAP, type: WidthType.DXA }, borders: noBorders, children: [para("")] }));
    cells.push(new TableCell({
      width: { size: w, type: WidthType.DXA }, borders, margins: { top: 50, bottom: 50, left: 90, right: 90 },
      children: [para([run(hints[i] || "", { size: 17, color: MUTE, italic: true })], { after: 0 })],
    }));
  }
  return new Table({
    width: { size: total, type: WidthType.DXA }, alignment: center ? AlignmentType.CENTER : undefined, layout: TableLayoutType.FIXED,
    columnWidths: Array.from({ length: 2 * n - 1 }, (_, i) => (i % 2 ? GAP : w)),
    rows: [new TableRow({ height: { value: height, rule: HeightRule.EXACT }, children: cells })],
  });
}
const spacer = (h = 60) => para("", { after: h });
const head = (title, sub) => [
  para([run(title, { bold: true, size: 32 })], { after: 20 }),
  para([run("Команда: ______________________    Проект: ______________________________", { size: 20 }), run("     " + sub, { size: 17, color: MUTE, italic: true })], { after: 40 }),
];

// ── Лицевая сторона: дерево WBS ──
const front = [
  ...head("Иерархическая структура работ (WBS)", "лицевая сторона · обратная — таблица пакетов"),
  label("ПРОЕКТ", "название и главный результат из паспорта"),
  row(1, ["проект"], 620, box(thick), 8000, true),
  para([run("▼", { bold: true })], { align: AlignmentType.CENTER, after: 0 }),
  label("КРУПНЫЕ РЕЗУЛЬТАТЫ", "из выбранных ветвей дерева целей; существительным; номера 1, 2, 3…"),
  row(5, ["1. результат", "2. результат", "3. результат", "4. отчёт и защита", "5. управление проектом"], 900, box(thick)),
  label("ПАКЕТЫ РАБОТ", "под своим результатом; номера 1.1, 1.2, 2.1…; два-три слова; подробности — на обороте"),
  ...[0, 1, 2, 3].flatMap((k) => [row(5, ["1." + (k + 1), "2." + (k + 1), "3." + (k + 1), "4." + (k + 1), "5." + (k + 1)], 1020, box(dashed)), spacer(50)]),
  para([run("Проверка:  ☐ все выбранные ветви дерева целей есть, границ нет    ☐ есть отчёт и управление проектом    ☐ элементы — результаты, а не действия    ☐ каждый пакет — одному человеку", { size: 18 })], { before: 60 }),
];

// ── Обратная сторона: таблица пакетов ──
const COLS = [["Код", 900], ["Пакет работ", 4300], ["Что предъявляем: предмет, документ, данные", 5038], ["Ответственный (один)", 2900], ["Длительность", 2300]];
const cell = (t, w, hdr) => new TableCell({
  width: { size: w, type: WidthType.DXA }, borders: box(thin), verticalAlign: VerticalAlign.CENTER,
  margins: { top: 40, bottom: 40, left: 90, right: 90 },
  children: [para([run(t, { bold: hdr, size: hdr ? 19 : 17, color: hdr ? INK : MUTE, italic: !hdr })], { after: 0 })],
});
const back = [
  new Paragraph({ children: [new PageBreak()] }),
  ...head("Пакеты работ", "обратная сторона · заполнить дома, принести на следующую пару"),
  new Table({
    width: { size: PAGE_W, type: WidthType.DXA }, layout: TableLayoutType.FIXED, columnWidths: COLS.map((c) => c[1]),
    rows: [
      new TableRow({ tableHeader: true, height: { value: 520, rule: HeightRule.ATLEAST }, children: COLS.map(([t, w]) => cell(t, w, true)) }),
      new TableRow({ height: { value: 460, rule: HeightRule.EXACT }, children: COLS.map(([, w], i) => cell(["1.2", "Схема собрана и проверена", "фото схемы, показания на 3 образцах почвы", "технический эксперт", "1 неделя"][i], w, false)) }),
      ...Array.from({ length: 15 }, () => new TableRow({ height: { value: 460, rule: HeightRule.EXACT }, children: COLS.map(([, w]) => cell("", w, false)) })),
    ],
  }),
  para([run("Серая строка — пример. Ответственный — один человек, не «все». Длительность — в днях или неделях, честно: если раньше никто так не делал, срок больше.", { size: 17, italic: true, color: MUTE })], { before: 80 }),
];

const doc = new Document({
  creator: "ГУАП · Кафедра № 3", title: "Занятие 6. Бланк WBS, лист А4",
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 560, bottom: 500, left: MARGIN_X, right: MARGIN_X } } },
    children: [...front, ...back],
  }],
});
Packer.toBuffer(doc).then((b) => {
  const out = "zanyatiya/Zanyatie_06_WBS_A4_Blank.docx";
  fs.writeFileSync(out, b);
  console.log("OK", out, b.length);
});
