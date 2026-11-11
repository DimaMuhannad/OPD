// Бланк к занятию 9 «Команда и исполнение» (самостоятельная работа): те же пять зон, что на доске Excalidraw
// (tools/excalidraw/z09_board.js) и в конспекте. Лицевая сторона: зоны 1–2 (команда). Обратная: зоны 3–5 (исполнение).
// Чёрно-белая печать, альбомная А4. Запуск:
//   NODE_PATH=/opt/node-tools/node_modules node tools/docx-konspekt/build_Zanyatie_09_Komanda_A4_Blank.js
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


// ── Лицевая сторона: зоны 1–2 ──
const Z1W = 6000, GAP = 250, Z2W = PAGE_W - Z1W - GAP;
const R = [2900, 1550, 1550];
const zone1 = table(R, [
  tr([["Пакет", "код и название из WBS"], ["Ответственный", "из WBS"], ["Запасной", "в курсе, подхватит"]]
    .map(([t, h], j) => cell([para([run(t, { bold: true, size: 16 })]), para([run(h, { size: 13, italic: true, color: MUTE })])], R[j], { fill: "E8E8E8" })), 480),
  ...Array.from({ length: 12 }, () => tr([cell("", R[0]), cell("", R[1]), cell("", R[2])], 600)),
]);
const roles = [
  para([run("Доводит до конца (доводчик): ", { bold: true, size: 16 }), run("______________________", { size: 16, color: MUTE })], { before: 120 }),
  para([run("Проверяет «а точно сработает?» (аналитик-критик): ", { bold: true, size: 16 }), run("__________", { size: 16, color: MUTE })], { before: 100 }),
  para([run("Пакеты критического пути отметьте звёздочкой ★ — у них запасной обязателен.", { size: 14, italic: true, color: MUTE })], { before: 80 }),
];
const Q = [500, 2650, Z2W - 3150];
const rules = [
  ["Как держим связь", "где пишем, за сколько отвечаем, как сообщаем о срочном"],
  ["Когда сверяемся", "день и время сверки, сколько длится, кто пишет журнал"],
  ["Как принимаем решения", "кто решает по пакету, кто по общему, если не договорились"],
  ["Что значит «сделано»", "есть проверяемый результат из WBS и его видел ещё один человек"],
  ["Если кто-то не успевает", "за сколько предупреждать, что делает запасной, когда к преподавателю"],
];
const zone2 = table(Q, [
  tr([cell("№", Q[0], { bold: true, size: 15 }), cell("Вопрос", Q[1], { bold: true, size: 15 }), cell([para([run("Наше правило", { bold: true, size: 15 }), run("  проверяемое: по нему видно, нарушено или нет", { size: 13, italic: true, color: MUTE })])], Q[2])], 360),
  ...rules.map(([t, h], i) => tr([cell(String(i + 1), Q[0], { bold: true, size: 18, valign: VerticalAlign.CENTER }),
    cell([para([run(t, { bold: true, size: 16 })]), para([run(h, { size: 13, italic: true, color: MUTE })])], Q[1]), cell("", Q[2])], 1480)),
]);
const sign = para([run("Согласны (подписи всех участников): ", { bold: true, size: 16 }), run("______________   ______________   ______________   ______________", { size: 16, color: MUTE })], { before: 140 });
const front = [
  ...head("Команда и исполнение", "лицевая сторона: зоны 1–2 · обратная: зоны 3–5"),
  new Table({
    width: { size: PAGE_W, type: WidthType.DXA }, layout: TableLayoutType.FIXED, columnWidths: [Z1W, GAP, Z2W],
    rows: [new TableRow({ children: [
      new TableCell({ width: { size: Z1W, type: WidthType.DXA }, borders: box(none), children: [zoneHead(1, "Кто за что отвечает", "сначала ближайшие недели"), zone1, ...roles] }),
      new TableCell({ width: { size: GAP, type: WidthType.DXA }, borders: box(none), children: [para("")] }),
      new TableCell({ width: { size: Z2W, type: WidthType.DXA }, borders: box(none), children: [zoneHead(2, "Командный договор: пять правил", "пишем до споров, ссылаемся при споре"), zone2, sign] }),
    ] })],
  }),
];

