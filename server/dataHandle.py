import sqlite3

def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS chat_history")
    cursor.execute('''
        CREATE TABLE chat_history (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT,
            recipient_id TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
def store_chat_history(client_id, recipient_id, message):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (client_id, recipient_id, message)
        VALUES (?, ?, ?)
    ''', (client_id, recipient_id, message))
    conn.commit()
    conn.close()

def retrieve_chat_history(client_id, recipient_id):
    conn = sqlite3.connect('chat_history.db') 
    cursor = conn.cursor()
    cursor.execute("""
    SELECT client_id, message
    FROM chat_history
    WHERE (client_id = ? AND recipient_id = ?)
       OR (client_id = ? AND recipient_id = ?)
    ORDER BY message_id;
    """, (client_id, recipient_id, recipient_id, client_id))

    ch = cursor.fetchall()
    chat = ''
    
    for row in ch:
        sender_id, message = row
        chat += (f"{sender_id}: {message.strip()}\n")  # Append to 'chat', not 'message'
    
    return chat