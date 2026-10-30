// Бланк к занятию 8 «Риски и ресурсы»: те же шесть зон, что на доске Excalidraw (tools/excalidraw/z08_board.js),
// в том же порядке и с теми же подписями — конспект ведёт по ним одинаково.
// Лицевая сторона: зоны 1–3 (риски). Обратная: зоны 4–6 (ресурсы и сборка плана).
// Чёрно-белая печать, альбомная А4. Запуск:
//   NODE_PATH=/opt/node-tools/node_modules node tools/docx-konspekt/build_Zanyatie_08_Riski_A4_Blank.js
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  AlignmentType, HeightRule, PageOrientation, PageBreak, TableLayoutType, VerticalAlign, ShadingType,
} = require("docx");
const fs = require("fs");

const FONT = "Arial", INK = "000000", MUTE = "666666";
const MARGIN_X = 650;
const PAGE_W = 16838 - 2 * MARGIN_X; // 15538
const thin = { style: BorderStyle.SINGLE, size: 6, color: INK };
const thick = { style: BorderStyle.SINGLE, size: 14, color: INK };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const box = (b) => ({ top: b, bottom: b, left: b, right: b });
const shade = (fill) => ({ type: ShadingType.CLEAR, color: "auto", fill });

const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 18, bold: !!o.bold, color: o.color || INK, italics: !!o.italic });
const para = (t, o = {}) => new Paragraph({
  alignment: o.align || AlignmentType.LEFT, spacing: { before: o.before || 0, after: o.after ?? 0 },
  children: Array.isArray(t) ? t : [run(t, o)],
});
const zoneHead = (n, title, hint) => para([run(`Зона ${n}. ${title}`, { bold: true, size: 22 }), run("   " + hint, { size: 16, italic: true, color: MUTE })], { before: 80, after: 40 });
const cell = (content, w, o = {}) => new TableCell({
  width: { size: w, type: WidthType.DXA }, borders: o.borders || box(thin), verticalAlign: o.valign || VerticalAlign.TOP,
  shading: o.fill ? shade(o.fill) : undefined, columnSpan: o.span, margins: { top: 30, bottom: 30, left: 60, right: 60 },
  children: Array.isArray(content) ? content : [para([run(content, { bold: !!o.bold, size: o.size || 16, color: o.color || (o.bold ? INK : MUTE), italic: !!o.italic })], { align: o.align })],
});
const table = (cols, rows) => new Table({ width: { size: cols.reduce((a, b) => a + b, 0), type: WidthType.DXA }, layout: TableLayoutType.FIXED, columnWidths: cols, rows });
const tr = (cells, h, rule = HeightRule.EXACT) => new TableRow({ height: { value: h, rule }, children: cells });
const head = (title, sub) => [
  para([run(title, { bold: true, size: 30 })]),
  para([run("Команда: ____________________   Проект: ______________________________", { size: 18 }), run("     " + sub, { size: 16, italic: true, color: MUTE })], { after: 20 }),
];

// ── Лицевая сторона ──
// Зона 1: четыре кармана, по два риска в каждом, риски нумеруются 1–8
const P1 = Math.floor(PAGE_W / 4);
const pockets = [["Люди", "кто-то выпал, не умеет, перегружен"], ["Вещи", "нет детали, сломалось, не подошло"],
  ["Время", "сессия, праздники, критический путь"], ["Чужие", "поставщик, лаборатория, респонденты"]];
const riskCell = (n) => [para([run(`${n}. Если `, { size: 17, bold: true }), run("_______________________________", { size: 17, color: MUTE })], { after: 60 }),
  para([run("то ", { size: 17, bold: true }), run("__________________________________", { size: 17, color: MUTE })], { after: 60 }),
  para([run("____________________________________", { size: 17, color: MUTE })])];
