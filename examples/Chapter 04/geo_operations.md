---
theme: default
title: "Линейка для карты: как измерить страну и границу"
info: |
  Разбор скриптов из Chapter 04 книги «Python Geospatial Development».
  Рамка вокруг страны, общая граница, длина, смена системы координат, компас, гистограмма — простыми словами.
layout: cover
class: text-center
transition: slide-left
mdc: true
---

# 📏 Линейка для карты

## Как измерить страну, границу и расстояние

<div class="mt-10 text-xl opacity-80">
Глава 04 · OGR · Shapely · pyproj · GDAL
</div>

<div class="mt-12 text-sm opacity-60">
Презентация для тех, кто ещё не знает, что такое ГИС
</div>

<!--
Задача занятия: показать, что карта — это набор фигур, и по ним можно
считать: где страна, какая у неё граница, сколько километров, где парк.
Никакой магии: прочитать → посчитать → показать.
-->

---
layout: center
class: text-center
---

# Карта — это не картинка 🙂

<div class="mt-8 grid grid-cols-3 gap-6 text-left text-base">

<div class="p-5 rounded-xl bg-blue-50">
<div class="text-3xl">🔴</div>
<b>Точка</b><br/>
Одно место: тут парк
</div>

<div class="p-5 rounded-xl bg-green-50">
<div class="text-3xl">➖</div>
<b>Линия</b><br/>
Дорога, река, граница
</div>

<div class="p-5 rounded-xl bg-amber-50">
<div class="text-3xl">⬛</div>
<b>Полигон</b><br/>
Страна, озеро, город
</div>

</div>

<div class="mt-10 text-xl">
Если это фигуры, то их можно <b>измерить</b>: рамкой, линейкой, циркулем.
</div>

<div class="mt-6 text-base opacity-70">
Именно этим и занимаются девять скриптов из главы 04.
</div>

<!--
Спросить детей: что можно узнать про страну, если у тебя есть её контур?
Подвести к ответам: где она (рамка), с кем граничит, какая граница длинная,
далеко ли парк от города.
-->

---
class: text-sm
---

# Семь вопросов — девять скриптов

| Вопрос | Скрипт | Что получается |
| --- | --- | --- |
| Где страна на карте? | `calcBoundingBoxes.py` | рамка вокруг каждой страны |
| Что у двух стран общее? | `calcCommonBorder.py` | линия общей границы |
| Сколько километров у границы? | `calcBorderLength.py` | длина в километрах |
| Где те же дороги в другой системе? | `changeDatum.py`, `changeProjection.py` | новый шейп-файл |
| Куда я приду, если пойду на запад? | `findShoshone.py` | новые координаты |
| Какой парк рядом с городом? | `findNearbyParks.py` | список парков |
| Сколько земли на каждой высоте? | `histogram.py` | таблица «высота → клетки» |

<div class="mt-4 p-4 rounded-xl bg-gray-50">
<b>Главное:</b> везде один и тот же порядок работы — <b>прочитать</b> данные,
<b>посчитать</b>, <b>напечатать</b> или <b>записать</b> в новый файл.
</div>

<!--
Не надо запоминать имена скриптов. Надо запомнить, что вопрос всегда
превращается в «прочитать → посчитать → записать».
-->

---
layout: section
---

# 📦 Часть 1. Рамка вокруг страны

## «Где ты живёшь?» — «Вот в этом прямоугольнике»

---
layout: two-cols
---

# `calcBoundingBoxes.py`: рамка

```python
shapefile = ogr.Open("TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = feature.GetGeometryRef()

    # minX, maxX, minY, maxY
    minLong, maxLong, minLat, maxLat = geometry.GetEnvelope()
```

<div class="mt-3 p-4 rounded-xl bg-green-50 text-sm">
<b>Envelope</b> — самый маленький прямоугольник,<br/>
в который помещается вся страна.<br/>
Как коробка для подарка неправильной формы 🎁
</div>

::right::

