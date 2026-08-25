# Teacher report design

Date: 2026-08-25
Status: approved in chat; implementation pending written-spec review
Scope: PR #15 / Lot 8 of issue #7

## Purpose

The teacher-report layer turns one frozen, auditable evidence-profile run from PR #14 into a self-contained local HTML artifact for human inspection. It is a presentation and audit layer only. It must not retrain models, recalculate splits, select thresholds, infer mastery, recommend interventions, or claim pedagogical effectiveness.

The report supports two views:

1. an individual student-by-skill evidence view; and
2. an aggregate descriptive skill view.

Both views must preserve the conceptual distinction between observed performance, contextual predicted probability, evidence support, and pedagogical interpretation.

## Upstream contract

The report consumes exactly one immutable profile run produced by PR #14. The CLI receives:

- `--profile-run-dir`: directory containing the profile artifacts;
- `--output-dir`: destination for the report artifacts.

It does not accept independent paths for profiles, importance, metrics, split, seed, model, or thresholds. This prevents accidentally combining artifacts from different runs.

The profile run must contain:

- `profile-manifest.json`;
- `skill-profiles.parquet`;
- `logistic-permutation-importance.csv`.

The report generator validates the SHA-256 values registered in `profile-manifest.json` before reading the derived artifacts. It also retains the upstream experiment/profile hashes in its own manifest.

`logistic-explanations.json` remains available upstream but is not embedded by default in the teacher-facing report because row-level model-computation traces are a technical audit artifact rather than necessary teacher-facing evidence.

## Scientific semantics

The individual table presents only fields supported by the PR #14 contract:

- pseudonymized student identifier;
- `skill_id`;
- `evidence_count`;
- `mean_predicted_correct_probability`;
- `predicted_probability_dispersion`;
- `observed_accuracy`;
- `observed_accuracy_lower`;
- `observed_accuracy_upper`;
- `evidence_status`;
- `probability_source`.

The report must never relabel `mean_predicted_correct_probability` as mastery, proficiency, competence, learning, fragility, or diagnosis. The probability is described as the mean of contextual probabilities of a correct response over the held-out interactions represented in that student-skill profile.

`predicted_probability_dispersion` is described as dispersion among contextual prediction probabilities, not as model uncertainty.

The Wilson interval is described only as uncertainty around the observed correctness proportion. It is not a confidence interval for the model probability and not a latent-skill uncertainty interval.

`insufficient_evidence` is displayed explicitly as insufficient evidence, never converted to a negative pedagogical judgment.

Ordinal levels, threshold versions, binary alerts, and mastery/fragility labels are excluded because PR #14 keeps them disabled and unvalidated.

## Aggregate view

The aggregate skill view is descriptive and derives from the already-produced student-skill profiles. For each `skill_id`, it reports:

- number of represented pseudonymized students;
- number with `reported` evidence status;
- number with `insufficient_evidence`;
- total evidence interactions summed across student-skill profiles;
- evidence-weighted mean observed accuracy;
- evidence-weighted mean contextual predicted-correct probability.

The aggregate view does not create a population-level proficiency score and does not compare demographic groups. No inferential subgroup or fairness analysis is added unless a separately approved contract later supports it.

## Technical appendix

The report includes a clearly separated technical appendix containing logistic-regression permutation importance from the same profile run.

The appendix labels these values as held-out predictive dependence. It states explicitly that permutation importance:

- does not establish causality;
- can be affected by correlated features;
- does not identify pedagogical causes of difficulty;
- is not used to select the model or thresholds in this report layer.

Model-comparison tables are excluded. Model selection and comparative evaluation belong to PR #13 and should not be silently reinterpreted in a teacher-facing artifact.

## Privacy model

Raw `student_id` values must never be embedded in the HTML or exported CSV.

Pseudonyms are computed with HMAC-SHA-256 using a secret local key supplied at generation time, preferably through `TCC_PSEUDONYM_KEY`. The key:

- must not be committed;
- must not be written to the report or manifest;
- must not be recoverable from the generated artifact;
- may be rotated between contexts when linkage is unnecessary.

The visible pseudonym uses a deterministic truncated digest, for example `Estudante-AB12CD34EF56`, with sufficient length to make collisions negligible for the expected dataset size. Generation fails if a collision is detected within the report.

