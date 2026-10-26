import Foundation

enum AppLanguage {
    case ru
    case en
}

@main
enum KnownReleaseIssuesVerification {
    static func main() {
        // Beta 9–11 lack the Sparkle rpath and crash at launch. / Beta 9–11 падают при запуске без rpath Sparkle.
        for tag in ["v0.1.0-beta.9", "v0.1.0-beta.10", "v0.1.0-beta.11", " V0.1.0-BETA.11 "] {
            let issue = KnownReleaseIssue.issue(forTag: tag)
            precondition(issue == .crashesAtLaunch, "\(tag) must be marked as crashing at launch / должна быть помечена")
            precondition(issue?.allowsDownload == false, "\(tag) must not be offered for download / нельзя предлагать для скачивания")
        }

        // Working builds keep their ordinary download link. / Рабочие сборки остаются со ссылкой на скачивание.
        for tag in ["v0.1.0-beta.1", "v0.1.0-beta.8", "v0.1.0-beta.12", "v0.1.0-beta.13", "v0.1.0-beta.110",
                    "preview-2026-10-11-current", ""] {
            precondition(KnownReleaseIssue.issue(forTag: tag) == nil, "\(tag) must not carry a known issue / не должна быть помечена")
        }

        for issue in KnownReleaseIssue.allCases {
            for key in [issue.badgeKey, issue.messageKey] {
                let russian = L10n.text(key, .ru)
                let english = L10n.text(key, .en)
                precondition(
                    russian != key && english != key && russian != english
                        && !russian.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
                        && !english.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                    "Every release warning needs Russian and English text / Нужен текст на обоих языках: \(key)"
                )
            }
        }
        precondition(
            L10n.text(KnownReleaseIssue.crashesAtLaunch.messageKey, .ru).contains("Beta 12")
                && L10n.text(KnownReleaseIssue.crashesAtLaunch.messageKey, .en).contains("Beta 12"),
            "The launch-crash warning must point to Beta 12 or later / Предупреждение должно советовать Beta 12 или новее"
        )

        print("Known release issue checks passed. / Проверка пометок проблемных версий пройдена.")
    }
}
