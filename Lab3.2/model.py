class Model:
    def __init__(self):
        self._a = 0
        self._b = 0
        self._c = 0
        self._observers = []
        self.load()

    def maxmin(self, value):
        return max(0, min(100, value))

    def get_a(self): return self._a
    def get_b(self): return self._b
    def get_c(self): return self._c

    def set_a(self, value):
        a = self.maxmin(value)

        if a == self._a:
            return False

        if a > self._b:
            self._b = a
            if self._b > self._c:
                self._c = a

        self._a = a
        self.save()
        self.uved_observers()
        return True

    def set_b(self, value):
        b = self.maxmin(value)

        if b < self._a:
            b = self._a
        if b > self._c:
            b = self._c

        self._b = b
        self.save()
        self.uved_observers()
        return True

    def set_c(self, value):
        c = self.maxmin(value)

        if c == self._c:
            return False

        if c < self._b:
            self._b = c
            if self._b < self._a:
                self._a = c

        self._c = c

        self.save()
        self.uved_observers()
        return True

    def subscribe(self, callback):
        self._observers.append(callback)

    def uved_observers(self):
        for observer in self._observers:
            observer()

    def save(self):
        with open("abc.txt", "w") as f:
            lines = [str(self._a), str(self._b), str(self._c)]
            f.write(";".join(lines))

    def load(self):
        try:
            with open("abc.txt", "r") as f:
                abc = f.read()
                a, b, c = abc.split(";")
                self._a = int(a)
                self._b = int(b)
                self._c = int(c)

                if self._a > self._b:
                    self._b = self._a
                    if self._b > self._c:
                        self._c = self._b
                elif self._c < self._b:
                    self._b = self._c
                    if self._b < self._a:
                        self._a = self._b

        except:
            self._a = 0
            self._b = 0
            self._c = 0

            self.uved_observers()


