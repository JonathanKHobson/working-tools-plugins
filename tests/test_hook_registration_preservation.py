"""Registrations survive release reconciliation and shipped hooks stay registered.

Only .codex-plugin/plugin.json (Codex) and .claude-plugin/plugin.json (Claude)
are checked for hook/MCP registration parity: the installed Codex CLI's loader
(core-plugins loader.rs) explicitly skips hook discovery for the Agent Plugins
root-manifest format (plugin.json/plugin.portable.json extensions.com.openai),
so that root manifest is portable metadata only, is never authoritative, and
is therefore excluded from the registration-equivalence requirement (it still
gets its version bumped and reconciled with canonical like any other reviewed
file, since that part of the existing sync is unrelated to hook dispatch).
"""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from release_manager import local_sync
SPEC=importlib.util.spec_from_file_location('hook_packages',ROOT/'scripts/packages.py')
packages=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(packages)


class RegistrationPreservationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.public=self.root/'plugins/fixture'
        self.canonical=self.root/'canonical';self.local=self.canonical/'fixture'
        payload={rel:{'name':'fixture','version':'1.0.0'} for rel in local_sync.MANIFESTS}
        for base in (self.public,self.local):
            for rel,value in payload.items():
                (base/rel).parent.mkdir(parents=True,exist_ok=True);local_sync.write(base/rel,value)
            (base/'CHANGELOG.md').write_text('# Changelog\n')
        files={path.relative_to(self.public).as_posix():local_sync.digest(path.read_bytes())
               for path in self.public.rglob('*') if path.is_file()}
        (self.root/'catalog').mkdir()
        local_sync.write(self.root/'catalog/source-inventory.json',{'packages':[{
            'id':'fixture','version':'1.0.0','files':files,
            'canonical_source':{'id':'fixture','revision':{}}}]})
        local_sync.write(self.root/'catalog/packages.json',{'packages':[{'id':'fixture','version':'1.0.0'}]})

    def edit(self,base,rel,field,value):
        document=local_sync.read(base/rel);document[field]=value;local_sync.write(base/rel,document)

    def snapshot(self,base=None):
        base=self.root if base is None else base
        return {path.relative_to(base).as_posix():path.read_bytes()
                for path in base.rglob('*') if path.is_file()}

    def test_refresh_rejects_missing_and_changed_registrations_without_writes(self):
        for rel,field,value in (
            ('.codex-plugin/plugin.json','hooks','./hooks/hooks.json'),
            ('.claude-plugin/plugin.json','mcpServers',{'server':{'command':'python3'}}),
        ):
            with self.subTest(rel=rel):
                self.edit(self.local,rel,field,value);before=self.snapshot()
                with self.assertRaisesRegex(ValueError,'fixture/'+rel.replace('.','\\.')+' -> '):
                    local_sync.refresh_reviewed(self.root,self.canonical,'fixture','1.0.1','Notes')
                self.assertEqual(self.snapshot(),before)
                self.edit(self.public,rel,field,value)
        self.edit(self.public,'.codex-plugin/plugin.json','hooks','./other/hooks.json')
        with self.assertRaisesRegex(ValueError,'Registration mismatch'):
            local_sync.refresh_reviewed(self.root,self.canonical,'fixture','1.0.1','Notes')

    def test_root_portable_manifest_registration_drift_does_not_block_refresh(self):
        """A root-manifest-only hooks field is non-authoritative at runtime, so it
        must not be required to match between public and canonical like the
        native .codex-plugin/.claude-plugin manifests are."""
        self.edit(self.local,'plugin.json','extensions',{'com.openai':{'hooks':'./hooks/hooks.json'}})
        local_sync.refresh_reviewed(self.root,self.canonical,'fixture','1.0.1','Notes')
        # The reviewed root manifest is bumped in public only; publication never
        # writes canonical, so canonical's bytes (including its drifted hooks
        # field) are left completely untouched by this operation.
        self.assertEqual(local_sync.read(self.public/'plugin.json')['version'],'1.0.1')
        self.assertEqual(local_sync.read(self.local/'plugin.json')['version'],'1.0.0')
        self.assertEqual(local_sync.read(self.local/'plugin.json')['extensions'],
                          {'com.openai':{'hooks':'./hooks/hooks.json'}})

    def test_reviewed_portable_registration_pins_expire_on_either_edit(self):
        rel='.codex-plugin/plugin.json'
        self.edit(self.local,rel,'hooks','./hooks/hooks.json')
        self.edit(self.public,rel,'hooks','./optional-hooks/hooks.json')
        inventory=local_sync.read(self.root/'catalog/source-inventory.json')
        row=inventory['packages'][0]
        row['canonical_files']={p:local_sync.digest((self.local/p).read_bytes()) for p in row['files']}
        row['files']={p:local_sync.digest((self.public/p).read_bytes()) for p in row['files']}
        local_sync.write(self.root/'catalog/source-inventory.json',inventory)
        local_sync.require_matching_registrations('fixture',rel,self.local/rel,self.public/rel)
        self.edit(self.public,rel,'hooks','./missing/hooks.json')
        with self.assertRaisesRegex(ValueError,'Registration mismatch'):
            local_sync.require_matching_registrations('fixture',rel,self.local/rel,self.public/rel)

    def test_pending_uses_canonical_baseline_after_public_version_bump(self):
        from release_manager import pending
        local_sync.refresh_reviewed(self.root,self.canonical,'fixture','1.0.1','Notes')
        row=local_sync.read(self.root/'catalog/source-inventory.json')['packages'][0]
        self.assertIsNone(pending.plugin_observation(self.root,{'canonical_root':str(self.canonical)},row,'1.0.1'))
        (self.local/'CHANGELOG.md').write_text('A later canonical change')
        observation=pending.plugin_observation(self.root,{'canonical_root':str(self.canonical)},row,'1.0.1')
        self.assertEqual([x['path'] for x in observation['changes']],['CHANGELOG.md'])

    def test_matching_registrations_allow_version_metadata_refresh(self):
        for base in (self.public,self.local):self.edit(base,'.codex-plugin/plugin.json','hooks','./hooks/hooks.json')
        canonical_before=self.snapshot(self.local)
        local_sync.refresh_reviewed(self.root,self.canonical,'fixture','1.0.1','Notes')
        manifest=local_sync.read(self.public/'.codex-plugin/plugin.json')
        self.assertEqual(manifest['hooks'],'./hooks/hooks.json');self.assertEqual(manifest['version'],'1.0.1')
        # Canonical already matched (no drift to publish), and publication never
        # writes it regardless, so it stays byte-identical.
        self.assertEqual(self.snapshot(self.local),canonical_before)

    def test_apply_content_copies_canonical_to_public_only(self):
        self.edit(self.local,'.codex-plugin/plugin.json','hooks','./hooks/hooks.json')
        self.edit(self.public,'.codex-plugin/plugin.json','hooks','./hooks/hooks.json')
        (self.local/'CHANGELOG.md').write_text('Changed notes')
        changes={'CHANGELOG.md':{'source':'canonical',
                                  'base':local_sync.digest((self.public/'CHANGELOG.md').read_bytes()),
                                  'sha256':local_sync.digest((self.local/'CHANGELOG.md').read_bytes()),
                                  'public_sha256':local_sync.digest((self.public/'CHANGELOG.md').read_bytes())}}
        canonical_before=self.snapshot(self.local)
        local_sync.apply_content(self.root,self.canonical,{'fixture':changes})
        self.assertEqual(self.snapshot(self.local),canonical_before)
        self.assertEqual((self.public/'CHANGELOG.md').read_text(),'Changed notes')

    def test_apply_content_rejects_any_non_canonical_source(self):
        changes={'CHANGELOG.md':{'source':'public',
                                  'base':local_sync.digest((self.local/'CHANGELOG.md').read_bytes()),
                                  'sha256':local_sync.digest((self.public/'CHANGELOG.md').read_bytes())}}
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'canonical -> public'):
            local_sync.apply_content(self.root,self.canonical,{'fixture':changes})
        self.assertEqual(self.snapshot(),before)

    def test_apply_content_preflights_registrations_before_any_copy(self):
        self.edit(self.local,'.codex-plugin/plugin.json','hooks','./hooks/hooks.json')
        (self.local/'CHANGELOG.md').write_text('Changed notes')
        changes={rel:{'source':'canonical','base':local_sync.digest((self.public/rel).read_bytes()),
                      'sha256':local_sync.digest((self.local/rel).read_bytes()),
                      'public_sha256':local_sync.digest((self.public/rel).read_bytes())}
                 for rel in ('CHANGELOG.md','.codex-plugin/plugin.json')}
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'fixture/\\.codex-plugin/plugin.json -> hooks'):
            local_sync.apply_content(self.root,self.canonical,{'fixture':changes})
        self.assertEqual(self.snapshot(),before)


    def test_full_publication_flow_never_writes_canonical(self):
        """End-to-end plan() + apply_content() + refresh_reviewed() snapshot:
        canonical is byte-identical before and after a real publication that
        edits a canonical source file, bumps the version and refreshes public
        manifests/changelog/metadata."""
        (self.local/'CHANGELOG.md').write_text('# Changelog\n\nCanonical edit.\n')
        canonical_before=self.snapshot(self.local)
        changes,conflicts=local_sync.plan(self.root,self.canonical,product_ids=['fixture'])
        self.assertEqual(conflicts,[])
        local_sync.apply_content(self.root,self.canonical,changes)
        local_sync.refresh_reviewed(self.root,self.canonical,'fixture','1.0.1','Notes')
        self.assertEqual(self.snapshot(self.local),canonical_before)
        self.assertIn('Canonical edit.',(self.public/'CHANGELOG.md').read_text())
        inventory=local_sync.read(self.root/'catalog/source-inventory.json')
        row=next(r for r in inventory['packages'] if r['id']=='fixture')
        self.assertEqual(row['canonical_files']['CHANGELOG.md'],
                          local_sync.digest((self.local/'CHANGELOG.md').read_bytes()))
        self.assertEqual(row['files']['CHANGELOG.md'],
                          local_sync.digest((self.public/'CHANGELOG.md').read_bytes()))
        self.assertNotEqual(row['canonical_files']['CHANGELOG.md'],row['files']['CHANGELOG.md'])


