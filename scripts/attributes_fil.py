from qgis.core import QgsProject, edit, QgsCategorizedSymbolRenderer
from qgis.PyQt.QtCore import QDate

# 1. Получаем слой
layer = QgsProject.instance().mapLayersByName("field_2_polygon")[0]  # замени "My polygons" на реальное имя

# # 2. Считываем рендерер, если он Categorized
# renderer = layer.renderer()
# cat_dict = {}
# if isinstance(renderer, QgsCategorizedSymbolRenderer):
#     # Строим словарь: { значение_категории : метка_категории }
#     # Пример: { 1 : "травы_клевер", 2 : "эспарцет", ... }
#     for cat in renderer.categories():
#         cat_dict[cat.value()] = cat.label()
# else:
#     print("Внимание: слой не использует Categorized Renderer. 'crop' заполниться не сможет.")
#     # Можно либо прервать, либо продолжить только с year и repetition

# 3. Переходим в режим редактирования слоя
with edit(layer):
    for feat in layer.getFeatures():
        # Устанавливаем год 2024 (берём 1 января 2024)
        feat["field"] = int(2)
        feat["year"] = QDate(2023,1,1)    
        # # Логика repetition по полю name
        # name_val = feat["name"]
        # if isinstance(name_val, str):
        #     # Смотрим начало строки
        #     if name_val.startswith("I\"") or name_val.startswith("I-") or name_val.startswith("I "):
        #         feat["repetition"] = 1
        #     elif name_val.startswith("II"):
        #         feat["repetition"] = 2
        #     elif name_val.startswith("III"):
        #         feat["repetition"] = 3
        #     elif name_val.startswith("IV"):
        #         feat["repetition"] = 4
        #     else:
        #         feat["repetition"] = None
        # else:
        #     feat["repetition"] = None
        
        # # Заполняем crop на основе категории
        # # Предположим, что поле для категоризации - это "id"
        # # И cat_dict[id] = метка_стиля, например "травы_клевер"
        # if cat_dict:
        #     val_id = feat["id"]  # или другое поле, по которому идёт классификация
        #     if val_id in cat_dict:
        #         feat["crop"] = cat_dict[val_id]
        #     else:
        #         feat["crop"] = None
        
        layer.updateFeature(feat)

print("Готово!  заполнены.")
