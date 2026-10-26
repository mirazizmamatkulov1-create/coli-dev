---
subject: mathematics
lesson_id: mathematics.trigonometry_and_periodic_functions
level: intermediate
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Тригонометрия и периодические функции / Trigonometry and Periodic Functions

## Русский

### Цель

Связать угол с координатами точки на единичной окружности и с графиками синуса и косинуса; объяснить, почему обе функции повторяются через полный оборот.

### Идея и механизм

Представь кабинку колеса обозрения. Пока колесо вращается, кабинка то поднимается, то опускается, то уходит влево, то вправо — и после полного оборота всё повторяется. Синус и косинус — это и есть «высота» и «сдвиг вбок» точки, которая движется по окружности. Поэтому они описывают всё, что повторяется: колебания, волны, сезоны.

Единичная окружность имеет центр в начале координат и радиус 1. Угол θ отсчитывают от положительного направления оси `x`; положительные углы идут против часовой стрелки. Соответствующая точка `P` имеет координаты `(cos θ, sin θ)`: **косинус — координата `x`, синус — координата `y`**. Поэтому значения обеих функций всегда лежат в отрезке `[−1, 1]`. Знак легко прочитать по четверти: в I четверти обе координаты положительны, во II — `x < 0`, `y > 0`, в III — обе отрицательны, в IV — `x > 0`, `y < 0`.

После добавления полного оборота точка возвращается в то же положение, поэтому `sin(θ + 2π) = sin θ` и `cos(θ + 2π) = cos θ`: обе функции периодичны с периодом `2π`. Углы измеряют в радианах или градусах; полный оборот — это `2π` радиан, или `360°`, поэтому `π` радиан = `180°`.

**Пример.** При `θ = 7π/6 = 210°` точка проходит половину оборота (`180°`) и ещё `30°`, то есть оказывается в III четверти. Её координаты `(−√3/2, −1/2)`, поэтому `cos(7π/6) = −√3/2 ≈ −0,87` и `sin(7π/6) = −1/2`: обе функции отрицательны, а точка лежит ниже оси `x` и левее оси `y`.

**Типичная ошибка.** Путать, какая координата — синус, а какая — косинус, или подставлять градусы туда, где ожидаются радианы. На калькуляторе и в программах важно, в каком режиме задан угол.

**Зачем это дальше.** В Python `math.sin(x)` принимает угол **в радианах**: `math.sin(30)` — это синус 30 радиан (около `−0,988`), а синус `30°` — это `math.sin(math.radians(30)) ≈ 0,5`. В физике синус и косинус описывают колебания маятника и пружины и раскладывают векторы на компоненты, а в машинном обучении синусы и косинусы разных частот кодируют позицию слова в архитектуре Transformer.

### Исследуй и потренируйся

Перед движением ползунка предскажи знаки координат точки. Проверь значения при `0`, `π/2`, `π`, `3π/2` и `2π`; свяжи каждый результат с четвертью или осью. Затем двигай угол и сравни положение точки с вертикальной меткой на обоих графиках. Найди несколько разных углов, при которых обе координаты повторяются, и объясни, почему это происходит.

### Вопрос

При `θ = 5π/6` какой знак у `sin θ`?

### Варианты

- Отрицательный
- Нулевой
- Положительный

### Ответ

3

### Разбор

`5π/6 = 150°`, это между `90°` и `180°`, то есть II четверть. Точка находится выше горизонтальной оси, значит её координата `y` положительна. Синус — это координата `y`, поэтому `sin(5π/6) = 1/2 > 0`. Точка левее вертикальной оси, поэтому косинус здесь отрицателен (`−√3/2`): не путай знак синуса со знаком косинуса. Нулевым синус бывает только на горизонтальной оси, при `θ = 0, π, 2π, …`.

### Границы модели

Тренажёр показывает участок углов от `−2π` до `2π`; это окно визуализации, а не область определения функций — синус и косинус определены для любого вещественного угла. Ползунок меняет угол шагами по `5°`. График построен из вычисленных значений функций и является визуальной иллюстрацией, а не измерением физической системы. Округлённые подписи могут не показывать точное значение; математические равенства в уроке остаются точными.

## English

### Goal

Connect an angle to a point's coordinates on the unit circle and to the sine and cosine graphs; explain why both functions repeat after one full turn.

### Idea and mechanism

Picture a cabin on a Ferris wheel. As the wheel turns, the cabin rises and falls and swings left and right, and after one full turn everything repeats. Sine and cosine are exactly the “height” and the “sideways position” of a point moving around a circle. That is why they describe anything that repeats: oscillations, waves, seasons.

The unit circle is centred at the origin and has radius 1. An angle θ is measured from the positive `x` direction; positive angles turn counterclockwise. The corresponding point `P` has coordinates `(cos θ, sin θ)`: **cosine is the `x`-coordinate, sine is the `y`-coordinate**. So both functions always stay in `[−1, 1]`. Signs follow from the quadrant: in quadrant I both coordinates are positive; in II, `x < 0` and `y > 0`; in III both are negative; in IV, `x > 0` and `y < 0`.