class ShippedHookValidationTests(unittest.TestCase):
    def test_top_level_hooks_require_exact_registration_and_archive_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'scripts').mkdir();(root/'scripts/demo.py').write_text('pass\n')
            expected={'hooks':{'UserPromptSubmit':[{'hooks':[{'type':'command','command':'python3 scripts/demo.py'}]}]}}
            archive=root/'libraries/foreign/hooks/hooks.json';archive.parent.mkdir(parents=True)
            local_sync.write(archive,expected)
            self.assertEqual(packages.hook_registration_errors(root,'fixture'),[])
            for folder in ('hooks','optional-hooks'):
                with self.subTest(folder=folder):
                    definition=root/folder/'hooks.json';definition.parent.mkdir(parents=True)
                    local_sync.write(definition,expected)
                    self.assertTrue(packages.hook_registration_errors(root,'fixture'))
                    manifest=root/'.codex-plugin/plugin.json';manifest.parent.mkdir(exist_ok=True)
                    local_sync.write(manifest,{'hooks':f'./{folder}/hooks.json'})
                    self.assertEqual(packages.hook_registration_errors(root,'fixture'),[])
                    local_sync.write(manifest,{'hooks':{'Stop':[]}})
                    self.assertTrue(any('differs from shipped' in error for error in packages.hook_registration_errors(root,'fixture')))
                    local_sync.write(manifest,{'hooks':'../../outside.json'})
                    self.assertTrue(any('escaping package' in error for error in packages.hook_registration_errors(root,'fixture')))
                    definition.unlink()

    def test_claude_uses_its_own_compatible_definition(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'hooks').mkdir();(root/'.claude-plugin').mkdir()
            (root/'scripts').mkdir();(root/'scripts/stop.py').write_text('pass\n')
            local_sync.write(root/'hooks/claude-hooks.json',{'hooks':{'Stop':[{'hooks':[{'type':'command','command':'python3 scripts/stop.py'}]}]}})
            self.assertTrue(packages.hook_registration_errors(root,'fixture'))
            local_sync.write(root/'.claude-plugin/plugin.json',{'hooks':'./hooks/claude-hooks.json'})
            self.assertEqual(packages.hook_registration_errors(root,'fixture'),[])

    def test_root_manifest_must_not_suppress_native_hooks(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'hooks').mkdir();(root/'.codex-plugin').mkdir()
            (root/'scripts').mkdir();(root/'scripts/demo.py').write_text('pass\n')
            handler={'type':'command','command':'python3 "${PLUGIN_ROOT}/scripts/demo.py"'}
            definition={'hooks':{'UserPromptSubmit':[{'hooks':[handler]}]}}
            local_sync.write(root/'hooks/hooks.json',definition)
            local_sync.write(root/'.codex-plugin/plugin.json',{'hooks':'./hooks/hooks.json'})
            local_sync.write(root/'plugin.portable.json',{'name':'fixture'})
            self.assertEqual(packages.hook_registration_errors(root,'fixture'),[])
            local_sync.write(root/'plugin.json',{'name':'fixture'})
            self.assertTrue(any('suppresses' in e for e in packages.hook_registration_errors(root,'fixture')))
            (root/'plugin.json').unlink()
            definition['hooks']['UserPromptSubmit'][0]['hooks'].append(dict(handler,timeout=10))
            local_sync.write(root/'hooks/hooks.json',definition)
            self.assertTrue(any('duplicate or conflicting' in e for e in packages.hook_registration_errors(root,'fixture')))
            (root/'scripts/demo.py').unlink()
            self.assertTrue(any('missing hook handler' in e for e in packages.hook_registration_errors(root,'fixture')))


