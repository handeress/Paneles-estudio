# Paneles estudio – closet oculto con TV

Modelo IFC4 (mm) del muro de listones convertido en closet oculto: zona alta fija con TV, dos hojas abajo para guardar dos colchones de canto.

- `closet_paneles_tv.ifc` – modelo para abrir/vincular en Revit (Insertar › Vincular IFC) o en cualquier visor IFC.
- `generar_ifc.py` – script que genera el IFC. Cambiar parámetros arriba del archivo y correr `python3 generar_ifc.py`.

## Supuestos
| Ítem | Valor |
|---|---|
| Nicho | 2500 × 2420, fondo 400 |
| Panel listones | 32 de fondo, listón 30 / luz 15 |
| Junta fija / puertas | 1500 |
| Hojas | 2 de ~1245 × 1477; bastidor tubo 1"×1" cal 18 + triplex 15 + listones |
| Fondo libre zona baja | 328 |
| TV | 55" (1230 × 710), centro a 1960, separadores tubo 40×40 anclados al muro |
| Colchones | 1.90×1.40 y 1.90×1.10, de canto, **grosor 150 c/u (por confirmar)** |

Cada pieza lleva `Pset_Despiece` con largo, fondo, alto y material.
