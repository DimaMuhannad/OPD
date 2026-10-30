// Доска занятия 8 «Риски и ресурсы» для совместной работы команды в Excalidraw.
// Шесть зон по ходу пары: письмо с защиты → поле-светофор → четыре ответа → кошелёк часов →
// есть / взять / купить → пазл сборки плана. Рамки и подписи закреплены, стикеры двигаются.
// Запуск: node tools/excalidraw/z08_board.js [файл] [команда]  → zanyatiya/Zanyatie_08_Doska.excalidraw
const fs = require("fs");
const { text, rect, sticker } = require("./scene");

const W = 1640, L = { locked: true };
const GREEN = "#b2f2bb", YELLOW = "#ffec99", RED = "#ffc9c9", BLUE = "#a5d8ff", ZONE = "#f8f9fa";
const els = [];
const EX = "#868e96"; // цвет примера
const ex = (t) => "Пример:\n" + t;
const add = (a) => els.push(...a);
let zoneStart = 0, zoneNo = 0;
const COLW = W + 120, ROWH = 1060;
const zone = (y, h, title, hint) => {
  zoneStart = els.length;
  add(rect(0, y, W, h, { backgroundColor: ZONE, strokeColor: "#adb5bd", strokeWidth: 2, ...L }));
  add(text(30, y + 22, title, 34, { ...L, strokeColor: "#1971c2" }));
  if (hint) add(text(30, y + 72, hint, 20, { ...L, strokeColor: "#495057" }));
};
// сдвигает элементы текущей зоны в клетку сетки и помечает номер зоны (для покадровой проверки)
const place = () => {
  const dx = (zoneNo % 3) * COLW, dy = Math.floor(zoneNo / 3) * ROWH;
  for (const e of els.slice(zoneStart)) { e.x += dx; e.y += dy; e.customData = { zone: zoneNo + 1 }; }
  zoneNo++;
};

// ── Шапка ──
add(text(0, -150, "Занятие 8 · Что может сломаться и хватит ли нам сил", 40, L));
const team = process.argv[3] || "______________";
add(text(0, -90, `Команда: ${team}   Проект: ______________________   Двойной щелчок по стикеру — писать; Ctrl+D — копия. Серые «Пример:» — про умный горшок: сотрите и впишите своё`, 20, { ...L, strokeColor: "#495057" }));

// ── 1. Письмо с защиты ──
let y = 0;
zone(y, 800, "1. Письмо с защиты",
  "26 декабря. Защита идёт, а прототипа на столе нет. Что случилось? Каждая причина — стикер: «Если ___, то ___».");
const pockets = [["Люди", "кто-то выпал, не умеет, перегружен", "если эксперт заболеет,\nто пайка встанет"],
  ["Вещи", "нет детали, сломалось, не подошло", "если датчика нет\nв магазине, то схему\nне собрать вовремя"],
  ["Время", "сессия, праздники, критический путь", "если испытания попадут\nна сессию, то не успеем\n10 циклов полива"],
  ["Чужие", "поставщик, лаборатория, респонденты", "если владельцы растений\nоткажутся, то проверки\nс людьми не будет"]];
pockets.forEach(([t, h, e], i) => {
  const x = 30 + i * 400;
  add(rect(x, y + 130, 370, 640, { backgroundColor: "#ffffff", strokeColor: "#ced4da", ...L }));
  add(text(x + 20, y + 145, t, 28, { ...L, strokeColor: "#1971c2" }));
  add(text(x + 20, y + 185, h, 17, { ...L, strokeColor: "#868e96" }));
  add(sticker(x + 75, y + 230, ex(e), { tc: EX, size: 15 }));
  for (let k = 1; k < 4; k++) add(sticker(x + 75, y + 230 + k * 132));
});

// ── 2. Поле-светофор ──
place();
y = 0;
zone(y, 900, "2. Поле-светофор",
  "Перетащите каждый стикер в клетку: насколько вероятно и насколько сильно ударит. Красные — нужен план действий, зелёные — принимаем.");
