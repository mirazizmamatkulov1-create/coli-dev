---
subject: mathematics
lesson_id: mathematics.quadratic_functions_and_transformations
level: intermediate
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Квадратичные функции и преобразования графика / Quadratic Functions and Graph Transformations

## Русский

### Цель

Записывать квадратичную функцию в вершинной форме, находить вершину и объяснять, как параметры сдвигают и растягивают график.

### Идея и механизм

Брошенный вверх мяч поднимается, на мгновение замирает в верхней точке и падает обратно; если пренебречь сопротивлением воздуха, его высота от времени описывается параболой. Самая важная точка параболы — **вершина**: там функция достигает наименьшего или наибольшего значения, и график симметричен относительно вертикальной прямой через неё.

Вершинная форма квадратичной функции: `f(x) = a(x − h)² + k`, где `a ≠ 0`. Вершина — точка `(h, k)`, ось симметрии — прямая `x = h`. Параметры отвечают за разные изменения графика `y = x²`:

- `h` сдвигает график вправо (при `h > 0`) или влево (при `h < 0`). Знак в скобках противоположен направлению сдвига: `x − 3` ставит вершину в `x = 3`, а `x + 3` — в `x = −3`, потому что `x + 3 = x − (−3)`.
- `k` сдвигает график вверх или вниз.
- Если `a > 0`, ветви направлены вверх и вершина — минимум; если `a < 0`, ветви направлены вниз и вершина — максимум. При `|a| > 1` график вытянут по вертикали и выглядит уже, чем `y = x²`; при `0 < |a| < 1` — сжат и выглядит шире.

Если функция дана в виде `f(x) = ax² + bx + c`, координата вершины по горизонтали равна `h = −b/(2a)`, а `k = f(h)`.

**Пример.** `f(x) = 2(x − 1)² − 8` имеет вершину `(1, −8)` и ось `x = 1`. Раскрыв скобки, получим `2x² − 4x − 6`, и `−b/(2a) = 4/4 = 1` — та же вершина. Нули функции находим из `2(x − 1)² − 8 = 0`: `(x − 1)² = 4`, значит `x − 1 = ±2`, то есть `x = −1` или `x = 3`. Они симметричны относительно оси `x = 1`. При `x = 0` значение равно `−6`.

**Типичная ошибка.** Читать знак `h` «как написано»: в `(x + 2)²` вершина находится при `x = −2`, а не при `x = 2`. Ещё одна ловушка — терминология: в учебнике OpenStax вершинная форма `a(x − h)² + k` называется *standard form*, а `ax² + bx + c` — *general form*. В других учебниках названия могут отличаться, поэтому опирайся на саму формулу, а не на её название.

**Зачем это дальше.** В физике высота тела при постоянном ускорении — квадратичная функция времени. В машинном обучении квадратичная функция потерь `(y − ŷ)²` имеет ровно одну вершину-минимум, поэтому её удобно минимизировать; градиентный спуск движется к этой вершине.

### Исследуй и потренируйся

Сначала предскажи ответ в тренажёре: если `h` увеличивается с `−1` до `2`, куда перемещается вершина? После ответа меняй `a`, `h` и `k` по отдельности. Для каждого изменения назови, что должно произойти, до того как сравнить прогноз с графиком. Проверь формулу для одного значения `x` подстановкой, а нули — решением уравнения `f(x) = 0`.

### Вопрос

Для `f(x) = −0,5(x + 2)² + 3` укажи вершину и направление ветвей.

### Варианты

- `(−2, 3)`, ветви вверх
- `(−2, 3)`, ветви вниз
- `(2, 3)`, ветви вниз

### Ответ

2

### Разбор

Так как `x + 2 = x − (−2)`, горизонтальная координата вершины равна `−2`, а вертикальная — `3`. Коэффициент `a = −0,5` отрицательный, поэтому ветви направлены вниз и вершина — максимум; `|a| < 1`, значит график шире `y = x²`. Вариант `(2, 3)` — типичная ошибка со знаком `h`.

### Границы модели

Здесь рассматриваются вещественные квадратичные функции с вертикальной осью симметрии и `a ≠ 0`. Окно тренажёра ограничено диапазонами `x` и `y`; обрезанные края графика не ограничивают область определения функции. Модель не показывает повёрнутые параболы, шум измерений и сопротивление воздуха в реальном броске.

## English

### Goal

