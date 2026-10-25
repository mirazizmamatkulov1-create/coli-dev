from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "macOS" / "ColiDev" / "ColiDev.xcodeproj" / "project.pbxproj"
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
RUNPATH = 'LD_RUNPATH_SEARCH_PATHS = ("$(inherited)", "@executable_path/../Frameworks");'


def test_both_app_configurations_search_the_embedded_frameworks_folder() -> None:
    lines = PROJECT.read_text(encoding="utf-8").splitlines()
    app_configurations = [
        line for line in lines
        if line.lstrip().startswith(("AC00000000000000000001 /* Debug */", "AC00000000000000000002 /* Release */"))
    ]
    assert len(app_configurations) == 2
    # Without this runpath dyld cannot find @rpath/Sparkle.framework and the app aborts at launch.
    assert all(RUNPATH in line for line in app_configurations)


def test_ci_launches_the_app_without_xcode_framework_paths() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    step = workflow.split("- name: Verify the app launches outside Xcode", 1)[1].split("- name: Package macOS app archive", 1)[0]
    assert 'env -i HOME="$HOME"' in step
    assert "@executable_path/../Frameworks" in step
    assert "Sparkle.framework/Versions/B/Sparkle" in step
    assert workflow.index("Verify the app launches outside Xcode") < workflow.index("- name: Package macOS app archive")
