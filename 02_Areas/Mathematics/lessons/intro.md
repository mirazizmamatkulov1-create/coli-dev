---
subject: mathematics
lesson_id: intro.mathematics
level: foundations
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Наклон как скорость изменения / Slope as Rate of Change

## Русский

### Цель

Понять, что показывает наклон линейной модели, и предсказывать изменение выхода при изменении входа.

### Идея и механизм

Наклон отвечает на вопрос: «на сколько меняется выход, когда вход растёт на одну единицу?» Если поездка стоит 3 доллара за каждый километр, то каждый следующий километр добавляет к цене ровно 3 доллара — неважно, первый это километр или десятый. Именно постоянная «цена одного шага» делает зависимость линейной.

В модели `y = mx + b` число `m` — наклон: при увеличении `x` на одну единицу `y` меняется на `m`, а при увеличении на `Δx` — на `Δy = m · Δx`. Число `b` — значение модели при `x = 0`, то есть точка, где прямая пересекает ось `y`. Если `m > 0`, функция возрастает; если `m < 0` — убывает; если `m = 0` — выход постоянен. Единицы наклона — единицы `y` на единицу `x`: например, «долларов за километр» или «метров в секунду».

**Пример.** В модели `y = −2x + 5` рост `x` на 3 меняет выход на `Δy = −2 · 3 = −6`, то есть `y` уменьшается на 6. Проверка подстановкой: при `x = 0` получаем `y = 5`, при `x = 3` — `y = −1`, и `−1 − 5 = −6`.

**Типичная ошибка.** Смешивать `b` и `m`. Начальное значение `b` поднимает или опускает всю прямую, но не меняет того, насколько изменится `y` при заданном шаге `x`.

**Зачем это дальше.** В физике наклон графика «положение — время» — это скорость. В Python модель записывается одной строкой `y = m * x + b`, а линейная регрессия в статистике и машинном обучении подбирает `m` и `b` так, чтобы прямая лучше всего проходила через данные. Наклон прямой — первый шаг к производной: она описывает скорость изменения и для кривых.

### Исследуй и потренируйся

Сначала предскажи изменение `y`, затем проверь его подстановкой в формулу. Меняй наклон, начальное значение и вход по отдельности; при каждом изменении назови, что должно произойти с прямой, и только потом смотри на график.

### Вопрос

В модели `y = 3x + 1` на сколько изменится `y`, если `x` увеличить на 2?

### Варианты

- 2
- 6
- 3

### Ответ

2

### Разбор

Изменение равно `m · Δx = 3 · 2 = 6`. Вариант 3 — это сам наклон (изменение на один шаг), а 2 — только шаг по `x`. Начальное значение `b = 1` влияет на сами значения `y`, но не на их изменение.

### Границы модели

Линейная модель предполагает постоянную скорость изменения. Реальные зависимости могут быть нелинейными, а смысл задачи может запрещать часть значений `x` (например, отрицательное расстояние). Не продолжай прямую за пределы обоснованного контекста без проверки.

## English

### Goal

Understand what the slope of a linear model represents and predict how the output changes when the input changes.

### Idea and mechanism

Slope answers one question: “by how much does the output change when the input grows by one unit?” If a ride costs 3 dollars for every kilometre, each extra kilometre adds exactly 3 dollars, whether it is the first kilometre or the tenth. That constant “price of one step” is what makes a relationship linear.

In `y = mx + b`, the number `m` is the slope: when `x` increases by one unit, `y` changes by `m`, and when `x` increases by `Δx`, `y` changes by `Δy = m · Δx`. The number `b` is the model's value at `x = 0`, where the line crosses the `y`-axis. If `m > 0`, the function is increasing; if `m < 0`, it is decreasing; if `m = 0`, the output is constant. Slope units are units of `y` per unit of `x`, such as “dollars per kilometre” or “metres per second”.

**Example.** In `y = −2x + 5`, increasing `x` by 3 changes the output by `Δy = −2 · 3 = −6`, so `y` drops by 6. Check by substitution: `x = 0` gives `y = 5`, `x = 3` gives `y = −1`, and `−1 − 5 = −6`.

**Common mistake.** Mixing up `b` and `m`. The starting value `b` raises or lowers the whole line, but it does not change how much `y` moves for a given step in `x`.

**Why it matters next.** In physics, the slope of a position–time graph is velocity. In Python the model is one line, `y = m * x + b`, and linear regression in statistics and machine learning chooses `m` and `b` so that the line fits the data best. The slope of a line is the first step toward the derivative, which describes the rate of change of curves as well.

### Explore and practise

Predict the change in `y` first, then check it by substitution. Change the slope, the starting value, and the input one at a time; before each change, say what should happen to the line, and only then look at the graph.

### Question

In `y = 3x + 1`, how much does `y` change when `x` increases by 2?

### Options

- 2
- 6
- 3

### Answer

2

### Explanation

The change is `m · Δx = 3 · 2 = 6`. The option 3 is the slope itself (the change for one step), and 2 is only the step in `x`. The starting value `b = 1` affects the values of `y`, not how much they change.

### Limits

A linear model assumes a constant rate of change. Real relationships may be nonlinear, and a problem's context may rule out some `x` values (a negative distance, for example). Do not extend the line beyond a justified context without checking.

## Sources

- OpenStax, *College Algebra 2e*, [§4.1 Linear Functions](https://openstax.org/books/college-algebra-2e/pages/4-1-linear-functions) — slope as a constant rate of change, initial value, increasing/decreasing/constant functions, slope units.
- OpenStax, *College Physics 2e*, [§2.8 Graphical Analysis of One-Dimensional Motion](https://openstax.org/books/college-physics-2e/pages/2-8-graphical-analysis-of-one-dimensional-motion) — the slope of a position–time graph is velocity.
- OpenStax, *Introductory Statistics 2e*, [§12.3 The Regression Equation](https://openstax.org/books/introductory-statistics-2e/pages/12-3-the-regression-equation) — the least-squares line chooses a slope and intercept that fit data.

OpenStax books are licensed CC BY-NC-SA 4.0. This lesson is written in original wording and does not copy textbook text or figures.