After one more full turn, the point returns to the same position, so `sin(θ + 2π) = sin θ` and `cos(θ + 2π) = cos θ`: both functions are periodic with period `2π`. Angles can be measured in radians or degrees; a full turn is `2π` radians, or `360°`, so `π` radians = `180°`.

**Example.** At `θ = 7π/6 = 210°`, the point goes half a turn (`180°`) plus another `30°`, landing in quadrant III. Its coordinates are `(−√3/2, −1/2)`, so `cos(7π/6) = −√3/2 ≈ −0.87` and `sin(7π/6) = −1/2`: both are negative, and the point lies below the `x`-axis and left of the `y`-axis.

**Common mistake.** Mixing up which coordinate is sine and which is cosine, or entering degrees where radians are expected. On a calculator and in code, the angle mode matters.

**Why it matters next.** In Python, `math.sin(x)` takes the angle **in radians**: `math.sin(30)` is the sine of 30 radians (about `−0.988`), while the sine of `30°` is `math.sin(math.radians(30)) ≈ 0.5`. In physics, sine and cosine describe pendulum and spring oscillations and split vectors into components; in machine learning, sines and cosines of different frequencies encode word positions in the Transformer architecture.

### Explore and practise

Predict the signs of the point's coordinates before moving the slider. Check the values at `0`, `π/2`, `π`, `3π/2`, and `2π`; connect each result to its quadrant or axis. Then move the angle and compare the point with the vertical marker on both graphs. Find different angles at which both coordinates repeat, and explain why.

### Question

At `θ = 5π/6`, what is the sign of `sin θ`?

### Options

- Negative
- Zero
- Positive

### Answer

3

### Explanation

`5π/6 = 150°`, which is between `90°` and `180°`: quadrant II. The point is above the horizontal axis, so its `y`-coordinate is positive. Sine is the `y`-coordinate, so `sin(5π/6) = 1/2 > 0`. The point is left of the vertical axis, so cosine is negative there (`−√3/2`): do not confuse the sign of sine with the sign of cosine. Sine is zero only on the horizontal axis, at `θ = 0, π, 2π, …`.

### Limits

The activity displays angles from `−2π` to `2π`; this is the visualization window, not the functions' domain: sine and cosine are defined for every real angle. The slider moves in `5°` steps. The graph is drawn from computed function values and illustrates the mathematics; it does not measure a physical system. Rounded labels may not show exact values, while the mathematical equalities in the lesson remain exact.

## Sources

- Abramson, Jay. *Precalculus 2e*, OpenStax, 2021. §5.2, “Unit Circle: Sine and Cosine Functions” / «Единичная окружность: функции синуса и косинуса»: <https://openstax.org/books/precalculus-2e/pages/5-2-unit-circle-sine-and-cosine-functions> — unit-circle coordinates, quadrants, radian measure, the range `[−1, 1]`, calculator degree/radian modes.
- Abramson, Jay. *Precalculus 2e*, OpenStax, 2021. §6.1, “Graphs of the Sine and Cosine Functions” / «Графики функций синуса и косинуса»: <https://openstax.org/books/precalculus-2e/pages/6-1-graphs-of-the-sine-and-cosine-functions> — graph properties and the period `2π`.
- Python documentation, [`math.sin` and `math.radians`](https://docs.python.org/3/library/math.html) — `math.sin` returns the sine of `x` radians; `math.radians` converts degrees to radians.
- OpenStax, *College Physics 2e*, [§16.3 Simple Harmonic Motion: A Special Periodic Motion](https://openstax.org/books/college-physics-2e/pages/16-3-simple-harmonic-motion-a-special-periodic-motion) — simple harmonic motion is described by sine and cosine functions of time.
- OpenStax, *College Physics 2e*, [§3.3 Vector Addition and Subtraction: Analytical Methods](https://openstax.org/books/college-physics-2e/pages/3-3-vector-addition-and-subtraction-analytical-methods) — vector components `A_x = A cos θ`, `A_y = A sin θ`.
- Vaswani et al., [“Attention Is All You Need”](https://arxiv.org/abs/1706.03762), 2017, §3.5 — sinusoidal positional encodings in the Transformer.
- OpenStax licensing and attribution / лицензия и правила указания источника: <https://openstax.org/books/precalculus-2e/pages/preface>. The lesson paraphrases the mathematical facts and uses an original diagram; it does not copy OpenStax text or figures. OpenStax content is under CC BY-NC-SA 4.0, which does not grant unrestricted commercial reuse; check page-specific third-party rights before reusing any source material. / Урок пересказывает математические факты своими словами и использует самостоятельно созданную схему; текст и иллюстрации OpenStax не копируются. Материалы OpenStax доступны по CC BY-NC-SA 4.0, которая не разрешает неограниченное коммерческое повторное использование; перед заимствованием следует проверить права для конкретной страницы и сторонних материалов.
