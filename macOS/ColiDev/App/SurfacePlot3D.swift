import Foundation

/// Triangle mesh of a surface z = f(x, y) over a square domain, in mathematical coordinates (z is height).
/// The scene layer only converts coordinates and colors; all geometry lives here so it can be verified.
/// Сетка поверхности z = f(x, y) в математических координатах; сцена только переводит её в SceneKit.
struct SurfaceMesh: Equatable {
    let positions: [SIMD3<Double>]
    let normals: [SIMD3<Double>]
    /// Height mapped to 0...1 symmetrically around z = 0, so 0.5 always means z = 0.
    let normalizedHeights: [Double]
    let triangleIndices: [Int32]
    /// Pairs of indices that draw every `gridStride`-th row and column as reading lines.
    let gridLineIndices: [Int32]
    let resolution: Int
    let heightLimit: Double
}

enum SurfacePlot3D {
    static func mesh(
        domain: ClosedRange<Double>,
        resolution: Int,
        gridStride: Int = 4,
        function: (Double, Double) -> Double,
        gradient: (Double, Double) -> SIMD2<Double>
    ) -> SurfaceMesh? {
        guard resolution >= 1, resolution <= 400, gridStride >= 1,
              domain.lowerBound.isFinite, domain.upperBound.isFinite,
              domain.upperBound > domain.lowerBound else { return nil }

        let step = (domain.upperBound - domain.lowerBound) / Double(resolution)
        let side = resolution + 1
        var positions: [SIMD3<Double>] = []
        var normals: [SIMD3<Double>] = []
        positions.reserveCapacity(side * side)
        normals.reserveCapacity(side * side)

        for row in 0..<side {
            let y = domain.lowerBound + Double(row) * step
            for column in 0..<side {
                let x = domain.lowerBound + Double(column) * step
                let z = function(x, y)
                let slope = gradient(x, y)
                guard z.isFinite, slope.x.isFinite, slope.y.isFinite else { return nil }
                positions.append(SIMD3(x, y, z))
                // The upward normal of z = f(x, y) is (-f_x, -f_y, 1), normalized.
                let normal = SIMD3(-slope.x, -slope.y, 1.0)
                normals.append(normal / length(normal))
            }
        }

        let heightLimit = max(positions.map { abs($0.z) }.max() ?? 0, 1e-9)
        let normalizedHeights = positions.map { 0.5 + 0.5 * $0.z / heightLimit }

        var triangles: [Int32] = []
        triangles.reserveCapacity(resolution * resolution * 6)
        for row in 0..<resolution {
            for column in 0..<resolution {
                let a = Int32(row * side + column)
                let b = a + 1
                let c = a + Int32(side)
                let d = c + 1
                // Counter-clockwise when viewed from above, so faces point up.
                triangles += [a, b, d, a, d, c]
            }
        }

        var gridLines: [Int32] = []
        for row in stride(from: 0, through: resolution, by: gridStride) {
            for column in 0..<resolution {
                let a = Int32(row * side + column)
                gridLines += [a, a + 1]
            }
        }
        for column in stride(from: 0, through: resolution, by: gridStride) {
            for row in 0..<resolution {
                let a = Int32(row * side + column)
                gridLines += [a, a + Int32(side)]
            }
        }

        return SurfaceMesh(
            positions: positions,
            normals: normals,
            normalizedHeights: normalizedHeights,
            triangleIndices: triangles,
            gridLineIndices: gridLines,
            resolution: resolution,
            heightLimit: heightLimit
        )
    }

    static func length(_ vector: SIMD3<Double>) -> Double {
        (vector * vector).sum().squareRoot()
    }
}

/// The lesson's problem in 3D: maximize f(x, y) = xy on the unit circle g(x, y) = x² + y² = 1.
/// Задача урока в 3D: экстремумы f(x, y) = xy на единичной окружности x² + y² = 1.
enum LagrangeSurfaceModel {
    static let domain: ClosedRange<Double> = -1.2...1.2

    static func objective(_ x: Double, _ y: Double) -> Double { x * y }
    static func objectiveGradient(_ x: Double, _ y: Double) -> SIMD2<Double> { SIMD2(y, x) }
    static func constraintGradient(_ x: Double, _ y: Double) -> SIMD2<Double> { SIMD2(2 * x, 2 * y) }

    static func surfaceMesh(resolution: Int = 48) -> SurfaceMesh? {
        SurfacePlot3D.mesh(
            domain: domain,
            resolution: resolution,
            function: objective,
            gradient: objectiveGradient
        )
    }

    /// Points where the constraint cylinder cuts the surface: (cos t, sin t, cos t · sin t).
    static func constraintCurve(samples: Int) -> [SIMD3<Double>] {
        guard samples >= 3 else { return [] }
        return (0...samples).map { index in
            let angle = Double(index) / Double(samples) * 2 * Double.pi
            let x = cos(angle)
            let y = sin(angle)
            return SIMD3(x, y, objective(x, y))
        }
    }

    /// Angle between ∇f and ∇g in degrees (0...180). Lagrange's condition ∇f = λ∇g holds exactly
    /// when the gradients are parallel: 0° gives λ > 0, 180° gives λ < 0.
    /// Угол между ∇f и ∇g в градусах; условие Лагранжа выполняется, когда он равен 0° или 180°.
    static func gradientAngleDegrees(x: Double, y: Double) -> Double? {
        let f = objectiveGradient(x, y)
        let g = constraintGradient(x, y)
        let fLength = (f * f).sum().squareRoot()
        let gLength = (g * g).sum().squareRoot()
        guard fLength > 1e-12, gLength > 1e-12 else { return nil }
        let cosine = max(-1, min(1, (f * g).sum() / (fLength * gLength)))
        return acos(cosine) * 180 / Double.pi
    }

    /// λ from ∇f = λ∇g, defined only where the gradients are parallel.
    // acos loses precision near ±1, so exact parallels can read as ~1e-6°; 1e-4° stays far below
    // the lab's 1° slider step. / acos теряет точность около ±1, поэтому допуск 1e-4°.
    static func lagrangeMultiplier(x: Double, y: Double, toleranceDegrees: Double = 1e-4) -> Double? {
        guard let angle = gradientAngleDegrees(x: x, y: y),
              angle <= toleranceDegrees || angle >= 180 - toleranceDegrees else { return nil }
        let f = objectiveGradient(x, y)
        let g = constraintGradient(x, y)
        return (f * g).sum() / (g * g).sum()
    }
}
