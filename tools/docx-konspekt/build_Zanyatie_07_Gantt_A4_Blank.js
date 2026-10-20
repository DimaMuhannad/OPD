// Бланк к занятию 7: лицевая сторона — диаграмма Ганта (сетка недель), обратная — нагрузка по людям,
// решение по сроку и домашнее задание (риски и потребности пакетов).
// Чёрно-белая печать, альбомная А4 (А3 нет), стиль — как Zanyatie_06_WBS_A4_Blank. Запуск:
//   NODE_PATH=/opt/node-tools/node_modules node tools/docx-konspekt/build_Zanyatie_07_Gantt_A4_Blank.js
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  AlignmentType, HeightRule, PageOrientation, PageBreak, TableLayoutType, VerticalAlign,
} = require("docx");
const fs = require("fs");

const FONT = "Arial", INK = "000000", MUTE = "666666";
const MARGIN_X = 700;
const PAGE_W = 16838 - 2 * MARGIN_X;
const WEEKS = 10;

const thin = { style: BorderStyle.SINGLE, size: 6, color: INK };
const box = (b) => ({ top: b, bottom: b, left: b, right: b });

const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 20, bold: !!o.bold, color: o.color || INK, italics: !!o.italic });
const para = (t, o = {}) => new Paragraph({
  alignment: o.align || AlignmentType.LEFT, spacing: { before: o.before || 0, after: o.after ?? 40 },
  children: Array.isArray(t) ? t : [run(t, o)],
});
const head = (title, sub) => [
  para([run(title, { bold: true, size: 32 })], { after: 20 }),
  para([run("Команда: ______________________    Проект: ______________________________", { size: 20 }), run("     " + sub, { size: 17, color: MUTE, italic: true })], { after: 60 }),
];
const label = (t, hint) => para([run(t, { bold: true, size: 21 }), run(hint ? "  " + hint : "", { size: 18, color: MUTE, italic: true })], { before: 100, after: 40 });

const cell = (t, w, o = {}) => new TableCell({
  width: { size: w, type: WidthType.DXA }, borders: box(thin), verticalAlign: VerticalAlign.CENTER,
  shading: o.fill, columnSpan: o.span, margins: { top: 30, bottom: 30, left: 70, right: 70 },
  children: [para([run(t, { bold: !!o.bold, size: o.size || 17, color: o.color || (o.bold ? INK : MUTE), italic: !!o.italic })], { after: 0, align: o.align })],
});
const table = (cols, rows) => new Table({
  width: { size: cols.reduce((a, b) => a + b, 0), type: WidthType.DXA }, layout: TableLayoutType.FIXED, columnWidths: cols, rows,
});
const tr = (cells, h, rule = HeightRule.EXACT) => new TableRow({ height: { value: h, rule }, children: cells });

// ── Лицевая сторона: диаграмма Ганта ──
const WK = 948;
const G = [650, 3300, 1150, 800]; // код, пакет, зависит от, недель
const gcols = [...G, ...Array(WEEKS).fill(WK)];
const gHead = [
  tr([cell("Код", G[0], { bold: true, size: 18 }), cell("Пакет работ", G[1], { bold: true, size: 18 }), cell("Зависит от", G[2], { bold: true, size: 18 }),
    cell("Нед.", G[3], { bold: true, size: 18 }),
    ...Array.from({ length: WEEKS }, (_, i) => cell(String(i + 1), WK, { bold: true, size: 20, align: AlignmentType.CENTER }))], 380, HeightRule.ATLEAST),
  tr([cell("с даты:", G[0] + G[1] + G[2] + G[3], { span: 4, size: 16, italic: true, align: AlignmentType.RIGHT }),
    ...Array.from({ length: WEEKS }, () => cell("", WK))], 340),
];
const emptyRow = () => tr([...G.map((w) => cell("", w)), ...Array.from({ length: WEEKS }, () => cell("", WK))], 480);
const mileRow = tr([cell("◆", G[0], { bold: true, align: AlignmentType.CENTER, size: 20 }), cell("Милстоуны: отметьте ◆ в конце недели и подпишите", G[1] + G[2] + G[3], { span: 3, italic: true }),
  ...Array.from({ length: WEEKS }, () => cell("", WK))], 520);
