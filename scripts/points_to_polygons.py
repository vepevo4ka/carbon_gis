from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsField,
    QgsFeatureRequest,
    QgsGeometry,
    QgsPointXY
)
from qgis.PyQt.QtCore import QVariant

# 1. Ищем слой с точками (замени "test spots" на точное имя слоя)
layer_points = QgsProject.instance().mapLayersByName("field_2_perimeter_points")[0]

# 2. Создаем слой-памяти (memory layer) для полигонов
#    Если твои точки в UTM (EPSG:32636), поменяй здесь crs=EPSG:32636
layer_polygon = QgsVectorLayer("Polygon?crs=EPSG:4326", "2field_2_polygon", "memory")
pr = layer_polygon.dataProvider()

# Добавим поля в атрибутивную таблицу
pr.addAttributes([
    QgsField("id", QVariant.Int),
    QgsField("name", QVariant.String)
])
layer_polygon.updateFields()

# 3. Формируем список полигонов (каждый описывается: ID, имя, список меток точек)
polygons_data = [
    # Блок I
    (1,  "I-1",  ["I1",  "I\"1",  "I\"2",  "I2"]),
    (2,  "I-2",  ["I2",  "I\"2",  "I\"3",  "I3"]),
    (3,  "I-3",  ["I3",  "I\"3",  "I\"4",  "I4"]),
    (4,  "I-4",  ["I4",  "I\"4",  "I\"5",  "I5"]),
    (5,  "I-5",  ["I5",  "I\"5",  "I\"6",  "I6"]),
    (6,  "I-6",  ["I6",  "I\"6",  "I\"6k", "I6k"]),

    # Блок II
    (7,  "II-1", ["II1",  "II\"1",  "II\"2",  "II2"]),
    (8,  "II-2", ["II2",  "II\"2",  "II\"3",  "II3"]),
    (9,  "II-3", ["II3",  "II\"3",  "II\"4",  "II4"]),
    (10, "II-4", ["II4",  "II\"4",  "II\"5",  "II5"]),
    (11, "II-5", ["II5",  "II\"5",  "II\"6",  "II6"]),
    (12, "II-6", ["II6",  "II\"6",  "II\"6k", "II6k"]),

    # Блок III
    (13, "III-1", ["III1",  "III\"1",  "III\"2",  "III2"]),
    (14, "III-2", ["III2",  "III\"2",  "III\"3",  "III3"]),
    (15, "III-3", ["III3",  "III\"3",  "III\"4",  "III4"]),
    (16, "III-4", ["III4",  "III\"4",  "III\"5",  "III5"]),
    (17, "III-5", ["III5",  "III\"5",  "III\"6",  "III6"]),
    (18, "III-6", ["III6",  "III\"6",  "III\"6k","III6k"]),

    # Блок IV
    (19, "IV-1", ["IV1",   "IV\"1",   "IV\"2",   "IV2"]),
    (20, "IV-2", ["IV2",   "IV\"2",   "IV\"3",   "IV3"]),
    (21, "IV-3", ["IV3",   "IV\"3",   "IV\"4",   "IV4"]),
    (22, "IV-4", ["IV4",   "IV\"4",   "IV\"5",   "IV5"]),
    (23, "IV-5", ["IV5",   "IV\"5",   "IV\"6",   "IV6"]),
    (24, "IV-6", ["IV6",   "IV\"6",   "IV\"6k",  "IV6k"]),
]

def coords_for_labels(layer, labels):
    """
    Возвращает список координат (QgsPointXY) в порядке, 
    соответствующем списку меток 'labels'.
    """
    # Формируем SQL-выражение вида "Point" IN ('I1','I"1',...)
    quoted = [f"'{l}'" for l in labels]
    expr = f"\"Point\" IN ({', '.join(quoted)})"
    request = QgsFeatureRequest().setFilterExpression(expr)
    
    # Собираем фичи (точки), у которых "Point" совпадает
    feats = list(layer.getFeatures(request))
    
    # Создадим словарь { label: индекс } для сортировки
    label_to_index = {lbl: i for i, lbl in enumerate(labels)}
    
    # Соберём (QgsPointXY, порядок)
    temp_list = []
    for f in feats:
        pt_label = f["Point"]
        geom = f.geometry()
        if not geom.isNull() and pt_label in label_to_index:
            idx = label_to_index[pt_label]
            pt = geom.asPoint()
            temp_list.append((pt, idx))
    
    # Сортируем по idx
    temp_list.sort(key=lambda x: x[1])
    
    # Извлекаем только координаты
    return [p[0] for p in temp_list]

# 4. Создаём полигоны для каждой записи в polygons_data
for poly_id, poly_name, labels in polygons_data:
    coords = coords_for_labels(layer_points, labels)
    
    # Если хотим ЗАМКНУТЬ полигон, повторяем первую точку в конце
    if len(coords) > 2:
        coords.append(coords[0])
    
    # Создаём геометрию
    polygon_geom = QgsGeometry.fromPolygonXY([coords])
    
    # Создаём объект (feature)
    feat_poly = QgsFeature()
    feat_poly.setGeometry(polygon_geom)
    feat_poly.setAttributes([poly_id, poly_name])
    
    # Добавляем в слой
    pr.addFeature(feat_poly)

# 5. Обновляем слой и добавляем его в проект
layer_polygon.updateExtents()
layer_polygon.triggerRepaint()
QgsProject.instance().addMapLayer(layer_polygon)

print("Готово! Все 24 полигона добавлены на карту.")
