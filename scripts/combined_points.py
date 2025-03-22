from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsPointXY,
    QgsCoordinateTransform
)
from qgis.PyQt.QtCore import QVariant

# Определим, какие слои и какие поля берем
layers_info = [
    ("points2020", "num2020", "нет_поля", 2020),
    ("points2023", "Name",    "name_2",   2023),
    ("points2024", "num",     "нет_поля", 2024)
]

def get_layer_by_name(layer_name):
    """Возвращает первый найденный слой с таким именем, либо None."""
    found = QgsProject.instance().mapLayersByName(layer_name)
    return found[0] if found else None

# Целевая система координат (EPSG:4326)
target_crs_id = "EPSG:4326"

# Создаем новый memory-слой, куда будем складывать все точки
combined_layer = QgsVectorLayer(f"Point?crs={target_crs_id}", "combined_points", "memory")
dp = combined_layer.dataProvider()

# Добавляем нужные поля: name, second_name, x, y, year
fields = [
    QgsField("name", QVariant.String),
    QgsField("second_name", QVariant.String),
    QgsField("x", QVariant.Double),
    QgsField("y", QVariant.Double),
    QgsField("year", QVariant.Int)
]
dp.addAttributes(fields)
combined_layer.updateFields()

def copy_and_transform(src_layer, name_field, second_field, year_value):
    """Копирует геометрию слоя (трансформируя в EPSG:4326) + атрибуты в combined_layer."""
    if not src_layer or not src_layer.isValid():
        print(f"Слой {src_layer} невалиден или не найден.")
        return

    # Создаем объект трансформации: из CRS слоя → EPSG:4326
    transform = QgsCoordinateTransform(
        src_layer.crs(),
        combined_layer.crs(),
        QgsProject.instance()
    )

    for feat in src_layer.getFeatures():
        # Извлекаем name
        if name_field in src_layer.fields().names():
            name_val = feat[name_field]
        else:
            name_val = ""

        # Извлекаем second_name
        if second_field in src_layer.fields().names():
            second_val = feat[second_field]
        else:
            second_val = ""

        # Берем геометрию
        geom = feat.geometry()
        if not geom or geom.isEmpty():
            continue

        # Клонируем геометрию, чтобы не портить оригинал
        geom_clone = QgsGeometry(geom)
        # Применяем трансформацию (geom_clone станет в EPSG:4326)
        result_code = geom_clone.transform(transform)
        if result_code != 0:
            # 0 = OK, иначе ошибка
            continue

        # Получаем координаты точки (в EPSG:4326, градусы)
        pt = geom_clone.asPoint()
        x_val = pt.x()
        y_val = pt.y()

        # Создаем новую фичу в combined_layer
        new_feat = QgsFeature(combined_layer.fields())
        new_feat.setAttribute("name", name_val)
        new_feat.setAttribute("second_name", second_val)
        new_feat.setAttribute("x", x_val)
        new_feat.setAttribute("y", y_val)
        new_feat.setAttribute("year", year_value)
        new_feat.setGeometry(geom_clone)

        dp.addFeatures([new_feat])

# Копируем данные из всех заданных слоев
for lyr_name, name_fld, second_fld, yr in layers_info:
    layer_obj = get_layer_by_name(lyr_name)
    copy_and_transform(layer_obj, name_fld, second_fld, yr)

# Обновляем экстент и добавляем слой в проект
combined_layer.updateExtents()
QgsProject.instance().addMapLayer(combined_layer)

print("Готово! Все точки перенесены и преобразованы к EPSG:4326 в слой 'combined_points'.")
