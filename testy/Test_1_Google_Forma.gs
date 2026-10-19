// Тест 1 «Инициация проекта» для онлайн-пары м631к: две Google Формы-теста (варианты А и Б) и ведомость.
// Как запустить: script.google.com → «Новый проект» → вставить этот файл целиком → сохранить →
// выбрать функцию в списке сверху и нажать «Выполнить» (в первый раз Google попросит разрешения).
//   sozdat()   — создать обе формы (закрытыми) и таблицу-ведомость; ссылки — в «Журнале выполнения»
//   otkryt()   — открыть приём ответов; через 12 минут формы закроются сами
//   zakryt()   — закрыть приём ответов вручную
//   vedomost() — посчитать баллы всех ответов в таблицу (можно запускать сколько угодно раз)
// Вопросы и ключ — те же, что в бумажном тесте (tools/docx-konspekt/build_Test_1.js).

const MINUT = 12;
const GRUPPA = "м631к";

const MC = [
  { q: "Кафедра каждый семестр проводит одни и те же лабораторные работы по одной методичке. Это проект?",
    opts: ["Нет: результат каждый раз повторяется, это процесс", "Да: у работ есть срок — конец семестра", "Да: в работах участвует группа студентов", "Нет: у лабораторных работ нет бюджета"] },
  { q: "Какие три параметра связаны «железным треугольником» проекта?",
    opts: ["Содержание, время, стоимость", "Команда, бюджет, риски", "Цель, задачи, результат", "План, факт, отклонение"] },
  { q: "Команде нужен контрольный влагомер. Его нет, и пока неизвестно, где его взять. Как записать это в разделе паспорта «Ресурсы»?",
    opts: ["«Нет», клетку «где берём» оставить пустой: это риск проекта", "«Есть»: на кафедре он, скорее всего, найдётся", "Не записывать, пока влагомер не найдётся", "Убрать влагомер из списка и обойтись без него"] },
  { q: "С какой фазы начинается жизненный цикл проекта?",
    opts: ["Инициация", "Планирование", "Исполнение", "Контроль"] },
  { q: "Что описывает ценностное предложение?",
    opts: ["Для кого проект, какую выгоду он даёт и чем лучше текущего способа", "Как команда распределит работу между участниками", "Сколько денег и материалов потребует проект", "В какие сроки команда сделает результат"] },
  { q: "В строке «в отличие от чего» команда написала: «аналогов нет». Что это обычно значит?",
    opts: ["Текущий способ решения задачи не искали", "Проект уникален, это сильная сторона", "На идею нужно оформить патент", "Проект никому не нужен"] },
  { q: "Цель: «Провести эксперименты к концу семестра». Что с ней не так?",
    opts: ["Описан процесс, а не результат, и нет точной даты", "Не указан бюджет проекта", "Не названы исполнители", "Всё в порядке, цель поставлена"] },
  { q: "Что из перечисленного — результат проекта (deliverable)?",
    opts: ["Прототип горшка и протокол десяти циклов полива", "Растения у владельцев гибнут реже", "Команда научилась паять схемы", "Провести испытания прототипа"] },
  { q: "Что происходит после решения go / no-go?",
    opts: ["Тема проекта фиксируется, дальше уточняются только формулировки", "Команда выбирает между Waterfall и Agile", "Заказчик принимает готовый результат", "Команда защищает проект перед комиссией"] },
  { q: "Зачем в паспорте проекта записывают границы?",
    opts: ["Чтобы зафиксировать, что в проект не входит", "Чтобы распределить работу между участниками", "Чтобы сократить срок проекта", "Чтобы перечислить стейкхолдеров"] },
  { q: "Какой из признаков есть у любого проекта?",
    opts: ["Ограниченный срок: у проекта есть дата окончания", "Внешнее финансирование от фонда или компании", "Заказчик со стороны предприятия", "Команда не меньше пяти человек"] },
  { q: "Кто такой стейкхолдер (заинтересованная сторона) проекта?",
    opts: ["Любой, кто влияет на проект или кого затрагивает его результат", "Только заказчик, который оплачивает работу", "Только участники команды проекта", "Только будущие пользователи результата"] },
  { q: "Заведующий лабораторией может не пустить команду к прибору, но сам результат проекта его почти не касается. Как с ним работать по матрице «влияние × заинтересованность»?",
    opts: ["Удовлетворять: заранее согласовать то, что от него зависит", "Работать плотно: согласовывать с ним каждое решение", "Информировать: регулярно сообщать о ходе работ", "Наблюдать: не тратить на него усилий"] },
  { q: "Команда записала в стейкхолдеры только преподавателя. Кого чаще всего упускают?",
    opts: ["Пользователей и тех, от кого зависят ресурсы", "Конкурентов на рынке", "Родственников участников команды", "Никого: преподавателя достаточно"] },
];
const POS = { A: [1, 0, 2, 3, 0, 2, 1, 3, 0, 1, 2, 3, 1, 0], B: [3, 2, 0, 1, 2, 0, 3, 1, 2, 3, 0, 1, 3, 2] };
const ORDER = { A: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], B: [5, 2, 9, 0, 12, 7, 3, 10, 1, 13, 6, 4, 11, 8] };
const SMART_ROWS = [
  ["Есть конкретная дата, а не «в течение семестра»", "T"],
  ["Результат проверяется числом, а не словом «хорошо»", "M"],
  ["Задача выполнима силами 3–4 человек с доступными ресурсами", "A"],
  ["Цель решает проблему из ценностного предложения, а не соседнюю", "R"],
  ["Понятно, что именно должно получиться: образ результата, а не процесс", "S"],
];
const SMART_ORDER = { A: [0, 1, 2, 3, 4], B: [4, 2, 0, 3, 1] };
const IDEAS = ["личное наблюдение — «я сам с этим столкнулся»", "чужая жалоба", "жеребьёвка среди свободных тем кафедры", "технология в поиске применения", "внешний запрос: научный руководитель, предприятие, конкурс", "идея, увиденная в рекламе"];
const IDEAS_OK = [0, 1, 3, 4];
const IDEAS_ORDER = { A: [0, 1, 2, 3, 4, 5], B: [3, 5, 1, 4, 2, 0] };
const STEPS = ["Выявление проблемы или возможности", "Генерация альтернатив — минимум двух", "Формулировка ценностного предложения", "Постановка цели по SMART", "Решение go / no-go и фиксация темы"];
const STEPS_ORDER = { A: [2, 1, 4, 0, 3], B: [3, 0, 2, 4, 1] };
const OPEN = [
  { q: "Цель: «Сделать удобное приложение для студентов к концу семестра». Назовите три требования SMART, которые не выполнены, и объясните каждое одной строкой.", b: 3 },
  { q: "Запишите одну границу вашего проекта в форме отказа и укажите тип: чего не делаем / для кого не делаем / чего не гарантируем.", b: 2 },
  { q: "Запишите один критерий успеха вашего проекта так, чтобы его можно было проверить ответом «да» или «нет».", b: 2 },
];
const IMYA = { A: "А", B: "Б" };

