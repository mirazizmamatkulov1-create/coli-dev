import Foundation

@main
enum StudyProgressDecodingVerification {
    // Shape returned by the bundled backend for GET /learning/progress (learning_progress.py):
    // knowledge checks are stored compactly as {task_type, passed, error_categories?, item_id?}.
    // Форма ответа встроенного backend: проверки знаний хранятся без полей попытки.
    static let backendEvidenceJSON = """
    [
      {"lesson_id": "biology.biomolecules_and_building_blocks", "assessment_count": 1,
       "task_type_counts": {"interactive_practice": 1}, "passed_task_type_counts": {}, "error_category_counts": {},
       "latest_assessment": {"attempts": 1, "first_try_correct": true, "hints_used": 0,
         "item_id": "biology.biomolecules_and_building_blocks.classify_starch", "task_type": "interactive_practice"},
       "latest_at": "2026-10-25T15:39:28Z"},
      {"lesson_id": "biology.mendelian_inheritance", "assessment_count": 3,
       "task_type_counts": {"knowledge_check": 3}, "passed_task_type_counts": {}, "error_category_counts": {},
       "latest_assessment": {"passed": false, "task_type": "knowledge_check"},
       "latest_at": "2026-10-17T22:34:13Z"},
      {"lesson_id": "physics.oscillations_and_waves", "assessment_count": 2,
       "task_type_counts": {"knowledge_check": 2}, "passed_task_type_counts": {"knowledge_check": 1},
       "error_category_counts": {"foundation": 1},
       "latest_assessment": {"passed": true, "task_type": "knowledge_check", "error_categories": ["foundation"],
         "item_id": "physics.oscillations_and_waves.knowledge_check"},
       "latest_at": "2026-10-25T16:28:03Z"}
    ]
    """

    static func main() {
        let decoder = JSONDecoder()

        let summaries: [StudyAssessmentEvidenceSummary]
        do {
            summaries = try decoder.decode([StudyAssessmentEvidenceSummary].self, from: Data(backendEvidenceJSON.utf8))
        } catch {
            fatalError("Backend evidence with compact knowledge checks must decode, otherwise the whole progress snapshot is dropped after relaunch. / Свидетельства со сжатыми проверками знаний должны декодироваться, иначе после перезапуска теряется весь снимок прогресса: \(error)")
        }
        precondition(summaries.count == 3, "All evidence summaries must decode. / Должны декодироваться все сводки.")

        let failedCheck = summaries[1].latestAssessment
        precondition(
            failedCheck.taskType == "knowledge_check"
                && failedCheck.passed == false
                && failedCheck.attempts == 1
                && failedCheck.firstTryCorrect == false
                && failedCheck.hintsUsed == 0,
            "A compact failed knowledge check must decode as one unsuccessful attempt. / Сжатая неудачная проверка должна читаться как одна неудачная попытка."
        )
        let passedCheck = summaries[2].latestAssessment
        precondition(
            passedCheck.passed == true
                && passedCheck.firstTryCorrect
                && passedCheck.errorCategories == [.foundation]
                && passedCheck.itemID == "physics.oscillations_and_waves.knowledge_check",
            "A compact passed knowledge check must keep its result, error categories, and item ID. / Сжатая успешная проверка должна сохранить результат, категории ошибок и ID задания."
        )
        let practice = summaries[0].latestAssessment
        precondition(
            practice.taskType == "interactive_practice" && practice.attempts == 1 && practice.passed == nil,
            "Full interactive evidence must still decode unchanged. / Полные данные интерактивных заданий должны читаться без изменений."
        )

        let interactiveWithoutAttempts = Data(#"{"task_type": "interactive_prediction", "passed": true}"#.utf8)
        precondition(
            (try? decoder.decode(StudyAssessmentEvidence.self, from: interactiveWithoutAttempts)) == nil,
            "Interactive evidence without attempt data must stay invalid. / Интерактивные данные без попытки должны оставаться недопустимыми."
        )
        let checkWithoutResult = Data(#"{"task_type": "knowledge_check"}"#.utf8)
        precondition(
            (try? decoder.decode(StudyAssessmentEvidence.self, from: checkWithoutResult)) == nil,
            "A knowledge check without a pass result must stay invalid. / Проверка знаний без результата должна оставаться недопустимой."
        )

        let coverage = StudyKnowledgeEvidenceCoverage(
            roadmaps: [
                StudyRoadmap(subjectID: "physics", lessonResources: ["oscillations_and_waves"]),
                StudyRoadmap(subjectID: "biology", lessonResources: ["mendelian_inheritance", "biomolecules_and_building_blocks"]),
            ],
            records: [],
            additionalEvidence: summaries
        )
        precondition(
            coverage.totalTopicCount == 3 && coverage.topicsWithChecks == 3,
            "Decoded backend evidence must count on the Today screen after relaunch. / Свидетельства из backend должны учитываться на экране «Сегодня» после перезапуска."
        )

        let compactEvent = Data(#"{"event_id": "e1", "lesson_id": "physics.oscillations_and_waves", "assessment": {"task_type": "knowledge_check", "passed": true}}"#.utf8)
        guard let event = try? decoder.decode(StudyAssessmentEvent.self, from: compactEvent) else {
            fatalError("Queued compact knowledge-check events must still decode. / Сжатые события проверки в очереди должны по-прежнему читаться.")
        }
        guard let encoded = try? JSONEncoder().encode(event),
              let roundTrip = try? decoder.decode(StudyAssessmentEvent.self, from: encoded) else {
            fatalError("Assessment events must round-trip through the pending queue. / События проверки должны сохраняться и читаться из очереди.")
        }
        precondition(
            roundTrip.assessment == event.assessment && roundTrip.lessonID == event.lessonID,
            "A round-tripped event must keep its assessment. / Событие после сохранения должно сохранить данные проверки."
        )

        print("Study progress decoding verification passed / Проверка чтения прогресса пройдена")
    }
}
