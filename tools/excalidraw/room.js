// Загружает сцену .excalidraw в excalidraw.com и (с --room) открывает комнату совместной работы.
// Комната хранится на сервере Excalidraw: ссылка работает и после выхода, регистрация не нужна.
//   node tools/excalidraw/room.js <сцена.excalidraw> <папка-для-PNG> [--room]
// Печатает ссылку на комнату; PNG — вид целиком (Shift+1) для проверки глазами.
// С --zones дополнительно снимает каждую зону отдельно (элементы с customData.zone = N).
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const [scenePath, outDir] = process.argv.slice(2);
const makeRoom = process.argv.includes("--room");
const byZones = process.argv.includes("--zones");

async function show(p, elements, png) {
  await p.evaluate((e) => {
    localStorage.setItem("excalidraw", JSON.stringify(e));
    localStorage.setItem("excalidraw-state", JSON.stringify({ viewBackgroundColor: "#ffffff" }));
  }, elements);
  await p.reload({ waitUntil: "load" });
  await p.waitForTimeout(3500);
  await p.mouse.click(5, 500);
  await p.keyboard.press("Shift+1");
  await p.waitForTimeout(1200);
  await p.screenshot({ path: png });
}

(async () => {
  const scene = JSON.parse(fs.readFileSync(scenePath, "utf8"));
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch({ executablePath: EXE });
  const p = await (await b.newContext({ viewport: { width: 1600, height: 1000 } })).newPage();
  await p.goto("https://excalidraw.com", { waitUntil: "load", timeout: 60000 });
  await p.waitForTimeout(3000);
  if (byZones) {
    const zones = [...new Set(scene.elements.map((e) => e.customData && e.customData.zone).filter(Boolean))];
    for (const z of zones) await show(p, scene.elements.filter((e) => e.customData && e.customData.zone === z), path.join(outDir, `zone${z}.png`));
  }
  await show(p, scene.elements, path.join(outDir, "whole.png"));
  if (makeRoom) {
    await p.getByRole("button", { name: /Live collaboration|Share/ }).first().click();
    await p.waitForTimeout(1500);
    await p.getByText("Start session").click();
    await p.waitForTimeout(15000); // дать сцене сохраниться на сервере
    console.log("ROOM", p.url());
  }
  await b.close();
})().catch((e) => { console.error("ERR", e.message); process.exit(1); });
