#-*- coding: utf-8 -*-

import math


class Point():


    def __init__(self, x, y):
        self.x = x
        self.y = y

    def multiplyBy(self, num):
        return Point(self.x * num, self.y * num)


class Transform():


    def __init__(self, a, b, c, d):
        self._a = a
        self._b = b
        self._c = c
        self._d = d


    def transform(self, point, scale): 
        scale = scale or 1
        point.x = scale * (self._a * point.x + self._b)
        point.y = scale * (self._c * point.y + self._d)
        return point


    def untransform(self, point, scale):
        scale = scale or 1;
        return Point((point.x / scale - self._b) / self._a, (point.y / scale - self._d) / self._c)

class LatLng():
    DEG_TO_RAD = math.pi / 180
    RAD_TO_DEG = 180 / math.pi
    
    def __init__(self, rawLat, rawLng, noWrap):
        lat = float(rawLat)
        lng = float(rawLng)

        if not noWrap:
            lat = math.max(math.min(lat, 90), -90)
            lng = (lng + 180) % 360
            if  (lng < -180 or lng == 180):
                lng_fix = 180 
            else:
                lng_fix = -180
            lng += lng_fix

        self.lat = lat
        self.lng = lng


class SphericalMercator():
    MAX_LATITUDE = 85.0511287798

    def project(self, latlng):
        d = LatLng.DEG_TO_RAD
        maxl = SphericalMercator.MAX_LATITUDE
        lat = max(min(maxl, latlng.lat), -maxl)
        x = latlng.lng * d
        y = lat * d
        y = math.log(math.tan((math.pi / 4) + (y / 2)))
        return Point(x, y)

    def unproject(self, point):
        d = LatLng.RAD_TO_DEG
        lng = point.x * d
        lat = (2 * math.atan(math.exp(point.y)) - (math.pi / 2)) * d

        return LatLng(lat, lng, True)


class CRS():
    def latLngToPoint(self, latlng, zoom):
        projectedPoint = self.projection.project(latlng)
        scale = self.scale(zoom)
        return self.transformation.transform(projectedPoint, scale)


    def pointToLatLng(self, point, zoom):
        scale = self.scale(zoom)
        untransformedPoint = self.transformation.untransform(point, scale)

        return self.projection.unproject(untransformedPoint)
    

    def project(self, latlng):
        return self.projection.project(latlng);
    

    def scale(self, zoom):
        return 256 * math.pow(2, zoom)


class CRS_EPSG3857(CRS):
    def __init__(self):
        self.code = 'EPSG:3857'
        self.projection = SphericalMercator()
        self.transformation = Transform(0.5 / math.pi, 0.5, -0.5 / math.pi, 0.5)

    def project(self, latlng):
        projectedPoint = self.projection.project(latlng)
        earthRadius = 6378137
        return projectedPoint.multiplyBy(earthRadius)


class Tile():

    def __init__(self, x, y, zoom, size = 256):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.size = size
        self._crs = CRS_EPSG3857()

    def getPixelBounds(self):
        point_min = Point(self.x * self.size, self.y * self.size)
        point_max = Point((self.x + 1) * self.size - 1, (self.y + 1) * self.size - 1)
        return (point_min, point_max)

    def getBounds(self):
        point_min, point_max = self.getPixelBounds()
        latlng_1 = self._crs.pointToLatLng(point_min, self.zoom)
        latlng_2 = self._crs.pointToLatLng(point_max, self.zoom)
        latlng_min = LatLng(min(latlng_1.lat, latlng_2.lat), min(latlng_1.lng, latlng_2.lng), True)
        latlng_max = LatLng(max(latlng_1.lat, latlng_2.lat), max(latlng_1.lng, latlng_2.lng), True)
        return (latlng_min, latlng_max)

    @staticmethod
    def tileByPoint(point, zoom):
        return Tile(point.x, point.y, zoom)
if __name__ == '__main__':
    test = CRS_EPSG3857()
    latlng = LatLng(25.48295, -45.70312, True)
    point = test.latLngToPoint(latlng, 2)
    print point.x, point.y
    print int(point.x / 256), int(point.y / 256)
    tile = Tile.tileByPoint(point, 2)
    l_min, l_max =  tile.getBounds()
    point2 = Point(int(point.x / 256), int(point.y / 256))
    latlng2 = test.pointToLatLng(point2, 2)
    print latlng2.lat, latlng2.lng

