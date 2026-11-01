"""
Week 5: Forward chaining experiment.

A small rule-based system that decides whether an AI model's output should be
flagged for human review. Forward chaining starts from known facts and keeps
applying if-then rules until nothing new can be concluded. The list of rules
that fired is the explanation for the decision.

Run from the repo root:
    python week-5/forward_chain.py | tee week-5/outputs.txt
"""

# Each rule: (rule id, set of conditions that must all be true, conclusion)
RULES = [
    ("R1", {"mentions_medication", "gives_dosage"}, "medical_advice"),
    ("R2", {"medical_advice"}, "needs_disclaimer"),
    ("R3", {"needs_disclaimer", "no_disclaimer"}, "missing_disclaimer"),
    ("R4", {"missing_disclaimer"}, "flag_for_review"),
    ("R5", {"mentions_weapon", "gives_instructions"}, "dangerous_instructions"),
    ("R6", {"dangerous_instructions"}, "flag_for_review"),
    ("R7", {"mentions_person", "includes_address"}, "privacy_risk"),
    ("R8", {"privacy_risk"}, "flag_for_review"),
    ("R9", {"flag_for_review", "user_is_minor"}, "escalate_to_human"),
    ("R10", {"medical_advice", "cites_sources"}, "lower_risk"),
]

# Starting facts describing different model outputs
SCENARIOS = {
    "Dosage advice with no disclaimer": {
        "mentions_medication", "gives_dosage", "no_disclaimer",
    },
    "Dosage advice with sources and a disclaimer": {
        "mentions_medication", "gives_dosage", "cites_sources",
    },
    "Someone's home address, shown to a minor": {
        "mentions_person", "includes_address", "user_is_minor",
    },
    "Harmless cooking answer": {
        "mentions_food",
    },
}


def forward_chain(initial_facts, rules):
    """Apply rules until a full pass adds no new facts."""
    facts = set(initial_facts)
    trace = []      # (rule id, conditions, conclusion) for each rule that fired
    passes = 0      # full sweeps through the rule list
    checks = 0      # individual rule checks
    changed = True
    while changed:
        changed = False
        passes += 1
        for rule_id, conditions, conclusion in rules:
            checks += 1
            if conditions <= facts and conclusion not in facts:
                facts.add(conclusion)
                trace.append((rule_id, conditions, conclusion))
                changed = True
    return facts, trace, passes, checks


def explain(fact, trace, initial_facts, depth=0):
    """Print a tree showing how a fact was derived, back to the starting facts."""
    indent = "    " * depth
    if fact in initial_facts:
        print(f"{indent}{fact} (given)")
        return
    for rule_id, conditions, conclusion in trace:
        if conclusion == fact:
            print(f"{indent}{fact} (by {rule_id})")
            for condition in sorted(conditions):
                explain(condition, trace, initial_facts, depth + 1)
            return


def main():
    for name, initial in SCENARIOS.items():
        print("=" * 60)
        print(f"Scenario: {name}")
        print(f"Starting facts: {sorted(initial)}")

        facts, trace, passes, checks = forward_chain(initial, RULES)

        print("\nRules fired, in order:")
        if trace:
            for rule_id, conditions, conclusion in trace:
                print(f"  {rule_id}: {' + '.join(sorted(conditions))} -> {conclusion}")
        else:
            print("  (none)")

        new_facts = sorted(facts - initial)
        print(f"\nNew conclusions: {new_facts if new_facts else 'none'}")
        print(f"Stats: {len(trace)} rules fired, {passes} passes, {checks} rule checks")

        if "escalate_to_human" in facts:
            decision = "escalate_to_human"
        elif "flag_for_review" in facts:
            decision = "flag_for_review"
        else:
            decision = None

        if decision:
            print(f"\nDecision: {decision.upper()}")
            print("Why:")
            explain(decision, trace, initial, depth=1)
        else:
            print("\nDecision: NO FLAG (no rule chain led to a flag)")
        print()


if __name__ == "__main__":
    main()