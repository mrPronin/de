"""Module for working with German verb data."""

from pathlib import Path
from typing import Dict, List, Optional, Any

import yaml


def get_data_dir() -> Path:
    """Get the directory where verb data files are stored."""
    # First, try to find the files relative to this module
    module_dir = Path(__file__).parent
    data_dir = module_dir / "data"

    # If that doesn't exist, use the current directory
    if not data_dir.exists():
        data_dir = Path.cwd() / "verben"

    return data_dir


def load_verb_data(
    filename: str = "irregular-verbs-a1.yaml"
) -> Dict[str, Any]:
    """Load verb data from a YAML file.

    Args:
        filename: Path to the YAML file to load.

    Returns:
        Dictionary containing the parsed YAML data.
    """
    # Try the path as provided directly
    direct_path = Path(filename)
    if direct_path.exists():
        with open(direct_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # Try relative to the data directory
    data_dir = get_data_dir()
    yaml_path = data_dir / filename
    if yaml_path.exists():
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # Try just the filename in the verben directory
    if "/" in filename or "\\" in filename:
        # Extract just the filename if a path was provided
        base_filename = Path(filename).name
        verben_path = Path("verben") / base_filename
        if verben_path.exists():
            with open(verben_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)

    # Try in the verben directory
    verben_path = Path("verben") / filename
    if verben_path.exists():
        with open(verben_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # Try in the current directory
    current_path = Path.cwd() / filename
    if current_path.exists():
        with open(current_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # If we get here, the file wasn't found
    raise FileNotFoundError(
        f"Verb data file not found: {filename}. "
        f"Searched in: {direct_path}, {yaml_path}, "
        f"{verben_path}, {current_path}"
    )


def get_verb_by_id(
    verb_id: int, data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Get a verb by its ID.

    Args:
        verb_id: The ID of the verb to retrieve.
        data: Pre-loaded verb data (optional)

    Returns:
        Dictionary containing the verb data.
    """
    if data is None:
        data = load_verb_data()

    for verb in data["verbs"]:
        if verb["id"] == verb_id:
            return verb

    raise ValueError(f"No verb found with ID {verb_id}")


def get_verb_by_infinitive(
    infinitive: str, data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Get a verb by its infinitive form.

    Args:
        infinitive: The infinitive form of the verb to retrieve.
        data: Pre-loaded verb data (optional)

    Returns:
        Dictionary containing the verb data.
    """
    if data is None:
        data = load_verb_data()

    for verb in data["verbs"]:
        if verb["infinitiv"].lower() == infinitive.lower():
            return verb

    raise ValueError(f"No verb found with infinitive '{infinitive}'")


def format_verb_display(verb: Dict[str, Any]) -> str:
    """Format a verb for display."""
    result = []
    result.append(f"Verb: {verb['infinitiv']} ({verb['person3']})")
    result.append("-" * 40)
    result.append(f"Präteritum: {verb['präteritum']}")
    result.append(f"Partizip II: {verb['partizip']}")
    result.append(f"English: {verb['translations']['english']}")
    result.append(f"Ukrainian: {verb['translations']['ukrainian']}")

    # Handle the simplified examples format
    if verb.get("examples") and verb["examples"].strip():
        result.append("\nExamples:")
        result.append("-" * 40)

        # Split examples by semicolons and display each on a new line
        examples = verb["examples"].split(";")
        for example in examples:
            if example.strip():
                result.append(example.strip())

    return "\n".join(result)


def list_all_verbs(
    data: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Get a list of all verbs.

    Args:
        data: Pre-loaded verb data (optional)

    Returns:
        List of dictionaries containing verb data.
    """
    if data is None:
        data = load_verb_data()

    return data["verbs"]
