import Foundation

@main
enum ReplicatorErrorThresholdVerification {
    static func close(_ value: Double, _ expected: Double, _ tolerance: Double = 0.0005) -> Bool {
        abs(value - expected) <= tolerance
    }

    static func main() {
        typealias Model = ReplicatorErrorThresholdModel

        // Lesson question: 300 letters, 1% error, tenfold advantage.
        precondition(close(Model.exactCopyProbability(length: 300, errorRate: 0.01), 0.0490), "0.99^300 ≈ 0.049")
        precondition(close(Model.exactOffspring(length: 300, errorRate: 0.01, advantage: 10), 0.4904), "10 · 0.049 ≈ 0.49")
        precondition(!Model.persists(length: 300, errorRate: 0.01, advantage: 10), "information is erased at 300 letters")

        // Lab starting point: 100 letters survive.
        precondition(close(Model.exactCopyProbability(length: 100, errorRate: 0.01), 0.3660))
        precondition(Model.persists(length: 100, errorRate: 0.01, advantage: 10))

        // The threshold sits between 229 and 230 letters.
        precondition(Model.persists(length: 229, errorRate: 0.01, advantage: 10))
        precondition(!Model.persists(length: 230, errorRate: 0.01, advantage: 10))
        precondition(Model.maximumLength(errorRate: 0.01, advantage: 10) == 229)

        // Ten times fewer errors allow about ten times longer molecules; more advantage helps only logarithmically.
        precondition(Model.maximumLength(errorRate: 0.001, advantage: 10) == 2301)
        precondition(Model.maximumLength(errorRate: 0.01, advantage: 100) == 458)

        precondition(Model.maximumLength(errorRate: 0.01, advantage: 1) == nil, "no advantage, no stable information")
        precondition(Model.maximumLength(errorRate: 0.5, advantage: 1.5) == nil, "even one letter fails")
        for length in stride(from: 10.0, through: 1000.0, by: 10.0) {
            let shorter = Model.exactCopyProbability(length: length, errorRate: 0.02)
            let longer = Model.exactCopyProbability(length: length + 10, errorRate: 0.02)
            precondition(longer < shorter, "longer molecules are copied exactly less often")
        }
        print("Replicator error threshold checks passed.")
    }
}
