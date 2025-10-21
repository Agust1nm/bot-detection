
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import re

# Configuración de semilla para reproducibilidad
SEED = 42
np.random.seed(SEED)
random.seed(SEED)


# ============================================================================
# Streamers y comunidades gaming de la región fueguina (simulados)
TDF_STREAMERS = [
    "UshuaiaGamer_TDF", "RioGrandeStreams", "FuegoAustral_Live",
    "PinguinoGaming", "CanalBeagle_Stream", "TierraDelJuego",
    "AustralPixels", "FinDelMundoTV", "PatagoniaLive"
]

# Horarios típicos de streaming en TDF (UTC-3)
# Pico de actividad: 18:00-02:00 hora local
TDF_PEAK_HOURS = list(range(18, 24)) + list(range(0, 3))

# ============================================================================
# NOMBRES DE USUARIOS REALES (proporcionados)
# ============================================================================
REAL_USERNAMES = [
    "Anii_tha", "triniyari", "lareinababy", "Antonella_12ofic", "Yair25wong",
    "guadalupe18reyna", "JAC187", "kaozkari", "Sonia2002", "Meli_ssa3",
    "Fiorella0208", "liziia7", "Mila_318", "Dalessandro97", "Evvv_fly",
    "Jos_2020", "Juniorxito1999", "Angie_x_x", "bri_hidalgo25", "h3llkittt",
    "sindyic", "abigail_JIJIJI", "GREZHIA", "Soplonazo", "gianiitt",
    "maffe900", "Nenamaria47", "Claudiafio", "alaniss_94", "frenchiexdd",
    "Denissegoau", "29Nataly", "iloveyomar", "Chaufitabsd", "jacqui_2025",
    "fioCas0704", "Ysatime2", "karolmarinaa", "zarela1", "rumualdo9",
    "ivani97", "ThuZambito_69", "Alexandra0901", "Anettec", "TP_MonicaMilagros1",
    "Alejo_ElPrrrinci", "Afra_02", "soia09", "Iamjesmar", "azuldi",
    "ladydelcarmen28U", "mikeee25AA", "Dolcezza12", "naoo2025", "TP_mafe26",
    "angela1127", "Khabib_nurvagomedov", "PaolaArone", "foxito1995", "Jimenaeste",
    "IvansM10", "Perruko96", "QCharaa", "iDiegod", "CHICHARO_25",
    "Elicitas2005", "Celeste_0340", "Sahory08", "abyy000", "Salome578",
    "natyfrag", "Klooz_OG", "KarlonchoCR6", "jeremswi", "Emy1222",
    "estrellamonterrey", "mariarosa21092000", "TP_ROSARIO112", "stephanycl",
    "Taxista_de_Tao", "Vanessit1", "stalynerick", "didio19", "alphatx",
    "cesarLCP", "liliangiuliana17", "alisandraq", "Alexcf10", "leidy123456",
    "geminis_03", "Emili_23", "veronicazcabellos", "daleshklu", "Fabrizzio2008",
    "BRISA_PUEE444", "Chalitho95", "abraham91289", "alberatriz", "Sheri_net",
    "fabiuhhh", "mixi_26", "RossiDC", "Saraivargas", "camilaaylen",
    "Aleadrije", "mariajusu", "Jeffer20xi", "alissonlama", "Alebc8",
    "chelu12", "yeni0707", "meliii234", "Naamin02", "rossacuario01",
    "Rosioz", "BorisKing97", "jhail10", "eilynmendezA", "juss10",
    "Adrieldlc", "realjjay", "Suscriptor", "Anderrr111", "GoldeHuijsen",
    "EL_SOBA_NALGAS", "Strongg7", "UnderIron", "kriller17losDiablos", "samlopez",
    "Beltrocho11", "Zell10", "patico7", "davidr103", "farruk1978",
    "Ajr_1403", "josefms", "ElmenorcitoOO", "Camilonia22", "yyxhir",
    "Carlos_pl2", "Giandrex", "MENDOO0405", "daniela0122", "Blaker117",
    "Ands19", "Jeronimo1208", "Cristian_1904", "Juanes_P30", "Euph96",
    "diazbernalsamuel", "dankel150", "Yesi2209", "jjy7", "rodrigo_750",
    "RDVS30", "Vity2025", "Narsiso", "Allanraul12", "Andresjr_11",
    "Darcka0", "Se3as", "Jeisber", "Juangua", "CDanQui_W",
    "mejia666", "yandel_correa", "Matthewbpv", "Javy0987", "Mikyyybb",
    "Wjeiner", "rxfaaas", "Yael912j", "mampano20", "Davidxx00",
    "Kamilozkt", "Sebaschar", "RodriTTMalibu", "JUANCHIMBO", "Sebgol",
    "Andres0524", "edwinmx2001", "emanuelc_10", "Tatar2001_7", "franc1sco21",
    "luchoovl2", "juanitinelli", "Monchiix", "Markitosss_23", "Carlos15yep",
    "Jsaints", "IBAUTI", "matias_antonio", "BEBERENO7", "ElPelucaMilei",
    "N0kc", "iracund", "Suty77x", "HaroldSkn", "Leax", "Tomas_v"
]

