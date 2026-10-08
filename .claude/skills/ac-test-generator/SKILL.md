---
name: ac-test-generator
description: Generates AC-tagged pytest test cases for feature acceptance criteria.
---

# AC Test Generator Skill

## Purpose & Usage
Use this skill to convert Given-When-Then criteria from specs into tagged pytest tests (TECH-04).

## Standard Marker Format
```python
@pytest.mark.ac("AC-01")
def test_customer_registration_active_state():
    ...
```
