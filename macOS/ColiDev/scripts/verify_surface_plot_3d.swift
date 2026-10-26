import Foundation

@main
enum SurfacePlot3DVerification {
    static func main() {
        let resolution = 24
        guard let mesh = LagrangeSurfaceModel.surfaceMesh(resolution: resolution) else {
            fatalError("The xy surface mesh must build. / Сетка поверхности xy должна строиться.")
        }

        let side = resolution + 1
        precondition(
            mesh.positions.count == side * side
                && mesh.normals.count == side * side
                && mesh.normalizedHeights.count == side * side
                && mesh.triangleIndices.count == resolution * resolution * 6,
            "Mesh sizes must match the grid. / Размеры сетки должны соответствовать разбиению."
        )
        precondition(
            mesh.triangleIndices.allSatisfy { $0 >= 0 && Int($0) < mesh.positions.count }
                && mesh.gridLineIndices.allSatisfy { $0 >= 0 && Int($0) < mesh.positions.count }
                && mesh.gridLineIndices.count % 2 == 0,
            "Every index must point at a vertex. / Каждый индекс должен указывать на вершину."
        )

        for (position, normal) in zip(mesh.positions, mesh.normals) {
            precondition(
                abs(position.z - position.x * position.y) < 1e-12,
                "Every vertex must lie on z = xy. / Каждая вершина должна лежать на z = xy."
            )
            precondition(
                abs(SurfacePlot3D.length(normal) - 1) < 1e-12 && normal.z > 0,
                "Normals must be unit length and point up. / Нормали должны быть единичными и смотреть вверх."
            )
            // Tangents of z = xy: (1, 0, y) and (0, 1, x); the normal must be perpendicular to both.
            let tangentX = SIMD3(1.0, 0.0, position.y)
            let tangentY = SIMD3(0.0, 1.0, position.x)
            precondition(
                abs((normal * tangentX).sum()) < 1e-12 && abs((normal * tangentY).sum()) < 1e-12,
                "Normals must be perpendicular to the surface. / Нормали должны быть перпендикулярны поверхности."
            )
        }

        precondition(
            mesh.normalizedHeights.allSatisfy { (0...1).contains($0) }
                && abs(mesh.heightLimit - 1.2 * 1.2) < 1e-12,
            "Heights must map to 0...1 around the largest |z|. / Высоты должны укладываться в 0...1."
        )
        let origin = mesh.positions.firstIndex { abs($0.x) < 1e-12 && abs($0.y) < 1e-12 }!
        precondition(
            abs(mesh.normalizedHeights[origin] - 0.5) < 1e-12,
            "z = 0 must map to the middle of the color scale. / z = 0 — середина цветовой шкалы."
        )

        // First triangle must face up (counter-clockwise from above).
        let a = mesh.positions[Int(mesh.triangleIndices[0])]
        let b = mesh.positions[Int(mesh.triangleIndices[1])]
        let c = mesh.positions[Int(mesh.triangleIndices[2])]
        let edge1 = b - a
        let edge2 = c - a
        let faceZ = edge1.x * edge2.y - edge1.y * edge2.x
        precondition(faceZ > 0, "Triangles must face up. / Треугольники должны смотреть вверх.")

        let curve = LagrangeSurfaceModel.constraintCurve(samples: 72)
        precondition(curve.count == 73, "The closed curve needs samples + 1 points. / Замкнутой кривой нужно samples + 1 точек.")
        for point in curve {
            precondition(
                abs(point.x * point.x + point.y * point.y - 1) < 1e-12
                    && abs(point.z - point.x * point.y) < 1e-12,
                "Curve points must lie on both the circle and the surface. / Точки кривой должны лежать и на окружности, и на поверхности."
            )
        }
        precondition(LagrangeSurfaceModel.constraintCurve(samples: 2).isEmpty, "Too few samples give no curve. / Слишком мало точек — кривой нет.")

        func point(degrees: Double) -> (Double, Double) {
            let angle = degrees * Double.pi / 180
            return (cos(angle), sin(angle))
        }

        for (degrees, expectedLambda, expectedAngle) in [(45.0, 0.5, 0.0), (225.0, 0.5, 0.0), (135.0, -0.5, 180.0), (315.0, -0.5, 180.0)] {
            let (x, y) = point(degrees: degrees)
            guard let angle = LagrangeSurfaceModel.gradientAngleDegrees(x: x, y: y),
                  let lambda = LagrangeSurfaceModel.lagrangeMultiplier(x: x, y: y) else {
                fatalError("Stationary point at \(degrees)° must satisfy ∇f = λ∇g. / Стационарная точка должна удовлетворять ∇f = λ∇g.")
            }
            precondition(
                abs(angle - expectedAngle) < 1e-4 && abs(lambda - expectedLambda) < 1e-9,
                "At \(degrees)° gradients must be parallel with λ = \(expectedLambda). / Градиенты должны быть параллельны."
            )
            // λ equals the objective xy on the unit circle, matching the existing 2D model.
            let model = ConstrainedOptimizationPoint(angleRadians: degrees * Double.pi / 180)!
            precondition(
                abs((model.lagrangeMultiplier ?? .nan) - lambda) < 1e-9,
                "3D and 2D models must agree on λ. / 3D- и 2D-модели должны давать одинаковый λ."
            )
        }

        let (x30, y30) = point(degrees: 30)
        guard let angle30 = LagrangeSurfaceModel.gradientAngleDegrees(x: x30, y: y30) else {
            fatalError("Gradient angle must exist away from the origin. / Угол между градиентами должен существовать.")
        }
        // ∇f = (y, x) points at 90° − θ and ∇g = (2x, 2y) at θ, so they differ by |90° − 2θ|.
        precondition(
            abs(angle30 - 30) < 1e-9 && LagrangeSurfaceModel.lagrangeMultiplier(x: x30, y: y30) == nil,
            "At 30° the gradients differ by 30° and there is no λ. / На 30° градиенты расходятся на 30°, λ нет."
        )
        precondition(
            LagrangeSurfaceModel.gradientAngleDegrees(x: 0, y: 0) == nil,
            "At the origin the gradients vanish. / В начале координат градиенты нулевые."
        )

        precondition(
            SurfacePlot3D.mesh(domain: -1...1, resolution: 0, function: { $0 + $1 }, gradient: { _, _ in SIMD2(1, 1) }) == nil
                && SurfacePlot3D.mesh(domain: -1...1, resolution: 4, function: { _, _ in .nan }, gradient: { _, _ in SIMD2(0, 0) }) == nil,
            "Invalid meshes must be rejected. / Недопустимые сетки должны отклоняться."
        )

        print("Surface plot 3D verification passed / Проверка 3D-поверхности пройдена")
    }
}
