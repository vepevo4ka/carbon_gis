# carbon_gis
- [ ] [ГИС карбонового полигона Покровский](https://carbonpolygon.nextgis.com/) 
- [ ] [сайт карбонового полигона Покровский](https://pokrovcarbon.ru/) 


## Описание

Проект работы с ГИС данными карбонового полигона "Покровский". Проект предназначен для хранения исходных файлов данных, стилей, обработанных слоев QGIS, выгруженных в веб NextGis результатов обработки. 

## Tools

- QGIS desktop 
- QGIS python console add-on
- QGIS NextGis connection add-on


## 📌 Structure

- **📄 `project.qgz`** – Основной файл проекта QGIS.
- **📁 `data/`** – Хранение пространственных данных:
  - **📁 `rasters/`** – растровые слои (`.tif`, `.png`, `.jpg`).
  - **📁 `vectors/`** – векторные слои (`.shp`, `.geojson`, `.kml`, `.gpkg`).
  - **📁 `db/`** – базы данных (`.gpkg`, `.sqlite`, PostGIS дампы `.sql`).
  - **📁 `tables/`** – табличные данные (`.csv`, `.txt`, `.xlsx`).
- **📁 `styles/`** – Файлы `.qml` для оформления слоев.
- **📁 `scripts/`** – Python-скрипты для обработки данных в QGIS.
- **📁 `exports/`** – результаты экспорта (карты, отчеты).
- **📁 `docs/`** – документация проекта.
- **📁 `config/`** – файлы конфигурации, например, `.env`.
- **📄 `.gitignore`** – исключенные файлы для Git.
- **📄 `requirements.txt`** – список зависимостей Python (если используются скрипты).




## Usage


## Support


## Roadmap



## Authors and acknowledgment

- amsha
- mike7109

## License


## Project status
running
