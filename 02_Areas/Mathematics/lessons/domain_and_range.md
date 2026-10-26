---
subject: mathematics
lesson_id: mathematics.domain_and_range
level: foundations
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Область определения и множество значений / Domain and Range

## Русский

### Цель

Для формулы находить допустимые вещественные входы, определять возможные выходы и записывать границы интервалами.

### Идея и механизм

У каждой функции есть «правила допуска». Калькулятор выдаст ошибку, если попросить его разделить на ноль или извлечь квадратный корень из отрицательного числа (в вещественных числах). Область определения отвечает на вопрос «какие входы разрешены?», а множество значений — «какие выходы правило действительно может дать?». Ограничения приходят из двух мест: из самой формулы и из смысла задачи.

Для формул чаще всего проверяют два запрета: знаменатель не может быть равен нулю, а под корнем чётной степени не может стоять отрицательное число.

**Пример.** Для вещественной функции `f(x) = √(8 − x)` подкоренное выражение должно быть неотрицательным: `8 − x ≥ 0`. Прибавим `x` к обеим частям: `8 ≥ x`, то есть `x ≤ 8`. Область определения — `(−∞, 8]`. Квадратный корень не бывает отрицательным: при `x = 8` выход равен `0`, а при уменьшении `x` он растёт без верхней границы, поэтому множество значений — `[0, ∞)`.

Контекст тоже ограничивает вход. Для поездки на такси расстояние не может быть отрицательным. Если рассматриваем только поездки до 4 км и цену `C(k) = 2 + 3k`, то `0 ≤ k ≤ 4`, а стоимость меняется от 2 до 14: `2 ≤ C ≤ 14`, или `[2, 14]`. Квадратная скобка означает, что граница включена; круглая — что не включена. У бесконечности скобка всегда круглая: `∞` — не число, его нельзя «достичь».

**Типичная ошибка.** Считать, что множество значений повторяет область определения. Для `y = x²` на `[−3, 3]` входы симметричны, а выходы лежат в `[0, 9]`: отрицательных значений нет вообще.

**Зачем это дальше.** В Python `math.sqrt(-1)` вызывает ошибку `ValueError`, а `1 / 0` — `ZeroDivisionError`: так программа сообщает о выходе за область определения. В машинном обучении логарифм в функции потерь определён только для положительных чисел, поэтому вероятности не должны быть равны нулю.

### Исследуй и потренируйся

В тренажёре переключай модели поездки, квадрата и корня, затем меняй N. Сверяй разрешённые входы и выходы с графиком. Для `y = x²` на `[−N, N]` проверь минимум в середине: область входа симметрична, но выходы начинаются с 0, а не с отрицательного числа.

Разбери `g(x) = 1/(x − 3)`: знаменатель не может быть нулём, поэтому `x ≠ 3`; значение 0 функция тоже не принимает, потому что дробь с числителем 1 не равна нулю. Всегда проверяй отдельно, что допускает формула, что допускает контекст и какие выходы действительно достигаются.

### Вопрос

Какова область определения `f(x) = √(8 − x)` среди вещественных чисел?

### Варианты

- x ≥ 8
- x ≤ 8
- Все вещественные x

### Ответ

2

### Разбор

Подкоренное выражение должно быть неотрицательным: `8 − x ≥ 0`, откуда `x ≤ 8`. В интервальной записи область определения — `(−∞, 8]`. Вариант `x ≥ 8` получается, если ошибиться с направлением неравенства: например, при `x = 9` под корнем `−1`. «Все вещественные `x`» не подходят по той же причине.

### Границы модели

Здесь рассматриваются вещественные входы и выходы; в комплексных числах правила для корней другие. Контекст может сделать математически допустимую формулу бессмысленной, а для сложной функции множество значений нельзя надёжно определить по одной формуле без анализа графика, знака, экстремумов или предельного поведения.

## English

### Goal

Find the allowed real inputs of a formula, determine its possible outputs, and express boundaries with interval notation.

### Idea and mechanism