<div class="text-center mt-2">
<svg viewBox="0 0 260 190" class="w-full">
  <rect x="0" y="0" width="260" height="190" fill="#fafafa"/>
  <path d="M70 40 L120 30 L165 60 L180 110 L150 155 L95 150 L60 105 Z"
        fill="#a5d6a7" stroke="#2e7d32" stroke-width="2"/>
  <rect x="60" y="30" width="120" height="125"
        fill="none" stroke="#c62828" stroke-width="2" stroke-dasharray="7 5"/>
  <text x="66" y="24" style="font-size:11px" fill="#b71c1c">maxLat</text>
  <text x="66" y="172" style="font-size:11px" fill="#b71c1c">minLat</text>
  <text x="188" y="90" style="font-size:11px" fill="#b71c1c">maxLong</text>
</svg>
</div>

<div class="text-center text-sm opacity-70">
Рамка почти всегда <b>больше</b> самой страны —<br/>
она не умеет повторять изгибы.
</div>

<!--
Аналогия: обвести страну прямоугольником по крайним точкам.
Рамка нужна, чтобы быстро понять, куда смотреть: в какой кусок карты.
-->

---
---

# Что печатает скрипт

```python
countries.sort()

for name, code, minLat, maxLat, minLong, maxLong in countries:
    print("{} ({}) lat={:.4f}..{:.4f},long={:.4f}..{:.4f}"
          .format(name, code, minLat, maxLat, minLong, maxLong))
```

<div class="mt-3 grid grid-cols-2 gap-4 text-sm">

<div class="p-4 rounded-xl bg-amber-50">
Строки сортируются <b>по названию страны</b> —<br/>
поэтому вывод начинается с «A», а не с «Афганистан».
</div>

<div class="p-4 rounded-xl bg-blue-50">

**Настоящий вывод** (файл `TM_WORLD_BORDERS-0.3.shp`, 246 стран):

```
Afghanistan (AFG)
  lat=29.4061..38.4721
  long=60.5042..74.9157
Algeria (DZA)
  lat=18.9764..37.0914
  long=-8.6672..11.9865
```

</div>

</div>

<!--
Обратить внимание: у Алжира долгота от -8.6 до 11.9 — рамка пересекает
нулевой меридиан. Отрицательная долгота = западное полушарие.
-->

---
layout: section
---

# ✂️ Часть 2. Общая граница

## Что останется, если наложить две страны друг на друга

---
layout: two-cols
---

# `calcCommonBorder.py`: пересечение

```python
# Таиланд — "TH", Мьянма — "MM"
thailand = shapely.wkt.loads(geometry.ExportToWkt())
myanmar  = shapely.wkt.loads(geometry.ExportToWkt())

commonBorder = thailand.intersection(myanmar)
```

<div class="mt-3 p-4 rounded-xl bg-green-50 text-sm">
<b>intersection</b> — «общая часть».<br/>
Как вырезать печенье формочкой: остаётся только то,<br/>
что попало в обе фигуры.
</div>

<div class="mt-2 text-sm opacity-70">
Результат — не полигон, а <b>линия</b>: граница.
</div>

::right::

<div class="text-center mt-2">
<svg viewBox="0 0 260 190" class="w-full">
  <rect x="0" y="0" width="260" height="190" fill="#fafafa"/>
  <path d="M20 30 L110 20 L125 90 L95 170 L15 160 Z"
        fill="#fff59d" stroke="#f9a825" stroke-width="2"/>
  <path d="M110 20 L240 35 L245 150 L95 170 L125 90 Z"
        fill="#b3e5fc" stroke="#0277bd" stroke-width="2"/>
  <path d="M110 20 L125 90 L95 170" fill="none"
        stroke="#c62828" stroke-width="5"/>
  <text x="20" y="185" style="font-size:11px" fill="#f57f17">Таиланд</text>
  <text x="200" y="185" style="font-size:11px" fill="#01579b">Мьянма</text>
  <text x="128" y="112" style="font-size:11px" fill="#b71c1c">граница</text>
</svg>
</div>

<div class="text-center text-sm opacity-70">
Красная линия принадлежит <b>обеим</b> странам сразу.
</div>

<!--
Ключевая мысль: граница — это не «вещь в стране», а общая часть двух стран.
Поэтому ищем пересечение, а не что-то внутри одной.
-->