// ── Обратная сторона: зоны 3–5 ──
const J0 = 1500, JW = Math.floor((PAGE_W - J0) / 3), JL = PAGE_W - J0 - 2 * JW;
const jrows = [["Думали", "что собирались по диаграмме Ганта"], ["Сделали", "только готовое по правилу «сделано»"], ["Узнали", "что нового, что пошло не так"], ["Дальше", "что и кто на следующей неделе"]];
const zone3 = table([J0, JW, JW, JL], [
  tr([cell("", J0, { fill: "E8E8E8" }), ...[JW, JW, JL].map((w) => cell([para([run("Неделя ___   с ______ по ______", { bold: true, size: 15 })])], w, { fill: "E8E8E8" }))], 330),
  ...jrows.map(([t, h]) => tr([cell([para([run(t, { bold: true, size: 16 })]), para([run(h, { size: 12, italic: true, color: MUTE })])], J0), cell("", JW), cell("", JW), cell("", JL)], 760)),
]);
const F = [3200, 1500, 1900, 1100, 3700, PAGE_W - 11400];
const zone4 = table(F, [
  tr([["Пакет", "★ — критический путь"], ["По плану", "неделя готовности"], ["По факту", "готов в неделю __ / в работе / не начат"], ["Откл.", "недель"], ["Причина", "одной фразой; «не успели» — не причина"], ["Решение", "держим план / меняем — что именно"]]
    .map(([t, h], j) => cell([para([run(t, { bold: true, size: 15 })]), para([run(h, { size: 12, italic: true, color: MUTE })])], F[j], { fill: "E8E8E8" })), 480),
  ...Array.from({ length: 6 }, () => tr(F.map((w, j) => cell(j === 3 ? [para([run("+ ___", { size: 15, color: MUTE })], { before: 80 })] : "", w)), 560)),
]);
const C = Math.floor(PAGE_W / 5);
const zone5 = table([C, C, C, C, PAGE_W - 4 * C], [
  tr([["Результат", "что покажем руками и кто принесёт"], ["Обещали", "к этой неделе"], ["Есть", "на самом деле"], ["Что следует", "держим или меняем, что именно"], ["Говорят", "кто что говорит, 5 минут"]]
    .map(([t, h], j) => cell([para([run(t, { bold: true, size: 15 })]), para([run(h, { size: 12, italic: true, color: MUTE })])], j < 4 ? C : PAGE_W - 4 * C, { fill: "E8E8E8" })), 460),
  tr([0, 1, 2, 3, 4].map((j) => cell("", j < 4 ? C : PAGE_W - 4 * C)), 1300),
]);
const back = [
  new Paragraph({ children: [new PageBreak()] }),
  ...head("Исполнение и чекпоинт", "обратная сторона: зоны 3–5"),
  zoneHead(3, "Журнал проекта", "одна запись в неделю после сверки; «работаем» — не статус"),
  zone3,
  zoneHead(4, "План против факта", "все пакеты, которые по плану должны были начаться к этой неделе"),
  zone4,
  zoneHead(5, "Что покажем на чекпоинте", "предъявляем то, что можно взять в руки или прочитать"),
  zone5,
  para([run("Сводный план — фото в тему команды сразу. Этот лист и промежуточный результат — на чекпоинт.", { size: 16, bold: true })], { before: 100 }),
];

const doc = new Document({
  creator: "ГУАП · Кафедра № 3", title: "Занятие 9. Команда и исполнение, лист А4",
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 450, bottom: 400, left: MARGIN_X, right: MARGIN_X } } },
    children: [...front, ...back],
  }],
});
Packer.toBuffer(doc).then((b) => {
  const out = process.argv[2] || "zanyatiya/Zanyatie_09_Komanda_A4_Blank.docx";
  fs.writeFileSync(out, b);
  console.log("OK", out, b.length);
});