Write a quadratic function in vertex form, find its vertex, and explain how its parameters shift and stretch the graph.

### Idea and mechanism

A ball thrown upward rises, pauses for an instant at the top, and falls back; if air resistance is ignored, its height over time follows a parabola. The key point of a parabola is its **vertex**: there the function reaches its smallest or largest value, and the graph is symmetric about the vertical line through it.

The vertex form of a quadratic function is `f(x) = a(x − h)² + k`, where `a ≠ 0`. The vertex is `(h, k)`, and the axis of symmetry is `x = h`. Each parameter changes the graph of `y = x²` in its own way:

- `h` shifts the graph right (when `h > 0`) or left (when `h < 0`). The sign inside the parentheses is opposite to the shift: `x − 3` puts the vertex at `x = 3`, while `x + 3` puts it at `x = −3`, because `x + 3 = x − (−3)`.
- `k` shifts the graph up or down.
- If `a > 0`, the graph opens upward and the vertex is a minimum; if `a < 0`, it opens downward and the vertex is a maximum. When `|a| > 1`, the graph is stretched vertically and looks narrower than `y = x²`; when `0 < |a| < 1`, it is compressed and looks wider.

If the function is given as `f(x) = ax² + bx + c`, the vertex's horizontal coordinate is `h = −b/(2a)`, and `k = f(h)`.

**Example.** `f(x) = 2(x − 1)² − 8` has vertex `(1, −8)` and axis `x = 1`. Expanding gives `2x² − 4x − 6`, and `−b/(2a) = 4/4 = 1`: the same vertex. Find the zeros from `2(x − 1)² − 8 = 0`: `(x − 1)² = 4`, so `x − 1 = ±2`, giving `x = −1` or `x = 3`. They are symmetric about the axis `x = 1`. At `x = 0`, the value is `−6`.

**Common mistake.** Taking the sign of `h` “as written”: in `(x + 2)²` the vertex is at `x = −2`, not `x = 2`. Terminology is another trap: OpenStax calls the vertex form `a(x − h)² + k` the *standard form* and `ax² + bx + c` the *general form*. Other textbooks may use different names, so rely on the formula itself rather than its label.

**Why it matters next.** In physics, the height of an object under constant acceleration is a quadratic function of time. In machine learning, the squared loss `(y − ŷ)²` has exactly one vertex, a minimum, which makes it convenient to minimize; gradient descent moves toward that vertex.

### Explore and practise

Predict first in the lab: if `h` increases from `−1` to `2`, where does the vertex move? After answering, change `a`, `h`, and `k` one at a time. For each change, state what should happen before comparing your prediction with the graph. Check one function value by substitution and check the zeros by solving `f(x) = 0`.

### Question

For `f(x) = −0.5(x + 2)² + 3`, identify the vertex and opening direction.

### Options

- `(−2, 3)`, opens upward
- `(−2, 3)`, opens downward
- `(2, 3)`, opens downward

### Answer

2

### Explanation

Since `x + 2 = x − (−2)`, the horizontal coordinate of the vertex is `−2`, and the vertical coordinate is `3`. The coefficient `a = −0.5` is negative, so the graph opens downward and the vertex is a maximum; `|a| < 1`, so the graph is wider than `y = x²`. The option `(2, 3)` is the typical sign error with `h`.

### Limits

This lesson considers real quadratic functions with a vertical axis of symmetry and `a ≠ 0`. The lab window is limited to ranges of `x` and `y`; a clipped graph does not restrict the function's domain. The model does not show rotated parabolas, measurement noise, or air resistance in a real throw.

## Sources

- OpenStax, *Algebra and Trigonometry 2e*, [§5.1 Quadratic Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/5-1-quadratic-functions) — vertex, axis of symmetry, minimum/maximum, standard (vertex) and general forms, `h = −b/(2a)`, vertical stretch and compression.
- OpenStax, *College Physics 2e*, [§3.4 Projectile Motion](https://openstax.org/books/college-physics-2e/pages/3-4-projectile-motion) — vertical position under constant acceleration when air resistance is neglected.
- Google for Developers, *Machine Learning Crash Course*, [Linear regression: Loss](https://developers.google.com/machine-learning/crash-course/linear-regression/loss) — squared (L2) loss.

OpenStax books are licensed CC BY-NC-SA 4.0. This lesson is written in original wording and does not copy textbook text or figures.
