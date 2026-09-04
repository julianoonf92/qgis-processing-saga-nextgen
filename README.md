# QGIS Processing SAGA next gen provider

[![Build Status](https://travis-ci.org/north-road/qgis-processing-saga-nextgen.svg?branch=master)](https://travis-ci.org/north-road/qgis-processing-r)

Processing SAGA Provider Plugin for SAGA 9.12.0 and later. The plugin supports
QGIS 3.22 through QGIS 4.x, including QGIS 4.2, and is primarily maintained and
tested on Windows.

SAGA nowadays comes with an Interface Creator for QGIS. To use it compile SAGA with

-DWITH_DEV_TOOLS:BOOL=ON

and run

saga_cmd dev_tools 7

The algorithm descriptions in `processing_saga_nextgen/description` must be
regenerated with SAGA 9.12 before a release whenever its command-line tool
interfaces change. Run `scripts/update-saga-descriptions.ps1` from PowerShell
and review the resulting diff before committing it.