# Plantillas adicionales para nombres humanos realistas
HUMAN_NAME_PATTERNS = [
    "{name}_{year}", "{name}{number}", "{adj}_{name}", 
    "TP_{name}{number}", "{name}_{city}", "El{name}",
    "{name}Gaming", "{name}TDF", "{name}Austral"
]

NAMES = ["Mateo", "Sofia", "Lucas", "Emma", "Diego", "Valentina", "Martin", 
         "Isabella", "Santiago", "Camila", "Benjamin", "Martina", "Nicolas"]
ADJECTIVES = ["Cool", "Epic", "Pro", "Real", "Super", "Ultra", "True"]
TDF_CITIES = ["Ushuaia", "RioGrande", "Tolhuin", "TDF"]

# Patrones de nombres de bots genéricos
BOT_NAME_PATTERNS = [
    "user{number}", "bot{number}", "test{number}", "guest{number}",
    "viewer{number}", "spam{number}", "promo{number}", "link{number}",
    "auto{number}", "fake{number}", "temp{number}", "anon{number}"
]

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def is_generic_name(username):
    """Detecta si un nombre sigue patrones genéricos de bot"""
    generic_patterns = [
        r'^(user|bot|test|guest|viewer|spam|promo|link|auto|fake|temp|anon)\d+$',
        r'^\w{1,4}\d{4,}$',  # Ej: abc12345
        r'^\d+\w{1,4}$',      # Ej: 12345abc
    ]
    username_lower = username.lower()
    return any(re.match(pattern, username_lower) for pattern in generic_patterns)

def extract_username_features(username):
    """Extrae características del nombre de usuario (Feature Engineering)"""
    return {
        'username_length': len(username),
        'has_numbers': int(any(c.isdigit() for c in username)),
        'has_underscore': int('_' in username),
        'numeric_ratio': sum(c.isdigit() for c in username) / len(username) if len(username) > 0 else 0,
        'uppercase_ratio': sum(c.isupper() for c in username) / len(username) if len(username) > 0 else 0,
        'special_char_count': sum(not c.isalnum() and c != '_' for c in username)
    }

def generate_human_username(use_real=0.4, tdf_themed=0.2):
    """Genera nombre de usuario humano realista"""
    if random.random() < use_real and REAL_USERNAMES:
        return random.choice(REAL_USERNAMES)
    
    # Nombres con temática de Tierra del Fuego
    if random.random() < tdf_themed:
        base = random.choice(NAMES)
        city = random.choice(TDF_CITIES)
        return random.choice([
            f"{base}_{city}",
            f"{base}TDF",
            f"{city}{base}",
            f"{base}Austral{random.randint(1,99)}"
        ])
    
    # Nombres estándar realistas
    pattern = random.choice(HUMAN_NAME_PATTERNS)
    return pattern.format(
        name=random.choice(NAMES),
        number=random.randint(1, 9999),
        year=random.randint(1995, 2010),
        adj=random.choice(ADJECTIVES),
        city=random.choice(TDF_CITIES)
    )

