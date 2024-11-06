# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Added `compas_rui.rui.Rui`.

### Changed

* Changed selection functions to require pre-drawing.

### Removed

## [0.3.1] 2024-11-01

### Added

* Added `message` param to `compas_rui.scene.RhinoMeshObject.select_vertices`.
* Added `message` param to `compas_rui.scene.RhinoMeshObject.select_edges`.

### Changed

### Removed


## [0.3.0] 2024-10-23

### Added

### Changed

* Changed `compas_rui.values.FloatValue.min` to `compas_rui.values.FloatValue.minval`.
* Changed `compas_rui.values.FloatValue.max` to `compas_rui.values.FloatValue.maxval`.
* Changed `compas_rui.values.IntValue.min` to `compas_rui.values.IntValue.minval`.
* Changed `compas_rui.values.IntValue.max` to `compas_rui.values.IntValue.maxval`.
* Fixed `compas_rui.forms.SplashForm.WindowStyle`.
* Changed `compas_rui.scene.RUIMeshObject.select_vertices` to require list of selectable vertices.
* Changed `compas_rui.scene.RUIMeshObject.select_edges` to require list of selectable edges.
* Changed `compas_rui.forms.NamedValuesForm` to have expanded "Name" column.

### Removed


## [0.2.0] 2024-10-01

### Added

* `compas_rui.scene.RUIMeshObject`.
* `compas_rui.values.BoolValue`.
* `compas_rui.values.ColorValue`.
* `compas_rui.values.DictValue`.
* `compas_rui.values.FloatValue`.
* `compas_rui.values.IntValue`.
* `compas_rui.values.ListValue`.
* `compas_rui.values.StrValue`.

### Changed

### Removed
