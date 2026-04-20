import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gpv2_neroflux import NerofluxRouter, normalize_packet


class NormalizePacketTests(unittest.TestCase):
    def test_requires_intention(self):
        with self.assertRaises(ValueError):
            normalize_packet({"emotion": 0.5})

    def test_clamps_numeric_values(self):
        packet = normalize_packet({
            "intention": "Route this.",
            "emotion": 2,
            "creativity": -1,
        })

        self.assertEqual(packet["emotion"], 1.0)
        self.assertEqual(packet["creativity"], 0.0)


class NerofluxRouterTests(unittest.TestCase):
    def test_routes_creative_symbolic_packet_to_dreamcore(self):
        router = NerofluxRouter()

        result = router.route({
            "intention": "Creer une architecture symbolique.",
            "emotion": 0.35,
            "creativity": 0.95,
            "logic": 0.20,
            "symbolic_density": 0.95,
            "context_density": 0.20,
            "urgency": 0.10,
        })

        self.assertEqual(result["dominant_route"], "DreamCore")
        self.assertIn("permit_dreamcore_drift", result["actions"])

    def test_contradiction_prioritizes_primordia(self):
        router = NerofluxRouter()

        result = router.route({
            "intention": "Arbitrer deux hypotheses incompatibles.",
            "emotion": 0.20,
            "creativity": 0.20,
            "logic": 0.60,
            "symbolic_density": 0.20,
            "context_density": 0.50,
            "urgency": 0.40,
            "contradiction": True,
        })

        self.assertEqual(result["dominant_route"], "Primordia")
        self.assertEqual(result["pace"], "fast")
        self.assertIn("redirect_to_primordia_tribunal", result["actions"])

    def test_high_emotion_dilates_emo_channel(self):
        router = NerofluxRouter()

        result = router.route({
            "intention": "Repondre a une demande emotionnelle dense.",
            "emotion": 0.90,
            "creativity": 0.20,
            "logic": 0.20,
            "symbolic_density": 0.20,
            "context_density": 0.20,
            "urgency": 0.10,
        })

        self.assertIn("dilate_emo_channels", result["actions"])
        self.assertGreater(result["channels"]["Emo+"], result["channels"]["DreamCore"])


if __name__ == "__main__":
    unittest.main()
