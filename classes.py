class ObfuscatedDict(dict):
    def __str__(self):
        return "We're pretty sure you didn't mean to access this. If you did try accessing the __dict__ attribute of " \
               "this object."

    def __repr__(self):
        return str(self)