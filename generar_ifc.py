"""Genera closet_paneles_tv.ifc (IFC4, mm) para el muro de paneles del estudio.

Ejes: X a lo largo del muro (0 = lateral izq. del nicho), Y desde el muro de
fondo hacia el salón (0 = cara del muro), Z vertical (0 = piso terminado).

Supuestos (editar abajo y volver a correr):
- Nicho 2500 x 2420, fondo 400. Panel listones 32 mm.
- Junta horizontal a 1500 mm. TV 65" fijo arriba, a ras de las puertas, colgado de un marco metalico anclado al techo y al dintel. 2 hojas abajo con pivotes.
- Un colchon 1.40 x 1.90 vertical, alineado a la izquierda; grosor 150 mm (SUPUESTO).
"""
import time, uuid, string

# ---------------- parámetros ----------------
ANCHO, ALTO, FONDO = 2500, 2420, 400
PANEL = 32            # fondo del panel de listones
TRIPLEX = 15          # forro
TUBO = 25             # bastidor hojas, tubo 1"x1"
JUNTA = 1500          # altura junta fija / puertas
LISTON, LUZ = 30, 15  # listón 30 mm, separación 15 mm
GROSOR_COLCHON = 150  # SUPUESTO
TV = (1450, 836, 30)  # 65" ancho, alto, grosor
LUZ_TV = 15
SEP_COLG = 600         # entre ejes de los colgantes del TV
VESA = 400             # patron VESA del TV (filas de anclaje)            # TV a ras de puertas, 15 mm sobre la junta

Y_PANEL = FONDO - PANEL            # 368
Y_TRIP = Y_PANEL - TRIPLEX         # 353
Y_TUBO = Y_TRIP - TUBO             # 328 -> fondo libre zona baja

# ---------------- escritor STEP ----------------
_chars = string.digits + string.ascii_uppercase + string.ascii_lowercase + "_$"
def gid():
    n = uuid.uuid4().int; s = ""
    for _ in range(22):
        s = _chars[n % 64] + s; n //= 64
    return s

lines, n = [], [0]
def E(txt):
    n[0] += 1; lines.append(f"#{n[0]}={txt};"); return f"#{n[0]}"
def f(v): return f"{float(v):.1f}"
def s(t): return "'" + t.replace("'", "''") + "'"

# contexto
origin = E("IFCCARTESIANPOINT((0.,0.,0.))")
zdir = E("IFCDIRECTION((0.,0.,1.))"); xdir = E("IFCDIRECTION((1.,0.,0.))")
world = E(f"IFCAXIS2PLACEMENT3D({origin},{zdir},{xdir})")
ctx = E(f"IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,{world},$)")
body = E(f"IFCGEOMETRICREPRESENTATIONSUBCONTEXT('Body','Model',*,*,*,*,{ctx},$,.MODEL_VIEW.,$)")
mm = E("IFCSIUNIT(*,.LENGTHUNIT.,.MILLI.,.METRE.)")
m2 = E("IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.)")
m3 = E("IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.)")
units = E(f"IFCUNITASSIGNMENT(({mm},{m2},{m3}))")
person = E("IFCPERSON($,'Andres',$,$,$,$,$,$)")
org = E("IFCORGANIZATION($,'Diseno y construccion',$,$,$)")
po = E(f"IFCPERSONANDORGANIZATION({person},{org},$)")
app = E(f"IFCAPPLICATION({org},'1.0','generar_ifc.py','genifc')")
now = int(time.time())
own = E(f"IFCOWNERHISTORY({po},{app},$,.ADDED.,{now},$,$,{now})")
project = E(f"IFCPROJECT('{gid()}',{own},'Closet oculto paneles estudio',$,$,$,$,({ctx}),{units})")
pl_site = E(f"IFCLOCALPLACEMENT($,{world})")
site = E(f"IFCSITE('{gid()}',{own},'Sitio',$,$,{pl_site},$,$,.ELEMENT.,$,$,$,$,$)")
pl_bld = E(f"IFCLOCALPLACEMENT({pl_site},{world})")
bld = E(f"IFCBUILDING('{gid()}',{own},'Casa',$,$,{pl_bld},$,$,.ELEMENT.,$,$,$)")
pl_st = E(f"IFCLOCALPLACEMENT({pl_bld},{world})")
storey = E(f"IFCBUILDINGSTOREY('{gid()}',{own},'Estudio',$,$,{pl_st},$,$,.ELEMENT.,0.)")
E(f"IFCRELAGGREGATES('{gid()}',{own},$,$,{project},({site}))")
E(f"IFCRELAGGREGATES('{gid()}',{own},$,$,{site},({bld}))")
E(f"IFCRELAGGREGATES('{gid()}',{own},$,$,{bld},({storey}))")

