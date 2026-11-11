// Работа с ЖИВОЙ комнатой Excalidraw (в которой, возможно, уже работают студенты).
//   node tools/excalidraw/live.js read  <url> <out.json>              — снять сцену (все элементы, включая удалённые) + сводка по зонам
//   node tools/excalidraw/live.js shot  <url> <out.png>               — снимок всей доски (Shift+1)
//   node tools/excalidraw/live.js zones <url> <scene.excalidraw> <z,z> — заменить зоны z на зоны из свежей сцены
// Как устроено: в браузере находим экземпляр App через React fiber и зовём app.updateScene — изменения
// уходят в комнату как от обычного участника. Правила (уроки 31.10):
//   • перед заменой — `read` и убедиться, что студенты не трогали заменяемые зоны (сравнить со свежей пустой доской);
//   • у новых элементов id с префиксом занятия (scene.js setPrefix) — иначе совпавший id затрёт чужой элемент;
//   • после updateScene ждать ≥ 45 с: сохранение на сервер идёт с задержкой, при раннем закрытии правка теряется;
//   • затем снова `read` в чистом браузере и сверить: вне заменённых зон ничего не пропало.
const { chromium } = require("playwright");
const fs = require("fs");
const [cmd, url, a3, a4] = process.argv.slice(2);
const findApp = () => {
  const root = document.querySelector(".excalidraw");
  const k = Object.keys(root).find((k) => k.startsWith("__reactFiber"));
  let f = root[k];
  while (f) { if (f.stateNode && typeof f.stateNode.updateScene === "function" && f.stateNode.scene) return f.stateNode; f = f.return; }
  return null;
};
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1600, height: 1000 } })).newPage();
  await p.goto(url, { waitUntil: "load", timeout: 60000 });
  await p.waitForTimeout(10000);
  if (cmd === "shot") {
    await p.mouse.click(800, 500); await p.keyboard.press("Shift+1"); await p.waitForTimeout(2000);
    await p.screenshot({ path: a3 }); console.log("OK", a3);
  } else if (cmd === "read") {
    const els = await p.evaluate(`(${findApp})().scene.getElementsIncludingDeleted()`);
    fs.writeFileSync(a3, JSON.stringify(els));
    const z = {};
    for (const e of els) if (!e.isDeleted) { const n = (e.customData && e.customData.zone) || "без зоны"; z[n] = (z[n] || 0) + 1; }
    console.log("элементов", els.length, "живых по зонам", JSON.stringify(z));
  } else if (cmd === "zones") {
    const want = a4.split(",").map(Number);
    const fresh = JSON.parse(fs.readFileSync(a3, "utf8")).elements.filter((e) => e.customData && want.includes(e.customData.zone));
    const r = await p.evaluate(({ src, fresh, want }) => {
      const app = eval(`(${src})`)();
      const cur = app.scene.getElementsIncludingDeleted();
      const ids = new Set(cur.map((e) => e.id));
      const clash = fresh.filter((e) => ids.has(e.id)).map((e) => e.id);
      if (clash.length) return { error: "совпадают id — задайте префикс в генераторе (setPrefix)", clash: clash.slice(0, 5) };
      const now = Date.now();
      const next = cur.map((e) => (!e.isDeleted && e.customData && want.includes(e.customData.zone))
        ? { ...e, isDeleted: true, version: e.version + 1, versionNonce: Math.floor(Math.random() * 1e9), updated: now } : e);
      app.updateScene({ elements: [...next, ...fresh.map((e) => ({ ...e, version: 2, updated: now, index: null }))], captureUpdate: "IMMEDIATELY" });
      return { deleted: next.filter((e, i) => e.isDeleted && !cur[i].isDeleted).length, added: fresh.length };
    }, { src: findApp.toString(), fresh, want });
    console.log(JSON.stringify(r));
    if (!r.error) await p.waitForTimeout(45000);
  } else console.log("команды: read | shot | zones");
  await b.close();
})();
