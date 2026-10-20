---
marp: true
theme: opd
paginate: true
size: 16:9
class: v2

---

<!-- _class: lead -->
<!-- _paginate: false -->

<img src="../../tools/marp/guap-brand/guap-logo-full.png" class="guap-logo-full" />

# ЗАНЯТИЕ 7 · ПЛАНИРОВАНИЕ

## Когда что делаем: зависимости, критический путь и диаграмма Ганта

*К концу пары у каждой команды будет диаграмма Ганта своего проекта и срок, сверенный с датой защиты*

24 октября 2026

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

<div class="roadmap-bar">До плана — 1 неделя · до чекпоинта (контрольной точки) — 4 недели · до защиты — 9 недель</div>

<div class="roadmap">
<div class="stop"><div class="d">26.09 · 03.10</div><div class="t">Тема зафиксирована</div><div class="r">Паспорт сдан</div><div class="pts">10 баллов</div></div>
<div class="stop here"><div class="d">31.10</div><div class="t">План собран</div><div class="r">WBS, Ганта, смета, риски</div><div class="pts">10 баллов</div></div>
<div class="stop"><div class="d">21.11</div><div class="t">Чекпоинт (контрольная точка)</div><div class="r">Промежуточный результат</div><div class="pts">10 баллов</div></div>
<div class="stop"><div class="d">26.12</div><div class="t">Питч-защита</div><div class="r">Результат, отчёт, защита</div><div class="pts">50 баллов</div></div>
</div>
<div class="tests">Два зачётных теста по 10 баллов: «Инициация» — написан, «Планирование и контроль» — 28.11. Итого 100 баллов</div>

<div class="grades">
<div><b>85–100</b>отлично</div>
<div><b>70–84</b>хорошо</div>
<div><b>55–69</b>удовлетворительно</div>
<div class="fail"><b>менее 55</b>не зачтено</div>
</div>
<div class="grades-note">Порог зачёта — 55 баллов. Всё, кроме защиты, даёт ровно 50: без защиты зачёта нет</div>

---

<!-- _class: v2 dark hook -->

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Найдите ошибку в графике

<p>Что не так с этим графиком умного горшка?</p>

<img src="../img/z07_hook.svg" class="fig" />

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Диаграмма Ганта

<div class="card dark">Диаграмма Ганта — столбчатая диаграмма расписания: каждая работа показана отрезком на шкале времени, длина отрезка равна длительности.</div>
<p class="src">PMBOK Guide, PMI</p>

<img src="../img/z07_place.svg" class="fig" />

<div class="note">Все оценки пакетов горшка в сумме дают 10 недель. Сколько займёт проект на самом деле, покажет порядок работ.</div>

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Зависимость между работами

<p>Работа ждёт другую, когда без её результата не начать.</p>

<img src="../img/z07_dep.svg" class="fig" />

<div class="note">Вопрос к каждому пакету: что должно быть готово, чтобы можно было начать? Записывайте только прямых предшественников.</div>

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Зависимости пакетов умного горшка

<p>Что должно быть готово до начала каждого пакета?</p>

<table class="contour">
<tr><th>Пакет</th><th class="w22">Недель</th><th class="w45">Зависит от</th></tr>
<tr><td>1.1 Компоненты куплены</td><td>1</td><td><span class="hint">например: ничего, можно начинать сразу</span></td></tr>
<tr><td>1.2 Схема собрана и проверена</td><td>1</td><td></td></tr>
<tr><td>1.3 Программа порога</td><td>1</td><td></td></tr>
<tr><td>1.4 Корпус с индикатором</td><td>1</td><td></td></tr>
<tr><td>2.1 Калибровка датчика</td><td>1</td><td></td></tr>
<tr><td>2.2 Десять циклов полива</td><td>2</td><td></td></tr>
<tr><td>3.1 Проба у владельцев растений</td><td>1</td><td></td></tr>
<tr><td>4.1 Отчёт · 4.2 Презентация и питч (защита)</td><td>1 · 1</td><td></td></tr>
</table>

