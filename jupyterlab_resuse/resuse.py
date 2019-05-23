import json
import os
import psutil

from traitlets import Float, Int, default
from traitlets.config import Configurable

from notebook.base.handlers import IPythonHandler

class MetricsHandler(IPythonHandler):
    def get(self):
        """
        Calculate and return current resource usage metrics
        """
        config = self.settings['nbresuse_display_config']
        cur_process = psutil.Process()
        all_processes = [cur_process] + cur_process.children(recursive=True)

        total_mem = psutil.virtual_memory()[0]
        
        rss = sum([p.memory_info().rss for p in all_processes])
        cpu_percent = sum([p.cpu_percent(interval=0.1) for p in all_processes])

        metrics = {
            'rss': rss,
            'total_mem': total_mem,
            'cpu_percent': cpu_percent,
        }
        self.write(json.dumps(metrics))

class ResourceUseDisplay(Configurable):
    """
    Holds server-side configuration for nbresuse
    """

    mem_warning_threshold = Float(
        0.1,
        help="""
        Warn user with flashing lights when memory usage is within this fraction
        memory limit.
        For example, if memory limit is 128MB, `mem_warning_threshold` is 0.1,
        we will start warning the user when they use (128 - (128 * 0.1)) MB.
        Set to 0 to disable warning.
        """,
        config=True
    )

    mem_limit = Int(
        0,
        config=True,
        help="""
        Memory limit to display to the user, in bytes.
        Note that this does not actually limit the user's memory usage!
        Defaults to reading from the `MEM_LIMIT` environment variable. If
        set to 0, no memory limit is displayed.
        """
    )

    @default('mem_limit')
    def _mem_limit_default(self):
        return int(os.environ.get('MEM_LIMIT', 0))