class PortableManifestRenameTests(unittest.TestCase):
    def test_validate_package_accepts_plugin_portable_json_in_place_of_plugin_json(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);plugins=root/'plugins/fixture';plugins.mkdir(parents=True)
            for rel in ('.codex-plugin','.claude-plugin'):(plugins/rel).mkdir()
            local_sync.write(plugins/'.codex-plugin/plugin.json',{'name':'fixture','version':'1.0.0'})
            local_sync.write(plugins/'.claude-plugin/plugin.json',{'name':'fixture','version':'1.0.0'})
            local_sync.write(plugins/'plugin.portable.json',{
                '$schema':'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
                'name':'fixture','version':'1.0.0'})
            for name in ('README.md','LICENSE','THIRD_PARTY_NOTICES.md'):(plugins/name).write_text('x')
            (plugins/'skills').mkdir()
            local_sync.write(plugins/'PROVENANCE.json',{'files':[]})
            orig_root=packages.ROOT
            packages.ROOT=root
            try:
                record={'id':'fixture','version':'1.0.0','skills':0,'requirements':[]}
                errors=packages.validate_package(record)
            finally:
                packages.ROOT=orig_root
            self.assertEqual([e for e in errors if 'missing plugin.json' in e or 'identity/version mismatch' in e],[])


if __name__=='__main__':unittest.main()
