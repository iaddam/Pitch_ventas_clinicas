"""Genera el pitch del vendedor en sus dos versiones, cada una en un solo archivo (todo incrustado):
    index.html  → clínicas dentales
    salud.html  → clínicas de salud (kinesiología, estética, medicina)
Se edita SOLO fuente/plantilla.html (y los textos de cada versión, abajo). Luego:
    python3 fuente/armar.py
"""
import base64, re, pathlib

FUENTE = pathlib.Path(__file__).resolve().parent
RAIZ = FUENTE.parent

VERSIONES = {
  'index.html': {
    'VERTICAL': 'dental',
    'TITULO': 'ADDAM · Pitch para clínicas dentales',
    'EYEBROW_PORTADA': 'MOTOR DE INGRESOS PARA CLÍNICAS DENTALES',
    # el punto ciego
    'J1': 'Hora agendada', 'J1T': 'por teléfono, web o WhatsApp',
    'J2': 'Presupuesto', 'J2T': 'después de la evaluación',
    'J3': 'Tratamiento y controles', 'J3T': 'el plan en marcha',
    'J4': 'Mantención', 'J4T': 'el paciente que terminó bien',
    'L1': 'Un sillón vacío. Esa hora no se recupera.',
    'L2H': 'El presupuesto que queda en el aire',
    'L2': 'Ortodoncia, implantes, rehabilitación. Si nadie lo retoma, no parte.',
    'F2H': 'Retoma el presupuesto',
    'L3H': 'El control al que no llega', 'L3': 'Y con él se cae el tratamiento a mitad de camino.',
    'F3': 'Le recuerda cada control y reagenda si no puede venir.',
    'L4H': 'La mantención que nadie recuerda', 'L4': 'El paciente que terminó bien y deja de venir.',
    'F4': 'Lo invita a su mantención cuando le corresponde.',
    # pilares
    'S5_DESC': 'Reglas por tratamiento y campañas a pacientes dormidos: mantención de implantes y controles periodontales.',
    'S5_SRC': 'Fuente: base de clientes ADDAM, clínicas dentales. Clientes anonimizados.',
    'S6_CLINICA': 'una clínica dental real de tamaño mediano',
    # chat
    'CHAT_PIDE': 'hacerme una limpieza', 'CHAT_COSA': 'la limpieza', 'CHAT_TU': 'tu limpieza', 'CHAT_PRO': 'la Dra. Soto',
    # calculadora
    'CALC_CITAS': '800', 'CALC_TICKET': '60000',
  },
  'salud.html': {
    'VERTICAL': 'salud',
    'TITULO': 'ADDAM · Pitch para clínicas de salud',
    'EYEBROW_PORTADA': 'MOTOR DE INGRESOS PARA CLÍNICAS DE SALUD',
    'J1': 'Hora agendada', 'J1T': 'por teléfono, web o WhatsApp',
    'J2': 'Plan de tratamiento', 'J2T': 'después de la evaluación',
    'J3': 'Sesiones y controles', 'J3T': 'el plan en marcha',
    'J4': 'Seguimiento', 'J4T': 'el paciente que terminó bien',
    'L1': 'Un box vacío. Esa hora no se recupera.',
    'L2H': 'El plan que queda en el aire',
    'L2': 'Sesiones, procedimientos, paquetes. Si nadie lo retoma, no parte.',
    'F2H': 'Retoma el plan',
    'L3H': 'La sesión a la que no llega', 'L3': 'Y con ella se corta el tratamiento a mitad de camino.',
    'F3': 'Le recuerda cada sesión y reagenda si no puede venir.',
    'L4H': 'El paciente que no vuelve', 'L4': 'El que terminó bien y deja de venir a su control.',
    'F4': 'Lo invita a su control cuando le corresponde.',
    'S5_DESC': 'Reglas por tratamiento y campañas a pacientes dormidos: controles pendientes, sesiones sin terminar y planes a medias.',
    'S5_SRC': 'Fuente: base de clientes ADDAM. Clientes anonimizados.',
    'S6_CLINICA': 'una clínica real de tamaño mediano',
    'CHAT_PIDE': 'sumar una evaluación', 'CHAT_COSA': 'la evaluación', 'CHAT_TU': 'tu evaluación', 'CHAT_PRO': 'Camila Soto',
    'CALC_CITAS': '1000', 'CALC_TICKET': '45000',
  },
}

def data_uri(ruta):
    tipo = {'.ttf': 'font/ttf', '.mp4': 'video/mp4', '.png': 'image/png', '.svg': 'image/svg+xml'}[ruta.suffix]
    return f"data:{tipo};base64,{base64.b64encode(ruta.read_bytes()).decode()}"

plantilla = (FUENTE / 'plantilla.html').read_text(encoding='utf-8')
for archivo, textos in VERSIONES.items():
    html = plantilla
    for clave, valor in textos.items():
        html = html.replace('{{' + clave + '}}', valor)
    faltan = sorted(set(re.findall(r'\{\{([A-Z0-9_]+)\}\}', html)))
    assert not faltan, f'{archivo}: faltan textos para {faltan}'
    html = re.sub(r'assets/[A-Za-z0-9._/-]+\.(?:ttf|mp4|png|svg)', lambda m: data_uri(FUENTE / m.group(0)), html)
    (RAIZ / archivo).write_text(html, encoding='utf-8')
    print(f'{archivo}: {len(html)/1024:.0f} KB')
