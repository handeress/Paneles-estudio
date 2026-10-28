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
| Hojas | 2 de ~1245 × 1477 sobre pivotes piso-dintel (80 kg); bastidor tubo 1"×1" cal 18 + triplex 15 + listones |
| Fondo libre zona baja | 328 |
| TV | 65" (1450 × 836), base 15 mm sobre la junta (a ras de puertas); marco colgante en tubo 40×40 cal 16 (2 verticales a 600 entre ejes + 2 travesaños VESA) anclado a techo con platina y al dintel con ángulo. Nada se ancla al muro de fondo |
| Colchón | Uno de 1.40×1.90, vertical (1.90 de alto), alineado a la izquierda, **grosor 150 (por confirmar)** |

Cada pieza lleva `Pset_Despiece` con largo, fondo, alto y material.
