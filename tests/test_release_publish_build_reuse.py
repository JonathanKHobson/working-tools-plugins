"""Exact source builds are shared only inside one publication invocation."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import complete_update
from release_manager import local_sync


class PublishBuildReuseTests(unittest.TestCase):
    def test_shared_commit_build_once_distinct_commits_build_separately(self):
        for sources in [('a'*40,'a'*40),('a'*40,'b'*40)]:
            with self.subTest(sources=sources),tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                records=[{'id':ident,'version':'1.0.1'} for ident in ('x','y')]
                (root/'catalog').mkdir()
                local_sync.write(root/'catalog/packages.json',{'packages':records})
                for row in records:
                    folder=root/'catalog/releases'/row['id'];folder.mkdir(parents=True)
                    local_sync.write(folder/'1.0.1.json',{'notes':'Specific '+row['id']+' change'})
                def build(_root,source,out):
                    out.mkdir(parents=True,exist_ok=True)
                    packages=[]
                    for row in records:
                        filename=row['id']+'-1.0.1.zip'
                        (out/filename).write_bytes(row['id'].encode())
                        (out/(Path(filename).stem+'.files.json')).write_text('{}')
                        packages.append({**row,'file':filename,'sha256':'c'*64,'files':{}})
                    return {'packages':packages}
                with (patch.object(complete_update,'ROOT',root),
                      patch.object(complete_update,'run',side_effect=[s.encode() for s in sources]),
                      patch.object(complete_update,'exact_commit_build',side_effect=build) as builds,
                      patch.object(complete_update,'publish',return_value={'html_url':'https://example.test/release'}) as publish):
                    receipt={'changed':records,'published':[]}
                    result=complete_update.publish_pending({},receipt)
                    self.assertEqual(builds.call_count,len(set(sources)))
                    self.assertEqual(publish.call_count,2)
                    self.assertEqual([r['id'] for r in result],['x','y'])
                    self.assertEqual([r['source_commit'] for r in result],list(sources))
                    for call,row,source in zip(publish.call_args_list,records,sources):
                        self.assertEqual(call.args[1]['id'],row['id'])
                        self.assertEqual(call.args[2],source)
                        self.assertEqual(call.kwargs['notes'],'Specific '+row['id']+' change')
                        self.assertEqual(len(call.args[3]),3)
                    # A later invocation must rebuild; no persistent evidence bypass.
                    complete_update.run.side_effect=[s.encode() for s in sources]
                    complete_update.publish_pending({},receipt)
                    self.assertEqual(builds.call_count,2*len(set(sources)))
                    self.assertEqual(publish.call_count,4)


if __name__=='__main__':unittest.main()
