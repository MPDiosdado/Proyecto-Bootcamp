import json
import random
import csv
from datetime import datetime, timedelta
from pathlib import Path


CATEGORIAS = {
    "Limpieza": [
        "basura sin recoger en la calle",
        "contenedor desbordado de residuos",
        "grafiti vandálico en fachada pública",
        "acumulación de escombros en solar",
        "limpieza de vía pública pendiente",
        "residuos en parque urbano",
        "contenedor incendiado",
        "abandono de muebles en calle",
    ],
    "Urbanismo": [
        "farola fundida en calle",
        "socavón en calzada",
        "señal de tráfico caída",
        "banco público roto en plaza",
        "alcorque sin árbol",
        "vía pública en mal estado",
        "acera deteriorada",
        "farola parpadeando",
    ],
    "Seguridad": [
        "accidente de tráfico en intersección",
        "pelea en la vía pública",
        "vandalismo en equipamiento municipal",
        "robo en zona urbana",
        "actividad sospechosa en parque",
        "incidente con animales abandonados",
        "persona herida en espacio público",
        "seguridad vial comprometida",
    ],
    "Tráfico": [
        "semáforo averiado",
        "corte de vía sin señalizar",
        "aparcamiento ilegal en zona azul",
        "vehículo abandonado en calle",
        "semáforo en rojo fijo",
        "señalización de obras deficiente",
        "congestión por mal estacionamiento",
        "limitador de velocidad dañado",
    ],
    "Otro": [
        "consulta sobre padrón municipal",
        "solicitud de documentos administrativos",
        "ruido de vecinos por obras",
        "queja sobre horario de atención",
        "información sobre licencias",
        "sugerencia para el municipio",
        "petición de mejora de servicios",
        "consulta sobre impuestos locales",
    ],
}

PRIORIDADES = {"Seguridad": 1, "Urbanismo": 2, "Limpieza": 2, "Tráfico": 3, "Otro": 3}

CALLES = [
    "Calle Mayor", "Avenida de la Constitución", "Plaza del Pueblo",
    "Calle San Juan", "Avenida del Sol", "Calle del Carmen",
    "Plaza España", "Calle Real", "Avenida de Europa", "Calle Nueva"
]

NOMBRES = [
    "Juan", "María", "Carlos", "Ana", "Pedro", "Laura", "Miguel", "Sofia",
    "David", "Isabel", "Antonio", "Carmen", "Francisco", "Elena", "Javier", "Rosa"
]

APELLIDOS = [
    "García", "Rodríguez", "Martínez", "Sánchez", "López", "González",
    "Fernández", "Pérez", "Gómez", "Díaz", "Cruz", "Reyes", "Morales", "Núñez"
]


def generate_solicitud(idx: int) -> dict:
    cat = random.choice(list(CATEGORIAS.keys()))
    desc = random.choice(CATEGORIAS[cat])
    nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
    email = f"{nombre.lower().replace(' ', '.')}@example.com"
    calle = f"{random.choice(CALLES)} {random.randint(1, 200)}"

    templates = [
        f"Buenos días, informo de {desc} en {calle}. Ruego atención urgente.",
        f"Por medio de la presente comunico que hay {desc} en {calle}. Es urgente.",
        f"Quiero comunicar que se ha detectado {desc} en {calle}. Gracias.",
        f"Adjuntouncio sobre {desc} situada en {calle}. Solicito actuación.",
        f"Me dirijo para informar de {desc} en la zona de {calle}.",
    ]

    if cat == "Seguridad":
        templates.append(f"URGENTE: {desc} en {calle}. Peligro para los vecinos.")
    if cat == "Otro":
        templates.append(f"Quisiera información sobre {desc}. Gracias.")

    body = random.choice(templates)

    return {
        "id": idx + 1,
        "subject": f"Solicitud sobre {desc.split(' en ')[0]}",
        "body": body,
        "email": email,
        "citizen_name": nombre,
        "categoria": cat,
        "prioridad": PRIORIDADES[cat],
        "created_at": (datetime.utcnow() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))).isoformat(),
    }


def main():
    output_dir = Path(__file__).parent / "synthetic"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = [generate_solicitud(i) for i in range(500)]

    csv_path = output_dir / "solicitudes_train.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    json_path = output_dir / "solicitudes_train.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"✓ {len(rows)} solicitudes generadas")
    print(f"  - CSV: {csv_path}")
    print(f"  - JSON: {json_path}")


if __name__ == "__main__":
    main()