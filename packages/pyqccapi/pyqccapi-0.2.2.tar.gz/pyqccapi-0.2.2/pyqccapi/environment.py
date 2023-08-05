class Environment(object):
    _env = None  # type: Environment

    def __init__(self, config):
        Environment._env = self
        self.config = config

    @classmethod
    def to_instance(cls):
        if Environment._env is None:
            raise RuntimeError(
                u'Environment has not been created. Use `Environment(config=your_config_path)` before api invoke.')
        return Environment._env

    def to_config(self):
        return self.config