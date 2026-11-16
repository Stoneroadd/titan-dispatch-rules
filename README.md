# Titan Dispatch Rules

MVP educativo de automatización: asigna camiones simulados a unidades de carga con reglas explícitas y devuelve la razón de cada asignación. **No es un sistema de despacho operacional** y no usa telemetría real.

## Ejecutar

Requiere Python 3.10 o superior, sin dependencias externas.

```powershell
python dispatch.py examples/scenario.json
```

La salida JSON contiene asignaciones, camiones no asignados y motivos. Para pruebas:

```powershell
python -m unittest discover -s tests -v
```

## Reglas del MVP

1. Solo participan camiones y unidades de carga con estado `available`.
2. La capacidad del camión debe ser igual o mayor al mínimo definido por la unidad.
3. Cada unidad tiene un máximo de camiones simultáneos.
4. Los camiones se procesan por ID; se elige la unidad con menos asignaciones, desempatando por ID.

La salida es determinista para una entrada dada. Las reglas son simplificaciones ilustrativas; no representan seguridad, rutas, tiempos, combustible ni restricciones reales de una faena.

## Licencia

MIT.