function arrange(opts, pos) {
  const wrong = opts.slice(1);
  const out = [];
  for (let i = 0, w = 0; i < 4; i++) out.push(i === pos ? opts[0] : wrong[w++]);
  return out;
}

function sozdat() {
  const props = PropertiesService.getScriptProperties();
  const ss = SpreadsheetApp.create(`Тест 1 · ${GRUPPA} · ведомость`);
  props.setProperty("ss", ss.getId());
  for (const V of ["A", "B"]) {
    const form = FormApp.create(`Тест 1. Инициация проекта · вариант ${IMYA[V]} · ${GRUPPA}`);
    form.setIsQuiz(true)
      .setShuffleQuestions(true)
      .setProgressBar(false)
      .setShowLinkToRespondAgain(false)
      .setAllowResponseEdits(false)
      .setPublishingSummary(false)
      .setDescription(`${MINUT} минут · без конспектов · максимум 30 баллов · зачтено от 15.\n` +
        "Форма закроется сама через " + MINUT + " минут после начала: отправьте ответы до этого.")
      .setConfirmationMessage("Ответы приняты. Баллы преподаватель сообщит после проверки.")
      .setCustomClosedFormMessage("Сейчас форма закрыта: тест откроется по команде преподавателя.");
    const ids = { mc: [], smart: null, ideas: null, steps: null, open: [] };

    form.addTextItem().setTitle("Фамилия и имя").setRequired(true);
    form.addTextItem().setTitle("Команда (название или номер)").setRequired(true);

    form.addPageBreakItem().setTitle("Часть 1. Выберите один ответ · по 1 баллу");
    ORDER[V].forEach((qi) => {
      const it = form.addMultipleChoiceItem().setTitle(MC[qi].q).setRequired(true).setPoints(1);
      it.setChoices(arrange(MC[qi].opts, POS[V][qi]).map((o) => it.createChoice(o, o === MC[qi].opts[0])));
      ids.mc.push({ id: it.getId(), ok: MC[qi].opts[0] });
    });

    form.addPageBreakItem().setTitle("Часть 2. Соответствие, несколько ответов, порядок");
    const sm = form.addGridItem()
      .setTitle("Выберите для каждой проверки букву SMART. Каждая буква — один раз. (5 б)")
      .setRows(SMART_ORDER[V].map((i) => SMART_ROWS[i][0]))
      .setColumns(["S", "M", "A", "R", "T"])
      .setRequired(true);
    sm.setValidation(FormApp.createGridValidation().setHelpText("Каждая буква — только один раз.").requireLimitOneResponsePerColumn().build());
    ids.smart = { id: sm.getId(), ok: SMART_ORDER[V].map((i) => SMART_ROWS[i][1]) };

    const id = form.addCheckboxItem().setTitle("Отметьте ВСЕ источники идей для проекта, которые разбирались на курсе. (2 б)").setRequired(true);
    id.setChoices(IDEAS_ORDER[V].map((i) => id.createChoice(IDEAS[i])));
    ids.ideas = { id: id.getId(), ok: IDEAS_OK.map((i) => IDEAS[i]) };

    const st = form.addGridItem()
      .setTitle("Расставьте шаги фазы инициации по порядку: какой шаг первый, какой второй и так далее. (2 б)")
      .setRows(STEPS_ORDER[V].map((i) => STEPS[i]))
      .setColumns(["1", "2", "3", "4", "5"])
      .setRequired(true);
    st.setValidation(FormApp.createGridValidation().setHelpText("Каждый номер — только один раз.").requireLimitOneResponsePerColumn().build());
    ids.steps = { id: st.getId(), ok: STEPS_ORDER[V].map((i) => String(i + 1)) };

    form.addPageBreakItem().setTitle("Часть 3. Коротко письменно");
    OPEN.forEach((o) => {
      const it = form.addParagraphTextItem().setTitle(`${o.q} (${o.b} б)`).setRequired(true).setPoints(o.b);
      ids.open.push({ id: it.getId(), b: o.b });
    });

    form.setAcceptingResponses(false);
    props.setProperty("form" + V, form.getId());
    props.setProperty("ids" + V, JSON.stringify(ids));
    Logger.log(`Вариант ${IMYA[V]} — ссылка для студентов: ${form.getPublishedUrl()}`);
    Logger.log(`Вариант ${IMYA[V]} — редактирование: ${form.getEditUrl()}`);
  }
  Logger.log(`Ведомость: ${ss.getUrl()}`);
}

