from addict import Dict
import os
import json


class Geojson:
    """
     Get geo json format
    """
    common_json = Dict({
        "type": "FeatureCollection",
        "features": []
    })

    @staticmethod
    def convertGeojsonData(rows, pointDistance, line):
        result = []
        for row in rows:
            row_as_dict = dict(row)
            result.append(row_as_dict)

        # output is the main content, rowOutput is the content from each record returned
        output = ""
        rowOutput = ""
        i = 0
        while i < len(result):

            firstCoord = (json.loads(result[i]['geometry']))
            result1 = firstCoord['coordinates']

            try:
                secondCoord = (json.loads(result[i + int(pointDistance)]['geometry']))
                result2 = secondCoord['coordinates']
            except IndexError:
                pass

            if result[i]['geometry'] is not None:
                coordinates = [
                    result1,
                    result2
                ]

                generateCoord = json.dumps({'type': 'Point', 'coordinates': coordinates})
                # If it's the first record, don't add a comma
                comma = "," if i > 0 else ""
                rowOutput = comma + '{"type": "Feature", "geometry": ' + str(generateCoord) + ', "properties": {'
                properties = ""

                j = 0
                comma = "," if j > 0 else ""
                properties += comma + '"' + "geom" + '":"' + str(result[i]['geom']) + '"'
                # j += 1

                rowOutput += properties + ', "lines":' + str(line) + '}'
                rowOutput += '}'

                output += rowOutput

            # start over
            rowOutput = ""

            i += int(pointDistance)

        # Assemble the GeoJSON
        totalOutput = '{ "type": "FeatureCollection", "features": [ ' + output + ' ]}'

        return totalOutput

    @staticmethod
    def get_geo_json(**kwargs) -> Dict:
        """
        Geo json Features format
        value: Dict,
        area: float,
        height: float, width: float,
        type: str
        """
        params = Dict(kwargs)

        if params.type == "Point":
            geom_type = {
                "type": params.type,
                "coordinates": [
                    params.lon,
                    params.lat
                ]
            }
        if params.type == "Polygon":
            geom_type = {
                "type"          : params.type,
                "coordinates"   : params.segmentation
            }
        if params.format == "paired":
            return Dict(
                {
                    "type": "Feature",
                    "properties": {
                        "score_1"           : params.score_1,
                        "score_2"           : params.score_2,
                        "objId_1"           : params.objId_1,
                        "objId_2"           : params.objId_2,
                        "bbox_1"            : params.bbox_1,
                        "bbox_2"            : params.bbox_2,
                        "segmentation_1"    : params.segmentation_1,
                        "segmentation_2"    : params.segmentation_2,
                        "panoId_1"          : params.panoId_1,
                        "panoId_2"          : params.panoId_2,
                    },
                    "geometry": geom_type
                })

        if params.format == "actual":
            return Dict(
                {
                    "type": "Feature",
                    "properties": {
                        "average_score"     : params.avg_score,
                        "classname"         : params.classname,
                        "area"              : params.area,
                        "height"            : params.height,
                        "width"             : params.width,
                        "confidence"        : params.confidence,
                        "match_id"          : params.match_id,
                        "matchedPoints"     : params.matchedPoints
                    },
                    "geometry": geom_type
                })

    @staticmethod
    def convert_dict_to_geojson(params: Dict, type: str) -> json:
        for key, value in params.items():
            value = Dict(value)
            ff = Geojson.get_geo_json(lat=value.lat, lon=value.lon,
                                      classname=value.classname,
                                      area=value.area,
                                      score=value.average_score,
                                      key=key,
                                      type=type)
            Geojson.common_json.features.append(ff)

        return Geojson.common_json


    @staticmethod
    def create_geojson_format(input):
        geoform = []
        for key, params in input.items():
            params = Dict(params).geojson

            geoform.append(Geojson.get_geo_json(**params))

        return geoform

    @staticmethod
    def export(points: Dict):
        """
        Export geo json format
        """
        Geojson.common_json.features = points
        with open(os.path.join('Exports', 'detected_points.json'), 'w') as f:
            json.dump(Geojson.common_json, f)
