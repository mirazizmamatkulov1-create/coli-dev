---
subject: zoology
lesson_id: zoology.logistic_population_growth
level: intermediate
languages: ru, en
source_checked: 2026-10-26
source_review_interval_days: 365
---

# Популяции: логистический рост и ёмкость среды / Populations: Logistic Growth and Carrying Capacity

## Русский

### Цель

Сравнивать экспоненциальный и логистический рост популяции, рассчитывать скорость роста по уравнению dN/dt = rmax · N · (K − N)/K и объяснять, почему популяции не растут бесконечно.

### Идея и механизм

Если ресурсов сколько угодно, популяция растёт экспоненциально: dN/dt = rmax · N, где N — численность, а rmax — наибольшая скорость роста вида, его биотический потенциал. Чем больше особей, тем быстрее прибавка. Но бесконечных ресурсов в природе не бывает.

Логистическая модель добавляет ёмкость среды K — наибольшую численность, которую среда может поддерживать долго. Скорость роста умножается на долю ещё свободного места: dN/dt = rmax · N · (K − N)/K. Когда популяция мала, (K − N)/K близко к единице, и рост почти экспоненциальный. Когда N приближается к K, множитель стремится к нулю, рост замедляется, и численность выходит на плато. Получается S-образная кривая. Это та же логика, что и у бактерий в закрытой культуре, только для природных популяций.

### Исследуй и потренируйся

Для rmax = 0,1 и K = 1000 посчитай скорость роста при N = 100, 500 и 900. При какой численности прирост оказался наибольшим? Затем найди скорость роста при N = 1000 и объясни результат.

### Вопрос

Популяция с rmax = 0,1 в единицу времени живёт в среде с ёмкостью K = 1000. Какова скорость её роста при N = 500 по логистической модели?

### Варианты

- 25 особей в единицу времени: 0,1 · 500 · (1000 − 500)/1000 = 25.
- 50 особей в единицу времени: 0,1 · 500 = 50.
- 0: рост прекращается уже на половине ёмкости.

### Ответ

1

### Разбор

Множитель свободного места при N = 500 равен (1000 − 500)/1000 = 0,5, поэтому скорость вдвое меньше экспоненциальной: 0,1 · 500 · 0,5 = 25. Ответ 50 — это экспоненциальный рост без учёта ёмкости среды. Рост останавливается только при N = K, а не на половине.

### Границы вывода

Логистическая модель — упрощение: в ней ёмкость среды постоянна, а все особи одинаковы и размножаются с одной скоростью. Модель описывает одну популяцию без связей с другими видами, поэтому не учитывает хищников, конкурентов и случайные события.

## English

### Goal

Compare exponential and logistic population growth, calculate the growth rate with dN/dt = rmax · N · (K − N)/K, and explain why populations do not grow forever.

### Idea and mechanism

With unlimited resources a population grows exponentially: dN/dt = rmax · N, where N is the population size and rmax is the species' maximal growth rate, its biotic potential. The more individuals, the faster the increase. But nature never has unlimited resources.

The logistic model adds the carrying capacity K, the largest population the environment can support over time. The growth rate is multiplied by the share of room still free: dN/dt = rmax · N · (K − N)/K. When the population is small, (K − N)/K is close to one and growth is nearly exponential. As N approaches K, the factor tends to zero, growth slows, and the population levels off. The result is an S-shaped curve. It is the same logic as bacteria in a closed culture, applied to natural populations.

### Explore and practise

For rmax = 0.1 and K = 1000, calculate the growth rate at N = 100, 500, and 900. At which size is the increase largest? Then find the growth rate at N = 1000 and explain the result.

### Question

A population with rmax = 0.1 per unit time lives in an environment with carrying capacity K = 1000. What is its growth rate at N = 500 under the logistic model?

### Options

- 25 individuals per unit time: 0.1 · 500 · (1000 − 500)/1000 = 25.
- 50 individuals per unit time: 0.1 · 500 = 50.
- 0: growth stops already at half the carrying capacity.

### Answer

1

### Explanation

The free-room factor at N = 500 is (1000 − 500)/1000 = 0.5, so the rate is half the exponential one: 0.1 · 500 · 0.5 = 25. The answer 50 is exponential growth that ignores carrying capacity. Growth stops only at N = K, not halfway.

### Limits of the inference

The logistic model is a simplification: carrying capacity is constant and all individuals are alike and reproduce at the same rate. The model describes one population without links to other species, so it ignores predators, competitors, and chance events.

## Sources

- Mary Ann Clark, Matthew Douglas, Jung Choi, *Biology 2e*, OpenStax, 2018, section 45.3 “Environmental Limits to Population Growth” (consulted 2026-10-26): exponential growth dN/dT = rmax N with rmax as biotic potential, the logistic equation dN/dT = rmax N (K − N)/K, (K − N)/K near one for small N, carrying capacity, and the S-shaped curve: [OpenStax Biology 2e, 45.3](https://openstax.org/books/biology-2e/pages/45-3-environmental-limits-to-population-growth)
- The OpenStax page states its own license terms; the lesson paraphrases the section and does not copy its text: [OpenStax terms of use](https://openstax.org/terms-of-use)