const colsL = ["мелочь", "заметно, перестроим план", "сдвигает защиту"];
const rowsL = ["почти точно", "может быть", "редко"];
const colour = [[YELLOW, RED, RED], [GREEN, YELLOW, RED], [GREEN, GREEN, YELLOW]];
const GX = 260, GY = y + 190, CW = 440, CH = 220;
add(text(GX + 3 * CW / 2 - 60, y + 125, "УДАР →", 22, { ...L, strokeColor: "#495057" }));
colsL.forEach((c, j) => add(text(GX + j * CW + 20, y + 158, c, 20, L)));
add(text(40, y + 158, "ШАНС ↓", 22, { ...L, strokeColor: "#495057" }));
rowsL.forEach((r, i) => {
  add(text(40, GY + i * CH + CH / 2 - 12, r, 20, L));
  colsL.forEach((_, j) => add(rect(GX + j * CW, GY + i * CH, CW, CH, { backgroundColor: colour[i][j], strokeColor: "#868e96", roundness: null, ...L })));
});
add(sticker(GX + 2 * CW + 110, GY + CH + 50, ex("датчика нет\nв магазине"), { tc: EX, size: 15 }));
add(sticker(GX + 110, GY + 2 * CH + 50, ex("корпус не влез\nв горшок"), { tc: EX, size: 15 }));

// ── 3. Одна угроза — четыре ответа ──
place();
y = 0;
zone(y, 820, "3. Одна угроза — четыре ответа",
  "Для каждого красного стикера: скопируйте его в первый столбец, придумайте ответы и обведите один, который берём. Внизу — кто отвечает.");
const answers = [["Избежать", "изменить план, чтобы причина исчезла"], ["Снизить", "уменьшить шанс или удар заранее"],
  ["Передать", "отдать тому, кто справится лучше"], ["Принять", "ничего заранее, есть запасной план"]];
const AX = 30, AW = 312;
add(text(AX + 20, y + 130, "Красный риск", 24, { ...L, strokeColor: "#c92a2a" }));
answers.forEach(([t, h], j) => {
  const x = AX + (j + 1) * AW + 20;
  add(text(x, y + 120, t, 24, { ...L, strokeColor: "#1971c2" }));
  add(text(x, y + 152, h, 15, { ...L, strokeColor: "#868e96" }));
});
const exRow = ["датчика нет\nв магазине,\nждать 3 недели", "выбрать датчик,\nкоторый точно есть", "купить сразу\nдва разных", "попросить датчик\nв лаборатории", "ждать, сдвинуть\nиспытания"];
for (let i = 0; i < 3; i++) {
  const ry = y + 200 + i * 200;
  const e = (j) => (i === 0 ? { label: ex(exRow[j]), tc: EX, size: 15 } : {});
  add(sticker(AX + 20, ry, " ", { backgroundColor: RED, strokeColor: "#c92a2a", ...e(0) }));
  for (let j = 0; j < 4; j++) add(sticker(AX + (j + 1) * AW + 20, ry, " ", { backgroundColor: "#ffffff", strokeColor: "#adb5bd", ...e(j + 1) }));
  add(text(AX + 20, ry + 130, i === 0 ? "Пример: берём «снизить», отвечает аналитик" : "Берём: ________   Отвечает (один): ________", 17, { ...L, strokeColor: i === 0 ? EX : "#495057", locked: i !== 0 }));
}

// ── 4. Кошелёк часов ──
place();
y = 0;
zone(y, 720, "4. Кошелёк часов",
  "Кошелёк = сколько часов в неделю человек реально даст × сколько недель до защиты. Растяните синюю полосу на сумму часов его пакетов.");
