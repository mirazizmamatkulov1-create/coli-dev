import Foundation

// Published builds with a known defect. The Updates list warns about them instead of offering the
// archive as an ordinary download. Add a tag here when a published build turns out to be broken.
enum KnownReleaseIssue: String, CaseIterable {
    // Beta 9–11 embedded Sparkle without the `@executable_path/../Frameworks` rpath, so macOS stops
    // them at launch ("Library missing"). Beta 12 is the first build with the fix.
    case crashesAtLaunch

    private static let issuesByTag: [String: KnownReleaseIssue] = [
        "v0.1.0-beta.9": .crashesAtLaunch,
        "v0.1.0-beta.10": .crashesAtLaunch,
        "v0.1.0-beta.11": .crashesAtLaunch
    ]

    static func issue(forTag tag: String) -> KnownReleaseIssue? {
        issuesByTag[tag.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()]
    }

    /// A build that cannot start is not offered as a download.
    var allowsDownload: Bool {
        switch self {
        case .crashesAtLaunch: return false
        }
    }

    /// Short badge for the collapsed release row.
    var badgeKey: String { "updates.issue.\(rawValue).badge" }

    /// Full warning shown in place of the download link.
    var messageKey: String { "updates.issue.\(rawValue).message" }
}
