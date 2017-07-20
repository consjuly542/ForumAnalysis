class Module:
    def __init__(self, name, dir_origin, dir_target):
        self.module_name = name
        self.dir_origin = dir_origin
        self.dir_target = dir_target

    def run(self, *args):
        raise NotImplementedError("Method run not implemented")
