import Foundation

enum AppLanguage {
    case ru
    case en
}

@main
enum UnitFormattingVerification {
    static func expect(_ actual: String, _ expected: String, _ message: String) {
        precondition(actual == expected, "\(message): expected «\(expected)», got «\(actual)»")
    }

    static func main() {
        let nbsp = "\u{00A0}"

        // Russian: decimal comma and Cyrillic units; English: decimal point and Latin units.
        // Русский: запятая и кириллические единицы; английский: точка и латинские единицы.
        expect(L10n.number(5, fractionDigits: 2, .ru), "5,00", "Russian decimal comma / Запятая в RU")
        expect(L10n.number(5, fractionDigits: 2, .en), "5.00", "English decimal point / Точка в EN")
        expect(L10n.number(0.05, fractionDigits: 2, .ru), "0,05", "Learning rate η in Russian / Шаг η в RU")
        expect(L10n.number(8192, fractionDigits: 0, .ru), "8192", "No thousands separator / Без разделителя тысяч")
        expect(L10n.number(-2.5, fractionDigits: 1, .ru), "\u{2212}2,5", "True minus sign / Настоящий минус")
        expect(L10n.number(-2.5, fractionDigits: 1, .en), "\u{2212}2.5", "True minus sign in English / Минус в EN")
        expect(L10n.number(-0.001, fractionDigits: 2, .ru), "0,00", "Rounded negative zero has no sign / Ноль без знака")

        expect(L10n.measurement(10, fractionDigits: 0, unit: "m", .ru), "10\(nbsp)м", "Metres / Метры")
        expect(L10n.measurement(10, fractionDigits: 0, unit: "m", .en), "10\(nbsp)m", "Metres in English / Метры в EN")
        expect(L10n.measurement(15, fractionDigits: 1, unit: "N", .ru), "15,0\(nbsp)Н", "Newtons / Ньютоны")
        expect(L10n.measurement(15, fractionDigits: 1, unit: "N", .en), "15.0\(nbsp)N", "Newtons in English / Ньютоны в EN")
        expect(L10n.measurement(5, fractionDigits: 2, unit: "kg", .ru), "5,00\(nbsp)кг", "Kilograms / Килограммы")
        expect(L10n.measurement(0, fractionDigits: 2, unit: "m/s²", .ru), "0,00\(nbsp)м/с²", "Acceleration / Ускорение")
        expect(L10n.measurement(2, fractionDigits: 2, unit: "s", .ru), "2,00\(nbsp)с", "Seconds / Секунды")
        expect(L10n.measurement(1, fractionDigits: 2, unit: "m", .ru), "1,00\(nbsp)м", "Pendulum length / Длина маятника")
        expect(L10n.measurement(0.5, fractionDigits: 2, unit: "Hz", .ru), "0,50\(nbsp)Гц", "Hertz / Герцы")
        expect(L10n.measurement(-60, fractionDigits: 0, unit: "mV", .ru), "\u{2212}60\(nbsp)мВ", "Membrane potential / Потенциал мембраны")
        expect(L10n.measurement(167.4, fractionDigits: 1, unit: "kJ", .ru), "167,4\(nbsp)кДж", "Kilojoules / Килоджоули")
        expect(L10n.measurement(-4, fractionDigits: 1, unit: "kg·m/s", .ru), "\u{2212}4,0\(nbsp)кг·м/с", "Momentum / Импульс")
        expect(L10n.measurement(50, fractionDigits: 1, unit: "°C", .ru), "50,0\(nbsp)°C", "Celsius keeps its symbol / Градусы Цельсия")
        expect(L10n.measurement(60, fractionDigits: 0, unit: "°", .ru), "60°", "Degrees attach to the number / Градусы без пробела")
        expect(L10n.measurement(3.1, fractionDigits: 1, unit: "%", .ru), "3,1%", "Percent attaches to the number / Процент без пробела")
        expect(L10n.measurement(0.4, fractionDigits: 2, unit: "", .ru), "0,40", "Dimensionless value / Безразмерная величина")

        let latinLetters = CharacterSet(charactersIn: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        for symbol in ["m", "cm", "km", "m²", "s", "kg", "N", "J", "kJ", "m/s", "m/s²", "kg·m/s", "Hz", "mV"] {
            let russian = L10n.unit(symbol, .ru)
            precondition(
                russian.unicodeScalars.allSatisfy { !latinLetters.contains($0) },
                "Russian unit symbols must not use Latin letters / Русские единицы без латиницы: \(symbol) → \(russian)"
            )
            expect(L10n.unit(symbol, .en), symbol, "English keeps SI symbols / EN сохраняет символы СИ")
        }

        // Lab templates take numbers that are already formatted, so no locale-blind %f is left in them.
        // Шаблоны тренажёров получают уже отформатированные числа: %f без учёта языка в них не осталось.
        let numericTemplates = [
            "lab.optimization.point", "lab.optimization.objective", "lab.optimization.derivative",
            "lab.optimization.multiplier", "lab.momentumVelocity", "lab.rationalSelectedInput",
            "lab.derivativeSecantValue", "lab.derivativeTangentValue", "lab.gd.state",
            "lab.pendulum.length", "lab.pendulum.mass", "lab.pendulum.reading",
            "lab.heat.mass", "lab.heat.result", "lab.heat.transfer",
            "lab.neuron.stimulus", "lab.neuron.potentialValue", "lab.synapse.potential"
        ]
        for key in numericTemplates {
            for language in [AppLanguage.ru, .en] {
                let template = L10n.text(key, language)
                precondition(template != key, "Missing template / Нет шаблона: \(key)")
                precondition(
                    template.range(of: #"%\.?\d*f"#, options: .regularExpression) == nil,
                    "Template still formats a float without the interface language / В шаблоне остался %f: \(key)"
                )
            }
        }

        expect(
            String(format: L10n.text("lab.pendulum.length", .ru), L10n.measurement(1, fractionDigits: 2, unit: "m", .ru)),
            "Длина нити L = 1,00\(nbsp)м",
            "Pendulum label / Подпись маятника"
        )
        expect(
            String(
                format: L10n.text("lab.pendulum.reading", .en),
                L10n.measurement(2.006, fractionDigits: 2, unit: "s", .en),
                L10n.measurement(0.498, fractionDigits: 2, unit: "Hz", .en)
            ),
            "Period T = 2.01\(nbsp)s · frequency f = 0.50\(nbsp)Hz",
            "English pendulum reading / Показания маятника в EN"
        )
        expect(
            String(format: L10n.text("lab.synapse.potential", .ru), L10n.measurement(-58, fractionDigits: 0, unit: "mV", .ru)),
            "Мембрана у аксонного холмика: \u{2212}58\(nbsp)мВ",
            "Synapse reading uses a minus sign / Минус в тренажёре синапса"
        )
        expect(
            String(format: L10n.text("lab.optimization.point", .ru), "0,707", "\u{2212}0,707"),
            "Точка: (0,707; \u{2212}0,707)",
            "Russian coordinates are separated by a semicolon / Координаты в RU через точку с запятой"
        )

        // VoiceOver reads the percent lab through String(format:), so the template must use %@ only.
        // VoiceOver читает лабораторию процентов через String(format:), поэтому в шаблоне только %@.
        for language in [AppLanguage.ru, .en] {
            let template = L10n.text("lab.percent.representations", language)
            precondition(
                template.components(separatedBy: "%@").count - 1 == 3
                    && template.range(of: #"%[1-9]"#, options: .regularExpression) == nil,
                "Percent representation template must have exactly three %@ / Нужны ровно три %@"
            )
        }
        expect(
            String(format: L10n.text("lab.percent.representations", .ru), "35%", "7/20", "0,35"),
            "35% равно дроби 7/20 и десятичному числу 0,35",
            "Percent VoiceOver label / Подпись VoiceOver для процентов"
        )

        let reinforce = String(format: L10n.text("home.knowledgeNeedPractice", .ru), 1)
        precondition(!reinforce.contains("1 тем"), "Topic count must agree with the number / Число тем должно согласоваться: \(reinforce)")

        print("Bilingual number and unit formatting checks passed. / Проверка чисел и единиц RU/EN пройдена.")
    }
}
