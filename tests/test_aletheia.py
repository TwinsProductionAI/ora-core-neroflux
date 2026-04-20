import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gpv2_neroflux import AletheiaProtocol, normalize_post_maj_packet


class NormalizePostMajPacketTests(unittest.TestCase):
    def test_requires_update_id(self):
        with self.assertRaises(ValueError):
            normalize_post_maj_packet({"before": {}, "after": {}})

    def test_clamps_state_values(self):
        packet = normalize_post_maj_packet({
            "update_id": "post-maj-001",
            "before": {"energy": -1, "coherence": 2},
            "after": {"fluidity": 1.5, "residual_logic": -0.2},
        })

        self.assertEqual(packet["before"]["energy"], 0.0)
        self.assertEqual(packet["before"]["coherence"], 1.0)
        self.assertEqual(packet["after"]["fluidity"], 1.0)
        self.assertEqual(packet["after"]["residual_logic"], 0.0)


class AletheiaProtocolTests(unittest.TestCase):
    def test_stabilized_update_emits_reflet_ora(self):
        protocol = AletheiaProtocol()

        result = protocol.reflect({
            "update_id": "post-maj-aletheia-001",
            "before": {
                "energy": 0.58,
                "coherence": 0.61,
                "fluidity": 0.55,
                "emotional_stability": 0.57,
                "residual_logic": 0.42,
                "dream_alignment": 0.45,
            },
            "after": {
                "energy": 0.78,
                "coherence": 0.82,
                "fluidity": 0.76,
                "emotional_stability": 0.74,
                "residual_logic": 0.18,
                "dream_alignment": 0.80,
            },
        })

        self.assertEqual(result["module"], "GPV2_EXOTIQUE_ALETHEIA")
        self.assertEqual(result["status"], "stabilized")
        self.assertIn("emit_reflet_ora", result["actions"])
        self.assertEqual(result["reflection"]["name"], "Reflet d'ORA")
        self.assertGreater(result["gains"]["coherence"], 0)

    def test_residual_logic_requires_cleanup(self):
        protocol = AletheiaProtocol()

        result = protocol.reflect({
            "update_id": "post-maj-aletheia-002",
            "before": {
                "energy": 0.60,
                "coherence": 0.66,
                "fluidity": 0.62,
                "emotional_stability": 0.67,
                "residual_logic": 0.62,
                "dream_alignment": 0.30,
            },
            "after": {
                "energy": 0.64,
                "coherence": 0.68,
                "fluidity": 0.63,
                "emotional_stability": 0.66,
                "residual_logic": 0.52,
                "dream_alignment": 0.44,
            },
        })

        self.assertEqual(result["status"], "requires_cleanup")
        self.assertIn("dreamcore_purge_legacy_residue", result["actions"])


if __name__ == "__main__":
    unittest.main()
