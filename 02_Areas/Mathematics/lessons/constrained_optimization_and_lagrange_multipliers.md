---
subject: mathematics
lesson_id: mathematics.constrained_optimization_and_lagrange_multipliers
level: advanced
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Оптимизация с ограничением и множители Лагранжа / Constrained Optimization and Lagrange Multipliers

## Русский

### Цель

Находить кандидатов на условный экстремум гладкой функции при одном гладком равенстве-ограничении, объяснять роль множителя Лагранжа и отдельно доказывать, какие кандидаты дают глобальный максимум или минимум.

### Идея и механизм

Представь, что ты идёшь по тропинке на склоне холма и хочешь найти самую высокую точку **именно на тропинке**, а не на всём холме. Пока тропинка пересекает линии равной высоты, можно сделать шаг и подняться выше. Наивысшая точка тропинки там, где тропинка лишь касается линии уровня. В этой точке направление «круче всего вверх» (градиент высоты) перпендикулярно тропинке — так же, как градиент функции ограничения. Значит, два градиента параллельны.

Пусть нужно исследовать `f(x, y)` при условии `g(x, y) = 0`. Если в точке условного локального экстремума `∇g ≠ 0` (точка регулярна), то градиенты целевой функции и ограничения параллельны:

`∇f(x, y) = λ∇g(x, y)`, одновременно с `g(x, y) = 0`.

Число `λ` — множитель Лагранжа: коэффициент, на который нужно умножить `∇g`, чтобы получить `∇f`. Значение `λ` зависит от того, как записано ограничение: если заменить `g` на `c·g` при `c ≠ 0`, множитель станет `λ/c`. Система даёт только **кандидатов** (необходимое условие); их тип нужно определить отдельно — например, сравнив значения `f`. Условия и порядок действий соответствуют OpenStax *Calculus Volume 3*, §4.8, теорема 4.20.

**Пример.** Найдём экстремумы `f(x, y) = xy` на единичной окружности `x² + y² = 1`. Здесь `g(x, y) = x² + y² − 1`, `∇f = (y, x)`, `∇g = (2x, 2y)`. Система Лагранжа: `y = 2λx`, `x = 2λy`, `x² + y² = 1`. Если бы `x = 0`, то из первого уравнения `y = 0`, но точка `(0, 0)` не лежит на окружности; значит, обе координаты ненулевые. Разделив, получим `y/x = 2λ = x/y`, откуда `x² = y²`, то есть `x = y` либо `x = −y`.

При `x = y` получаются точки `(1/√2, 1/√2)` и `(−1/√2, −1/√2)` с `f = 1/2` и `λ = 1/2`. При `x = −y` — точки `(1/√2, −1/√2)` и `(−1/√2, 1/√2)` с `f = −1/2` и `λ = −1/2`. Окружность — замкнутое ограниченное множество, а `f` непрерывна, поэтому по теореме об экстремальном значении (§4.7, теорема 4.18) наибольшее и наименьшее значения существуют. Сравнение всех кандидатов даёт глобальный максимум `1/2` и минимум `−1/2`.

**Типичная ошибка.** Считать, что каждое решение системы Лагранжа — максимум. Система находит и максимумы, и минимумы, и другие стационарные точки; без сравнения значений или иного обоснования вывод о типе точки не сделан.

**Зачем это дальше.** В машинном обучении много задач с ограничениями. Например, метод главных компонент (PCA) ищет направление `w` с наибольшей дисперсией при условии `‖w‖ = 1`; условие Лагранжа для этой задачи приводит к уравнению на собственные векторы `Σw = λw` — это связь с темой «Собственные значения» маршрута. Для ограничений-неравенств метод обобщают условия Каруша — Куна — Таккера (KKT), на которых построены, например, метод опорных векторов и многие численные оптимизаторы.

### Исследуй и потренируйся

В лаборатории двигай точку по окружности ползунком или перетаскиванием. Окружность — допустимое множество, пунктирные диагонали показывают направления `x = y` и `x = −y`, где лежат стационарные точки. Сначала предскажи знак `xy` и стационарность точки, затем сравни ответ с вычисленными координатами, значением цели и `λ`. Проверь четыре точки пересечения диагоналей с окружностью и объясни, почему две дают максимум, а две — минимум.

### Вопрос

Какая пара точек задаёт глобальные максимумы `xy` при `x² + y² = 1`?

### Варианты

- `(1/√2, −1/√2)` и `(−1/√2, 1/√2)`
- `(1/√2, 1/√2)` и `(−1/√2, −1/√2)`
- `(1, 0)` и `(0, 1)`

### Ответ

2

### Разбор

На единичной окружности точки с `x = y` имеют координаты одного знака и дают `xy = 1/2`; точки с `x = −y` имеют разные знаки и дают `xy = −1/2` — это минимумы. Поэтому вторая пара достигает глобального максимума. Точки `(1, 0)` и `(0, 1)` лежат на окружности, но дают `xy = 0`; в них `∇f` не параллелен `∇g` (например, в `(1, 0)`: `∇f = (0, 1)`, `∇g = (2, 0)`), поэтому условие Лагранжа не выполняется.

### Границы модели

Условие `∇f = λ∇g` — необходимое условие первого порядка только для гладкого равенства в регулярной точке, где `∇g ≠ 0`; точки, где градиент ограничения равен нулю, нужно проверять отдельно. Оно находит кандидатов, а не классифицирует их автоматически. Для неравенств, углов, границ и негладких ограничений требуются дополнительные условия (например, KKT) и отдельная проверка. Интерактив показывает двумерный пример на окружности, а не универсальный решатель оптимизации.

## English

### Goal

Find candidates for constrained extrema of a smooth function under one smooth equality constraint, explain the role of a Lagrange multiplier, and separately justify which candidates are global maxima or minima.

