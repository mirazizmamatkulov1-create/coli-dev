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