def generate_bot_username(sophisticated=False):
    """Genera nombre de usuario de bot"""
    if sophisticated and random.random() < 0.3:
        # Bots sofisticados intentan parecer humanos
        return generate_human_username(use_real=0, tdf_themed=0)
    
    # Bots típicos con nombres genéricos
    pattern = random.choice(BOT_NAME_PATTERNS)
    return pattern.format(number=random.randint(1000, 99999))

def generate_timestamp(days_back=30):
    """Genera timestamp aleatorio en los últimos N días"""
    base_date = datetime(2025, 10, 20)  # Fecha actual del proyecto
    days_offset = random.randint(0, days_back)
    hour = random.choice(TDF_PEAK_HOURS) if random.random() < 0.7 else random.randint(0, 23)
    
    return base_date - timedelta(days=days_offset, hours=random.randint(0, 23), 
                                   minutes=random.randint(0, 59))

# ============================================================================
# GENERADORES DE USUARIOS
# ============================================================================

def generate_typical_bot():
    """Genera un bot típico fácilmente detectable"""
    username = generate_bot_username(sophisticated=False)
    
    data = {
        'username': username,
        'frequency': np.random.uniform(40, 200),
        'avg_message_length': np.random.uniform(10, 40),
        'total_messages': np.random.randint(50, 300),
        'url_ratio': np.random.uniform(0.5, 1.0),
        'repetition_ratio': np.random.uniform(0.6, 0.98),
        'time_in_channel': np.random.uniform(10, 100),
        'suspicious_links': 1 if np.random.random() > 0.2 else 0,
        'generic_name': 1,  # Casi siempre tienen nombre genérico
        'is_bot': 1,
        'channel': random.choice(TDF_STREAMERS),
        'timestamp': generate_timestamp()
    }
    
    # Agregar features derivadas del username
    username_features = extract_username_features(username)
    data.update(username_features)
    
    return data

def generate_sophisticated_bot():
    """Genera un bot sofisticado que intenta evadir detección"""
    username = generate_bot_username(sophisticated=True)
    
    # Agregar ruido para simular comportamiento más humano
    noise_factor = np.random.uniform(0.8, 1.2)
    
    data = {
        'username': username,
        'frequency': np.random.uniform(25, 45) * noise_factor,  # Más sutil
        'avg_message_length': np.random.uniform(30, 70),
        'total_messages': np.random.randint(20, 100),
        'url_ratio': np.random.uniform(0.3, 0.6),  # Menos URLs obvias
        'repetition_ratio': np.random.uniform(0.45, 0.7),  # Menos repetitivo
        'time_in_channel': np.random.uniform(30, 150),
        'suspicious_links': 1 if np.random.random() > 0.6 else 0,  # Menos obvio
        'generic_name': 1 if is_generic_name(username) else 0,
        'is_bot': 1,
        'channel': random.choice(TDF_STREAMERS),
        'timestamp': generate_timestamp()
    }
    
    username_features = extract_username_features(username)
    data.update(username_features)
    
    return data

def generate_typical_human():
    """Genera un usuario humano típico"""
    username = generate_human_username()
    
    data = {
        'username': username,
        'frequency': np.random.uniform(2, 25),
        'avg_message_length': np.random.uniform(30, 120),
        'total_messages': np.random.randint(5, 60),
        'url_ratio': np.random.uniform(0.0, 0.25),
        'repetition_ratio': np.random.uniform(0.0, 0.35),
        'time_in_channel': np.random.uniform(30, 180),
        'suspicious_links': 0,
        'generic_name': 1 if is_generic_name(username) else 0,  # Algunos humanos también
        'is_bot': 0,
        'channel': random.choice(TDF_STREAMERS),
        'timestamp': generate_timestamp()
    }
    
    username_features = extract_username_features(username)
    data.update(username_features)
    
    return data