### Idea and mechanism

Imagine walking along a trail on a hillside and looking for the highest point **on the trail**, not on the whole hill. While the trail still crosses contour lines, one more step can take you higher. The trail's highest point is where the trail only touches a contour line. There, the direction of steepest ascent (the gradient of height) is perpendicular to the trail, and so is the gradient of the constraint function. So the two gradients are parallel.

Suppose we want to analyze `f(x, y)` subject to `g(x, y) = 0`. If a constrained local extremum occurs at a point where `∇g ≠ 0` (a regular point), the objective and constraint gradients are parallel there:

`∇f(x, y) = λ∇g(x, y)`, together with `g(x, y) = 0`.

The scalar `λ` is the Lagrange multiplier: the factor that turns `∇g` into `∇f`. Its value depends on how the constraint is written: replacing `g` with `c·g` for `c ≠ 0` changes the multiplier to `λ/c`. The system gives only **candidates** (a necessary condition); their type must be determined separately, for example by comparing values of `f`. The conditions and procedure follow OpenStax *Calculus Volume 3*, §4.8, Theorem 4.20.

**Example.** Find the extrema of `f(x, y) = xy` on the unit circle `x² + y² = 1`. Here `g(x, y) = x² + y² − 1`, `∇f = (y, x)`, and `∇g = (2x, 2y)`. The Lagrange system is `y = 2λx`, `x = 2λy`, `x² + y² = 1`. If `x = 0`, the first equation gives `y = 0`, but `(0, 0)` is not on the circle; so both coordinates are non-zero. Dividing gives `y/x = 2λ = x/y`, so `x² = y²`: either `x = y` or `x = −y`.

When `x = y`, the points are `(1/√2, 1/√2)` and `(−1/√2, −1/√2)`, with `f = 1/2` and `λ = 1/2`. When `x = −y`, the points are `(1/√2, −1/√2)` and `(−1/√2, 1/√2)`, with `f = −1/2` and `λ = −1/2`. The circle is closed and bounded and `f` is continuous, so by the Extreme Value Theorem (§4.7, Theorem 4.18) the largest and smallest values exist. Comparing every candidate gives the global maximum `1/2` and minimum `−1/2`.

**Common mistake.** Treating every solution of the Lagrange system as a maximum. The system finds maxima, minima, and other stationary points alike; without comparing values or another argument, the type of a point has not been established.

**Why it matters next.** Machine learning is full of constrained problems. For example, principal component analysis (PCA) looks for the direction `w` of largest variance subject to `‖w‖ = 1`; the Lagrange condition for this problem leads to the eigenvector equation `Σw = λw`, which connects to the “Eigenvalues” topic on the route. For inequality constraints, the method is generalized by the Karush–Kuhn–Tucker (KKT) conditions, which underlie, for example, support vector machines and many numerical optimizers.

### Explore and practise

Move the point around the circle with the slider or by dragging it. The circle is the feasible set; dashed diagonals show `x = y` and `x = −y`, where the stationary points lie. First predict the sign of `xy` and whether the selected point is stationary, then compare with the displayed coordinates, objective value, and `λ`. Check the four intersections of the diagonals with the circle and explain why two are maxima and two are minima.

### Question

Which pair gives the global maxima of `xy` subject to `x² + y² = 1`?

### Options

- `(1/√2, −1/√2)` and `(−1/√2, 1/√2)`
- `(1/√2, 1/√2)` and `(−1/√2, −1/√2)`
- `(1, 0)` and `(0, 1)`

### Answer

2

### Explanation

On the unit circle, points with `x = y` have coordinates of the same sign and give `xy = 1/2`; points with `x = −y` have opposite signs and give `xy = −1/2`, so they are minima. The second pair therefore gives the global maximum. The points `(1, 0)` and `(0, 1)` lie on the circle but give `xy = 0`; there `∇f` is not parallel to `∇g` (at `(1, 0)`, for example, `∇f = (0, 1)` and `∇g = (2, 0)`), so the Lagrange condition fails.

### Limits

The condition `∇f = λ∇g` is a first-order necessary condition only for a smooth equality at a regular point where `∇g ≠ 0`; points where the constraint gradient is zero must be checked separately. It identifies candidates and does not classify them automatically. Inequalities, corners, boundaries, and nonsmooth constraints require additional conditions (such as KKT) and separate checks. This interactive is a two-dimensional circle example, not a general-purpose optimization solver.

## Sources

- OpenStax, *Calculus Volume 3*, §4.8 “Lagrange Multipliers” / «Множители Лагранжа» (Theorem 4.20): <https://openstax.org/books/calculus-volume-3/pages/4-8-lagrange-multipliers>
- OpenStax, *Calculus Volume 3*, §4.7 “Maxima/Minima Problems” / «Задачи на максимумы и минимумы» (Theorem 4.18, Extreme Value Theorem): <https://openstax.org/books/calculus-volume-3/pages/4-7-maxima-minima-problems>
- Boyd, S., & Vandenberghe, L. *Convex Optimization*. Cambridge University Press, 2004, §5.5.3 “KKT optimality conditions” (many optimization algorithms can be interpreted as methods for solving the KKT conditions): <https://web.stanford.edu/~boyd/cvxbook/>
- Bishop, C. M. *Pattern Recognition and Machine Learning*. Springer, 2006, §12.1.1 “Maximum variance formulation” (PCA via a Lagrange multiplier leads to an eigenvector of the covariance matrix) and §7.1 “Maximum Margin Classifiers” (support vector machines and KKT conditions): <https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf>

OpenStax books are licensed CC BY-NC-SA 4.0. This lesson is written in original wording and does not copy textbook text or figures.