---
---

# Куда девается результат

```python
if os.path.exists("common-border"):
    shutil.rmtree("common-border")
os.mkdir("common-border")

dstFile = driver.CreateDataSource("common-border/border.shp")
dstLayer = dstFile.CreateLayer("layer", spatialReference)

wkt = shapely.wkt.dumps(commonBorder)
feature.SetGeometry(ogr.CreateGeometryFromWkt(wkt))
```

<div class="mt-3 grid grid-cols-2 gap-4 text-sm">

<div class="p-4 rounded-xl bg-red-50">
<b>Осторожно:</b> папка <code>common-border/</code><br/>
удаляется и создаётся заново при каждом запуске.
</div>

<div class="p-4 rounded-xl bg-blue-50">
<b>WKT</b> — фигура, записанная буквами:
<code>LINESTRING (98.4 9.9, ...)</code>.<br/>
Так Shapely и OGR понимают друг друга:<br/>
один умеет считать, другой — хранить.
</div>

</div>

<div class="mt-3 text-sm">
Внутри — <b>15.9 градуса</b> длины (это ~1 700 км).
Градусы — ещё не километры, сейчас увидим почему.
</div>

<!--
Мостик к следующей части: длина в градусах — плохая единица.
Один градус у экватора и у полюса — разные расстояния.
-->

---
layout: section
---

# 📐 Часть 3. Сколько километров?

## Линейка должна быть круглой

---
layout: two-cols
---

# `calcBorderLength.py`: шаг за шагом

```python
geod = pyproj.Geod(ellps="WGS84")

for segment in segments:
    for j in range(len(segment) - 1):
        long1, lat1 = segment[j]
        long2, lat2 = segment[j + 1]

        angle1, angle2, distance = geod.inv(
            long1, lat1, long2, lat2)
        totLength += distance
```

<div class="mt-3 p-4 rounded-xl bg-green-50 text-sm">
<b>inv</b> — «обратная задача»: даны две точки,<br/>
найди расстояние между ними <b>по шарику Земли</b>.
</div>

::right::

<div class="mt-2 text-center">
<svg viewBox="0 0 240 180" class="w-full">
  <circle cx="120" cy="90" r="72" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <ellipse cx="120" cy="90" rx="72" ry="24" fill="none"
           stroke="#90caf9" stroke-width="1.5" stroke-dasharray="4 4"/>
  <path d="M55 55 Q120 20 185 55" fill="none" stroke="#c62828" stroke-width="3"/>
  <circle cx="55" cy="55" r="5" fill="#b71c1c"/>
  <circle cx="185" cy="55" r="5" fill="#b71c1c"/>
  <text x="96" y="150" style="font-size:11px" fill="#0d47a1">Земля — шар</text>
</svg>
</div>

<div class="p-3 rounded-xl bg-amber-50 text-sm">
Нельзя просто вычесть координаты:<br/>
1° по широте — <b>111 км</b>, а 1° по долготе<br/>
в Петербурге — только <b>~55 км</b>.
</div>

<!--
Проверить вместе: градус долготы сжимается к полюсам.
Поэтому длину считают по шарику, а не по листу бумаги.
-->

---
---

# Как скрипт разбирает фигуру

```python
def getLineSegmentsFromGeometry(geometry):
    segments = []
    if geometry.GetPointCount() > 0:
        segment = [geometry.GetPoint_2D(i)
                   for i in range(geometry.GetPointCount())]
        segments.append(segment)

    for i in range(geometry.GetGeometryCount()):
        segments.extend(getLineSegmentsFromGeometry(
            geometry.GetGeometryRef(i)))
    return segments
```

<div class="mt-3 grid grid-cols-2 gap-4 text-sm">

<div class="p-4 rounded-xl bg-blue-50">
Полигон — это «матрёшка»: полигон → кольца → точки.<br/>
Функция заходит внутрь и собирает <b>все</b> кусочки линий.
</div>

<div class="p-4 rounded-xl bg-green-50">

**Что печатает:**

```
Total length of feature 0 is 127.28 km
Total length of feature 1 is 7264.69 km
Total length of feature 2 is 2514.76 km
```

