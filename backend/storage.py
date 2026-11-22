import json
import os
from copy import deepcopy
from backend.templates import CV_TEMPLATES, LETTER_TEMPLATES

DATA_DIR = "data"
PROFILE_PATH = os.path.join(DATA_DIR, "user_profile.json")


def _default_data() -> dict:
    return {
        "master_history": "",
        "custom_cv_templates": deepcopy(CV_TEMPLATES),
        "custom_letter_templates": deepcopy(LETTER_TEMPLATES),
    }


def load_user_data() -> dict:
    """Loads saved career history and custom templates from disk, falling back to defaults."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PROFILE_PATH):
        data = _default_data()
        save_user_data(data)
        return data

    try:
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            stored = json.load(f)
    except (json.JSONDecodeError, OSError):
        return _default_data()

    # Merge with defaults so any newly added template keys remain available
    merged = _default_data()
    merged["master_history"] = stored.get("master_history", "")
    merged["custom_cv_templates"].update(stored.get("custom_cv_templates", {}))
    merged["custom_letter_templates"].update(stored.get("custom_letter_templates", {}))
    return merged


def save_user_data(data: dict) -> None:
    """Persists user profile data to disk."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_master_history(history_text: str) -> None:
    data = load_user_data()
    data["master_history"] = history_text
    save_user_data(data)


def get_active_cv_templates() -> dict:
    return load_user_data()["custom_cv_templates"]


def get_active_letter_templates() -> dict:
    return load_user_data()["custom_letter_templates"]


def update_cv_template(job_type: str, analysis_focus: str, structure: str) -> None:
    data = load_user_data()
    data["custom_cv_templates"][job_type]["analysis_focus"] = analysis_focus
    data["custom_cv_templates"][job_type]["structure"] = structure
    save_user_data(data)


def update_letter_template(doc_type: str, structure: str) -> None:
    data = load_user_data()
    data["custom_letter_templates"][doc_type]["structure"] = structure
    save_user_data(data)


def reset_templates_to_default() -> None:
    data = load_user_data()
    data["custom_cv_templates"] = deepcopy(CV_TEMPLATES)
    data["custom_letter_templates"] = deepcopy(LETTER_TEMPLATES)
    save_user_data(data)
