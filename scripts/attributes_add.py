from qgis.core import QgsProject, QgsField, edit, QgsEditorWidgetSetup
from qgis.PyQt.QtCore import QVariant

# 1. Получаем слой, куда добавляем поля
layer = QgsProject.instance().mapLayersByName("Perim Polygons")[0]

# 2. Формируем список полей, которые хотим добавить
fields_to_add = [
    QgsField("id", QVariant.Int),
    QgsField("name", QVariant.String),
    QgsField("field", QVariant.String),
    QgsField("crop", QVariant.String),
    QgsField("repetition", QVariant.Int),
    QgsField("test_plot", QVariant.Int),
    QgsField("old_number", QVariant.Int),
    QgsField("year", QVariant.Date)
]

# 3. Добавляем поля в слой
with edit(layer):
    layer.dataProvider().addAttributes(fields_to_add)
    layer.updateFields()

# 4. Настраиваем виджет для поля year (формат yyyy)
year_idx = layer.fields().indexOf("year")
if year_idx != -1:
    config = {"field_format": "yyyy"}  # как показывать дату
    widgetSetup = QgsEditorWidgetSetup("DateTime", config)
    layer.setEditorWidgetSetup(year_idx, widgetSetup)

print("Все нужные поля добавлены в 'field_1_plots_polygon', формат даты year = yyyy")
