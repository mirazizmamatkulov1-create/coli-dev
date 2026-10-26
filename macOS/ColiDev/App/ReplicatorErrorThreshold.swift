import Foundation

/// Eigen's error threshold (Die Naturwissenschaften 58, 1971) for the biology "what is life" lesson.
/// A replicator of `length` letters copies each letter with `errorRate`; the exact copy is selected
/// `advantage` times faster than faulty ones and persists only while advantage · (1 − e)^L > 1.
/// The simplified model ignores back mutation, neutral mutations, and population size.
enum ReplicatorErrorThresholdModel {
    static let lengthRange = 10.0...1000.0
    static let errorRateRange = 0.001...0.05
    static let advantageRange = 2.0...100.0

    static func exactCopyProbability(length: Double, errorRate: Double) -> Double {
        pow(1 - errorRate, length)
    }

    /// Exact offspring per correct molecule per generation: above 1 the information persists.
    static func exactOffspring(length: Double, errorRate: Double, advantage: Double) -> Double {
        advantage * exactCopyProbability(length: length, errorRate: errorRate)
    }

    static func persists(length: Double, errorRate: Double, advantage: Double) -> Bool {
        exactOffspring(length: length, errorRate: errorRate, advantage: advantage) > 1
    }

    /// The longest whole number of letters that still persists, or nil when even one letter fails.
    static func maximumLength(errorRate: Double, advantage: Double) -> Int? {
        guard errorRate > 0, errorRate < 1, advantage > 1 else { return nil }
        var length = Int((log(advantage) / -log(1 - errorRate)).rounded(.down))
        // Guard the strict inequality against floating-point rounding at the boundary.
        while length > 0, !persists(length: Double(length), errorRate: errorRate, advantage: advantage) {
            length -= 1
        }
        return length > 0 ? length : nil
    }
}
