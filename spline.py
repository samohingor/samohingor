"""
Аппроксимация кубическими сплайнами
"""
import array
import numpy

class spline:
    def __init__ (self, xval, yval):
        self.xval = xval
        self.yval = yval
        assert (len (xval) == len(yval) )
        
        n = len (xval)
        self.m = numpy.array ([0.0] * n, "d")
        l = numpy.array ([0.0] * n, "d")
        r = numpy.array ([0.0] * n, "d")
        s = numpy.array ([0.0] * n, "d")
        
        d = xval[1] - xval[0]
        e = (yval[1] - yval[0]) / d
        
        for k in range (1, n - 1):
            h = d
            d = xval[k + 1] - xval[k]
            
            f = e
            e = (yval[k + 1] - yval[k]) / d
            
            l[k] = d / (d + h)
            r[k] = 1 - l[k]
            s[k] = 6 * (e - f) / (h + d)
            
        for k in range (1, n - 1):
            p = 1.0 / (r[k] * l[k - 1] + 2)
            l[k] *= -p
            s[k] = (s[k] - r[k] * s[k - 1]) * p
            
        self.m[n - 1] = 0
        l[n - 2] = s[n - 2]
        self.m[n - 2] = l[n - 2]
        
        for k in range (n - 3, -1, -1):
            l[k] = l[k] * l[k + 1] + s[k]
            self.m[k] = l[k]
            
    def interpolate (self, xpoint):
        i = 0
        while (xpoint > self.xval[i]):
            i += 1
        j = i - 1
        d = self.xval[i] - self.xval[j]
        h = xpoint - self.xval[j]
        r = self.xval[i] - xpoint
        p = d * d / 6.0
        y = (self.m[j] * r * r * r + self.m[i] * h * h * h) / (6.0 * d)
        y += ((self.yval[j] - self.m[j] * p) * r + (self.yval[i] - self.m[i] * p) * h) / d
        return y
            
    def extrapolateRight (self, xpoint):
        n = len (self.xval)
        d = self.xval[n - 1] - self.xval[n - 2]
        y = d * self.m[n - 2] / 6.0 + (self.yval[n - 1] - self.yval[n - 2]) / d
        y = y * (xpoint - self.xval[n - 1]) + self.yval[n - 1]
        return y
        
    def extrapolateLeft (self, xpoint):
        d = self.xval[1] - self.xval[0];
        y = -d * self.m[1] / 6.0 + (self.yval[1] - self.yval[0]) / d
        y = y * (xpoint - self.xval[0]) + self.yval[0]
        return y
        
    def getValue (self, xpoint):
        if (xpoint > self.xval[len (self.xval) - 1]):
            return self.extrapolateRight (xpoint)

        if (xpoint <= self.xval[0]):
            return self.extrapolateLeft (xpoint)

        return self.interpolate (xpoint)