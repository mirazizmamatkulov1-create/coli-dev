---
subject: mathematics
lesson_id: mathematics.geometry_area_perimeter
level: foundations
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Площадь и периметр фигур / Area and Perimeter of Shapes

## Русский

### Цель

Различать длину границы и площадь поверхности, вычислять обе величины для прямоугольника и прямоугольного треугольника, правильно указывать единицы.

### Идея и механизм

Представь комнату. Чтобы купить плинтус, нужно знать длину стен по краю пола — это **периметр**. Чтобы купить плитку, нужно знать, сколько квадратиков `1 м × 1 м` покроют пол, — это **площадь**. Периметр измеряется в метрах, площадь — в квадратных метрах: это разные величины, и одна не вычисляется из другой без знания формы.

Для прямоугольника с основанием `b` и высотой `h`: `P = 2b + 2h`, `A = bh`. Диагональ делит прямоугольник на два одинаковых треугольника, поэтому треугольник с основанием `b` и перпендикулярной к нему высотой `h` имеет площадь `A = bh/2`. У прямоугольного треугольника два катета (стороны при прямом угле) можно взять за основание и высоту, а гипотенузу находят по теореме Пифагора: `c = √(b² + h²)`; тогда `P = b + h + c`.

**Пример.** Прямоугольник `6 м × 4 м` имеет `A = 24 м²` и `P = 20 м`. Прямоугольный треугольник с катетами `6 м` и `4 м` имеет площадь `12 м²`, гипотенузу `√52 ≈ 7,21 м` и периметр примерно `17,21 м`.

**Типичная ошибка.** Терять единицы или путать их: `6 × 4 = 24` — это `24 м²`, а не `24 м`. Вторая частая ошибка — брать в формулу треугольника наклонную сторону вместо высоты: высота всегда перпендикулярна основанию.

**Зачем это дальше.** Площадь — простейший пример «накопления»: в анализе интеграл считает площадь под графиком, а в физике площадь под графиком скорости даёт смещение (при движении в одну сторону — пройденный путь). Масштабирование тоже важно: если увеличить все размеры в `k` раз, длины вырастут в `k` раз, а площади — в `k²` раз. В Python гипотенузу удобно считать функцией `math.hypot(b, h)`.

### Исследуй и потренируйся

Выбери прямоугольник или прямоугольный треугольник, затем меняй основание и высоту. Сравни площадь и периметр при изменении размеров. Предскажи, что произойдёт при удвоении обоих размеров, и проверь: площадь увеличится в четыре раза, а периметр — в два. Для одинаковых `b` и `h` площадь треугольника вдвое меньше площади прямоугольника; периметры так просто не сравниваются, потому что у фигур разные границы.

Задача для самопроверки: прямоугольный треугольник имеет катеты `9 м` и `12 м`. Найди площадь, гипотенузу и периметр. Ответ: `54 м²`, `15 м`, `36 м`.

### Вопрос

Прямоугольный треугольник имеет основание `8 м` и перпендикулярную высоту `5 м`. Какова его площадь?

### Варианты

- `20 м²`
- `40 м`
- `26 м²`

### Ответ

1

### Разбор

Площадь треугольника равна половине произведения основания на перпендикулярную высоту: `A = 8 · 5 / 2 = 20 м²`. Вариант `40 м` забывает деление на 2 и имеет единицу длины, а не площади. `26` — это периметр прямоугольника `8 м × 5 м` (`2 · 8 + 2 · 5`), к тому же с неверной единицей `м²`.

### Границы модели

Тренажёр работает только с прямоугольником и прямоугольным треугольником; у треугольника основание и высота являются перпендикулярными катетами. В тупоугольном треугольнике высота может падать за пределы фигуры, на продолжение основания, а третью сторону произвольного треугольника нельзя найти по двум сторонам без угла между ними. Значения в тренажёре показываются до сотых; знак `≈` отмечает округлённое число. Модель не охватывает окружности, составные фигуры, объём и погрешность измерения.

## English

### Goal

Distinguish boundary length from surface area, calculate both for a rectangle and a right triangle, and use the correct units.

