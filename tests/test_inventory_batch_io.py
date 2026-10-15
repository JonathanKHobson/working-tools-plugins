"""The Git batch must consume a large request while returning large early blobs."""
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from release_manager.inventory import expected_package_files

class BatchIOTest(unittest.TestCase):
    def test_request_larger_than_pipe_with_large_first_blob(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);plugin=root/'plugins/demo';plugin.mkdir(parents=True)
            subprocess.run(['git','init','-q'],cwd=root,check=True)
            data=b'a'*100000;(plugin/'000-big.txt').write_bytes(data)
            for i in range(600):(plugin/f'file-{i:04}.txt').write_text(str(i))
            subprocess.run(['git','add','.'],cwd=root,check=True)
            subprocess.run(['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture'],cwd=root,check=True)
            result=expected_package_files(root,'HEAD','demo')
            self.assertEqual(len(result),601)
            self.assertEqual(result['000-big.txt'],hashlib.sha256(data).hexdigest())
            self.assertEqual(list((root/'dist').iterdir()),[])

if __name__=='__main__':unittest.main()