_styles = {}
def style(rgb, transp=0.0):
    k = (rgb, transp)
    if k not in _styles:
        col = E(f"IFCCOLOURRGB($,{rgb[0]:.3f},{rgb[1]:.3f},{rgb[2]:.3f})")
        ren = E(f"IFCSURFACESTYLESHADING({col},{transp:.2f})")
        _styles[k] = E(f"IFCSURFACESTYLE($,.BOTH.,({ren}))")
    return _styles[k]

COL = {
    "muro": ((0.92, 0.92, 0.90), 0.6), "liston": ((0.62, 0.38, 0.20), 0),
    "triplex": ((0.85, 0.72, 0.50), 0), "madera": ((0.75, 0.60, 0.40), 0),
    "metal": ((0.25, 0.25, 0.27), 0), "tv": ((0.05, 0.05, 0.05), 0),
    "colchon": ((0.55, 0.70, 0.90), 0.0), "herraje": ((0.70, 0.70, 0.72), 0),
}

materiales = {}
elements = []
def caja(nombre, clase, x, y, z, dx, dy, dz, color, material, tipo=None):
    p = E(f"IFCCARTESIANPOINT(({f(x)},{f(y)},{f(z)}))")
    a = E(f"IFCAXIS2PLACEMENT3D({p},{zdir},{xdir})")
    lp = E(f"IFCLOCALPLACEMENT({pl_st},{a})")
    c2 = E(f"IFCCARTESIANPOINT(({f(dx/2)},{f(dy/2)}))")
    a2 = E(f"IFCAXIS2PLACEMENT2D({c2},$)")
    prof = E(f"IFCRECTANGLEPROFILEDEF(.AREA.,$,{a2},{f(dx)},{f(dy)})")
    sol = E(f"IFCEXTRUDEDAREASOLID({prof},{world},{zdir},{f(dz)})")
    rgb, tr = COL[color]
    E(f"IFCSTYLEDITEM({sol},({style(rgb, tr)}),$)")
    rep = E(f"IFCSHAPEREPRESENTATION({body},'Body','SweptSolid',({sol}))")
    pds = E(f"IFCPRODUCTDEFINITIONSHAPE($,$,({rep}))")
    ot = s(tipo) if tipo else "$"
    extra = {
        "IFCWALL": ",.NOTDEFINED.", "IFCMEMBER": ",.NOTDEFINED.", "IFCPLATE": ",.NOTDEFINED.",
        "IFCBEAM": ",.NOTDEFINED.", "IFCFURNITURE": ",.NOTDEFINED.",
        "IFCBUILDINGELEMENTPROXY": ",.NOTDEFINED.", "IFCMECHANICALFASTENER": ",$,$,.NOTDEFINED.",
        "IFCELECTRICAPPLIANCE": ",.TV.", "IFCCOVERING": ",.CLADDING.", "IFCSLAB": ",.FLOOR.",
    }[clase]
    el = E(f"{clase}('{gid()}',{own},{s(nombre)},$,{ot},{lp},{pds},$" + extra + ")")
    elements.append(el)
    materiales.setdefault(material, []).append(el)
    medidas[el] = (nombre, dx, dy, dz, material)
    return el

medidas = {}

# ---------------- muros existentes (referencia) ----------------
caja("Muro fondo (existente)", "IFCWALL", -100, -150, 0, ANCHO + 200, 150, ALTO, "muro", "Muro existente")
caja("Muro lateral izq (existente)", "IFCWALL", -100, 0, 0, 100, FONDO + 50, ALTO, "muro", "Muro existente")
caja("Muro lateral der (existente)", "IFCWALL", ANCHO, 0, 0, 100, FONDO + 50, ALTO, "muro", "Muro existente")

