#!/usr/bin/env python3
# generate_kick_dataset_random_time.py
"""
Extrae mensajes desde kick_scraper.db (tablas prefijo kickchat_) y genera CSV con las columnas:
user_id, username, frequency, avg_message_length, total_messages, url_ratio, repetition_ratio,
time_in_channel, suspicious_links, generic_name, username_length, has_numbers, has_underscore,
numeric_ratio, uppercase_ratio, special_char_count, is_bot
"""

import sqlite3
import pandas as pd
import numpy as np
import re
import random
from typing import List

DB_PATH = "kick_scraper.db"
OUTPUT_CSV = "kick_chat_datasetV4.csv"
RANDOM_STATE = 42
MIN_TIME_MIN = 5       # minutos mínimo en canal (ajustable)
MAX_TIME_MIN = 240     # minutos máximo en canal (ajustable)
TARGET_TOTAL = None    # si querés forzar tamaño final, implementá sampling/augment; por defecto usar todos los usuarios
HUMAN_RATIO = 0.6      # 60% humanos
BOT_RATIO = 0.4        # 40% bots

random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)

URL_REGEX = re.compile(r"http[s]?://", flags=re.IGNORECASE)
SUSPICIOUS_PATTERNS = ["bit.ly", "tinyurl", "grabify", "discord.gg", "join.discord"]

def list_kickchat_tables(conn: sqlite3.Connection) -> List[str]:
    q = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'kickchat_%';"
    cur = conn.execute(q)
    return [row[0] for row in cur.fetchall()]

def load_messages_from_tables(conn: sqlite3.Connection, tables: List[str]) -> pd.DataFrame:
    frames = []
    for t in tables:
        q = f'''
        SELECT
            COALESCE(user_id, sender_id) AS user_id,
            COALESCE(username, sender_username) AS username,
            COALESCE(content, '') AS content,
            COALESCE(event_type, '') AS event_type,
            COALESCE(timestamp, created_at) AS created_at
        FROM "{t}"
        WHERE (event_type IS NULL OR lower(event_type) LIKE '%chat%' OR lower(event_type) LIKE '%message%' OR event_type='message')
        '''
        try:
            df = pd.read_sql_query(q, conn)
            if not df.empty:
                frames.append(df)
        except Exception:
            try:
                df2 = pd.read_sql_query(f'SELECT * FROM "{t}"', conn)
                cols = df2.columns
                uid = next((c for c in cols if c.lower() in ("user_id", "sender_id")), None)
                uname = next((c for c in cols if c.lower() in ("username", "sender_username")), None)
                content_col = next((c for c in cols if c.lower() in ("content", "message", "processed_message")), None)
                if uid and uname and content_col:
                    df_clean = df2[[uid, uname, content_col]].rename(columns={uid: "user_id", uname: "username", content_col: "content"})
                    frames.append(df_clean)
            except Exception:
                continue
    if not frames:
        return pd.DataFrame(columns=["user_id", "username", "content", "event_type", "created_at"])
    return pd.concat(frames, ignore_index=True, sort=False)

def aggregate_by_user(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["user_id", "username", "messages"])
    df["username"] = df["username"].fillna("").astype(str)
    df["user_id"] = df["user_id"].astype(str)
    df["content"] = df["content"].fillna("").astype(str)
    grouped = df.groupby(["user_id", "username"])["content"].apply(list).reset_index().rename(columns={"content": "messages"})
    return grouped

def compute_username_features(username: str):
    u = username or ""
    L = len(u) if len(u) > 0 else 1
    return {
        "username_length": len(u),
        "has_numbers": int(any(ch.isdigit() for ch in u)),
        "has_underscore": int("_" in u),
        "numeric_ratio": float(sum(ch.isdigit() for ch in u) / L),
        "uppercase_ratio": float(sum(ch.isupper() for ch in u) / L),
        "special_char_count": int(sum(not ch.isalnum() for ch in u)),
        "generic_name": int(u.lower().startswith("user") or u.lower().startswith("guest"))
    }

