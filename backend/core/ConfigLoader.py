import yaml

# class ConfigLoad(dict):
#     def __init__(self, pathConfFile: str) -> None:
#         self.pathConfFile = pathConfFile
#         self.config = None
#         self.loadConfig()

#     def loadConfig(self) -> None:
#         try:
#             with open(self.pathConfFile, "r") as f:
#                 self.config = yaml.load(f, Loader=yaml.FullLoader)

#             for k, v in self.config.items():
#                 self.__setattr__(k, v)

#         except ValueError:
#             raise ValueError("The configuration file does not exist")

#     def __setitem__(self, key, item):
#         self.config[key] = item
#         self.__setattr__(key, item)

#     def __getitem__(self, key):
#         if not self.has_key(key):
#             if self.__getattribute__(key):
#                 self.config[key] = self.__getattribute__(key)
#         return self.config[key]

#     def __repr__(self):
#         return repr(self.config)

#     def __len__(self):
#         return len(self.config)

#     def __delitem__(self, key):
#         del self.config[key]

#     def clear(self):
#         return self.config.clear()

#     def copy(self):
#         return self.config.copy()

#     def has_key(self, k):
#         return k in self.config

#     def update(self, *args, **kwargs):
#         return self.config.update(*args, **kwargs)

#     def keys(self):
#         return self.config.keys()

#     def values(self):
#         return self.config.values()

#     def items(self):
#         return self.config.items()

#     def pop(self, *args):
#         return self.config.pop(*args)

#     def __cmp__(self, dict_):
#         return self.__cmp__(self.config, dict_)

#     def __contains__(self, item):
#         return item in self.config

#     def __iter__(self):
#         return iter(self.config)

    # def __unicode__(self):
    #     return unicode(repr(self.__dict__))


class ConfigLoader(dict):
    def __init__(self, file_path):
        self.file_path = file_path
        self.load()

    def load(self):
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
                if data is not None:
                    self.update(data)
        except FileNotFoundError:
            pass

    def save(self):
        with open(self.file_path, 'w') as file:
            yaml.dump(dict(self), file)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.save()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.save()

    def add(self, key, value):
        super().update({key: value})
        self.save()

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"'ConfigDict' object has no attribute '{name}'")

Configuration = ConfigLoader('./conf.yaml')

if __name__ == "__main__":

    Configuration['name'] = 'John'
    Configuration['age'] = 30
    Configuration.update({'country': 'USA'})
    Configuration.add('username', 'line')

    print(Configuration.name)
    print(Configuration.age)
    print(Configuration.country)