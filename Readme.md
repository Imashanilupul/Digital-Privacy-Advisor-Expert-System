# Digital Privacy Advisor — Expert System

A small rule-based expert system that evaluates a user's digital privacy and security posture and produces prioritized recommendations. The project is implemented in Python with a simple, testable inference engine and uses CLIPS rule files for an example knowledge base.

## What is an expert system? (properties and how this app fits)

An expert system emulates decision-making of a domain expert using a set of explicitly encoded rules and facts. Core properties:

- Knowledge base: domain knowledge encoded separately from code (rules, templates). In this app: `clips/knowledge_base.clp` and `clips/templates.clp`.
- Working memory (facts): the current situation described as facts. In this app: a `user-profile` fact from `clips/sample_facts.clp` (or user inputs collected by `InputHandler`).
- Inference engine: applies rules to facts to derive new facts/recommendations. In this app: CLIPS runtime (optional) and a pure-Python `InferenceEngine` in `src/inference_engine.py`.
- Reasoning strategy: we use forward chaining (data-driven). When facts match rule conditions, actions assert `recommendation` facts.
- Conflict resolution: when multiple rules are eligible, priority resolves order. In CLIPS, this can be managed with salience; in Python we encode a `priority` and `risk-score` to sort outputs.
- Explanation facility: the system can explain outcomes in human terms. In this app, each recommendation carries `message`, `details`, and `action`. You can extend this to include rule IDs for a why-trace.
- Uncertainty handling: many expert systems attach confidence/weights. Here we approximate with an additive `risk-score` per recommendation and compute an overall risk level.
- Separation of knowledge and control: rules (knowledge) live in CLIPS files; control/UI lives in Python, making knowledge editable without changing code.
- Modularity and maintainability: rules are small and focused; templates define a clear schema for facts and outputs.

### How this project maps properties to files

- Knowledge base: `clips/knowledge_base.clp`, `clips/templates.clp`
- Facts / Working memory: `clips/sample_facts.clp`; at runtime, facts can be asserted from user input
- Inference engine: `src/inference_engine.py` (Python), optional CLIPS runtime via `clipspy`
- Recommendations / Explanation: `deftemplate recommendation` with `message`, `details`, `action`; `src/output_handler.py` for sorting/summary
- Control and UI: `src/app_controller.py`, `gui/`

### Reasoning strategy (forward chaining)

Forward chaining starts from known facts and repeatedly fires rules whose conditions match those facts, asserting new facts (recommendations) along the way. Example excerpt from `clips/knowledge_base.clp`:

```clips
(defrule no-vpn-rule
	(user-profile (vpn no))
	=>
	(assert (recommendation
		(priority medium)
		(category "Network Security")
		(message "Consider using a VPN for all internet activity")
		(details "VPNs protect your privacy by hiding your IP address and encrypting traffic.")
		(action "Research and subscribe to a reputable VPN service")
		(risk-score 12))))
```

When the working memory contains `(user-profile (vpn no))`, this rule fires and asserts a `recommendation` fact capturing the explanation and action.

## Key ideas
- Facts describing a user's profile are represented as CLIPS facts (see `clips/sample_facts.clp`).
- Domain rules and recommendations are authored in CLIPS (`clips/knowledge_base.clp`) using templates defined in `clips/templates.clp`.
- A pure-Python inference engine (`src/inference_engine.py`) provides an alternative, testable rule implementation that the GUI and controller use when CLIPS is not required.
- `src/app_controller.py` wires input handling, inference, and output formatting for use by the (optional) GUI under `gui/`.

## Repository layout

- `clips/` — CLIPS rule files and templates
	- `templates.clp` — CLIPS deftemplate definitions
	- `knowledge_base.clp` — CLIPS rules that assert `recommendation` facts
	- `sample_facts.clp` — example facts used for testing
- `src/` — Python application code
	- `inference_engine.py` — Python rule-based inference implementation (used in tests)
	- `input_handler.py` — input validation and conversion
	- `output_handler.py` — formatting and ranking of recommendations
	- `app_controller.py` — top-level controller (ties together input, inference, output)
	- `main.py` — small runner for the application (see below)
- `gui/` — optional GUI components (PyQt/Tkinter, etc.)
- `tests/` — pytest tests for the repository
- `scripts/` — helper scripts (parsing, diagnostics)

## Setup

These commands assume Windows `cmd.exe`. Use similar commands on macOS / Linux (bash/zsh).

1. Create and activate a virtual environment

```bat
python -m venv .venv
.venv\Scripts\activate
```

2. Install development dependencies

There is no pinned `requirements.txt` in this repo by default. For testing and CLIPS support you may want:

```bat
pip install pytest
pip install clipspy    # optional: enables loading .clp files from Python tests
```

Add other dev tools as needed (flake8, mypy, black).

## Running the app (basic)

The repository provides a small runner in `src/main.py`. From the repository root run:

```bat
python -m src.main
```

This will use the Python `InferenceEngine` implementation which does not require CLIPS. If you want to exercise the CLIPS knowledge base directly, install `clipspy` (see above) and use the parser helper in `scripts/` or run the unit tests.

## Tests

Run the test suite with pytest from the repository root:

```bat
python -m pytest -q
```

Notes about tests
- `tests/test_clips.py` checks that the expected CLIPS files exist and, if `clipspy` is installed, attempts to load and run them. If `clipspy` is not installed the runtime portion of the test is skipped.
- The Python `InferenceEngine` has its own behavior tests (you can add more unit tests under `tests/` for edge cases).

## Working with CLIPS files

- Templates first: `clips/templates.clp` defines `deftemplate user-profile` and `deftemplate recommendation`. Templates must be loaded before any rules that use them.
- Rules: `clips/knowledge_base.clp` contains `defrule` forms that assert `recommendation` facts. Keep rules small and focused.
- Facts: `clips/sample_facts.clp` demonstrates asserting a `user-profile` fact and running the engine.

Common CLIPS pitfalls and tips
- Watch multislot binding syntax. Use `$?name` in the pattern to bind a multislot and use `?name` inside function calls such as `(length$ ?name)` in constraints.
- Ensure parentheses are balanced. Small mismatches lead to parser errors that include a file and line number when using `clipspy`.
- If you see parser errors in tests, run the diagnostics script to get a contextual snippet:

```bat
python scripts\parse_clips.py clips\knowledge_base.clp
```


## Contributing

- Add tests for any changes to `src/inference_engine.py` and for additional CLIPS files you add.
- Follow typical Python project conventions: run tests locally, keep commits small, and open PRs for review.

## Next improvements (ideas)

- Add `requirements.txt` and `dev-requirements.txt` to pin dependencies.
- Add a GitHub Actions workflow to run pytest and optionally install `clipspy` so CLIPS parser errors are caught on CI.
- Add more unit tests for `InferenceEngine` covering edge cases (empty inputs, unexpected types).
- Improve the GUI to allow editing facts and re-running the CLIPS engine interactively.



