"""Compare the shared transport against a saved original SDK generation."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import uuid

from fixtures import ROOT, make_fixture
from catalog import Catalog, DOMAINS
from test_runtime import StdioClient

BASELINE = os.environ.get("ACTIVITIES_BASELINE_ROOT")


def normalized(value):
    if isinstance(value, dict):
        return {k: normalized(v) for k, v in value.items() if k not in {"first_seen", "last_seen"}}
    if isinstance(value, list):
        return [normalized(v) for v in value]
    if isinstance(value, str) and value.startswith("{"):
        try:
            return normalized(json.loads(value))
        except ValueError:
            pass
    return value


@unittest.skipUnless(BASELINE, "Set ACTIVITIES_BASELINE_ROOT to the saved original generation")
class TransportParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="atlas-parity-")
        cls.directory = Path(cls.tmp.name).resolve()
        cls.vault, cls.db = make_fixture(cls.directory)
        cls.bindings = []
        for version in ("before", "after"):
            path = cls.directory / (version + ".json")
            path.write_text(json.dumps({"interpreter": sys.executable, "database": str(cls.db),
                "search_misses_database": str(cls.directory / (version + "-misses.sqlite"))}))
            cls.bindings.append(path)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def clients(self, domain):
        clients = []
        for root, binding in zip((Path(BASELINE), ROOT), self.bindings):
            env = dict(os.environ, ACTIVITIES_ATLAS_CONFIG=str(binding), PYTHONDONTWRITEBYTECODE="1",
                       ACTIVITIES_BACKEND_IDLE_SECONDS="2")
            c = StdioClient([sys.executable, str(root / "scripts/atlas_library_mcp.py"), domain], env)
            clients.append(c)
            c.initialize()
        return clients

    def test_all_domain_contracts_results_errors_resources_feedback(self):
        digest = hashlib.sha256(self.db.read_bytes()).hexdigest()
        all_ids = {i["id"] for d in DOMAINS for i in Catalog(self.db, d).export()["items"]}
        for domain in [r['args'][1] for r in json.loads((ROOT / '.mcp.json').read_text())['mcpServers'].values()]:
            if domain == "visualization":
                continue  # Defined in the catalog but not one of the twelve registrations.
            with self.subTest(domain=domain):
                before, after = self.clients(domain)
                try:
                    def equal(method, params=None):
                        a = before.request(method, params)
                        b = after.request(method, params)
                        self.assertEqual(normalized(a), normalized(b), method)
                        return b.get("result")
                    equal("tools/list")
                    equal("resources/list")
                    equal("resources/templates/list")
                    equal("prompts/list")
                    equal("ping")
                    name = domain.replace("-", "_")
                    search = equal("tools/call", {"name": f"search_{name}_atlas", "arguments": {"limit":100}})
                    own = search["structuredContent"]["items"][0]["id"]
                    own_ids = {i["id"] for i in search["structuredContent"]["items"]}
                    foreign = next(i for i in sorted(all_ids) if i not in own_ids)
                    equal("tools/call", {"name": f"browse_{name}_atlas", "arguments": {"limit":100}})
                    equal("tools/call", {"name": f"read_{name}_atlas", "arguments": {"entry_ids":[own]}})
                    for args in ({"entry_ids":[]}, {"entry_ids":[own]*6},
                                 {"entry_ids":[own],"intent":"x"*4001}, {"entry_ids":[foreign]}):
                        result = equal("tools/call", {"name":f"read_{name}_atlas", "arguments":args})
                        self.assertTrue(result["isError"])
                    equal("tools/call", {"name":f"search_{name}_atlas", "arguments":{"limit":"invalid"}})
                    equal("tools/call", {"name":"not_a_tool", "arguments":{}})
                    equal("resources/read", {"uri":f"ui://atlas-{domain}/library-prompt-v2.html"})
                    equal("resources/read", {"uri":"ui://foreign/absent.html"})
                    payload = {"task_key":str(uuid.uuid4()), "need_key":"fixture-"+domain,
                               "route":"synthetic contract test", "intent":"Verify feedback parity",
                               "search_terms":"synthetic", "evidence":"No matching synthetic activity observed", "result_count":0}
                    first = equal("tools/call", {"name":"record_library_search_miss", "arguments":payload})
                    self.assertTrue(json.loads(first["content"][0]["text"])["logged"])
                    again = equal("tools/call", {"name":"record_library_search_miss", "arguments":payload})
                    self.assertTrue(json.loads(again["content"][0]["text"])["deduplicated"])
                    equal("tools/call", {"name":"review_library_search_misses", "arguments":{"need_key":payload["need_key"]}})
                finally:
                    before.close()
                    after.close()
        self.assertEqual(hashlib.sha256(self.db.read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
