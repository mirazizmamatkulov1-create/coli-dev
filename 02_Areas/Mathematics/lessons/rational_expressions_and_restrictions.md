---
subject: mathematics
lesson_id: mathematics.rational_expressions_and_restrictions
level: intermediate
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Рациональные выражения: сокращай множители, сохраняй ограничения / Rational Expressions: Cancel Factors, Keep Restrictions

## Русский

### Цель

Раскладывать простое рациональное выражение на множители, сокращать только общие множители и сохранять запрещённые значения исходного знаменателя.

### Идея и механизм

Сокращение дроби — это деление числителя и знаменателя на одно и то же ненулевое число: `6/9 = (2 · 3)/(3 · 3) = 2/3`. Рациональное выражение — дробь, у которой числитель и знаменатель — многочлены, и с ним работает тот же приём. Но есть ловушка: сокращая, мы «делим на выражение», а выражение при некоторых `x` равно нулю. Эти `x` нужно запомнить **до** сокращения.

Рассмотрим `f(x) = (x² − 9)/(x − 3)`. Знаменатель сразу показывает, что `x ≠ 3`. Разложим числитель как разность квадратов: `x² − 9 = (x − 3)(x + 3)`. Для допустимых `x` общий **множитель** `(x − 3)` сокращается, поэтому `f(x) = x + 3` — но только при сохранённом условии `x ≠ 3`.

**Пример.** При `x = 5` исходная дробь равна `(25 − 9)/(5 − 3) = 16/2 = 8`, и `x + 3` тоже даёт `8`. При `x = 3` исходная дробь превращается в `0/0` и не определена, хотя упрощённая формула даёт 6. На графике это прямая `y = x + 3` с «выколотой» точкой `(3, 6)` — устранимый разрыв.

**Типичная ошибка.** Сокращать слагаемые вместо множителей. `((x − 3)(x + 3))/(x − 3)` сократить можно: `(x − 3)` умножается на остальное. А в `(x + 5)/(x + 3)`, где `x + 5 = (x + 3) + 2`, «сократить `x + 3`» нельзя: это слагаемое суммы, а не множитель. Проверка числами сразу ловит ошибку: при `x = 0` дробь равна `5/3`, а при `x = 1` — `6/4 = 3/2`; значение зависит от `x`, значит, к постоянному числу её «сократить» нельзя.

**Зачем это дальше.** В анализе именно такие выражения появляются при вычислении пределов и производных: дробь `(f(x+h) − f(x))/h` упрощают при `h ≠ 0`, а потом устремляют `h` к нулю. В Python выражение `(x**2 - 9) / (x - 3)` при `x = 3` вызывает `ZeroDivisionError`, а с числами с плавающей точкой (например, в NumPy) может вернуть `nan` — компьютер «помнит» ограничение, даже если человек его забыл.

### Исследуй и потренируйся

Двигай `x` от −5 до 5. Сравни значения исходной дроби и `x + 3`. При `x = 3` исходная дробь недопустима, хотя упрощённая формула показывает число. Вернись к знаменателю и объясни, почему значение 6 не является значением исходной функции в этой точке.

### Вопрос

Какое утверждение верно для `f(x) = (x² − 9)/(x − 3)` после разложения числителя и сокращения?

### Варианты

- `f(x) = x + 3` при всех вещественных `x`, включая 3.
- `f(x) = x + 3` при `x ≠ 3`; значение исходной функции при 3 не определено.
- Общий множитель нельзя сокращать, потому что после этого выражение меняет значение при любом `x`.

### Ответ

2

### Разбор

Первый вариант теряет исходное ограничение знаменателя. Третий путает множитель со слагаемым: для `x ≠ 3` сокращение общего множителя сохраняет значение дроби (проверь при `x = 5`: обе формулы дают 8). Поэтому верен второй вариант.

### Границы модели

Тренажёр исследует один пример с линейным исключённым множителем и не упрощает произвольные рациональные выражения. Для каждого нового выражения сначала выпиши значения, обращающие исходный знаменатель в ноль, затем проверь все преобразования на этой области. Если после сокращения множитель знаменателя остаётся, в этой точке будет не «дырка», а вертикальная асимптота. При решении уравнений с дробями нужно дополнительно подставить найденные корни в исходное уравнение.

