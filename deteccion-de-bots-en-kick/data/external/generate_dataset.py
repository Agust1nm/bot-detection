"""
Generador de Dataset Sintético - Detección de Bots en Kick
Genera entre 1500-2000 instancias realistas
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

# Semilla para reproducibilidad
np.random.seed(42)

# Usuarios reales observados
REAL_USERS = [
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

def is_generic_name(username):
    """Detecta nombres genéricos de bots"""
    patterns = [r'^user\d+$', r'^bot\d+$', r'^test\d+$', r'^player\d+$', r'^guest\d+$']
    return any(re.match(pattern, username.lower()) for pattern in patterns)

def generate_bot_username():
    """Genera nombres típicos de bots"""
    patterns = [
        f"user{np.random.randint(1000, 9999)}",
        f"bot{np.random.randint(100, 999)}",
        f"test{np.random.randint(1000, 9999)}",
        f"viewer{np.random.randint(100, 9999)}",
        f"guest{np.random.randint(1000, 9999)}"
    ]
    return np.random.choice(patterns)

def generate_human_username():
    """Genera nombres personalizados"""
    if np.random.random() < 0.6:
        return np.random.choice(REAL_USERS)
    
    prefixes = ["Dark", "Pro", "King", "Queen", "Master", "Gamer", "Epic", "Shadow"]
    suffixes = ["XD", "YT", "Pro", "123", "2025", "Gaming", "_", "xx"]
    name = np.random.choice(prefixes) + np.random.choice(suffixes)
    if np.random.random() < 0.3:
        name += str(np.random.randint(1, 999))
    return name

def generate_bot_instance():
    """Genera instancia de BOT"""
    frequency = np.random.uniform(40, 200)
    avg_message_length = np.random.uniform(10, 40)
    total_messages = int(np.random.uniform(30, 300))
    url_ratio = np.random.uniform(0.5, 1.0)
    repetition_ratio = np.random.uniform(0.6, 0.98)
    time_in_channel = np.random.uniform(5, 120)
    suspicious_links = 1 if np.random.random() < 0.8 else 0
    username = generate_bot_username() if np.random.random() < 0.9 else generate_human_username()
    
    return {
        'username': username,
        'frequency': round(frequency, 2),
        'avg_message_length': round(avg_message_length, 1),
        'total_messages': total_messages,
        'url_ratio': round(url_ratio, 3),
        'repetition_ratio': round(repetition_ratio, 3),
        'time_in_channel': round(time_in_channel, 1),
        'suspicious_links': suspicious_links,
        'generic_name': 1 if is_generic_name(username) else 0,
        'is_bot': 1
    }

def generate_human_instance():
    """Genera instancia de HUMANO"""
    frequency = np.random.uniform(2, 30)
    avg_message_length = np.random.uniform(20, 120)
    total_messages = int(np.random.uniform(3, 50))
    url_ratio = np.random.uniform(0.0, 0.3)
    repetition_ratio = np.random.uniform(0.0, 0.4)
    time_in_channel = np.random.uniform(10, 180)
    suspicious_links = 1 if np.random.random() < 0.1 else 0
    username = generate_human_username()
    
    return {
        'username': username,
        'frequency': round(frequency, 2),
        'avg_message_length': round(avg_message_length, 1),
        'total_messages': total_messages,
        'url_ratio': round(url_ratio, 3),
        'repetition_ratio': round(repetition_ratio, 3),
        'time_in_channel': round(time_in_channel, 1),
        'suspicious_links': suspicious_links,
        'generic_name': 1 if is_generic_name(username) else 0,
        'is_bot': 0
    }

def generate_dataset(total_size=1800, bot_ratio=0.40):
    """Genera el dataset completo"""
    n_bots = int(total_size * bot_ratio)
    n_humans = total_size - n_bots
    
    print(f"🤖 Generando dataset de {total_size} usuarios...")
    print(f"   Bots: {n_bots} ({bot_ratio*100}%)")
    print(f"   Humanos: {n_humans} ({(1-bot_ratio)*100}%)")
    print("-" * 50)
    
    data = []
    
    # Generar BOTS
    print(f"Generando {n_bots} bots...")
    for i in range(n_bots):
        data.append(generate_bot_instance())
        if (i + 1) % 100 == 0:
            print(f"  ✓ {i + 1}/{n_bots} bots")
    
    # Generar HUMANOS
    print(f"Generando {n_humans} humanos...")
    for i in range(n_humans):
        data.append(generate_human_instance())
        if (i + 1) % 100 == 0:
            print(f"  ✓ {i + 1}/{n_humans} humanos")
    
    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df['username'] = df['username'] + '_' + df.index.astype(str)
    
    print("-" * 50)
    print("✅ Dataset generado exitosamente!")
    return df

if __name__ == "__main__":
    # Generar dataset
    df = generate_dataset(total_size=1800, bot_ratio=0.40)
    
    # Mostrar info
    print("\n📊 INFORMACIÓN DEL DATASET")
    print("=" * 50)
    print(f"Total instancias: {len(df)}")
    print(f"Bots: {df['is_bot'].sum()} ({df['is_bot'].sum()/len(df)*100:.1f}%)")
    print(f"Humanos: {(1-df['is_bot']).sum()} ({(1-df['is_bot']).sum()/len(df)*100:.1f}%)")
    print(f"Valores nulos: {df.isnull().sum().sum()}")
    
    # Guardar
    output_file = '../../data/raw/kick_chat_bot_detection_dataset.csv'
    df.to_csv(output_file, index=False)
    print(f"\n💾 Dataset guardado: {output_file}")
    
    # Muestra
    sample_file = '../../data/interim/dataset_sample.csv'
    df.head(50).to_csv(sample_file, index=False)
    print(f"📄 Muestra guardada: {sample_file}")
    
    print("\n✅ ¡Proceso completado!")