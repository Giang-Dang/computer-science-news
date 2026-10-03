import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    'validate_papers', Path(__file__).resolve().parents[1] / 'scripts/validate_papers.py')
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class PrimaryIdentityTests(unittest.TestCase):
    def test_metadata_formats_and_versions(self):
        for declaration in (
            '**ArXiv ID:** [2601.12345v2](https://arxiv.org/abs/2601.12345v2)',
            '**ArXiv ID**: 2601.12345',
            '- **arxiv id:** https://arxiv.org/pdf/2601.12345.pdf',
            '**Paper ID:** arXiv:2601.12345',
            '__ArXiv ID:__ https://arxiv.org/html/2601.12345v3',
            '**ArXiv ID:** 2601.1234',
        ):
            with self.subTest(declaration=declaration):
                identity, errors = validator.primary_identity('# Paper\n\n' + declaration)
                self.assertFalse(errors)
                self.assertEqual(identity, '2601.1234' if declaration.endswith('2601.1234') else '2601.12345')

    def test_reference_and_code_ids_are_not_primary(self):
        text = '''# Paper
```markdown
**ArXiv ID:** 2601.99999
```
## Related Work & Context
### Other papers
- **ArXiv ID:** 2601.22222
## References
- **ArXiv ID:** 2601.33333
## Paper Metadata
- **ArXiv ID:** 2601.12345
'''
        self.assertEqual(validator.primary_identity(text), ('2601.12345', []))

    def test_missing_identity_does_not_use_unlabelled_url(self):
        identity, errors = validator.primary_identity('# Paper\nhttps://arxiv.org/abs/2601.12345')
        self.assertIsNone(identity)
        self.assertIn('missing primary', errors[0])

    def test_generic_arxiv_resource_is_not_an_identity(self):
        text = '# Paper\n**ArXiv ID:** 2601.12345\n## Resources\n- **arXiv**: https://arxiv.org/'
        self.assertEqual(validator.primary_identity(text), ('2601.12345', []))
        identity, errors = validator.primary_identity('**arXiv**: https://arxiv.org/')
        self.assertIsNone(identity)
        self.assertIn('missing primary', errors[0])

    def test_malformed_and_conflicting_identities(self):
        for text in (
            '**ArXiv ID:** 2601.123456',
            '**ArXiv ID:** pending',
            '**ArXiv ID:** 2601.12345\n**Paper ID:** 2601.22222',
            '**ArXiv ID:** [2601.12345](https://arxiv.org/abs/2601.22222)',
        ):
            with self.subTest(text=text):
                identity, errors = validator.primary_identity(text)
                self.assertIsNone(identity)
                self.assertTrue(errors)

    def test_repeated_same_identity_with_versions_is_consistent(self):
        self.assertEqual(validator.primary_identity(
            '**ArXiv ID:** 2601.12345v2\n**Paper ID:** 2601.12345'), ('2601.12345', []))


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'xai').mkdir()
        (self.root / 'xai/one.md').write_text('# One\n**ArXiv ID:** 2601.12345', encoding='utf-8')
        self.tracked = ['INDEX.md', 'README.md', 'CLAUDE.md', 'docs/guide.md', 'xai/one.md']

    def run_index(self, text):
        (self.root / 'INDEX.md').write_text(text, encoding='utf-8')
        return validator.validate_collection(self.root, self.tracked)

    def test_valid_collection_ignores_non_paper_docs_and_external_links(self):
        errors, papers, links = self.run_index(
            '[One](./xai/one.md#summary)\n[Website](https://example.com/readme.md)')
        self.assertEqual((errors, papers, links), ([], 1, 1))

    def test_broken_and_untracked_targets(self):
        errors, _, _ = self.run_index('[Missing](xai/missing.md)')
        self.assertTrue(any('missing paper target: xai/missing.md' in e for e in errors))
        self.assertTrue(any('paper not indexed: xai/one.md' in e for e in errors))

    def test_repeated_index_paths(self):
        errors, _, links = self.run_index('[One](xai/one.md)\n[Again](xai/one.md)')
        self.assertEqual(links, 2)
        self.assertTrue(any('repeated index path' in e for e in errors))

    def test_duplicate_papers_across_paths_and_versions(self):
        (self.root / 'xai/two.md').write_text('# Two\n- **ArXiv ID**: 2601.12345v3', encoding='utf-8')
        self.tracked.append('xai/two.md')
        errors, _, _ = self.run_index('[One](xai/one.md)\n[Two](xai/two.md)')
        self.assertTrue(any('duplicate primary ArXiv ID 2601.12345' in e and
                            'xai/one.md' in e and 'xai/two.md' in e for e in errors))

    def test_missing_tracked_file(self):
        (self.root / 'xai/one.md').unlink()
        errors, _, _ = self.run_index('[One](xai/one.md)')
        self.assertTrue(any('tracked paper is missing' in e for e in errors))

    def test_missing_identity_is_blocking(self):
        (self.root / 'xai/one.md').write_text('# One', encoding='utf-8')
        errors, _, _ = self.run_index('[One](xai/one.md)')
        self.assertTrue(any('missing primary' in e for e in errors))

    def test_missing_index(self):
        errors, papers, links = validator.validate_collection(self.root, self.tracked)
        self.assertEqual((errors, papers, links), (['INDEX.md: missing index'], 1, 0))


if __name__ == '__main__':
    unittest.main()