</div>

</div>

<div class="mt-3 text-sm opacity-80">
Запуск: <code>python3 calcBorderLength.py файл.shp</code> — без аргумента скрипт попросит его указать.
Если у файла <b>нет</b> системы координат, скрипт считает, что это широта/долгота WGS84.
</div>

<!--
Рекурсия здесь — просто «загляни внутрь и вглубь».
Длины считаются по всем линиям фигуры: и внешним, и внутренним (дыркам).
-->

---
layout: two-cols
---

# ⚠️ Ловушка: два одинаковых файла

<div class="p-4 rounded-xl bg-red-50 text-sm">

### `calcFeatureLengths.py` — это копия

Внутри **тот же самый код**, что в `calcCommonBorder.py`:
Таиланд, Мьянма и общая граница.

Скрипт **ничего не печатает** и создаёт `common-border/`.

</div>

<div class="mt-3 text-sm">
Это ошибка книги при копировании файла, а не ваша.<br/>
Настоящая длина — в <code>calcBorderLength.py</code>.
</div>

::right::

<div class="mt-4 p-4 rounded-xl bg-amber-50 text-sm">

### И ещё одна путаница

`calcBorderLength.py` при неверном запуске пишет:

```
Usage: calcFeatureLengths.py <shapefile>
```

То есть подсказка называет **другой** файл.

</div>

<div class="mt-4 text-sm opacity-80">
Правило на будущее: <b>имя файла — не гарантия</b>.<br/>
Открой и посмотри, что внутри, прежде чем верить названию.
</div>

<!--
Хороший урок про чтение чужого кода: сверить имя и содержимое.
Не «исправлять» копию без просьбы — это архив учебных материалов.
-->

---
layout: section
---

# 🔄 Часть 4. Другая система координат

## Один и тот же город — два разных «адреса»

---
layout: two-cols
---

# `changeProjection.py`: метры → градусы

```python
srcProjection = osr.SpatialReference()
srcProjection.SetUTM(17)          # метры, зона 17

dstProjection = osr.SpatialReference()
dstProjection.SetWellKnownGeogCS("WGS84")   # градусы

transform = osr.CoordinateTransformation(
    srcProjection, dstProjection)

newGeometry = geometry.Clone()
newGeometry.Transform(transform)
```

<div class="mt-3 p-4 rounded-xl bg-green-50 text-sm">
<b>Clone</b> — скопировать фигуру,<br/>
чтобы не испортить оригинал в исходном файле.
</div>

::right::

<div class="mt-2 text-center">
<svg viewBox="0 0 250 170" class="w-full">
  <rect x="0" y="0" width="250" height="170" rx="10" fill="#fafafa"/>
  <rect x="20" y="35" width="90" height="70" fill="#bbdefb" stroke="#1565c0" stroke-width="2"/>
  <text x="30" y="125" style="font-size:11px" fill="#0d47a1">UTM: 580 000 м</text>
  <path d="M120 70 L162 70" stroke="#546e7a" stroke-width="3"/>
  <path d="M156 64 L166 70 L156 76" fill="#546e7a"/>
  <rect x="170" y="35" width="70" height="70" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2"/>
  <text x="172" y="125" style="font-size:11px" fill="#1b5e20">WGS84: −80.2°</text>
</svg>
</div>

<div class="text-center text-sm opacity-70">
Одно и то же место,<br/>
записанное в разных «линейках».
</div>

<!--
Аналогия: рост можно записать в сантиметрах и в дюймах.
Место не изменилось — изменилась только запись.
-->

---
layout: two-cols
---

# `changeDatum.py`: другая «нулевая точка»

```python
srcDatum.SetWellKnownGeogCS("NAD27")
dstDatum.SetWellKnownGeogCS("WGS84")

transform = osr.CoordinateTransformation(
    srcDatum, dstDatum)
```

<div class="mt-3 p-4 rounded-xl bg-blue-50 text-sm">
<b>Датум</b> — это договорённость,<br/>
от какой точки отсчитывать координаты.
</div>

