import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gpv2_neroflux import AncolieIndexer, build_rag_chunk_meta, normalize_ancolie_packet


class NormalizeAncoliePacketTests(unittest.TestCase):
    def test_requires_text_or_voice(self):
        with self.assertRaises(ValueError):
            normalize_ancolie_packet({})

    def test_normalizes_voice_features(self):
        packet = normalize_ancolie_packet({
            "input_type": "voice",
            "voice_features": {
                "loudness": 2,
                "speech_rate": 0.7,
                "pause_ratio": -1,
                "pitch_variation": 0.3,
                "tension": 0.9,
            },
        })

        self.assertEqual(packet["voice_features"]["loudness"], 1.0)
        self.assertEqual(packet["voice_features"]["pause_ratio"], 0.0)
        self.assertEqual(packet["mode"], "LIGHT")


class AncolieIndexerTests(unittest.TestCase):
    def test_frustrated_concrete_request_prefers_concrete_outputs(self):
        indexer = AncolieIndexer()

        result = indexer.analyze({
            "text": "Je veux que ce soit concret, arrete les trucs vagues.",
            "mode": "FULL",
        })

        self.assertEqual(result["module"], "GPV2_EXOTIQUE_ANCOLIE")
        self.assertTrue(result["signature"]["emo"].startswith("frustr"))
        self.assertEqual(result["signature"]["memory"], "prefer_concrete_outputs")
        self.assertIn("λ.rim", result["signature"]["route"])
        self.assertIn("μ.me", result["signature"]["route"])
        self.assertEqual(result["signature"]["risk"], "medium")

    def test_shallow_document_feedback_requests_deep_export(self):
        indexer = AncolieIndexer()

        result = indexer.analyze({
            "text": "Je veux que tu arretes de faire des documents vides, prends ton temps et fais-le bien.",
            "mode": "TRACE",
        })

        self.assertEqual(result["signature"]["friction"], "output_too_shallow")
        self.assertEqual(
            result["signature"]["action"],
            "produce_deep_structured_content_before_export",
        )
        self.assertEqual(result["signature"]["memory"], "avoid_shallow_document_generation")
        self.assertTrue(result["storage_recommended"])
        self.assertIn("τ.hal", result["signature"]["route"])

    def test_doubt_routes_to_verified_answer(self):
        indexer = AncolieIndexer()

        result = indexer.analyze({
            "text": "Tu es sur ? Verifie les faits et donne-moi une preuve claire.",
            "mode": "FULL",
        })

        self.assertIn("doubt", result["signature"]["emo"])
        self.assertIn("π.pri", result["signature"]["route"])
        self.assertIn("τ.hal", result["signature"]["route"])
        self.assertEqual(result["signature"]["action"], "provide_verified_answer")

    def test_voice_urgency_selects_fast_companion_mode(self):
        indexer = AncolieIndexer()

        result = indexer.analyze({
            "input_type": "voice",
            "voice_features": {
                "loudness": 0.8,
                "speech_rate": 0.95,
                "pause_ratio": 0.1,
                "pitch_variation": 0.6,
                "tension": 0.9,
            },
        })

        self.assertIn("urgency", result["signature"]["emo"])
        self.assertEqual(result["companion_mode"], "FAST")
        self.assertEqual(result["signature"]["action"], "surface_next_action")

    def test_build_rag_meta_raises_priority_for_vision_chunks(self):
        indexer = AncolieIndexer()
        result = indexer.analyze({
            "text": "Construis une roadmap strategique long terme pour ce produit.",
            "mode": "FULL",
        })

        metadata = build_rag_chunk_meta(
            "ora_companion_strategy_v1",
            result,
            use_case="business_strategy",
        )

        self.assertIn("α.aur", metadata["essence_tags"])
        self.assertIn("vision", metadata["emo_tags"])
        self.assertEqual(metadata["retrieval_priority"], "high")


if __name__ == "__main__":
    unittest.main()
