// Печать HTML в PDF А5 через полифил Paged.js в установленном Chromium (Playwright).
// Запуск: NODE_PATH=/opt/stack/npm/node_modules node pechat_paged.js <in.html> <out.pdf>
const { chromium } = require("playwright-core");
const path = require("path");
const [inp, out] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({
    executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    args: ["--allow-file-access-from-files"], // Paged.js читает CSS через XHR
  });
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(inp));
  await page.evaluate(() => { window.PagedConfig = { auto: false }; });
  await page.addScriptTag({ path: path.join(path.dirname(require.resolve("playwright-core")), "..", "pagedjs", "dist", "paged.polyfill.js") });
  await page.evaluate(async () => { await window.PagedPolyfill.preview(); });
  const pages = await page.evaluate(() => document.querySelectorAll(".pagedjs_page").length);
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  console.log(`${out}: ${pages} стр.`);
  await browser.close();
})();