<div class="mt-2 text-sm">
NAD27 и WGS84 — две такие договорённости.<br/>
Разница — десятки метров. Для пешехода мелочь,<br/>
а для карты дома — уже важно.
</div>

::right::

<div class="p-4 rounded-xl bg-amber-50 text-sm">

### Оба скрипта делают одно и то же

1. открыть старый шейп-файл
2. создать новый с нужной системой
3. каждую фигуру пересчитать
4. записать в новый файл

</div>

<div class="mt-3 p-3 rounded-xl bg-red-50 text-sm">
Папки <code>roads-reprojected/</code> и<br/>
<code>miami-reprojected/</code> удаляются при запуске.
</div>

<!--
Не углубляться в математику датумов. Главное: «перевести адрес»
и «сохранить в новый файл, не трогая старый».
-->

---
layout: section
---

# 🧭 Часть 5. Компас и расстояние

## «Иди на запад 132 километра»

---
layout: two-cols
---

# `findShoshone.py`: идём на запад

```python
distance = 132.7 * 1000   # метры
angle    = 270.0          # 270° = запад

geod = pyproj.Geod(ellps="WGS84")
newLong, newLat, invAngle = geod.fwd(
    longitude, latitude, angle, distance)
```

<div class="mt-3 p-4 rounded-xl bg-green-50 text-sm">
<b>fwd</b> — «прямая задача»:<br/>
даны точка, направление и расстояние —<br/>
найди, куда придёшь.
</div>

<div class="mt-2 text-sm">
Раньше мы искали расстояние между точками (<b>inv</b>),<br/>
теперь — точку по расстоянию (<b>fwd</b>). Обратные задачи 🙂
</div>

::right::

<div class="mt-2 text-center">
<svg viewBox="0 0 250 180" class="w-full">
  <rect x="0" y="0" width="250" height="180" rx="10" fill="#e8f5e9"/>
  <circle cx="200" cy="90" r="7" fill="#2e7d32"/>
  <circle cx="50" cy="80" r="7" fill="#c62828"/>
  <path d="M195 90 L60 80" stroke="#1565c0" stroke-width="3"
        stroke-dasharray="8 5"/>
  <path d="M66 75 L56 80 L66 85" fill="#1565c0"/>
  <text x="176" y="112" style="font-size:11px" fill="#1b5e20">Shoshone</text>
  <text x="22" y="102" style="font-size:11px" fill="#b71c1c">финиш</text>
  <text x="100" y="70" style="font-size:11px" fill="#0d47a1">132.7 км</text>
  <text x="100" y="150" style="font-size:11px" fill="#0d47a1">← 270°</text>
</svg>
</div>

<div class="p-3 rounded-xl bg-blue-50 text-sm">
<b>35.9730, −116.2711</b> → <b>35.9640, −117.7423</b><br/>
Долгота уменьшилась: мы ушли на запад.
</div>

<!--
Проверить компас: 0° север, 90° восток, 180° юг, 270° запад.
Запад — это минус по долготе, если она в градусах.
-->

---
layout: two-cols
---

# `findNearbyParks.py`: «надуваем» город

```python
MAX_DISTANCE = 0.1      # в градусах, ~10 км

outline = shapely.wkt.loads(geometry.ExportToWkt())
dilatedOutline = outline.buffer(MAX_DISTANCE)
urbanAreas[name] = dilatedOutline

# ...
if urbanArea.contains(pt):
    print(parkName, "is in or near", urbanName)
```

<div class="mt-3 p-4 rounded-xl bg-green-50 text-sm">
<b>buffer</b> — «надуть» фигуру, как шарик.<br/>
<b>contains</b> — «лежит ли точка внутри».
</div>

::right::

<div class="mt-2 text-center">
<svg viewBox="0 0 250 175" class="w-full">
  <rect x="0" y="0" width="250" height="175" fill="#fafafa"/>
  <circle cx="120" cy="85" r="62" fill="#e3f2fd" stroke="#64b5f6"
          stroke-width="2" stroke-dasharray="6 4"/>
  <path d="M85 70 L120 55 L150 80 L140 110 L95 115 Z"
        fill="#c8e6c9" stroke="#2e7d32" stroke-width="2"/>
  <circle cx="155" cy="50" r="5" fill="#c62828"/>
  <circle cx="75" cy="120" r="5" fill="#c62828"/>
  <circle cx="200" cy="120" r="5" fill="#9e9e9e"/>
  <text x="146" y="40" style="font-size:10px" fill="#b71c1c">парк рядом</text>
  <text x="188" y="138" style="font-size:10px" fill="#616161">далеко</text>
