from concurrent.futures import ThreadPoolExecutor, wait, Future
import sys
from pysquid import stream_logger
from pysquid.plugin import Hook
from pysquid.core import _ID_TASK


class ThreadedEngine():

    def __init__(self, template, plugins, except_hook=None, log=None):
        self.template = template
        self.plugins = plugins
        self.log = log if log else stream_logger()
        self.except_hook = except_hook if except_hook else self.inbuilt_except_hook
        sys.except_hook = self.except_hook
        self.exceptions = []
        self.pools = {}

    def inbuilt_except_hook(self, exctype, value, tb):
        """
        Catch exceptions
        """
        self.log.info(f'Exception: {exctype}, {value}, {tb}')
        self.exceptions.append({'type': exctype})
        
    def build(self):

        services = self.template.get(_ID_TASK)
        plugins = self.plugins
        
        pools = {
            'thread': {}
        }

        playbook = {}

        for sid, service in services.items():

            mode = service.get('__mode__')
            plugin = service.get('__plugin__')
            workers = service.get('__workers__')

            if mode not in pools or plugin not in plugins:
                continue

            enabled_workers = set(workers.keys())

            plugin_ = plugins.get(plugin)()
            plugin_.add_service(service, self.template)

            setup = plugin_.iterate_workers(enabled_workers)

            for pid, stages in setup.items():
                if pid not in playbook:
                    playbook[pid] = {}
                    
                for sid, stage in stages.items():
                    if sid not in playbook[pid]:
                        playbook[pid][sid] = []

                    playbook[pid][sid] = playbook[pid][sid] + setup[pid][sid] 

        pools['thread'] = playbook
        self.pools = pools
        
    def exec_pool(self, hook: Hook = None):

        pools = self.pools.get('thread')        
        futures = set()

        hook = hook if isinstance(hook, Hook) else Hook()

        for pid, pool in pools.items():
            self.log.info(f'Running pool {pid}')
            e = ThreadPoolExecutor()

            try:            
                future = e.submit(self.exec_workers, pool, hook)

                if isinstance(future, Future):
                    futures.add(future)

            except Exception as e:
                self.log.info(f'Error submitting pool: {e!r}')

        self.log.info(f'Waiting on {futures}')
        wait(futures)

        for finished_worker in futures:
            self.log.info(finished_worker.__dict__)
        
        self.log.info(f'Future done: {futures}')
            
    def exec_workers(self, pool, hook):

        e = ThreadPoolExecutor()
        futures = set()

        pipeline = dict(sorted(pool.items(), key=lambda item: item[0]))
        
        for sid, stage in pipeline.items():
            
            for worker in stage:
                # Set worker and run init

                try:
                    hook.set_worker(worker)
                    hook.init()                
                    worker.pre()
                    future = e.submit(worker.apply)

                    if isinstance(future, Future):
                        futures.add(future)

                except Exception as e:
                    self.log.info(f'Error submitting worker: {e!r}')

            wait(futures)

            for finished_worker in futures:
                self.log.info(finished_worker.__dict__)

            for worker in stage:

                try:                
                    worker.post()
                    hook.set_worker(worker)
                    hook.cleanup()

                except Exception as e:
                    self.log.info(f'Error submitting worker: {e!r}')
                
        return True
    


