# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

### Removed


## [0.5.1] 2025-06-24

### Added

### Changed

### Removed


## [0.5.0] 2025-02-07

### Added

* Added `use_edges` parameter to `RUIMeshObject.select_vertices`.

### Changed

* Changed `guid` retrieval to not fail when edges or vertices are missing from the dict.

### Removed


## [0.4.2] 2025-02-03

### Added

### Changed

### Removed

* Removed `compas` from requirements to solve problem in Rhino plugins.
* Removed selection of vertices on edge strip.

## [0.4.1] 2024-11-09

### Added

### Changed

### Removed


## [0.4.0] 2024-11-08

### Added

* Added `RhinoMeshObject.select_faces()`.
* Added `RhinoMeshObject.select_vertices_all()`.
* Added `RhinoMeshObject.select_vertices_boundary()`.
* Added `RhinoMeshObject.select_vertices_degree()`.
* Added `RhinoMeshObject.select_vertices_edgeloop()`.
* Added `RhinoMeshObject.select_vertices_edgestrip()`.
* Added `RhinoMeshObject.select_vertices_manual()`.
* Added `RhinoMeshObject.select_edges_all()`.
* Added `RhinoMeshObject.select_edges_boundary()`.
* Added `RhinoMeshObject.select_edges_loop()`.
* Added `RhinoMeshObject.select_edges_strip()`.
* Added `RhinoMeshObject.select_edges_manual()`.
* Added `RhinoMeshObject.select_faces_all()`.
* Added `RhinoMeshObject.select_faces_boundary()`.
* Added `RhinoMeshObject.select_faces_strip()`.
* Added `RhinoMeshObject.select_faces_manual()`.

### Changed

### Removed

## [0.3.2] 2024-11-07

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
