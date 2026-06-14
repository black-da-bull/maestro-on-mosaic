"""Budget profiles for the Triad validator.

Each profile encodes a specific Maestro version's character budgets for the
four Suno-facing fields. Adding a new profile means adding a dataclass entry
here — never touching the check logic.

Sources:
- v4_2_3: master.json (summary_chars_limit=1000, macro_chars_limit=4800)
- v4_5_2: maestro.md INV-14 (Show Summary ≤ 1000, Macro Lyric Prompt ≤ 4990)
- v0_spec: maestro_v0.md §1 mount manifest budget_constraints
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Range:
    """Inclusive character-count range. `min=None` means no lower bound."""
    min: int | None
    max: int


@dataclass(frozen=True)
class Profile:
    """Character budgets for one Triad version."""
    name: str
    show_summary: Range
    creative_ust: Range
    persona_profile: Range | None  # not present in v4_2_3
    persona_style: Range | None    # not present in v4_2_3


PROFILES: dict[str, Profile] = {
    "v4_2_3": Profile(
        name="v4.2.3",
        show_summary=Range(min=None, max=1000),
        creative_ust=Range(min=None, max=4800),
        persona_profile=None,
        persona_style=None,
    ),
    "v4_5_2": Profile(
        name="v4.5.2",
        show_summary=Range(min=None, max=1000),
        creative_ust=Range(min=None, max=4990),
        persona_profile=None,
        persona_style=None,
    ),
    "v0_spec": Profile(
        name="v0",
        show_summary=Range(min=950, max=1000),
        creative_ust=Range(min=4950, max=4995),
        persona_profile=Range(min=1950, max=1995),
        persona_style=Range(min=None, max=150),
    ),
}


def get_profile(name: str) -> Profile:
    """Resolve a profile by name, raising a clear error on miss."""
    if name not in PROFILES:
        raise KeyError(
            f"Unknown profile {name!r}. Known profiles: {sorted(PROFILES)}"
        )
    return PROFILES[name]
