---
subject: mathematics
lesson_id: mathematics.solving_linear_equations
level: foundations
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 180
---

# Линейные уравнения: сохраняем равенство / Linear Equations: Keep Both Sides Equal

## Русский

### Цель

Решить уравнение вида `ax + b = c`, применяя одинаковые обратные операции к обеим сторонам, а затем проверить ответ подстановкой.

### Идея и механизм

Представь чашечные весы в равновесии. Если снять с обеих чаш по одинаковому грузу или разделить груз на каждой чаше пополам, весы останутся в равновесии. Уравнение работает так же: знак равенства означает, что значения слева и справа одинаковы, и наша задача — менять обе стороны одинаково, пока `x` не останется в одиночестве.

Если к обеим сторонам прибавить или из обеих сторон вычесть одно и то же число, равенство сохранится. Так же работает умножение или деление обеих сторон на одно и то же **ненулевое** число. Чтобы изолировать `x`, выполняют обратные операции в порядке, обратном порядку действий: сначала убирают слагаемое, затем коэффициент.

**Пример.** `3x − 5 = 16`. Прибавим `5` к обеим сторонам: `3x = 21`. Разделим обе стороны на `3`: `x = 7`. Проверка: слева `3 · 7 − 5 = 16`, справа тоже `16`, значит ответ подходит.

**Типичная ошибка.** Применить операцию только к одной стороне или к одному слагаемому: например, разделить на `3` только `3x`, но не `16`. Фраза «перенести с противоположным знаком» — лишь сокращённая запись того, что одно и то же число прибавили к обеим сторонам; если забыть это, легко ошибиться в знаке.

**Зачем это дальше.** Почти любая формула в физике решается относительно нужной величины тем же приёмом: из `v = v₀ + at` получаем `t = (v − v₀)/a` при `a ≠ 0`. В Python операция `=` означает присваивание, а не равенство; проверку подстановкой можно записать как сравнение `3 * 7 - 5 == 16`.

### Исследуй и потренируйся

В тренажёре сначала убери постоянное слагаемое одинаковым действием с обеих сторон, затем раздели обе стороны на коэффициент при `x`. После этого подставь найденное значение в исходное равенство. В каждом новом примере меняются коэффициент, решение и постоянное слагаемое.

### Вопрос

Реши `4x + 3 = 19`. Какое значение `x` удовлетворяет равенству?

### Варианты

- `3`
- `4`
- `5`

### Ответ

2

### Разбор

Вычтем `3` из обеих сторон: `4x = 16`. Разделим обе стороны на `4`: `x = 4`. Подстановка даёт `4 · 4 + 3 = 19`, поэтому равенство верно. Для сравнения: `x = 5` даёт `23`, а `x = 3` — `15`.

### Границы модели

Этот первый тренажёр охватывает уравнения `ax + b = c` с целыми числами и положительным коэффициентом `a`. Он не охватывает дробные коэффициенты, переменные по обе стороны, несколько переменных, системы или неравенства. Делить обе стороны можно только на ненулевое число. При решении неравенств умножение или деление обеих частей на отрицательное число дополнительно меняет направление знака неравенства.

## English

### Goal

Solve an equation of the form `ax + b = c` by applying the same inverse operation to both sides, then check the answer by substitution.

### Idea and mechanism

Picture a balance scale at rest. If you remove the same weight from both pans, or halve the load on each pan, the scale stays balanced. An equation works the same way: the equals sign says the left and right values are the same, and the job is to change both sides in the same way until `x` stands alone.

Adding or subtracting the same number on both sides preserves equality. So does multiplying or dividing both sides by the same **non-zero** number. To isolate `x`, undo the operations in reverse order: remove the added term first, then the coefficient.

**Example.** `3x − 5 = 16`. Add `5` to both sides: `3x = 21`. Divide both sides by `3`: `x = 7`. Check: the left side is `3 · 7 − 5 = 16`, which matches the right side, so the answer works.

**Common mistake.** Applying an operation to only one side or to only one term: for example, dividing `3x` by `3` but not `16`. “Move it across and change the sign” is only shorthand for adding the same number to both sides; forgetting that makes sign errors easy.

**Why it matters next.** Almost every physics formula is solved for the quantity you need with the same move: `v = v₀ + at` gives `t = (v − v₀)/a` when `a ≠ 0`. In Python, `=` means assignment, not equality; a substitution check can be written as the comparison `3 * 7 - 5 == 16`.

### Explore and practise

In the trainer, first remove the constant term with the same operation on both sides. Then divide both sides by the coefficient of `x`. Substitute the result into the original equation. Each new example changes the coefficient, solution, and constant term.

### Question

Solve `4x + 3 = 19`. What value of `x` makes the equation true?

### Options

- `3`
- `4`
- `5`

### Answer

2

### Explanation

Subtract `3` from both sides: `4x = 16`. Divide both sides by `4`: `x = 4`. Substitution gives `4 · 4 + 3 = 19`, so the equality holds. For comparison, `x = 5` gives `23` and `x = 3` gives `15`.

### Limits

This first trainer covers integer equations `ax + b = c` with a positive coefficient `a`. It does not cover fractional coefficients, variables on both sides, multiple variables, systems, or inequalities. Dividing both sides is valid only for a non-zero number. When solving inequalities, multiplying or dividing both sides by a negative number also reverses the inequality sign.

## Sources

- OpenStax, *Prealgebra 2e*, [2.3 Solving Equations Using the Subtraction and Addition Properties of Equality](https://openstax.org/books/prealgebra-2e/pages/2-3-solving-equations-using-the-subtraction-and-addition-properties-of-equality) — applying the same addition or subtraction to both sides; checking by substitution.
- OpenStax, *Prealgebra 2e*, [8.2 Solve Equations Using the Division and Multiplication Properties of Equality](https://openstax.org/books/prealgebra-2e/pages/8-2-solve-equations-using-the-division-and-multiplication-properties-of-equality) — multiplying or dividing both sides, with a non-zero divisor.
- OpenStax, *Elementary Algebra 2e*, [2.7 Solve Linear Inequalities](https://openstax.org/books/elementary-algebra-2e/pages/2-7-solve-linear-inequalities) — multiplying or dividing an inequality by a negative number reverses its sign.

OpenStax books are licensed CC BY-NC-SA 4.0. This lesson is written in original wording and does not copy textbook text or figures.
