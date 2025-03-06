from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsPointXY
)
from qgis.PyQt.QtCore import QVariant

# Если ваши координаты в UTM (EPSG:32636),
# замените "Polygon?crs=EPSG:4326" на "Polygon?crs=EPSG:32636"
layer_polygon = QgsVectorLayer("Polygon?crs=EPSG:4326", "Perim Polygons", "memory")
pr = layer_polygon.dataProvider()

# Добавим поля в таблицу (например, id, name)
pr.addAttributes([
    QgsField("id", QVariant.Int),
    QgsField("name", QVariant.String)
])
layer_polygon.updateFields()

# --- СЛОВАРЬ ВСЕХ ТОЧЕК (X, Y) ---

all_points = {
    "Perim1":  (34.993914, 54.910743),
    "Perim2":  (34.995005, 54.910395),
    "Perim3":  (34.996095, 54.910047),
    "Perim4":  (34.997186, 54.909699),
    "Perim5":  (34.993702, 54.910523),
    "Perim6":  (34.994793, 54.910175),
    "Perim7":  (34.995883, 54.909827),
    "Perim8":  (34.996974, 54.909479),

    "Perim9":  (34.99368,  54.9105),
    "Perim10": (34.994771, 54.910152),
    "Perim11": (34.995861, 54.909804),
    "Perim12": (34.996952, 54.909456),
    "Perim13": (34.993468, 54.91028),
    "Perim14": (34.994559, 54.909932),
    "Perim15": (34.995649, 54.909584),
    "Perim16": (34.99674,  54.909236)
}

# --- СПИСОК ПОЛИГОНОВ ---
# Здесь я предполагаю, что первые 8 точек составляют один полигон,
# а вторые 8 — второй полигон. Порядок точек - примерный!
# Если линии будут пересекаться, меняйте порядок.
polygons_data = [
    # (ID, "Имя полигона", [список точек по порядку])
    (1, "Polygon1", ["Perim1", "Perim2", "Perim3", "Perim4", "Perim8", "Perim7", "Perim6", "Perim5"]),
    (2, "Polygon2", ["Perim9", "Perim10", "Perim11", "Perim12", "Perim16", "Perim15", "Perim14", "Perim13"])
]

def create_polygon(coords):
    """
    Принимает список QgsPointXY (в порядке обхода),
    замыкает их и создаёт геометрию полигона.
    """
    if len(coords) > 2:
        coords.append(coords[0])  # замыкаем
    return QgsGeometry.fromPolygonXY([coords])

# 2. Генерируем полигоны и добавляем их в слой
for poly_id, poly_name, point_labels in polygons_data:
    # Получаем координаты в заданном порядке
    coords_list = []
    for lbl in point_labels:
        x, y = all_points[lbl]
        coords_list.append(QgsPointXY(x, y))
    
    # Создаём полигон
    poly_geom = create_polygon(coords_list.copy())
    
    # Создаём объект (feature) и задаём атрибуты
    feat = QgsFeature()
    feat.setGeometry(poly_geom)
    feat.setAttributes([poly_id, poly_name])
    
    pr.addFeature(feat)

# 3. Обновляем слой и добавляем его в проект
layer_polygon.updateExtents()
layer_polygon.triggerRepaint()
QgsProject.instance().addMapLayer(layer_polygon)

print("Готово! Два полигона (Polygon1 и Polygon2) добавлены на карту.")