def generate_active_human():
    """Genera un usuario humano muy activo (casos edge)"""
    username = generate_human_username()
    
    data = {
        'username': username,
        'frequency': np.random.uniform(20, 38),  # Muy activo pero humano
        'avg_message_length': np.random.uniform(15, 80),
        'total_messages': np.random.randint(40, 120),
        'url_ratio': np.random.uniform(0.15, 0.45),  # Comparte algunos links
        'repetition_ratio': np.random.uniform(0.25, 0.55),  # Algo repetitivo
        'time_in_channel': np.random.uniform(60, 200),
        'suspicious_links': 0,
        'generic_name': 1 if is_generic_name(username) else 0,
        'is_bot': 0,
        'channel': random.choice(TDF_STREAMERS),
        'timestamp': generate_timestamp()
    }
    
    username_features = extract_username_features(username)
    data.update(username_features)
    
    return data

# ============================================================================
# GENERADOR PRINCIPAL
# ============================================================================

def generate_dataset(n_samples=1800, bot_ratio=0.40):
    """
    Genera dataset balanceado con distribución realista
    
    Parámetros:
    -----------
    n_samples : int
        Total de instancias a generar
    bot_ratio : float
        Proporción de bots (0.40 = 40% bots, 60% humanos)
    """
    
    print("=" * 70)
    print("GENERADOR DE DATASET - DETECCIÓN DE BOTS EN KICK")
    print("Proyecto: Protección de Streamers en Tierra del Fuego")
    print("=" * 70)
    print(f"\nConfigurando generación:")
    print(f"  • Total de instancias: {n_samples}")
    print(f"  • Ratio de bots: {bot_ratio*100:.1f}%")
    print(f"  • Ratio de humanos: {(1-bot_ratio)*100:.1f}%")
    print(f"  • Semilla aleatoria: {SEED}")
    print(f"  • Contexto regional: Tierra del Fuego, Argentina")
    
    n_bots = int(n_samples * bot_ratio)
    n_humans = n_samples - n_bots
    
    # Distribución de tipos de usuarios
    n_typical_bots = int(n_bots * 0.70)
    n_sophisticated_bots = n_bots - n_typical_bots
    
    n_typical_humans = int(n_humans * 0.80)
    n_active_humans = n_humans - n_typical_humans
    
    print(f"\nDistribución de usuarios:")
    print(f"  BOTS ({n_bots} total):")
    print(f"    - Bots típicos: {n_typical_bots}")
    print(f"    - Bots sofisticados: {n_sophisticated_bots}")
    print(f"  HUMANOS ({n_humans} total):")
    print(f"    - Humanos típicos: {n_typical_humans}")
    print(f"    - Humanos activos: {n_active_humans}")
    
    print("\nGenerando instancias...")
    
    data = []
    
    # Generar bots
    for i in range(n_typical_bots):
        data.append(generate_typical_bot())
        if (i + 1) % 200 == 0:
            print(f"  ✓ Bots típicos: {i+1}/{n_typical_bots}")
    
    for i in range(n_sophisticated_bots):
        data.append(generate_sophisticated_bot())
        if (i + 1) % 100 == 0:
            print(f"  ✓ Bots sofisticados: {i+1}/{n_sophisticated_bots}")
    
    # Generar humanos
    for i in range(n_typical_humans):
        data.append(generate_typical_human())
        if (i + 1) % 200 == 0:
            print(f"  ✓ Humanos típicos: {i+1}/{n_typical_humans}")
    
    for i in range(n_active_humans):
        data.append(generate_active_human())
        if (i + 1) % 100 == 0:
            print(f"  ✓ Humanos activos: {i+1}/{n_active_humans}")
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Mezclar aleatoriamente
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
    
    # Agregar ID único
    df.insert(0, 'user_id', range(1, len(df) + 1))
    
    print(f"\n✅ Dataset generado exitosamente!")
    print(f"   Total de instancias: {len(df)}")
    print(f"   Columnas: {len(df.columns)}")
    
    return df

# ============================================================================
# ANÁLISIS Y VALIDACIÓN
# ============================================================================

