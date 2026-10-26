---
subject: mathematics
lesson_id: mathematics.numbers_fractions_and_percentages
level: foundations
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 180
---

# Часть целого: дроби, десятичная запись и проценты / Parts of a whole: fractions, decimals, and percentages

## Русский

### Цель

Представить одну и ту же долю как дробь, десятичное число и процент, а затем найти эту долю от заданного количества.

### Идея и механизм

Представь пиццу, разрезанную на 4 равных куска, из которых ты съел 3. Это можно сказать тремя способами: «три четверти» (`3/4`), «0,75 пиццы» или «75% пиццы». Количество еды одно и то же — меняется только запись. Умение переходить между записями нужно постоянно: в рецептах, скидках, вероятностях и данных.

В общем случае дробь `a/b` — это частное целых чисел `a` и `b`, где `b ≠ 0`. Здесь используется модель неотрицательной доли целого: `b > 0` и `0 ≤ a ≤ b`; знаменатель показывает, на сколько равных частей разделено целое, а числитель — сколько частей взято. Чтобы перевести дробь в десятичную запись, числитель делят на знаменатель. Процент означает «из ста»: `p% = p/100`. Например, `35% = 35/100 = 7/20 = 0,35`.

Чтобы найти долю от целого, умножь целое на десятичную запись доли: `35%` от `240` равно `240 × 0,35 = 84`. У части те же единицы, что и у целого: `84 доллара` из `240 долларов`. Приставка `кило-` означает тысячу, поэтому `1,5 км = 1 500 м` — это то же расстояние в другой единице. Перед вычислениями приводи величины к совместимым единицам.

**Пример.** Какую долю составляют `18` учеников из `24`? Делим: `18 ÷ 24 = 0,75`. Умножив на `100`, получаем `75%`; дробь `18/24` сокращается на `6` и даёт `3/4`. Проверка: `24 × 0,75 = 18`.

**Типичная ошибка.** Сравнивать проценты от разных целых. «`10%` от `500`» (это `50`) больше, чем «`20%` от `200`» (это `40`), хотя процент во втором случае больше. Процент всегда нужно читать вместе с тем, от чего он взят.

**Зачем это дальше.** В Python деление `3 / 4` даёт десятичное число `0.75`, а `1 / 3` — лишь приближение `0.333…` с конечным числом знаков. В физике без перевода единиц (км → м) формулы дают неверные ответы, а в статистике и машинном обучении доли и проценты описывают частоты, вероятности и точность модели.

### Исследуй и потренируйся

В лаборатории меняй процент и размер целого. Полоса показывает долю от целого, а рядом синхронно обновляются процент, сокращённая дробь, десятичная запись и значение части. Ниже измени расстояние в километрах и сравни эквивалентную запись в метрах. Предскажи, как изменится часть, если процент останется тем же, а целое удвоится.

### Вопрос

Какую долю `240` составляет `60`? Запиши ответ в виде процента и сокращённой дроби.

### Варианты

- `20% = 1/5`
- `25% = 1/4`
- `40% = 2/5`

### Ответ

2

### Разбор

Доля равна `60 ÷ 240 = 0,25`. Умножив десятичную запись на `100`, получаем `25%`; дробь `60/240` сокращается до `1/4`. Проверка: `240 × 0,25 = 60`. Остальные варианты не проходят такую же обратную проверку: `240 × 0,2 = 48` и `240 × 0,4 = 96`, а не `60`.

### Границы модели

Лаборатория показывает целые проценты от `0%` до `100%` и простую долю от положительного целого. Проценты больше `100%`, отрицательные изменения, округление при денежных операциях, налоги, последовательные скидки и размерности сложных физических величин требуют отдельных моделей. Десятичная запись дроби с целыми числителем и знаменателем либо конечна, либо бесконечна и периодична; округление периодической записи даёт приближение, а не точное значение.

## English

### Goal

Represent the same part as a fraction, decimal, and percentage, then find that part of a given whole.

### Idea and mechanism

Picture a pizza cut into 4 equal slices, and you ate 3. You can say this three ways: “three quarters” (`3/4`), “0.75 of the pizza”, or “75% of the pizza”. The amount of food is the same; only the notation changes. Moving between these forms comes up constantly: recipes, discounts, probabilities, and data.