<div class="stop-work">■ СТОП · 4 МИНУТЫ — зависимости горшка</div>

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Расстановка пакетов по неделям

<p>Пакет стартует после самого позднего предшественника.</p>

<img src="../img/z07_gantt1.svg" class="fig" />

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Критический путь

<div class="card dark">Критический путь — самая длинная по времени последовательность связанных работ от начала проекта до его окончания. Она определяет минимально возможный срок.</div>
<p class="src">PMBOK Guide, PMI</p>

<img src="../img/z07_gantt2.svg" class="fig" />

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Милстоуны (вехи)

<p>Милстоун (веха) — момент, когда виден результат. Длительности у него нет.</p>

<img src="../img/z07_gantt3.svg" class="fig" />

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Нагрузка по людям

<p>Диаграмма не знает, что технический эксперт один.</p>

<img src="../img/z07_people.svg" class="fig" />

<div class="note">Проверьте каждую неделю по каждому человеку: два параллельных пакета у одного участника на деле пойдут по очереди.</div>

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Рычаги при нехватке срока

<p>Если срок не помещается до защиты, у команды три рычага.</p>

| Рычаг | Что делаем | Чем платим |
|---|---|---|
| Содержание | Убираем или сокращаем пакет, записываем в границы | Меньше результата |
| Время | Пересматриваем оценку, только если узнали что-то новое | Риск, что оценка ошибочна |
| Ресурсы | Передаём пакет свободному участнику | Нагрузка на человека |

<div class="card dark">Это те же три вершины железного треугольника из вводной лекции. Сдвинули одну — пересчитайте остальные.</div>

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Буфер (резерв времени)

<p>Один буфер ставят в конце критического пути.</p>

<img src="../img/z07_buffer.svg" class="fig" />

<div class="note">Запас, заложенный в каждый пакет, расходуется раньше, чем нужен. Буфер в конце виден всем и расходуется осознанно.</div>

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Практика: диаграмма Ганта своего проекта

<div class="cols">
<div>
<ol>
<li><b>10 мин.</b> Для каждого пакета запишите зависимости</li>
<li><b>15 мин.</b> Расставьте пакеты по неделям, найдите критический путь и заштрихуйте его</li>
<li><b>10 мин.</b> Проверьте нагрузку по людям и отсчитайте срок назад от защиты</li>
</ol>
<div class="note">Берите WBS (иерархическую структуру работ) с оценками и ответственными. Бланк с сеткой недель или своя таблица — на ваш выбор.</div>
</div>
<img src="../img/z07_sheet.svg" class="fig" />
</div>

<div class="stop-work">■ СТОП · 35 МИНУТ — диаграмма Ганта на бланке</div>

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Проверка диаграммы соседней команды

<p>Четыре вопроса.</p>

1. Каждый пакет из WBS есть в диаграмме, и лишних нет?
2. У каждого зависимого пакета записан предшественник, и без него начать действительно нельзя?
3. Критический путь выделен, и его длина совпадает со сроком проекта?
4. Нет недель, в которых у одного человека два параллельных пакета?

<div class="card dark">Срок проекта сверьте с защитой: помещается с запасом, впритык или не помещается. Последние два случая требуют решения команды.</div>

<div class="stop-work">■ СТОП · 8 МИНУТ — обмен листами</div>

---

<img src="../../tools/marp/guap-brand/guap-logo-compact.png" class="guap-logo" />

# Домашнее задание: риски и потребности пакетов

<div class="cols">
<div>
<ul>
<li>Доведите диаграмму: поправьте по замечаниям соседей, впишите срок проекта и решение, если он не помещается до защиты</li>
<li>Для каждого пакета на критическом пути — одна фраза: <b>что может пойти не так</b></li>
<li>Для каждого пакета — что нужно, чтобы его сделать: часы участников и материалы</li>
</ul>
</div>
<img src="../img/z07_sheet.svg" class="fig" />
</div>