const zone1 = table(Array(4).fill(P1), [
  tr(pockets.map(([t, h]) => cell([para([run(t, { bold: true, size: 20 }), run("  " + h, { size: 15, italic: true, color: MUTE })])], P1, { fill: "E8E8E8" })), 330),
  tr([1, 3, 5, 7].map((n) => cell(riskCell(n), P1)), 1250),
  tr([2, 4, 6, 8].map((n) => cell(riskCell(n), P1)), 1250),
]);

// Зона 2: поле 3×3. В клетке — подсказка, что делать с риском этой клетки
const ACT = { R: "нужен ответ (зона 3)", Y: "ответ, если дёшево", G: "принимаем" };
const map = [["Y", "R", "R"], ["G", "Y", "R"], ["G", "G", "Y"]];
const FILL = { R: "BFBFBF", Y: "E3E3E3", G: "FFFFFF" };
const LW = 1250, GW = 1700;
const zone2 = table([LW, GW, GW, GW], [
  tr([cell("шанс ↓   удар →", LW, { size: 14, italic: true }), ...["мелочь", "заметно, перестроим план", "сдвигает защиту"].map((t) => cell(t, GW, { bold: true, size: 15 }))], 380),
  ...["почти точно", "может быть", "редко"].map((r, i) => tr([cell(r, LW, { bold: true, size: 15, valign: VerticalAlign.CENTER }),
    ...map[i].map((k) => cell([para([run(ACT[k], { size: 13, italic: true, color: "555555" })]), para(""), para([run("номера рисков: ", { size: 13, color: MUTE })])], GW, { fill: FILL[k] }))], 1250)),
]);
const Z2W = LW + 3 * GW; // 6350

// Зона 3: для двух красных рисков — четыре ответа, выбранный обвести
const Z3W = PAGE_W - Z2W - 200;
const A0 = 800, A1 = Math.floor((Z3W - A0 - 1500) / 4), A2 = Z3W - A0 - 4 * A1;
const zone3 = table([A0, A1, A1, A1, A1, A2], [
  tr([cell("№ риска", A0, { bold: true, size: 14 }), ...[["Избежать", "убрать причину"], ["Снизить", "меньше шанс или удар"], ["Передать", "тому, кто справится"], ["Принять", "запасной план"]]
    .map(([t, h]) => cell([para([run(t, { bold: true, size: 15 })]), para([run(h, { size: 12, italic: true, color: MUTE })])], A1)),
    cell([para([run("Берём", { bold: true, size: 15 })]), para([run("и кто отвечает", { size: 12, italic: true, color: MUTE })])], A2)], 520),
  ...[0, 1, 2].map(() => tr([cell("", A0), cell("", A1), cell("", A1), cell("", A1), cell("", A1), cell("", A2)], 1400)),
]);
const pair = new Table({
  width: { size: PAGE_W, type: WidthType.DXA }, layout: TableLayoutType.FIXED, columnWidths: [Z2W, 200, Z3W],
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: Z2W, type: WidthType.DXA }, borders: box(none), children: [zoneHead(2, "Поле-светофор", "впишите номера рисков в клетки"), zone2] }),
    new TableCell({ width: { size: 200, type: WidthType.DXA }, borders: box(none), children: [para("")] }),
    new TableCell({ width: { size: Z3W, type: WidthType.DXA }, borders: box(none), children: [zoneHead(3, "Одна угроза — четыре ответа", "для рисков из тёмных клеток; выбранный ответ обведите"), zone3] }),
  ] })],
});

const front = [
  ...head("Риски и ресурсы проекта", "лицевая сторона: зоны 1–3 · обратная: зоны 4–6"),
  zoneHead(1, "Письмо с защиты", "26 декабря. Защита идёт, а прототипа нет. Что случилось? Каждая причина — риск «Если…, то…»"),
  zone1,
  pair,
];