add(text(330, y + 125, "часов в неделю × недель = кошелёк", 18, { ...L, strokeColor: "#495057" }));
add(text(760, y + 125, "зелёная рамка — кошелёк, синяя полоса — сколько часов просят пакеты", 18, { ...L, strokeColor: "#495057" }));
for (let i = 0; i < 4; i++) {
  const ry = y + 170 + i * 135;
  const first = i === 0;
  add(sticker(30, ry, first ? ex("аналитик") : "участник", { width: 260, height: 100, backgroundColor: "#ffffff", strokeColor: "#adb5bd", tc: first ? EX : "#1e1e1e" }));
  add(sticker(330, ry + 10, first ? ex("5 × 8 = 40 ч") : "___ × ___ = ___ ч", { width: 380, height: 80, backgroundColor: "#ffffff", strokeColor: "#adb5bd", tc: first ? EX : "#1e1e1e" }));
  add(rect(760, ry + 20, 800, 30, { backgroundColor: "transparent", strokeColor: "#2f9e44", strokeWidth: 3, roundness: null, ...L }));
  add(rect(760, ry + 60, first ? 680 : 300, 26, { backgroundColor: BLUE, strokeColor: "#1971c2", roundness: null }));
  if (first) add(text(760, ry + 92, "пример: пакеты аналитика 34 ч из 40 — влезает", 15, { strokeColor: EX }));
}
add(text(760, y + 680, "Синяя вылезла за зелёную — перегрузка: стикер «Если ___ не успеет, то ___» в зону 1.", 18, { ...L, strokeColor: "#c92a2a" }));

// ── 5. Есть / взять / купить ──
place();
y = 0;
zone(y, 700, "5. Есть / взять / купить",
  "Что нужно пакетам: материалы, оборудование, доступ. Раскладывайте стикеры по столбцам. «Пока не знаем» — тоже риск, в зону 1.");
[["Есть у команды", GREEN, "паяльник,\nмакетная плата"], ["Взять (кафедра, лаборатория, друзья)", BLUE, "контрольный\nвлагомер — кафедра"],
  ["Купить", YELLOW, "два датчика,\nплата, провода"]].forEach(([t, c, e], j) => {
  const x = 30 + j * 535;
  add(rect(x, y + 130, 510, 540, { backgroundColor: "#ffffff", strokeColor: "#ced4da", ...L }));
  add(text(x + 20, y + 145, t, 24, { ...L, strokeColor: "#1971c2" }));
  for (let k = 0; k < 6; k++) add(sticker(x + 20 + (k % 2) * 245, y + 200 + Math.floor(k / 2) * 150, " ",
    { backgroundColor: c, strokeColor: "#868e96", ...(k === 0 ? { label: ex(e), tc: EX, size: 15 } : {}) }));
});
add(text(30 + 2 * 535 + 20, y + 640, "Сумма покупок ____ ₽ ≤ лимит из паспорта ____ ₽", 18, { ...L, strokeColor: "#c92a2a" }));

// ── 6. Пазл сборки плана ──
place();
y = 0;
zone(y, 760, "6. Пазл: план собран, когда все стыки сходятся",
  "Поставьте ✓ на стыке, когда проверка выполнена. Хотя бы один пустой — план ещё не собран.");
const P = [["WBS\nиерархическая структура работ", 260, y + 150], ["Диаграмма Ганта", 900, y + 150],
  ["Риски\nполе и ответы", 260, y + 470], ["Кошелёк часов\nи покупки", 900, y + 470]];
P.forEach(([t, x, py]) => add(rect(x, py, 480, 230, { backgroundColor: BLUE, strokeColor: "#1971c2", strokeWidth: 2, label: t, size: 26, valign: "top", ...L })));
const J = [[600, y + 245, "☐ каждый пакет есть на диаграмме"], [345, y + 405, "☐ красный ответ стал пакетом\n    или сдвигом на диаграмме"],
  [1000, y + 405, "☐ часы пакетов влезают\n    в кошельки"], [600, y + 565, "☐ «купить» влезает в лимит паспорта"]];
J.forEach(([x, jy, t]) => add(rect(x, jy, 470, 70, { backgroundColor: "#ffffff", strokeColor: "#f08c00", strokeWidth: 2, label: t, size: 18, align: "left" })));

place();
const scene = { type: "excalidraw", version: 2, source: "https://excalidraw.com",
  elements: els, appState: { viewBackgroundColor: "#ffffff", gridSize: null }, files: {} };
const out = process.argv[2] || "zanyatiya/Zanyatie_08_Doska.excalidraw";
fs.writeFileSync(out, JSON.stringify(scene));
console.log("OK", out, els.length, "элементов");
