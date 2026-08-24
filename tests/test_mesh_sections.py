from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mesh = _load("mesh_sections")

PACK = """§PACK Demo
§VERSION 1

§THEOREM_D1_aaa: §GAUGE_ORTHO(P_2, (p_or_p) -> p) ⊢ COMMIT
  // Hyperbolic coordinates: CP=1.0000, BERRY=1.5708
  §ORTHO_PRIME_BASIS: 2
  §HOLOPORT

§THEOREM_D2_bbb: §GAUGE_ORTHO(P_3, q -> (p_or_q)) ⊢ COMMIT
  // Hyperbolic coordinates: CP=1.0000, BERRY=1.5709
  §ORTHO_PRIME_BASIS: 3
  §HOLOPORT
"""


class MeshSectionTests(unittest.TestCase):
    def write(self, text: str) -> Path:
        handle = tempfile.NamedTemporaryFile("w", suffix=".lang", delete=False, encoding="utf-8")
        handle.write(text)
        handle.close()
        self.addCleanup(Path(handle.name).unlink, missing_ok=True)
        return Path(handle.name)

    def test_declarations_are_parsed_with_their_stated_values(self) -> None:
        sections = mesh.parse_pack(self.write(PACK))
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]["depth"], 1)
        self.assertEqual(sections[0]["prime"], 2)
        self.assertEqual(sections[0]["coordinates"]["berry"], 1.5708)
        self.assertEqual(sections[1]["prime"], 3)

    def test_verdict_token_is_recorded_verbatim_not_interpreted(self) -> None:
        """The turnstile token is transcribed, never turned into a pass."""
        sections = mesh.parse_pack(self.write(PACK))
        self.assertEqual(sections[0]["declared_verdict"], "COMMIT")
        self.assertNotIn("proved", sections[0])
        self.assertNotIn("verified", sections[0])

    def test_links_attach_each_section_to_a_shallower_one(self) -> None:
        sections = mesh.parse_pack(self.write(PACK))
        links = mesh.build_links(sections)
        self.assertEqual(links, [{"source": 0, "target": 1, "kind": "declaration_adjacency"}])

    def test_roots_have_no_parent_so_links_are_fewer_than_sections(self) -> None:
        """A forest with k roots yields n-k links, not n-1."""
        text = PACK + "\n§THEOREM_D1_ccc: §GAUGE_ORTHO(P_5, r) ⊢ COMMIT\n  §ORTHO_PRIME_BASIS: 5\n"
        sections = mesh.parse_pack(self.write(text))
        links = mesh.build_links(sections)
        roots = sum(1 for s in sections if s["depth"] == 1)
        self.assertEqual(roots, 2)
        self.assertEqual(len(links), len(sections) - roots)

    def test_cosmos_scopes_do_not_link_across_each_other(self) -> None:
        text = (
            "§PACK Demo\n§VERSION 1\n"
            "§THEOREM_C1_D1: §GAUGE_ORTHO(P_3) ⊢ COMMIT\n"
            "§THEOREM_C1_D2: §GAUGE_ORTHO(P_5) ⊢ COMMIT\n"
            "§THEOREM_C2_D2: §GAUGE_ORTHO(P_7) ⊢ COMMIT\n"
        )
        sections = mesh.parse_pack(self.write(text))
        links = mesh.build_links(sections)
        self.assertEqual(sections[2]["cosmos"], 2)
        # C2_D2 has no depth-1 section inside cosmos 2, so it stays a root.
        self.assertEqual([(l["source"], l["target"]) for l in links], [(0, 1)])

    def test_undeclared_sources_are_refused(self) -> None:
        with self.assertRaises(SystemExit):
            mesh.resolve_pack("README.md")

    def test_legacy_block_sources_are_refused(self) -> None:
        """Only pack surfaces project; a block source is not a mesh."""
        with self.assertRaises(SystemExit):
            mesh.resolve_pack("LANG.v1.2.0.unified_geometry.lang")

    def test_summary_reports_counts_not_conclusions(self) -> None:
        sections = mesh.parse_pack(self.write(PACK))
        summary = mesh.summarize(sections, mesh.build_links(sections))
        self.assertEqual(summary["declared_verdicts"], {"COMMIT": 2})
        self.assertEqual(summary["distinct_primes"], 2)
        self.assertNotIn("proved", summary)


if __name__ == "__main__":
    unittest.main()