</svg>
</div>

<div class="text-center text-sm opacity-70">
Красные точки попали в «надутый» город —<br/>
значит, парк близко.
</div>

<!--
0.1 градуса — это не километры: по широте ~11 км, по долготе в Калифорнии ~9 км.
Поэтому «надутый» город получается немного овальным. Для учебной задачи это нормально.
-->

---
layout: section
---

# 🏔️ Часть 6. Растр и высоты

## Сколько клеток на каждой высоте

---
layout: two-cols
---

# `histogram.py`: считаем клетки

```python
dataset = gdal.Open("l10g")
band = dataset.GetRasterBand(1)

scanline = band.ReadRaster(minX, y, width, 1,
                           width, 1, gdalconst.GDT_Int16)
values = struct.unpack(fmt, scanline)

for value in values:
    try:
        histogram[value] += 1
    except KeyError:
        histogram[value] = 1
```

<div class="mt-3 p-4 rounded-xl bg-blue-50 text-sm">
Читаем растр <b>по строчке</b>, как книгу,<br/>
и в словаре считаем: «высота → сколько клеток».
</div>

::right::

<div class="mt-3 p-4 rounded-xl bg-green-50 text-sm">

### Пример вывода

```
0 15234
12 8830
45 611
...
```

Числа здесь условные: файла `l10g`<br/>
в архиве нет. Важен порядок:<br/>
слева высота, справа число клеток.

</div>

<div class="mt-3 p-3 rounded-xl bg-amber-50 text-sm">
Скрипт смотрит только на кусок карты:<br/>
широта −48…−33, долгота 165…179 —<br/>
это район <b>Тасмании</b> 🇦🇺
</div>

<div class="mt-2 text-sm opacity-70">
Строка <code>fmt = "&lt;" + ("h" * width)</code> — это просто<br/>
«прочитать <code>width</code> целых чисел».
</div>

<!--
struct.unpack — перевод байтов в числа. Не пугать: это упаковка.
Обратить внимание: числа со знаком, поэтому высоты могут быть отрицательными (море).
-->

---
layout: center
class: text-center
---

# Общий рецепт всех скриптов

<div class="mt-6 grid grid-cols-3 gap-5 text-left text-base">

<div class="p-5 rounded-xl bg-blue-50">
<div class="text-2xl">📖</div>
<b>1. Прочитать</b><br/>
<code>ogr.Open</code> / <code>gdal.Open</code>
</div>

<div class="p-5 rounded-xl bg-green-50">
<div class="text-2xl">🧮</div>
<b>2. Посчитать</b><br/>
envelope, intersection, geod, buffer
</div>

<div class="p-5 rounded-xl bg-amber-50">
<div class="text-2xl">💾</div>
<b>3. Отдать результат</b><br/>
<code>print</code> или новый шейп-файл
</div>

</div>

<div class="mt-8 text-lg">
Девять скриптов — девять разных вопросов.<br/>
Но порядок работы <b>всегда одинаковый</b>.
</div>

<div class="mt-6 p-4 rounded-xl bg-gray-50 text-sm inline-block">
Каждый инструмент умеет одно: OGR — читать, Shapely — считать фигуры,
pyproj — считать по шарику, GDAL — читать растр.
</div>

<!--
Это главный слайд для запоминания: не API, а порядок действий.
-->

---
layout: two-cols
---

# Попробуй сам

```bash
cd "Chapter 04/Windows"

# нужен файл TM_WORLD_BORDERS-0.3.shp
# (взять в GDAL/.../Chapter 03)
python3 calcBoundingBoxes.py
python3 calcCommonBorder.py
python3 calcBorderLength.py \
    TM_WORLD_BORDERS-0.3.shp
```

