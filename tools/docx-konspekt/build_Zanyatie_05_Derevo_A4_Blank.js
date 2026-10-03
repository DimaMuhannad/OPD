// Бланк листа А4 к занятию 5: лицевая сторона — дерево проблем, обратная — дерево целей.
// Чёрно-белая печать, альбомная А4, как Zanyatie_04_Pasport_Blank.docx. Запуск:
//   NODE_PATH=<scratchpad>/node_modules node tools/docx-konspekt/build_Zanyatie_05_Derevo_A4_Blank.js
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  AlignmentType, HeightRule, PageOrientation, PageBreak, TableLayoutType,
} = require("docx");
const fs = require("fs");

const FONT = "Arial", INK = "000000", MUTE = "666666";
const MARGIN_X = 700;
const PAGE_W = 16838 - 2 * MARGIN_X; // A4 альбомная минус поля, twips
const GAP = 200;
const CENTRAL_W = 10000;

const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: none, bottom: none, left: none, right: none };
const thick = { style: BorderStyle.SINGLE, size: 12, color: INK };
const dashed = { style: BorderStyle.DASHED, size: 10, color: INK };
const boxBorders = { top: thick, bottom: thick, left: thick, right: thick };
const dashBorders = { top: dashed, bottom: dashed, left: dashed, right: dashed };

const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 22, bold: !!o.bold, color: o.color || INK, italics: !!o.italic });
const para = (t, o = {}) => new Paragraph({
  alignment: o.align || AlignmentType.LEFT,
  spacing: { before: o.before || 0, after: o.after ?? 60 },
  children: Array.isArray(t) ? t : [run(t, o)],
});
const label = (t, hint) => para([run(t, { bold: true, size: 22 }), run(hint ? "  " + hint : "", { size: 19, color: MUTE, italic: true })], { before: 80, after: 40 });
const arrow = (t) => para(t, { align: AlignmentType.CENTER, size: 22, bold: true, before: 20, after: 20 });

function boxCell(width, text) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders: arguments[2],
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: (Array.isArray(text) ? text : [text || ""]).map((t) => para(t, { size: 19, color: MUTE, italic: true, after: 160 })),
  });
}
function gapCell() {
  return new TableCell({ width: { size: GAP, type: WidthType.DXA }, borders: noBorders, children: [para("")] });
}
// ряд из n рамок одинаковой ширины с зазорами; подписи — серым курсивом в углу рамки
function boxRow(n, labels, height, borders = boxBorders, total = PAGE_W) {
  const w = Math.floor((total - (n - 1) * GAP) / n);
  const cells = [];
  for (let i = 0; i < n; i++) {
    if (i) cells.push(gapCell());
    cells.push(boxCell(w, labels[i] || "", borders));
  }
  return new Table({
    width: { size: total, type: WidthType.DXA }, alignment: AlignmentType.CENTER,
    layout: TableLayoutType.FIXED,
    columnWidths: Array.from({ length: 2 * n - 1 }, (_, i) => (i % 2 ? GAP : w)),
    rows: [new TableRow({ height: { value: height, rule: HeightRule.ATLEAST }, children: cells })],
  });
}
// ряд подписей «берём / граница» под подцелями
function pickRow(n) {
  const w = Math.floor((PAGE_W - (n - 1) * GAP) / n);
  const cells = [];
  for (let i = 0; i < n; i++) {
    if (i) cells.push(gapCell());
    cells.push(new TableCell({
      width: { size: w, type: WidthType.DXA }, borders: noBorders,
      children: [para([run("☐ берём в проект   ☐ граница", { size: 20 })], { align: AlignmentType.CENTER, before: 30, after: 0 })],
    }));
  }
  return new Table({
    width: { size: PAGE_W, type: WidthType.DXA }, layout: TableLayoutType.FIXED,
    columnWidths: Array.from({ length: 2 * n - 1 }, (_, i) => (i % 2 ? GAP : w)),
    rows: [new TableRow({ children: cells })],
  });
}
const head = (title, sub) => [
  para([run(title, { bold: true, size: 34 })], { after: 20 }),
  para([run("Команда: ______________________    Проект: ______________________________", { size: 21 }), run("     " + sub, { size: 18, color: MUTE, italic: true })], { after: 40 }),
];

// ── Лицевая сторона: дерево проблем ──
const front = [
  ...head("Дерево проблем", "лицевая сторона листа А4"),
  label("СЛЕДСТВИЯ", "к чему это приводит? не меньше двух"),
  boxRow(3, ["следствие", "следствие", "следствие"], 1350),
  arrow("▲   приводит к   ▲"),
  label("ЦЕНТРАЛЬНАЯ ПРОБЛЕМА", "одна; состояние дел, а не отсутствие продукта; без названия вашего продукта"),
  boxRow(1, ["центральная проблема"], 900, boxBorders, CENTRAL_W),
  arrow("▲   приводит к   ▲"),
  label("ПРИЧИНЫ", "почему это происходит? не меньше трёх; состояния, а не действия"),
  boxRow(4, ["причина", "причина", "причина", "причина"], 1900),
  para([run("Проверка:  ☐ проблему можно записать, не называя продукт    ☐ в причинах нет глаголов действия    ☐ каждая связь прочитана вслух: факт или догадка?  Догадки отметьте «?»", { size: 19 })], { before: 100 }),
];
// ── Обратная сторона: дерево целей ──
const back = [
  new Paragraph({ children: [new PageBreak()] }),
  ...head("Дерево целей", "обратная сторона листа А4"),
  label("ОЖИДАЕМЫЕ ЭФФЕКТЫ", "каждое следствие переписано как желаемое состояние"),
  boxRow(3, ["эффект", "эффект", "эффект"], 1000),
  arrow("▲   достигается через   ▲"),
  label("ГЛАВНАЯ ЦЕЛЬ", "центральная проблема, переписанная как состояние, при котором её нет"),
  boxRow(1, ["главная цель"], 800, boxBorders, CENTRAL_W),
  arrow("▲   достигается через   ▲"),
  label("ПОДЦЕЛИ", "каждая причина, переписанная как состояние; отметьте, что берёте в проект"),
  boxRow(4, ["подцель", "подцель", "подцель", "подцель"], 1400),
  pickRow(4),
  label("ГРАНИЦЫ", "ветви, которые оставляем: каждую записать как отказ («… не делаем»)"),
  boxRow(1, [["1)  … не делаем", "2)  … не делаем", "3)  … не делаем"]], 900, dashBorders, PAGE_W),
  para([run("Проверка:  ☐ для каждой цели есть причина на лицевой стороне    ☐ выбранное помещается в срок до защиты    ☐ цели записаны как состояния, а не как действия", { size: 19 })], { before: 80 }),
];

const doc = new Document({
  creator: "ГУАП · Кафедра № 3", title: "Занятие 5. Бланк листа А4: дерево проблем и дерево целей",
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE },
        margin: { top: 560, bottom: 560, left: MARGIN_X, right: MARGIN_X },
      },
    },
    children: [...front, ...back],
  }],
});
Packer.toBuffer(doc).then((b) => {
  const out = "zanyatiya/Zanyatie_05_Derevo_A4_Blank.docx";
  fs.writeFileSync(out, b);
  console.log("OK", out, b.length);
});