### Idea and mechanism

Picture a room. To buy skirting board, you need the length around the edge of the floor: that is the **perimeter**. To buy floor tiles, you need how many `1 m × 1 m` squares cover the floor: that is the **area**. Perimeter is measured in metres and area in square metres; they are different quantities, and one cannot be found from the other without knowing the shape.

For a rectangle with base `b` and height `h`: `P = 2b + 2h` and `A = bh`. A diagonal cuts the rectangle into two identical triangles, so a triangle with base `b` and a height `h` perpendicular to it has area `A = bh/2`. In a right triangle, the two legs (the sides that form the right angle) can serve as base and height, and the hypotenuse comes from the Pythagorean theorem: `c = √(b² + h²)`; then `P = b + h + c`.

**Example.** A `6 m × 4 m` rectangle has `A = 24 m²` and `P = 20 m`. A right triangle with legs `6 m` and `4 m` has area `12 m²`, hypotenuse `√52 ≈ 7.21 m`, and perimeter about `17.21 m`.

**Common mistake.** Dropping or mixing units: `6 × 4 = 24` is `24 m²`, not `24 m`. Another frequent error is using a slanted side instead of the height in the triangle formula; the height is always perpendicular to the base.

**Why it matters next.** Area is the simplest example of accumulation: in calculus, an integral measures area under a graph, and in physics the area under a velocity graph gives the displacement (the distance travelled when motion stays in one direction). Scaling matters too: if every dimension grows by a factor `k`, lengths grow by `k` and areas by `k²`. In Python, `math.hypot(b, h)` computes the hypotenuse.

### Explore and practise

Choose a rectangle or right triangle, then change the base and height. Compare area and perimeter as the dimensions change. Predict what happens when both dimensions double, then check: area becomes four times larger and perimeter two times larger. With the same `b` and `h`, the triangle's area is half the rectangle's; their perimeters do not share that simple ratio because their boundaries differ.

Self-check task: a right triangle has legs `9 m` and `12 m`. Find its area, hypotenuse, and perimeter. Answer: `54 m²`, `15 m`, `36 m`.

### Question

A right triangle has base `8 m` and perpendicular height `5 m`. What is its area?

### Options

- `20 m²`
- `40 m`
- `26 m²`

### Answer

1

### Explanation

A triangle's area is half its base times its perpendicular height: `A = 8 · 5 / 2 = 20 m²`. The option `40 m` forgets to halve and uses a length unit instead of an area unit. `26` is the perimeter of an `8 m × 5 m` rectangle (`2 · 8 + 2 · 5`), and it is labelled with the wrong unit, `m²`.

### Limits

The lab covers only rectangles and right triangles; for the triangle, the base and height are perpendicular legs. In an obtuse triangle, the height can fall outside the shape, onto the extension of the base, and the third side of a general triangle cannot be found from two sides without the angle between them. The lab displays values to two decimal places; `≈` marks a rounded value. Circles, compound shapes, volume, and measurement uncertainty are outside this model.

## Sources

- OpenStax, *Prealgebra 2e*, [9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem](https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem) — right-triangle legs, hypotenuse, and the Pythagorean theorem.
- OpenStax, *Prealgebra 2e*, [9.4 Use Properties of Rectangles, Triangles, and Trapezoids](https://openstax.org/books/prealgebra-2e/pages/9-4-use-properties-of-rectangles-triangles-and-trapezoids) — perimeter versus area, square units, rectangle formulas, triangle area as half a rectangle, perpendicular height.
- OpenStax, *Calculus Volume 1*, [5.4 Integration Formulas and the Net Change Theorem](https://openstax.org/books/calculus-volume-1/pages/5-4-integration-formulas-and-the-net-change-theorem) — integrating velocity gives net displacement; total distance uses the absolute value of velocity.
- Python documentation, [`math.hypot`](https://docs.python.org/3/library/math.html#math.hypot).

OpenStax books are licensed CC BY-NC-SA 4.0. This lesson is written in original wording and does not copy textbook text or figures.