// ── Обратная сторона ──
const K = [2600, 3100, 6038, 3800];
const zone4 = table(K, [
  tr([["Участник", "имя или роль"], ["Кошелёк", "часов в неделю × недель до защиты"], ["Его пакеты и часы работы", "код — часы, затем сложите"], ["Итог и что делаем", "влезает / не влезает → решение"]]
    .map(([t, h], j) => cell([para([run(t, { bold: true, size: 16 })]), para([run(h, { size: 13, italic: true, color: MUTE })])], K[j])), 480),
  ...[0, 1, 2, 3].map(() => tr([cell("", K[0]), cell([para([run("___ × ___ = ___ ч", { size: 17, color: MUTE })], { before: 120 })], K[1]), cell("", K[2]),
    cell([para([run("___ из ___ ч", { size: 17, color: MUTE })], { before: 120 })], K[3])], 880)),
]);
const C5 = Math.floor(PAGE_W / 3);
const lines = (n) => Array.from({ length: n }, () => para([run("_____________________________________________", { size: 17, color: MUTE })], { before: 70 }));
const zone5 = table([C5, C5, PAGE_W - 2 * C5], [
  tr([["Есть у команды", ""], ["Взять", "кафедра, лаборатория, друзья — у кого?"], ["Купить", "что и примерно за сколько"]]
    .map(([t, h], j) => cell([para([run(t, { bold: true, size: 17 }), run(h ? "  " + h : "", { size: 13, italic: true, color: MUTE })])], j < 2 ? C5 : PAGE_W - 2 * C5, { fill: "E8E8E8" })), 330),
  tr([cell(lines(7), C5), cell(lines(7), C5), cell([...lines(6), para([run("Сумма покупок ______ ₽ ≤ лимит из паспорта ______ ₽", { size: 16, bold: true })], { before: 90 })], PAGE_W - 2 * C5)], 2700),
]);
const checks = [
  "1. WBS ↔ Ганта: каждый пакет WBS есть на диаграмме, лишних нет",
  "2. Риски ↔ WBS и Ганта: ответ на красный риск стал пакетом или строкой на диаграмме",
  "3. Ганта ↔ кошелёк: часы пакетов влезают в кошельки (зона 4)",
  "4. Риски ↔ ресурсы: ответы на риски учтены в часах и покупках",
  "5. Ганта ↔ защита: срок помещается до 26.12, есть запасная неделя",
  "6. Покупки ↔ паспорт: «купить» не больше лимита из паспорта",
];
const H6 = Math.floor(PAGE_W / 2);
const zone6 = table([H6, PAGE_W - H6], [0, 1, 2].map((i) => tr([0, 1].map((j) => cell([para([run("☐  " + checks[i + j * 3], { size: 16, color: INK })])], j ? PAGE_W - H6 : H6, { valign: VerticalAlign.CENTER })), 520)));

const back = [
  new Paragraph({ children: [new PageBreak()] }),
  ...head("Ресурсы и сборка плана", "обратная сторона: зоны 4–6"),
  zoneHead(4, "Кошелёк часов", "хватит ли каждому времени на его пакеты? Часы работы, а не длительность на диаграмме"),
  zone4,
  zoneHead(5, "Есть / взять / купить", "что нужно пакетам: материалы, оборудование, доступ. «Пока не знаем» — тоже риск, в зону 1"),
  zone5,
  zoneHead(6, "Пазл: план собран, когда все стыки сходятся", "части плана: WBS (бланк занятия 6), Ганта (бланк занятия 7), риски (зоны 1–3), ресурсы (зоны 4–5)"),
  zone6,
  para([run("Сдать к следующему занятию: бланк WBS, бланк Ганта и этот лист — скрепить вместе.", { size: 17, bold: true })], { before: 100 }),
];

const doc = new Document({
  creator: "ГУАП · Кафедра № 3", title: "Занятие 8. Риски и ресурсы, лист А4",
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 450, bottom: 400, left: MARGIN_X, right: MARGIN_X } } },
    children: [...front, ...back],
  }],
});
Packer.toBuffer(doc).then((b) => {
  const out = process.argv[2] || "zanyatiya/Zanyatie_08_Riski_A4_Blank.docx";
  fs.writeFileSync(out, b);
  console.log("OK", out, b.length);
});