## English

### Goal

Factor a simple rational expression, cancel only common factors, and retain values excluded by the original denominator.

### Idea and mechanism

Reducing a fraction means dividing the numerator and denominator by the same non-zero number: `6/9 = (2 · 3)/(3 · 3) = 2/3`. A rational expression is a fraction whose numerator and denominator are polynomials, and the same move works. But there is a trap: cancelling means “dividing by an expression”, and that expression is zero for some `x`. Record those `x` values **before** cancelling.

Consider `f(x) = (x² − 9)/(x − 3)`. The denominator immediately tells us `x ≠ 3`. Factor the numerator as a difference of squares: `x² − 9 = (x − 3)(x + 3)`. For allowed inputs, the common **factor** `(x − 3)` cancels, giving `f(x) = x + 3`, but only while keeping the condition `x ≠ 3`.

**Example.** At `x = 5`, the original fraction is `(25 − 9)/(5 − 3) = 16/2 = 8`, and `x + 3` also gives `8`. At `x = 3`, the original fraction becomes `0/0` and is undefined, even though the simplified formula gives 6. The graph is the line `y = x + 3` with an open point at `(3, 6)`: a removable discontinuity.

**Common mistake.** Cancelling terms instead of factors. `((x − 3)(x + 3))/(x − 3)` can be reduced, because `(x − 3)` multiplies the rest. In `(x + 5)/(x + 3)`, where `x + 5 = (x + 3) + 2`, you cannot “cancel `x + 3`”: it is a term of a sum, not a factor. A quick number check catches the error: at `x = 0` the fraction is `5/3`, and at `x = 1` it is `6/4 = 3/2`; the value depends on `x`, so it cannot be “cancelled” down to a constant.

**Why it matters next.** In calculus, exactly these expressions appear when computing limits and derivatives: the quotient `(f(x+h) − f(x))/h` is simplified while `h ≠ 0`, and only then does `h` approach zero. In Python, `(x**2 - 9) / (x - 3)` raises `ZeroDivisionError` at `x = 3`, and with floating-point arrays (for example in NumPy) it can return `nan`: the computer keeps the restriction even if a person forgets it.

### Explore and practise

Move `x` from −5 to 5. Compare the original fraction with `x + 3`. At `x = 3`, the original fraction is undefined even though the reduced formula displays a number. Return to the denominator and explain why 6 is not a value of the original function at that input.

### Question

Which statement is correct after factoring and reducing `f(x) = (x² − 9)/(x − 3)`?

### Options

- `f(x) = x + 3` for every real `x`, including 3.
- `f(x) = x + 3` for `x ≠ 3`; the original function is undefined at 3.
- The common factor cannot be cancelled because that changes the fraction for every `x`.

### Answer

2

### Explanation

The first choice loses the original denominator restriction. The third confuses a factor with a term: for `x ≠ 3`, cancelling a common factor preserves the fraction's value (check at `x = 5`: both formulas give 8). Therefore the second choice is correct.

### Limits

The trainer explores one example with a linear excluded factor; it does not simplify arbitrary rational expressions. For a new expression, first record inputs that make the original denominator zero, then keep that domain restriction through every transformation. If a denominator factor remains after cancelling, that input gives a vertical asymptote rather than a hole. When solving rational equations, also substitute candidate roots into the original equation.

## Sources

- OpenStax, *College Algebra 2e*, [§1.6 Rational Expressions](https://openstax.org/books/college-algebra-2e/pages/1-6-rational-expressions) — simplifying by cancelling common factors; a term that is not a factor cannot be cancelled.
- OpenStax, *College Algebra 2e*, [§5.6 Rational Functions](https://openstax.org/books/college-algebra-2e/pages/5-6-rational-functions) — domain restrictions, removable discontinuities (holes), and vertical asymptotes.
- OpenStax, *Calculus Volume 1*, [3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative) — the difference quotient whose simplification precedes the limit.

OpenStax books are licensed CC BY-NC-SA 4.0; this lesson is a new explanation, not copied source text. The source monitor tracks metadata only and does not cache these pages for RAG.