Pseudonymization reduces direct identifier exposure but does not make the report anonymous. Documentation must continue to describe the report as potentially sensitive educational data requiring access control.

## Security model

The report is one standalone HTML file with no remote scripts, stylesheets, fonts, analytics, APIs, or network requests.

Embedded JSON is serialized with non-finite values rejected and characters capable of terminating a script element escaped. Dynamic table cells are populated with `textContent`, not HTML interpolation.

The generated HTML must not contain the pseudonymization key, raw student identifiers, file-system paths to raw data, or unescaped user-controlled markup.

## Accessibility and interaction

The report supports:

- semantic headings, sections, tables, labels, and captions;
- keyboard-operable student selection;
- visible focus states;
- text labels in addition to any visual styling;
- responsive layout;
- print styles;
- a skip link to the main content;
- accessible status text for insufficient evidence.

The report provides:

- student selection;
- individual profile table;
- aggregate skill table;
- technical permutation-importance appendix;
- export of the selected student profile to CSV using only the pseudonym;
- browser printing.

A free-form teacher-notes field is excluded from this lot. Persisting or operationalizing human notes introduces an additional workflow and data-governance problem that has not been validated with teachers.

## Output contract

One generation produces an immutable directory keyed by the upstream profile-manifest SHA-256 and report configuration/version. It contains:

- `teacher-report.html`;
- `teacher-report-manifest.json`.

The manifest records:

- schema version;
- upstream `profile-manifest.json` SHA-256;
- upstream profile/importance hashes;
- report-generator version/contract version;
- pseudonymization algorithm identifier (`HMAC-SHA-256`), but never the key;
- student and skill counts;
- SHA-256 of the generated HTML;
- scientific interpretation guardrail.

Generation refuses to overwrite an existing immutable report directory.

## CLI

The command is:

```bash
export TCC_PSEUDONYM_KEY='local-secret-key'

tcc-prototype build-teacher-report \
  --profile-run-dir data/reports/<profile-run> \
  --output-dir data/reports/teacher
```

There are no CLI options for model, split, seed, threshold, profile probability source, or minimum evidence. Those choices belong upstream and are inherited from the frozen profile run.

## Error handling

Generation aborts when:

- a required upstream artifact is missing;
- a registered SHA-256 does not match the artifact on disk;
- required profile columns are missing;
- profile probabilities are invalid/non-finite;
- the pseudonymization key is missing or empty;
- a raw student identifier is detected in the rendered HTML;
- pseudonym collision is detected;
- the target immutable output directory already exists.

No partial report is treated as successful output.

## Testing strategy

Development follows RED -> GREEN. Tests are added before implementation and must cover:

1. rejection of the old PR #15 profile schema (`predicted_probability`, `prediction_std`, `level`, `threshold_version`);
2. acceptance of the PR #14 profile schema;
3. verification of profile and permutation-importance hashes against `profile-manifest.json`;
4. HMAC pseudonymization and absence of raw IDs from HTML/CSV payloads;
5. collision detection;
6. script-termination escaping and safe DOM rendering markers;
7. permanent scientific warnings;
8. explicit insufficient-evidence text;
9. aggregate calculations using evidence-weighted means;
10. absence of ordinal/mastery/fragility labels;
11. basic semantic/accessibility elements;
12. immutable output behavior and report-manifest hashes;
13. CLI absence of split/seed/model/threshold controls;
14. full prototype regression suite and TCC quality workflow.

The tests use synthetic fixtures only and do not constitute teacher usability validation or educational validation.

## Documentation and claims

`docs/TCC_TEACHER_REPORT.md` and `prototype/README.md` describe:

- exact upstream inputs and provenance checks;
- meanings of the displayed fields;
- privacy limitations;
- accessibility features;
- allowed and prohibited interpretations;
- absence of teacher usability testing.

Permitted claim: the software can generate an auditable, privacy-reduced, standalone interface that presents frozen predictive/observational evidence with explicit limitations.

Prohibited claims include that the interface diagnoses students, measures true mastery, improves teacher decisions, improves learning, has validated usability, or establishes causal pedagogical factors.

## Out of scope

This lot does not add:

- model training or selection;
- new prediction methods;
- thresholds or ordinal skill labels;
- intervention recommendations;
- teacher-note persistence;
- authentication/access-control infrastructure;
- remote deployment;
- demographic subgroup analysis;
- usability study with teachers;
- efficacy or causal evaluation.
