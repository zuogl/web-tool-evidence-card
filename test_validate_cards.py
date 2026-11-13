"""Format checks, never product acceptance tests."""

from copy import deepcopy
import unittest

from validate_cards import validate


BASE = {
    "schema_version": 1,
    "project": "Example",
    "reference_url": "https://example.com/how-it-works",
    "recorded_on": "2026-11-13",
    "illustrative": True,
    "source_summary": "A source statement belongs here.",
    "checked_at": None,
    "observations": [],
    "unverified": ["Runtime behavior has not been checked."],
    "next_check": "Record one authorized observation with its scope.",
}


class FormatTests(unittest.TestCase):
    def test_illustration_passes(self):
        self.assertEqual(validate(BASE), [])

    def test_record_with_observation_passes(self):
        card = deepcopy(BASE)
        card.update(illustrative=False, checked_at="2026-11-13T13:00:00+08:00", observations=[{
            "observed_at": "2026-11-13T13:00:00+08:00",
            "method": "manual page read",
            "result": "An example record, not a product observation.",
        }])
        self.assertEqual(validate(card), [])

    def test_missing_and_extra_fields(self):
        card = deepcopy(BASE)
        del card["next_check"]
        card["extra"] = "surprise"
        self.assertTrue(validate(card))

    def test_boolean_is_not_schema_version(self):
        card = dict(BASE, schema_version=True)
        self.assertTrue(validate(card))

    def test_bad_urls(self):
        for url in ["/relative", "http://example.com", "https://a:b@example.com", "https://exam ple.com", "https://[bad"]:
            with self.subTest(url=url):
                self.assertTrue(validate(dict(BASE, reference_url=url)))

    def test_bad_dates(self):
        for day in ["2026-02-30", "20261113", None]:
            with self.subTest(day=day):
                self.assertTrue(validate(dict(BASE, recorded_on=day)))

    def test_missing_timezone(self):
        card = dict(BASE, illustrative=False, checked_at="2026-11-13T13:00:00")
        self.assertTrue(validate(card))

    def test_illustration_cannot_claim_observation(self):
        card = dict(BASE, checked_at="2026-11-13T05:00:00Z")
        self.assertTrue(validate(card))

    def test_observation_needs_scope_and_time(self):
        card = dict(BASE, illustrative=False, observations=[{"observed_at": "today", "method": "", "result": ""}])
        self.assertTrue(validate(card))

    def test_required_limitation(self):
        self.assertTrue(validate(dict(BASE, unverified=[])))

    def test_null_card_is_invalid(self):
        self.assertTrue(validate(None))


if __name__ == "__main__":
    unittest.main()
