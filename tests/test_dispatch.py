import unittest

from dispatch import assign


class DispatchTest(unittest.TestCase):
    def test_deterministic_assignment_and_reasons(self):
        scenario = {
            "trucks": [
                {"id": "T-2", "status": "available", "capacity_t": 200},
                {"id": "T-1", "status": "available", "capacity_t": 200},
                {"id": "T-3", "status": "unavailable", "capacity_t": 200},
            ],
            "loaders": [
                {"id": "L-2", "status": "available", "min_capacity_t": 150, "max_trucks": 1},
                {"id": "L-1", "status": "available", "min_capacity_t": 150, "max_trucks": 1},
            ],
        }
        result = assign(scenario)
        self.assertEqual([(item["truck_id"], item["loader_id"]) for item in result["assignments"]],
                         [("T-1", "L-1"), ("T-2", "L-2")])
        self.assertEqual(result["unassigned"][0]["reason"], "truck_unavailable")
        self.assertEqual(result, assign(scenario))

    def test_reject_duplicate_ids(self):
        scenario = {"trucks": [{"id": "X", "status": "available", "capacity_t": 200}],
                    "loaders": [{"id": "X", "status": "available", "min_capacity_t": 150, "max_trucks": 1}]}
        with self.assertRaisesRegex(ValueError, "unique"):
            assign(scenario)


if __name__ == "__main__":
    unittest.main()
