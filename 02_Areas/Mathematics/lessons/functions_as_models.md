---
subject: mathematics
lesson_id: mathematics.functions_as_models
level: foundations
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Функции как модели / Functions as Models

## Русский

### Цель

По контексту определить вход и выход, записать простую функцию и понять её график, область определения и множество значений.

### Идея и механизм

Функция похожа на автомат с напитками: нажимаешь кнопку (вход) — получаешь ровно один напиток (выход). Если одна и та же кнопка иногда выдаёт чай, а иногда кофе, это уже не функция. Математически функция — правило, которое каждому допустимому входу ставит в соответствие **ровно один** выход. Допустимые входы образуют область определения, возможные выходы — множество значений. Одно и то же правило можно показать словами, таблицей, формулой или графиком.

Пусть поездка на такси стоит 2 условные денежные единицы за подачу машины (начальная плата) и ещё 3 за каждый километр. Если `k` — километры, а `C` — стоимость, то `C(k) = 2 + 3k`. Число 2 — начальное значение, а коэффициент 3 — наклон: на столько растёт стоимость с каждым километром.

**Пример.** При `k = 4`: `C(4) = 2 + 3 · 4 = 14`. В виде таблицы: `k = 0, 1, 2, 3` → `C = 2, 5, 8, 11`; каждый шаг по `k` добавляет 3. Расстояние не бывает отрицательным, поэтому область модели — `k ≥ 0`, а стоимость не меньше 2. Графиком модели служит не вся прямая, а луч, который начинается в точке `(0, 2)` и идёт вправо.

**Типичная ошибка.** Путать запись `C(4)` с умножением `C · 4`. Скобки здесь означают «подставь 4 вместо `k`», а не «умножь на 4».

**Зачем это дальше.** В Python функция пишется почти так же: `def cost(k): return 2 + 3 * k`, и `cost(4)` вернёт `14`. В физике формулы движения — функции времени, а модель машинного обучения — это функция, которая по входным признакам возвращает предсказание.

### Исследуй и потренируйся

На интерактивном графике меняй начальное значение `b` и наклон `m` в формуле `y = mx + b`. Сначала предскажи, куда сдвинется прямая, затем проверь. Для каждой выбранной точки подставь `x` в формулу и сравни вычисление с координатой на графике.

Задача: для модели `y = 2x − 1` найди выход при `x = 3`. **Подсказка:** сначала умножь `x` на коэффициент, потом прибавь начальное значение `−1`. Ответ: `5`.

### Вопрос

По модели `C(k) = 2 + 3k`, сколько стоит поездка на 4 км?

### Варианты

- 12
- 14
- 20

### Ответ

2

### Разбор

`C(4) = 2 + 3 · 4 = 14`. Число 12 пропускает начальную плату, а 20 получается, если умножить на 4 всё выражение: `4 · (2 + 3)`.

### Границы модели

Линейная модель предполагает неизменную цену за километр и не учитывает пробки, ожидание, налоги и минимальную стоимость поездки. Функция описывает выбранные допущения, а не гарантирует, что реальная система всегда им следует. Не подставляй входы вне разумной области контекста.

## English

### Goal

Identify an input and an output in a short context, write a simple function, and interpret its graph, domain, and range.

### Idea and mechanism

A function is like a vending machine: press a button (input) and you get exactly one drink (output). If the same button sometimes gives tea and sometimes coffee, it is not a function. Mathematically, a function is a rule that assigns **exactly one** output to each allowed input. The allowed inputs form the domain, and the possible outputs form the range. The same rule can be shown in words, a table, a formula, or a graph.

Suppose a taxi ride costs 2 currency units to start (the starting charge) plus 3 units per kilometre. Let `k` be distance in kilometres and `C` the fare: `C(k) = 2 + 3k`. The 2 is the starting value, and the coefficient 3 is the slope: how much the fare rises for each kilometre.

**Example.** For `k = 4`, `C(4) = 2 + 3 · 4 = 14`. As a table: `k = 0, 1, 2, 3` → `C = 2, 5, 8, 11`; each step in `k` adds 3. Distance cannot be negative, so the model domain is `k ≥ 0` and the fare is at least 2. The model's graph is not the whole line but a ray starting at `(0, 2)` and going to the right.

**Common mistake.** Treating `C(4)` as the product `C · 4`. Here the parentheses mean “substitute 4 for `k`”, not “multiply by 4”.

**Why it matters next.** In Python a function looks almost the same: `def cost(k): return 2 + 3 * k`, and `cost(4)` returns `14`. In physics, equations of motion are functions of time, and a machine-learning model is a function that maps input features to a prediction.

### Explore and practise

On an interactive graph, change the starting value `b` and slope `m` in `y = mx + b`. Predict how the line moves, then check. For a point on the graph, substitute `x` into the formula and compare your result with the plotted coordinate.

Try `y = 2x − 1` at `x = 3`. **Hint:** multiply `x` by its coefficient, then add the starting value `−1`. Answer: `5`.

### Question

Using `C(k) = 2 + 3k`, what does a 4 km ride cost?

### Options

- 12
- 14
- 20

### Answer

2

### Explanation

`C(4) = 2 + 3 · 4 = 14`. The answer 12 misses the starting charge; 20 comes from multiplying the whole expression by 4: `4 · (2 + 3)`.

### Limits

The linear model assumes a constant price per kilometre and ignores traffic, waiting time, taxes, and minimum fares. A function describes chosen assumptions; it does not guarantee that a real system always follows them. Do not use inputs outside the context's sensible domain.

## Sources

- OpenStax, *Algebra and Trigonometry 2e*, [3.1 Functions and Function Notation](https://openstax.org/books/algebra-and-trigonometry-2e/pages/3-1-functions-and-function-notation) — a function assigns exactly one output to each input; representations.
- OpenStax, *Algebra and Trigonometry 2e*, [3.2 Domain and Range](https://openstax.org/books/algebra-and-trigonometry-2e/pages/3-2-domain-and-range) — domain and range, including restrictions from context.
- OpenStax, *College Algebra 2e*, [4.1 Linear Functions](https://openstax.org/books/college-algebra-2e/pages/4-1-linear-functions) — initial value and constant rate of change.

OpenStax books are licensed CC BY-NC-SA 4.0. This lesson is written in original wording and does not copy textbook text or figures.
