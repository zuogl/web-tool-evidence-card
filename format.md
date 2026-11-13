# Evidence card format, version 1

Every field below is required. Unexpected top-level fields are rejected so that misspellings do not silently disappear.

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | integer `1` | Format identifier, not a product version. |
| `project` | nonempty string | Human-readable source or product name. |
| `reference_url` | HTTPS URL | Selected source page; no embedded credentials or whitespace. |
| `recorded_on` | `YYYY-MM-DD` | Calendar date on which this record was assembled. |
| `illustrative` | boolean | Whether this is an example rather than an observation record. |
| `source_summary` | nonempty string | A statement attributed to the selected source. |
| `checked_at` | null or timestamp | Actual check time with timezone, separately supplied by the observer. |
| `observations` | array | Zero or more observation objects; see below. |
| `unverified` | nonempty array of nonempty strings | Limits and questions that remain open. |
| `next_check` | nonempty string | Proposed follow-up work, not a completed result. |

Each observation contains exactly `observed_at`, `method` and `result`. The first is a timestamp with a timezone; the latter two are nonempty strings. For example, the timestamp shape is `2026-11-13T13:00:00+08:00` or `2026-11-13T05:00:00Z`. An observation requires a non-null `checked_at`.

For `illustrative: true`, `checked_at` must be null and `observations` must be empty. This keeps the supplied examples from masquerading as completed checks. A real record can also have no observations yet; its empty fields must not be interpreted as a successful test.

The validator does not determine whether the observer used the method correctly or whether the result is true. It also does not enforce chronology between timestamps. Record source-reported dates in the attributed summary, and record genuine observation times separately.