<div class="mt-3 text-sm">
Остальные скрипты ждут своих данных:<br/>
<code>roads/</code>, <code>miami/</code>, <code>l10g</code>,
<code>CA_Features_XXXX.txt</code>.
</div>

::right::

<div class="mt-2 p-4 rounded-xl bg-amber-50 text-sm">

**Порядок важен!**

Скрипты ищут файлы **рядом с собой**,<br/>
поэтому запускать их нужно из папки с данными.

</div>

<div class="mt-3 p-4 rounded-xl bg-blue-50 text-sm">
<b>Показать презентацию:</b>

```bash
npx @slidev/cli geo_operations.md
```

</div>

<div class="mt-3 text-sm opacity-70">
<code>CA_Features_XXXX.txt</code> — в книге<br/>
вместо <code>XXXX</code> должен быть год файла.
</div>

<!--
Если данных нет — скрипты упадут. Это нормально: сначала положите
файл рядом, потом запускайте. Для шейп-файла нужны .shp, .shx, .dbf, .prj.
-->

---
layout: two-cols
---

# Осторожно: три ловушки

<div class="space-y-3 mt-2 text-sm">

<div class="p-3 rounded-xl bg-red-50">
<b>1. Нет входного файла</b><br/>
<code>'NoneType' object has no attribute 'GetLayer'</code><br/>
Это «файл не найден», а не «сломался Python».
</div>

<div class="p-3 rounded-xl bg-red-50">
<b>2. Папки удаляются</b><br/>
<code>common-border/</code>, <code>roads-reprojected/</code>,
<code>miami-reprojected/</code> стираются при каждом запуске.
</div>

<div class="p-3 rounded-xl bg-red-50">
<b>3. Два файла с одинаковым кодом</b><br/>
<code>calcFeatureLengths.py</code> — копия <code>calcCommonBorder.py</code>.
</div>

</div>

::right::

<div class="mt-4 p-4 rounded-xl bg-blue-50 text-sm">

### Почему «NoneType»?

`ogr.Open` и `gdal.Open` не падают,<br/>
если файла нет — они возвращают **None**.

А `None.GetLayer()` уже не умеет ничего. 🙃

</div>

<div class="mt-4 p-4 rounded-xl bg-green-50 text-sm">
<b>Полезная привычка:</b> проверять, что файл открылся,<br/>
прежде чем с ним работать.
</div>

<div class="mt-3 text-sm opacity-70">
Ещё в консоли будет <code>FutureWarning</code> про
<code>UseExceptions</code> — это просто предупреждение GDAL.
</div>

<!--
Эти ловушки проверены запуском. Не «чинить» их без просьбы:
это архив учебных материалов из книги.
-->

---
layout: center
class: text-center
---

# Что запомнить

<div class="mt-6 grid grid-cols-2 gap-4 text-left text-base">

<div class="p-4 rounded-xl bg-blue-50">📦 <b>Envelope</b> — рамка вокруг фигуры</div>
<div class="p-4 rounded-xl bg-green-50">✂️ <b>Intersection</b> — общая часть двух фигур</div>
<div class="p-4 rounded-xl bg-amber-50">📐 <b>Geod.inv</b> — расстояние по шарику Земли</div>
<div class="p-4 rounded-xl bg-pink-50">🧭 <b>Geod.fwd</b> — куда придёшь по компасу</div>
<div class="p-4 rounded-xl bg-purple-50">🔄 <b>Transform</b> — перевод координат</div>
<div class="p-4 rounded-xl bg-gray-100">🎈 <b>Buffer</b> — «надуть» фигуру на расстояние</div>

</div>

<div class="mt-10 text-xl">
Карту можно <b>измерять</b>: у стран есть рамки, у границ — длина,<br/>
у городов — окрестности.
</div>

<div class="mt-8 text-lg opacity-70">
А теперь вопрос: сколько километров границы у твоего района? 🤔
</div>

<!--
Финальный вопрос — на обсуждение. Хороший ответ: нужно найти границу
района, разбить её на кусочки и сложить расстояния — как calcBorderLength.
-->