def validate_dataset(df):
    """Valida la calidad del dataset generado"""
    print("\n" + "=" * 70)
    print("VALIDACIÓN DEL DATASET")
    print("=" * 70)
    
    # Información básica
    print(f"\n📊 INFORMACIÓN GENERAL:")
    print(f"   Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
    print(f"   Memoria: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # Balance de clases
    print(f"\n⚖️  BALANCE DE CLASES:")
    class_dist = df['is_bot'].value_counts()
    for class_label, count in class_dist.items():
        class_name = "Bot" if class_label == 1 else "Humano"
        percentage = (count / len(df)) * 100
        print(f"   {class_name} (is_bot={class_label}): {count} ({percentage:.1f}%)")
    
    # Valores faltantes
    print(f"\n🔍 VALORES FALTANTES:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✅ No hay valores faltantes")
    else:
        print(missing[missing > 0])
    
    # Duplicados
    duplicates = df.duplicated(subset='username').sum()
    print(f"\n🔄 DUPLICADOS:")
    print(f"   Usernames duplicados: {duplicates}")
    
    # Estadísticas por clase
    print(f"\n📈 ESTADÍSTICAS POR CLASE:")
    numeric_cols = ['frequency', 'avg_message_length', 'total_messages', 
                    'url_ratio', 'repetition_ratio', 'time_in_channel']
    
    for col in numeric_cols:
        bot_mean = df[df['is_bot'] == 1][col].mean()
        human_mean = df[df['is_bot'] == 0][col].mean()
        separation = abs(bot_mean - human_mean) / max(bot_mean, human_mean)
        
        print(f"\n   {col}:")
        print(f"      Bots:    {bot_mean:>8.2f}")
        print(f"      Humanos: {human_mean:>8.2f}")
        print(f"      Separación: {separation*100:.1f}%")
    
    # Distribución de canales (TDF)
    print(f"\n🌎 DISTRIBUCIÓN POR CANAL (Tierra del Fuego):")
    channel_dist = df['channel'].value_counts()
    for channel, count in channel_dist.head().items():
        print(f"   {channel}: {count} usuarios")
    
    return True

# ============================================================================
# EXPORTACIÓN
# ============================================================================

def export_dataset(df, filename='kick_bot_dataset_v2.csv'):
    """Exporta el dataset a CSV"""
    
    # Seleccionar columnas para el CSV final (sin timestamp y channel para simplificar)
    export_cols = ['user_id', 'username', 'frequency', 'avg_message_length', 
                   'total_messages', 'url_ratio', 'repetition_ratio', 
                   'time_in_channel', 'suspicious_links', 'generic_name',
                   'username_length', 'has_numbers', 'has_underscore',
                   'numeric_ratio', 'uppercase_ratio', 'special_char_count',
                   'is_bot']
    
    df_export = df[export_cols].copy()
    
    df_export.to_csv(filename, index=False, encoding='utf-8')
    print(f"\n💾 Dataset exportado: {filename}")
    print(f"   Columnas exportadas: {len(export_cols)}")
    
    # Generar archivo de metadatos
    metadata_filename = filename.replace('.csv', '_metadata.txt')
    with open(metadata_filename, 'w', encoding='utf-8') as f:
        f.write("METADATA - KICK BOT DETECTION DATASET v2.0\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total de instancias: {len(df_export)}\n")
        f.write(f"Semilla aleatoria: {SEED}\n")
        f.write(f"Contexto: Tierra del Fuego, Argentina\n\n")
        f.write("Columnas:\n")
        for i, col in enumerate(export_cols, 1):
            f.write(f"  {i}. {col}\n")
    
    print(f"📝 Metadata generada: {metadata_filename}")
    
    return df_export

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    # Generar dataset
    df = generate_dataset(n_samples=1800, bot_ratio=0.40)
    
    # Validar
    validate_dataset(df)
    
    # Exportar
    df_final = export_dataset(df, 'kick_bot_dataset_v2.csv')
    
    # Mostrar muestra
    print("\n" + "=" * 70)
    print("MUESTRA DEL DATASET (primeras 5 filas)")
    print("=" * 70)
    print(df_final.head())
    
    print("\n" + "=" * 70)
    print("✅ GENERACIÓN COMPLETADA")
    print("=" * 70)
    print("\n📋 Próximos pasos:")
    print("   1. Revisar el archivo CSV generado")
    print("   2. Realizar análisis exploratorio (EDA)")
    print("   3. Entrenar modelos de clasificación")
    print("   4. Evaluar métricas de desempeño")
    print("\n🎯 Objetivo: Proteger streamers de Tierra del Fuego contra bots")
    print("=" * 70)
