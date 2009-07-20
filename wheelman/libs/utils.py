class ObjDict(dict):
    def init(self, d): self.update(d)
    def __getattr__(self, attr): return self[attr]
    def __setattr__(self, attr, val): self[attr] = val