const front = [
  ...head("Диаграмма Ганта", "лицевая сторона · обратная — нагрузка по людям и риски"),
  table(gcols, [...gHead, ...Array.from({ length: 15 }, emptyRow), mileRow]),
  para([run("Как заполнять: ", { bold: true, size: 17 }),
    run("1) в «Зависит от» — коды прямых предшественников;  2) закрасьте простым карандашом клетки недель, на которые приходится пакет, начиная после самого позднего предшественника;  3) критический путь — самую длинную цепочку — заштрихуйте поверх закраски;  4) под сеткой отметьте милстоуны.", { size: 17, color: MUTE })], { before: 80 }),
  para([run("Срок проекта (длина критического пути): ______ недель     До защиты: ______ недель     Помещается:  ☐ с запасом   ☐ впритык   ☐ нет", { size: 19 })], { before: 80 }),
];

// ── Обратная сторона ──
const L = [2958, ...Array(WEEKS).fill(1248)]; // участник + недели
const loadRows = [
  tr([cell("Участник и его роль", L[0], { bold: true, size: 18 }), ...Array.from({ length: WEEKS }, (_, i) => cell(String(i + 1), L[1], { bold: true, size: 20, align: AlignmentType.CENTER }))], 360, HeightRule.ATLEAST),
  ...Array.from({ length: 5 }, () => tr([cell("", L[0]), ...Array.from({ length: WEEKS }, () => cell("", L[1]))], 440)),
];
const D = [1300, 5800, 8338]; // пакет, что может пойти не так, что нужно
const hw = [
  tr([cell("Пакет", D[0], { bold: true, size: 18 }), cell("Что может пойти не так (пакеты критического пути)", D[1], { bold: true, size: 18 }), cell("Что нужно, чтобы сделать: часы участников, материалы", D[2], { bold: true, size: 18 })], 440, HeightRule.ATLEAST),
  tr([cell("1.2", D[0], { italic: true }), cell("пример: нужного датчика нет в магазине, везти две недели", D[1], { italic: true }), cell("пример: 8 часов технического эксперта; датчик, плата, провода", D[2], { italic: true })], 420),
  ...Array.from({ length: 6 }, () => tr([cell("", D[0]), cell("", D[1]), cell("", D[2])], 440)),
];
const back = [
  new Paragraph({ children: [new PageBreak()] }),
  ...head("Нагрузка по людям и риски", "обратная сторона"),
  label("НАГРУЗКА ПО ЛЮДЯМ", "впишите коды пакетов, которые участник ведёт в эту неделю; два кода в одной клетке — перегрузка"),
  table(L, loadRows),
  label("РЕШЕНИЕ ПО СРОКУ", "если перегрузка или срок не помещается до защиты: что меняем — содержание, оценку или ресурсы — и почему"),
  table([PAGE_W], [tr([cell("", PAGE_W)], 440), tr([cell("", PAGE_W)], 440)]),
  label("РИСКИ И ПОТРЕБНОСТИ ПАКЕТОВ", "к следующему занятию, заполнить дома; пример — первая строка"),
  table(D, hw),
];

const doc = new Document({
  creator: "ГУАП · Кафедра № 3", title: "Занятие 7. Бланк диаграммы Ганта, лист А4",
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 500, bottom: 440, left: MARGIN_X, right: MARGIN_X } } },
    children: [...front, ...back],
  }],
});
Packer.toBuffer(doc).then((b) => {
  const out = "zanyatiya/Zanyatie_07_Gantt_A4_Blank.docx";
  fs.writeFileSync(out, b);
  console.log("OK", out, b.length);
});