# ---------------- base piso closet ----------------
caja("Base piso closet", "IFCSLAB", 0, 0, 0, ANCHO, Y_TUBO, 15, "triplex", "Triplex 15 mm")

# ---------------- zona alta fija ----------------
B = 45  # madera 2"x2" cepillada
yb = Y_TRIP - B
caja("Dintel junta", "IFCBEAM", 0, Y_TRIP - 70, JUNTA, ANCHO, 70, 45, "madera", "Madera 2x3", "Dintel 2x3")
for nm, x in [("Parante alto izq", 0), ("Parante alto der", ANCHO - B)]:
    caja(nm, "IFCMEMBER", x, yb, JUNTA + 45, B, B, ALTO - JUNTA - 45, "madera", "Madera 2x2", "Bastidor fijo")
caja("Travesano alto techo", "IFCMEMBER", B, yb, ALTO - B, ANCHO - 2 * B, B, B, "madera", "Madera 2x2", "Bastidor fijo")
caja("Forro triplex zona alta", "IFCPLATE", 0, Y_TRIP, JUNTA, ANCHO, TRIPLEX, ALTO - JUNTA, "triplex", "Triplex 15 mm")

def listones(prefijo, x0, ancho, z0, alto):
    paso = LISTON + LUZ
    nlist = int((ancho + LUZ) // paso)
    sobra = ancho - (nlist * paso - LUZ)
    x = x0 + sobra / 2
    for i in range(nlist):
        caja(f"{prefijo} liston {i+1:02d}", "IFCCOVERING", x, Y_PANEL, z0, LISTON, PANEL, alto,
             "liston", "Liston madera (panel existente)", "Panel listones")
        x += paso
    return nlist

n_alto = listones("Alto", 0, ANCHO, JUNTA, ALTO - JUNTA)

# ---------------- marco colgante del TV (anclado al techo, no al muro de fondo) ----------------
# 2 verticales 40x40 cal 16 desde platina de techo hasta el dintel, 2 horizontales en las filas VESA.
z_tv = JUNTA + LUZ_TV + TV[1] / 2
T, PL = 40, 6
y_m = Y_TRIP - T                       # pegado detras del triplex
z_base = JUNTA + 45                    # cara superior del dintel
xs = [ANCHO / 2 - SEP_COLG / 2 - T / 2, ANCHO / 2 + SEP_COLG / 2 - T / 2]
for lado, x in zip(["izq", "der"], xs):
    caja(f"Platina techo {lado}", "IFCPLATE", x + T / 2 - 75, y_m + T / 2 - 75, ALTO - PL, 150, 150, PL, "metal", "Platina acero 6 mm")
    caja(f"Colgante TV {lado}", "IFCMEMBER", x, y_m, z_base, T, T, ALTO - PL - z_base, "metal", "Tubo 40x40 cal 16", "Colgante TV")
    caja(f"Angulo base colgante {lado}", "IFCPLATE", x - 30, y_m - 30, z_base, 100, 30, 50, "metal", "Angulo 1 1/2 x 1/8", "Anclaje a dintel")
for fila, z in [("inferior", z_tv - VESA / 2), ("superior", z_tv + VESA / 2)]:
    caja(f"Travesano TV {fila}", "IFCMEMBER", xs[0] + T, y_m, z - T / 2, SEP_COLG - T, T, T, "metal", "Tubo 40x40 cal 16", "Travesano TV")
caja("Soporte TV fijo", "IFCPLATE", (ANCHO - 500) / 2, FONDO, z_tv - 200, 500, 20, 400, "metal", "Soporte TV fijo")
caja('TV 65"', "IFCELECTRICAPPLIANCE", (ANCHO - TV[0]) / 2, FONDO + 20, z_tv - TV[1] / 2, TV[0], TV[2], TV[1], "tv", "TV")

# ---------------- hojas zona baja ----------------
G, Z0 = 3, 20
PIVOTE = 35  # eje del pivote desde el canto exterior
z_top = JUNTA - G
alto_h = z_top - Z0
hojas = [("H1", G, ANCHO / 2 - 2), ("H2", ANCHO / 2 + 2, ANCHO / 2 - 2 - G)]
n_bajo = 0
for h, x0, w in hojas:
    caja(f"{h} tubo vertical izq", "IFCMEMBER", x0, Y_TUBO, Z0, TUBO, TUBO, alto_h, "metal", 'Tubo 1"x1" cal 18', "Bastidor hoja")
    caja(f"{h} tubo vertical der", "IFCMEMBER", x0 + w - TUBO, Y_TUBO, Z0, TUBO, TUBO, alto_h, "metal", 'Tubo 1"x1" cal 18', "Bastidor hoja")
    for nm, z in [("inferior", Z0), ("medio", Z0 + alto_h / 2 - TUBO / 2), ("superior", z_top - TUBO)]:
        caja(f"{h} tubo horizontal {nm}", "IFCMEMBER", x0 + TUBO, Y_TUBO, z, w - 2 * TUBO, TUBO, TUBO, "metal", 'Tubo 1"x1" cal 18', "Bastidor hoja")
    caja(f"{h} forro triplex", "IFCPLATE", x0, Y_TRIP, Z0, w, TRIPLEX, alto_h, "triplex", "Triplex 15 mm")
    n_bajo += listones(f"{h}", x0, w, Z0, alto_h)
    # pivotes piso-dintel del lado exterior (eje a 35 mm del canto): la carga baja al piso
    xp = (x0 + PIVOTE if h == "H1" else x0 + w - PIVOTE) - 25
    yp = Y_TUBO + (FONDO - Y_TUBO) / 2 - 25
    caja(f"{h} pivote inferior", "IFCMECHANICALFASTENER", xp, yp, 15, 50, 50, Z0 - 15, "herraje", "Pivote puerta 80 kg")
    caja(f"{h} pivote superior", "IFCMECHANICALFASTENER", xp, yp, z_top, 50, 50, JUNTA + 45 - z_top, "herraje", "Pivote puerta 80 kg")

# ---------------- colchones (referencia de capacidad) ----------------
# un solo colchon, vertical (1.90 de alto), de canto contra el muro de fondo, alineado a la izquierda
caja("Colchon 1.40 x 1.90 (vertical)", "IFCFURNITURE", 0, 15, 15, 1400, GROSOR_COLCHON, 1900, "colchon", "Colchon")

# ---------------- relaciones ----------------
E(f"IFCRELCONTAINEDINSPATIALSTRUCTURE('{gid()}',{own},$,$,({','.join(elements)}),{storey})")
for mat, els in materiales.items():
    m = E(f"IFCMATERIAL({s(mat)},$,$)")
    E(f"IFCRELASSOCIATESMATERIAL('{gid()}',{own},$,$,({','.join(els)}),{m})")

# Pset con medidas por pieza
for el, (nombre, dx, dy, dz, mat) in medidas.items():
    props = [E(f"IFCPROPERTYSINGLEVALUE({s(k)},$,IFCLENGTHMEASURE({f(v)}),$)") for k, v in
             [("Largo X mm", dx), ("Fondo Y mm", dy), ("Alto Z mm", dz)]]
    props.append(E(f"IFCPROPERTYSINGLEVALUE('Material',$,IFCLABEL({s(mat)}),$)"))
    ps = E(f"IFCPROPERTYSET('{gid()}',{own},'Pset_Despiece',$,({','.join(props)}))")
    E(f"IFCRELDEFINESBYPROPERTIES('{gid()}',{own},$,$,({el}),{ps})")

hdr = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [ReferenceView_V1.2]'),'2;1');
FILE_NAME('closet_paneles_tv.ifc','{time.strftime('%Y-%m-%dT%H:%M:%S')}',('Andres'),(''),'generar_ifc.py','generar_ifc.py','');
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
"""
with open("closet_paneles_tv.ifc", "w") as fh:
    fh.write(hdr + "\n".join(lines) + "\nENDSEC;\nEND-ISO-10303-21;\n")
print(f"OK: {len(elements)} elementos | listones alto {n_alto}, bajo {n_bajo} | fondo libre bajo {Y_TUBO} mm")
