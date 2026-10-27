import Foundation

/// The pH scale for the chemistry water lesson: pH = −log[H⁺] (OpenStax Chemistry 2e, 14.2).
/// Neutral pH 7 holds for pure water at 25 °C; the lab stays at that temperature.
enum PHScaleModel {
    static let pHRange = 0.0...14.0
    static let neutralPH = 7.0

    enum Acidity: Equatable {
        case acidic, neutral, basic
    }

    /// Hydrogen-ion concentration in mol/L.
    static func hydrogenConcentration(pH: Double) -> Double {
        pow(10, -pH)
    }

    /// How many times more H⁺ a solution with `pH` has than one with `reference`; below 1 means fewer.
    static func hydrogenRatio(pH: Double, comparedTo reference: Double) -> Double {
        pow(10, reference - pH)
    }

    static func acidity(pH: Double) -> Acidity {
        if pH < neutralPH { return .acidic }
        if pH > neutralPH { return .basic }
        return .neutral
    }
}

/// Simple molecules built from one central atom and hydrogen atoms joined by single covalent bonds,
/// for the chemistry bonding lesson. Valence follows the outer-electron count (OpenStax Chemistry 2e, 7.2).
enum MoleculeBuilderModel {
    enum CentralAtom: String, CaseIterable, Identifiable {
        case hydrogen = "H"
        case oxygen = "O"
        case nitrogen = "N"
        case carbon = "C"

        var id: String { rawValue }

        /// Electrons in the neutral atom: its atomic number.
        var electrons: Int {
            switch self {
            case .hydrogen: return 1
            case .oxygen: return 8
            case .nitrogen: return 7
            case .carbon: return 6
            }
        }

        /// Outer-shell electrons: the first shell holds at most two.
        var outerElectrons: Int { electrons <= 2 ? electrons : electrons - 2 }

        /// Single bonds needed to fill the outer shell: two electrons for hydrogen, eight otherwise.
        var valence: Int { (self == .hydrogen ? 2 : 8) - outerElectrons }

        var nameKey: String { "lab.molecule.atom.\(rawValue)" }
    }

    enum Status: Equatable {
        case missingBonds(Int)
        case complete
        case tooManyBonds(Int)
    }

    static let hydrogenRange = 0...4

    static func status(central: CentralAtom, hydrogens: Int) -> Status {
        let difference = hydrogens - central.valence
        if difference < 0 { return .missingBonds(-difference) }
        if difference > 0 { return .tooManyBonds(difference) }
        return .complete
    }

    /// Formula with Unicode subscripts, e.g. "CH₄"; two hydrogen atoms make "H₂".
    static func formula(central: CentralAtom, hydrogens: Int) -> String {
        if central == .hydrogen {
            return hydrogens == 0 ? "H" : "H" + subscriptDigits(hydrogens + 1)
        }
        guard hydrogens > 0 else { return central.rawValue }
        let hydrogenPart = "H" + (hydrogens == 1 ? "" : subscriptDigits(hydrogens))
        // By convention water is written with hydrogen first (H₂O), ammonia and methane with the central atom first.
        return central == .oxygen ? hydrogenPart + central.rawValue : central.rawValue + hydrogenPart
    }

    /// Name key of the finished molecule, if the combination is complete.
    static func moleculeKey(central: CentralAtom, hydrogens: Int) -> String? {
        guard status(central: central, hydrogens: hydrogens) == .complete else { return nil }
        return "lab.molecule.name.\(central.rawValue)"
    }

    private static func subscriptDigits(_ number: Int) -> String {
        let digits = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"]
        return String(number).compactMap { Int(String($0)) }.map { digits[$0] }.joined()
    }
}

/// Energy profile of one reaction step for the catalysis lesson, at 25 °C.
/// ΔG and activation energy follow OpenStax Biology 2e 6.2 and 6.5; the rate factor uses the Arrhenius
/// equation k = A · e^(−Eₐ/RT) from Chemistry 2e 12.5, with the same factor A with and without a catalyst.
enum ReactionEnergyModel {
    static let gasConstant = 8.314
    static let temperature = 298.0
    static let freeEnergyRange = -60.0...60.0
    static let activationRange = 40.0...120.0
    static let loweringRange = 0.0...40.0

    enum Kind: Equatable {
        case exergonic, endergonic, balanced
    }

    static func kind(freeEnergyChange: Double) -> Kind {
        if freeEnergyChange < 0 { return .exergonic }
        if freeEnergyChange > 0 { return .endergonic }
        return .balanced
    }

    /// The barrier peak must lie above both reactants (0) and products (ΔG).
    static func minimumBarrier(freeEnergyChange: Double) -> Double {
        max(freeEnergyChange, 0)
    }

    static func uncatalyzedBarrier(activation: Double, freeEnergyChange: Double) -> Double {
        max(activation, minimumBarrier(freeEnergyChange: freeEnergyChange))
    }

    /// Activation energy with the catalyst, in kJ/mol; it cannot drop below the minimum barrier.
    static func catalyzedBarrier(activation: Double, lowering: Double, freeEnergyChange: Double) -> Double {
        max(uncatalyzedBarrier(activation: activation, freeEnergyChange: freeEnergyChange) - max(lowering, 0),
            minimumBarrier(freeEnergyChange: freeEnergyChange))
    }

    /// How many times faster the catalysed reaction runs: e^(ΔEₐ/RT) with ΔEₐ in kJ/mol.
    static func speedup(activation: Double, lowering: Double, freeEnergyChange: Double) -> Double {
        let before = uncatalyzedBarrier(activation: activation, freeEnergyChange: freeEnergyChange)
        let after = catalyzedBarrier(activation: activation, lowering: lowering, freeEnergyChange: freeEnergyChange)
        return exp((before - after) * 1000 / (gasConstant * temperature))
    }

    /// Smooth sketch of energy along the reaction path, x from 0 (reactants) to 1 (products).
    /// Each half rises or falls monotonically, so the highest point is exactly `barrier` at x = 0.5.
    static func profileEnergy(at x: Double, barrier: Double, freeEnergyChange: Double) -> Double {
        let t = min(max(x, 0), 1)
        func smoothstep(_ u: Double) -> Double { u * u * (3 - 2 * u) }
        if t <= 0.5 { return barrier * smoothstep(2 * t) }
        return barrier + (freeEnergyChange - barrier) * smoothstep(2 * t - 1)
    }
}
