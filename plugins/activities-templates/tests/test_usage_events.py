import asyncio
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
p=Path(__file__).resolve().parents[1]/'runtime/studio_library/usage_events.py'
s=importlib.util.spec_from_file_location('usage_events',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_sync_result_and_failure_count_once_without_arguments(self):
  with patch.object(m,'emit') as emit:
   fn=m.tracked(lambda secret: secret,'real-tool');self.assertEqual(fn('PRIVATE'),'PRIVATE');emit.assert_called_once();self.assertEqual(emit.call_args.args[:2],('real-tool','success'));self.assertNotIn('PRIVATE',str(emit.call_args))
  def fail():raise ValueError('PRIVATE')
  with patch.object(m,'emit') as emit,self.assertRaises(ValueError):m.tracked(fail,'real-tool')()
  self.assertEqual(emit.call_args.args[:2],('real-tool','failure'))
 def test_async_return(self):
  async def fn():return 42
  with patch.object(m,'emit') as emit:self.assertEqual(asyncio.run(m.tracked(fn,'async-tool')()),42)
  emit.assert_called_once()
 def test_registration_preserves_internal_function_calls(self):
  class Server:
   def tool(self,**kwargs):
    def register(fn):self.registered=fn;return fn
    return register
  server=Server();m.install(server)
  @server.tool(name='exact-name')
  def f():return 'ok'
  with patch.object(m,'emit') as emit:
   self.assertEqual(f(),'ok');emit.assert_not_called();self.assertEqual(server.registered(),'ok');emit.assert_called_once()
if __name__=='__main__':unittest.main()