In general, a fraction `a/b` is a quotient of integers `a` and `b`, where `b ≠ 0`. Here we use the nonnegative part-of-a-whole model: `b > 0` and `0 ≤ a ≤ b`; the denominator counts the equal parts in the whole, and the numerator counts the parts taken. Divide the numerator by the denominator to write a fraction as a decimal. Percent means “per hundred”: `p% = p/100`. For example, `35% = 35/100 = 7/20 = 0.35`.

To find a part of a whole, multiply the whole by the decimal form of the part: `35%` of `240` is `240 × 0.35 = 84`. The part keeps the whole's unit: `84 dollars` out of `240 dollars`. The prefix `kilo-` means one thousand, so `1.5 km = 1,500 m`: the same distance in another unit. Convert quantities to compatible units before calculating.

**Example.** What part of `24` students is `18`? Divide: `18 ÷ 24 = 0.75`. Multiplying by `100` gives `75%`; dividing the numerator and denominator of `18/24` by `6` gives `3/4`. Check: `24 × 0.75 = 18`.

**Common mistake.** Comparing percentages of different wholes. “`10%` of `500`” (that is `50`) is more than “`20%` of `200`” (that is `40`), even though the second percentage is larger. Always read a percentage together with the whole it is taken from.

**Why it matters next.** In Python, `3 / 4` gives the decimal `0.75`, while `1 / 3` gives only a finite approximation `0.333…`. In physics, formulas give wrong answers if units are not converted (km → m), and in statistics and machine learning, fractions and percentages describe frequencies, probabilities, and model accuracy.

### Explore and practise

Change the percentage and the whole in the lab. The bar shows the part of the whole, while the percentage, reduced fraction, decimal, and part value update together. Below it, change a distance in kilometres and compare its equivalent in metres. Predict what happens to the part if the percentage stays the same and the whole doubles.

### Question

What fraction of `240` is `60`? Give the answer as a percentage and a reduced fraction.

### Options

- `20% = 1/5`
- `25% = 1/4`
- `40% = 2/5`

### Answer

2

### Explanation

The part is `60 ÷ 240 = 0.25`. Multiply the decimal by `100` to get `25%`; reduce `60/240` to `1/4`. Check: `240 × 0.25 = 60`. The other options fail the same reverse check: `240 × 0.2 = 48` and `240 × 0.4 = 96`, not `60`.

### Limits

The lab represents whole-number percentages from `0%` through `100%` and a simple part of a positive whole. Percentages above `100%`, negative changes, rounding in money, tax, successive discounts, and dimensions in complex physical quantities need separate models. The decimal form of a fraction with an integer numerator and denominator either terminates or repeats forever; rounding a repeating decimal gives an approximation, not an exact value.

## Sources

- OpenStax, *Prealgebra 2e*, [4.1 Visualize Fractions](https://openstax.org/books/prealgebra-2e/pages/4-1-visualize-fractions) — fractions as parts of a whole, numerator and denominator, `b ≠ 0`.
- OpenStax, *Prealgebra 2e*, [5.3 Decimals and Fractions](https://openstax.org/books/prealgebra-2e/pages/5-3-decimals-and-fractions) — converting a fraction to a decimal by division; repeating decimals.
- OpenStax, *Prealgebra 2e*, [6.1 Understand Percent](https://openstax.org/books/prealgebra-2e/pages/6-1-understand-percent) — percent as a ratio per hundred and conversions.
- OpenStax, *Prealgebra 2e*, [6.2 Solve General Applications of Percent](https://openstax.org/books/prealgebra-2e/pages/6-2-solve-general-applications-of-percent) — finding an amount by multiplying the percent by the base.
- OpenStax, *Prealgebra 2e*, [7.1 Rational and Irrational Numbers](https://openstax.org/books/prealgebra-2e/pages/7-1-rational-and-irrational-numbers) — every rational number has a decimal form that stops or repeats.
- NIST, [Metric (SI) Prefixes](https://www.nist.gov/pml/owm/metric-si-prefixes) — `kilo` denotes a factor of 1,000.

The lesson is written in original wording. OpenStax material is linked for study and remains metadata/preview-only in the app; the book is licensed CC BY-NC-SA 4.0, which requires a separate release review before redistribution of adapted material.