function forms_() {
  const props = PropertiesService.getScriptProperties();
  return ["A", "B"].map((V) => ({ V, form: FormApp.openById(props.getProperty("form" + V)), ids: JSON.parse(props.getProperty("ids" + V)) }));
}

function otkryt() {
  forms_().forEach(({ form }) => form.setAcceptingResponses(true));
  ScriptApp.getProjectTriggers().filter((t) => t.getHandlerFunction() === "zakryt").forEach((t) => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger("zakryt").timeBased().after(MINUT * 60 * 1000).create();
  Logger.log(`Формы открыты, закроются примерно через ${MINUT} мин (Google запускает таймер с точностью до минуты).`);
}

function zakryt() {
  forms_().forEach(({ form }) => form.setAcceptingResponses(false));
  Logger.log("Формы закрыты.");
}

// 16: ровно нужные пункты — 2; одна ошибка (лишний или пропущенный) — 1; иначе 0.
function ballIdei_(got, ok) {
  const err = got.filter((x) => !ok.includes(x)).length + ok.filter((x) => !got.includes(x)).length;
  return err === 0 ? 2 : err === 1 ? 1 : 0;
}

// 17: всё верно — 2; переставлены местами два соседних шага — 1; иначе 0.
function ballShagi_(got, ok) {
  const bad = ok.map((v, i) => (got[i] === v ? -1 : i)).filter((i) => i >= 0);
  if (bad.length === 0) return 2;
  if (bad.length !== 2) return 0;
  const [i, j] = bad;
  return got[i] === ok[j] && got[j] === ok[i] && Math.abs(Number(ok[i]) - Number(ok[j])) === 1 ? 1 : 0;
}

function vedomost() {
  const ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty("ss"));
  const sh = ss.getSheets()[0].setName("Ведомость");
  const head = ["Вариант", "Отправлено", "Фамилия и имя", "Команда", "Ч. 1 (14)", "15 SMART (5)", "16 идеи (2)", "17 шаги (2)",
    "18 (3)", "19 (2)", "20 (2)", "Итого (30)", "Зачтено", "В БРС (÷3)", "Ответ 18", "Ответ 19", "Ответ 20"];
  const rows = [];
  for (const { V, form, ids } of forms_()) {
    for (const r of form.getResponses()) {
      const by = {};
      r.getItemResponses().forEach((ir) => { by[ir.getItem().getId()] = ir.getResponse(); });
      const score = {};
      r.getGradableItemResponses().forEach((g) => { score[g.getItem().getId()] = g.getScore(); });
      const text = r.getItemResponses().slice(0, 2).map((ir) => ir.getResponse());
      const ch1 = ids.mc.filter((m) => by[m.id] === m.ok).length;
      const smart = (by[ids.smart.id] || []).filter((x, i) => x === ids.smart.ok[i]).length;
      const idei = ballIdei_(by[ids.ideas.id] || [], ids.ideas.ok);
      const shagi = ballShagi_(by[ids.steps.id] || [], ids.steps.ok);
      const open = ids.open.map((o) => Number(score[o.id]) || 0);
      const total = ch1 + smart + idei + shagi + open.reduce((a, b) => a + b, 0);
      rows.push([IMYA[V], r.getTimestamp(), text[0], text[1], ch1, smart, idei, shagi, ...open, total,
        total >= 15 ? "да" : "нет", Math.round((total / 3) * 10) / 10, ...ids.open.map((o) => by[o.id] || "")]);
    }
  }
  rows.sort((a, b) => String(a[2]).localeCompare(String(b[2]), "ru"));
  sh.clear();
  sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight("bold");
  if (rows.length) sh.getRange(2, 1, rows.length, head.length).setValues(rows);
  sh.setFrozenRows(1);
  Logger.log(`Посчитано ответов: ${rows.length}. ${ss.getUrl()}`);
}