def compute_message_features(messages: List[str], time_in_channel_min: int):
    total_messages = len(messages)
    if total_messages == 0:
        return {
            "frequency": 0.0,
            "avg_message_length": 0.0,
            "total_messages": 0,
            "url_ratio": 0.0,
            "repetition_ratio": 0.0,
            "time_in_channel": time_in_channel_min,
            "suspicious_links": 0
        }
    lengths = [len(m) for m in messages]
    avg_length = float(np.mean(lengths))
    url_flags = [1 if URL_REGEX.search(m) else 0 for m in messages]
    url_ratio = float(sum(url_flags) / total_messages)
    repetition_ratio = float(total_messages / len(set(messages))) if len(set(messages)) > 0 else float(total_messages)
    suspicious_links = int(any(any(p in m.lower() for p in SUSPICIOUS_PATTERNS) for m in messages))
    frequency = float(total_messages / time_in_channel_min)  # msgs per minute using random time
    return {
        "frequency": frequency,
        "avg_message_length": avg_length,
        "total_messages": int(total_messages),
        "url_ratio": url_ratio,
        "repetition_ratio": repetition_ratio,
        "time_in_channel": time_in_channel_min,
        "suspicious_links": suspicious_links
    }

def extract_all_features(grouped_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in grouped_df.iterrows():
        user_id = r["user_id"]
        username = r["username"]
        messages = r["messages"] if isinstance(r["messages"], list) else []
        time_in_channel = random.randint(MIN_TIME_MIN, MAX_TIME_MIN)
        msg_feats = compute_message_features(messages, time_in_channel)
        name_feats = compute_username_features(username)
        row = {
            "user_id": user_id,
            "username": username,
            **msg_feats,
            **name_feats
        }
        rows.append(row)
    return pd.DataFrame(rows)

def heuristic_label(row) -> int:
    score = 0
    if row["url_ratio"] > 0.6:           # Bots de spam con links
        score += 2
    if row["avg_message_length"] > 40:   # Mensajes largos = links
        score += 1
    if row["repetition_ratio"] > 8.0:    # Repetición extrema
        score += 1
    if row["frequency"] > 2.0:           # Muy alta actividad
        score += 1
    if row["generic_name"] == 1:         # Nombre genérico
        score += 1
    if row["suspicious_links"] == 1:     # Links maliciosos
        score += 1
    return int(score >= 3)

def balance_dataset(df: pd.DataFrame, human_ratio: float = HUMAN_RATIO, bot_ratio: float = BOT_RATIO, target_total: int = None) -> pd.DataFrame:
    """
    Balancea el dataset para que tenga human_ratio de humanos y bot_ratio de bots.
    Si target_total es None, usa el tamaño del dataset original.
    """
    if df.empty:
        return df
    
    # Separar humanos y bots
    humans = df[df["is_bot"] == 0]
    bots = df[df["is_bot"] == 1]
    
    # Calcular tamaño objetivo
    total_size = len(df) if target_total is None else target_total
    target_humans = int(total_size * human_ratio)
    target_bots = int(total_size * bot_ratio)
    
    # Ajustar tamaños
    if len(humans) >= target_humans:
        humans_sample = humans.sample(n=target_humans, random_state=RANDOM_STATE)
    else:
        # Sobremuestreo si no hay suficientes humanos
        humans_sample = humans.sample(n=target_humans, replace=True, random_state=RANDOM_STATE)
    
    if len(bots) >= target_bots:
        bots_sample = bots.sample(n=target_bots, random_state=RANDOM_STATE)
    else:
        # Sobremuestreo si no hay suficientes bots
        bots_sample = bots.sample(n=target_bots, replace=True, random_state=RANDOM_STATE)
    
    # Combinar y mezclar
    balanced_df = pd.concat([humans_sample, bots_sample], ignore_index=True)
    balanced_df = balanced_df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    
    return balanced_df

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        tables = list_kickchat_tables(conn)
        messages_df = load_messages_from_tables(conn, tables)
    finally:
        conn.close()

    grouped = aggregate_by_user(messages_df)
    features_df = extract_all_features(grouped)
    if features_df.empty:
        print("No users detected. Output CSV will be empty.")
        return
    
    # Aplicar etiquetado heurístico
    features_df["is_bot"] = features_df.apply(heuristic_label, axis=1)
    
    # Balancear el dataset al 60% humanos y 40% bots
    final_df = balance_dataset(features_df, human_ratio=HUMAN_RATIO, bot_ratio=BOT_RATIO, target_total=TARGET_TOTAL)

    columns = [
        "user_id", "username", "frequency", "avg_message_length", "total_messages",
        "url_ratio", "repetition_ratio", "time_in_channel", "suspicious_links",
        "generic_name", "username_length", "has_numbers", "has_underscore",
        "numeric_ratio", "uppercase_ratio", "special_char_count", "is_bot"
    ]
    for c in columns:
        if c not in final_df.columns:
            final_df[c] = np.nan
    final_df = final_df[columns]
    final_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Saved {len(final_df)} rows to {OUTPUT_CSV} with {HUMAN_RATIO*100}% humans and {BOT_RATIO*100}% bots")

if __name__ == "__main__":
    main()