Every function has “entry rules”. A calculator reports an error if you ask it to divide by zero or to take the square root of a negative number (over the real numbers). The domain answers “which inputs are allowed?” The range answers “which outputs can the rule actually produce?” Restrictions come from two places: the formula itself and the situation being modelled.

For formulas, the two most common checks are: a denominator cannot be zero, and an even root cannot contain a negative number.

**Example.** For the real-valued function `f(x) = √(8 − x)`, the radicand must be non-negative: `8 − x ≥ 0`. Add `x` to both sides: `8 ≥ x`, so `x ≤ 8`. The domain is `(−∞, 8]`. A square root is never negative: at `x = 8` the output is `0`, and as `x` decreases the output grows without an upper bound, so the range is `[0, ∞)`.

Context can restrict inputs too. A taxi distance cannot be negative. If we consider rides up to 4 km and the fare is `C(k) = 2 + 3k`, then `0 ≤ k ≤ 4` and the fare runs from 2 to 14: `2 ≤ C ≤ 14`, or `[2, 14]`. A square bracket means the endpoint is included; a parenthesis means it is excluded. Infinity always gets a parenthesis: `∞` is not a number and cannot be reached.

**Common mistake.** Assuming the range copies the domain. For `y = x²` on `[−3, 3]`, the inputs are symmetric, but the outputs lie in `[0, 9]`: there are no negative outputs at all.

**Why it matters next.** In Python, `math.sqrt(-1)` raises `ValueError` and `1 / 0` raises `ZeroDivisionError`: that is how a program reports an input outside the domain. In machine learning, the logarithm inside a loss function is defined only for positive numbers, so predicted probabilities must not be exactly zero.

### Explore and practise

In the interactive lab, switch between taxi, square, and square-root models, then change N. Compare allowed inputs and outputs with the graph. For `y = x²` on `[−N, N]`, check the minimum at the middle: the input domain is symmetric, but the outputs start at 0 rather than a negative value.

Consider `g(x) = 1/(x − 3)`: the denominator cannot be zero, so `x ≠ 3`; the function also never outputs 0, because a fraction with numerator 1 is never zero. Check separately what the formula allows, what the context allows, and which outputs are actually reached.

### Question

What is the domain of `f(x) = √(8 − x)` over the real numbers?

### Options

- x ≥ 8
- x ≤ 8
- Every real x

### Answer

2

### Explanation

The radicand must be non-negative: `8 − x ≥ 0`, so `x ≤ 8`. In interval notation, the domain is `(−∞, 8]`. The option `x ≥ 8` reverses the inequality: at `x = 9`, for example, the radicand is `−1`. “Every real `x`” fails for the same reason.

### Limits

This lesson uses real inputs and outputs; roots follow different rules over the complex numbers. Context can make a mathematically allowed formula meaningless, and a complex range cannot be determined reliably from the formula alone without checking its graph, sign, extrema, or limiting behaviour.

## Sources

- OpenStax, *Algebra and Trigonometry 2e*, [3.2 Domain and Range](https://openstax.org/books/algebra-and-trigonometry-2e/pages/3-2-domain-and-range) — restrictions from denominators and even roots, context restrictions, interval notation with brackets and parentheses.
- OpenStax, *College Algebra 2e*, [6.4 Graphs of Logarithmic Functions](https://openstax.org/books/college-algebra-2e/pages/6-4-graphs-of-logarithmic-functions) — the domain of a logarithm contains only positive real numbers.
- Python documentation, [`math` — Mathematical functions](https://docs.python.org/3/library/math.html) — `math.sqrt` raises `ValueError` for a negative input.
- Google for Developers, *Machine Learning Crash Course*, [Logistic regression: Loss and regularization](https://developers.google.com/machine-learning/crash-course/logistic-regression/loss-regularization) — Log Loss, a loss function built from logarithms of predicted probabilities.

OpenStax books are licensed CC BY-NC-SA 4.0. This lesson is written in original wording and does not copy textbook text or figures.
