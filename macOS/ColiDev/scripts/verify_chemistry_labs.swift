import Foundation

@main
enum ChemistryLabsVerification {
    static func close(_ value: Double, _ expected: Double) -> Bool {
        abs(value - expected) <= expected * 1e-9
    }

    static func main() {
        // pH scale: lesson question and practice tasks.
        precondition(close(PHScaleModel.hydrogenRatio(pH: 4, comparedTo: 6), 100), "pH 4 has 100 times more H⁺ than pH 6")
        precondition(close(PHScaleModel.hydrogenRatio(pH: 3, comparedTo: 7), 10_000), "pH 3 vs pH 7")
        precondition(close(PHScaleModel.hydrogenRatio(pH: 8, comparedTo: 5), 0.001), "pH 8 has 1000 times fewer H⁺ than pH 5")
        precondition(close(PHScaleModel.hydrogenConcentration(pH: 7), 1e-7), "pure water at 25 °C")
        precondition(PHScaleModel.acidity(pH: 3) == .acidic)
        precondition(PHScaleModel.acidity(pH: 7) == .neutral)
        precondition(PHScaleModel.acidity(pH: 11) == .basic)
        for pH in stride(from: 0.0, to: 14.0, by: 1.0) {
            precondition(close(PHScaleModel.hydrogenConcentration(pH: pH) / PHScaleModel.hydrogenConcentration(pH: pH + 1), 10), "each unit is a factor of 10")
        }

        // Molecule builder: valence from outer electrons.
        typealias Model = MoleculeBuilderModel
        let expected: [(Model.CentralAtom, outer: Int, valence: Int, formula: String)] = [
            (.hydrogen, 1, 1, "H₂"),
            (.oxygen, 6, 2, "H₂O"),
            (.nitrogen, 5, 3, "NH₃"),
            (.carbon, 4, 4, "CH₄"),
        ]
        for (atom, outer, valence, formula) in expected {
            precondition(atom.outerElectrons == outer, "\(atom.rawValue) outer electrons")
            precondition(atom.valence == valence, "\(atom.rawValue) valence")
            precondition(Model.status(central: atom, hydrogens: valence) == .complete)
            precondition(Model.formula(central: atom, hydrogens: valence) == formula, "\(atom.rawValue) formula")
            precondition(Model.moleculeKey(central: atom, hydrogens: valence) == "lab.molecule.name.\(atom.rawValue)")
        }
        precondition(Model.status(central: .carbon, hydrogens: 2) == .missingBonds(2))
        precondition(Model.status(central: .oxygen, hydrogens: 3) == .tooManyBonds(1), "oxygen has only two free bonds")
        precondition(Model.moleculeKey(central: .nitrogen, hydrogens: 4) == nil)
        precondition(Model.formula(central: .oxygen, hydrogens: 1) == "HO")
        precondition(Model.formula(central: .carbon, hydrogens: 0) == "C")
        print("Chemistry lab model checks passed.")
    }
}
