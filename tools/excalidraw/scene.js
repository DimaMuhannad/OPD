// Хелперы для сцен Excalidraw: прямоугольники, текст, стикеры с текстом внутри.
// Сцена — массив элементов; Excalidraw дополняет недостающие поля при загрузке.
let n = 0;
const uid = (p) => `${p}${++n}`;
const FONT = 6; // Nunito: есть кириллица
const base = (o) => ({
  angle: 0, strokeColor: "#1e1e1e", backgroundColor: "transparent", fillStyle: "solid",
  strokeWidth: 1, strokeStyle: "solid", roughness: 0, opacity: 100, groupIds: [], frameId: null,
  seed: Math.floor(Math.random() * 1e9), version: 1, versionNonce: Math.floor(Math.random() * 1e9),
  isDeleted: false, boundElements: null, updated: 1, link: null, locked: false, ...o,
});
const measure = (s, size) => {
  const lines = s.split("\n");
  return { w: Math.max(...lines.map((l) => l.length)) * size * 0.56, h: lines.length * size * 1.25 };
};
function text(x, y, s, size = 20, o = {}) {
  const m = measure(s, size);
  return [base({ id: uid("t"), type: "text", x, y, width: m.w, height: m.h, text: s, originalText: s,
    fontSize: size, fontFamily: FONT, textAlign: "left", verticalAlign: "top", containerId: null,
    lineHeight: 1.25, autoResize: true, ...o })];
}
function rect(x, y, w, h, o = {}) {
  const { label, size = 18, align = "center", valign = "middle", tc = "#1e1e1e", ...rest } = o;
  const r = base({ id: uid("r"), type: "rectangle", x, y, width: w, height: h, roundness: { type: 3 }, ...rest });
  if (!label) return [r];
  const m = measure(label, size);
  const ty = valign === "middle" ? y + (h - m.h) / 2 : y + 8;
  const t = base({ id: uid("t"), type: "text", x: x + 8, y: ty, width: w - 16, height: m.h, text: label,
    originalText: label, fontSize: size, fontFamily: FONT, textAlign: align, verticalAlign: valign,
    containerId: r.id, lineHeight: 1.25, autoResize: true, locked: rest.locked || false, strokeColor: tc });
  r.boundElements = [{ type: "text", id: t.id }];
  return [r, t];
}
const sticker = (x, y, label = "", o = {}) =>
  rect(x, y, 220, 120, { backgroundColor: "#fff3bf", strokeColor: "#f08c00", label: label || " ", size: 17, ...o });
module.exports = { text, rect, sticker };
