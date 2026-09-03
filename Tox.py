import os
import re
import time
import asyncio
import random
import sys
import requests
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    ChatAdminRequiredError,
    UserNotMutualContactError,
    UserAlreadyParticipantError,
    PeerFloodError,
    UsernameInvalidError,
    UserIdInvalidError,
    UserPrivacyRestrictedError
)
from telethon.tl.functions.channels import InviteToChannelRequest

# CONFIGURAZIONE STRUTTURA E VERSIONING
# CONFIGURAZIONE STRUTTURA E VERSIONING
VERSIONE_LOCALE = "1.4.0"  # Lascialo a 1.2.0 per fare il test, poi rimettilo a 1.3.0
URL_SERVER_CHECK = "https://github.com/isoterico/tox-update/blob/main/update.json"

SESSIONS_DIR = "sessions_data"
LOG_ELABORATI = "elaborati.txt"
ENV_FILE = ".env"
MESSAGGI_FILE = "messaggi.txt"

def esegui_autoupdate(url_download):
    """
    Scarica il codice sorgente reale (.py) da GitHub, crea un updater temporaneo,
    chiude questo programma e lo sovrascrive senza fare confusione con il JSON.
    """
    print("\n📥 Download dell'aggiornamento automatico in corso...")
    try:
        # Scarica il codice Python pulito dal link RAW
        risposta = requests.get(url_download, timeout=15)
        if risposta.status_code == 200:
            nuovo_codice = risposta.text
            
            # Trova i percorsi fisici del file sul tuo computer
            file_corrente = os.path.abspath(sys.argv[0])
            cartella_corrente = os.path.dirname(file_corrente)
            file_updater = os.path.join(cartella_corrente, "updater_temp.py")
            file_nuovo_codice = os.path.join(cartella_corrente, "tox_nuovo.tmp")
            
            # Salva temporaneamente il codice Python scaricato
            with open(file_nuovo_codice, "w", encoding="utf-8") as f:
                f.write(nuovo_codice)
            
            # Crea lo script esterno che farà la sostituzione fisica sul disco
            codice_updater = f"""import time
import os
import sys

time.sleep(1)  # Aspetta che il Tox.py vecchio si chiuda del tutto
try:
    if os.path.exists("{file_nuovo_codice}"):
        # Sostituisce il vecchio codice con quello nuovo
        os.replace("{file_nuovo_codice}", "{file_corrente}")
        print("✅ Aggiornamento applicato con successo!")
        # Riavvia il programma aggiornato
        os.system(f"{{sys.executable}} {{file_corrente}}")
except Exception as e:
    print(f"Errore durante l'applicazione del fix: {{e}}")

if os.path.exists(__file__):
    os.remove(__file__)
"""
            with open(file_updater, "w", encoding="utf-8") as f:
                f.write(codice_updater)
                
            print("🔄 Riavvio del tool in corso per applicare le patch...")
            # Protegge i percorsi inserendo i doppi apici per gestire gli spazi vuoti nelle cartelle
            if os.name == 'nt':
                os.system(f'start /b "{sys.executable}" "{file_updater}"')
            else:
                os.system(f'"{sys.executable}" "{file_updater}" &')
            sys.exit()

        else:
            print("❌ Impossibile scaricare il file di aggiornamento da GitHub.")
    except Exception as e:
        print(f"❌ Errore durante la fase di auto-update: {e}")

def verifica_aggiornamenti_e_stato():
    print("🔍 Verifica integrità e aggiornamenti su GitHub...")
    try:
        risposta = requests.get(URL_SERVER_CHECK, timeout=5)
        
        if risposta.status_code == 200:
            dati = risposta.json()
            versione_remota = dati.get("versione_corrente")
            blocco_obbligatorio = dati.get("blocco_obbligatorio", False)
            stato_servizio = dati.get("stato_servizio", "attivo")
            messaggio_server = dati.get("messaggio", "")

            if stato_servizio == "manutenzione":
                print(f"\n❌ IL SERVIZIO È IN MANUTENZIONE:\n📢 {messaggio_server}\n")
                sys.exit()
            elif stato_servizio == "disattivato":
                print("\n❌ QUESTA VERSIONE DEL TOOL È STATA DISATTIVATA DAL PROPRIETARIO.\n")
                sys.exit()

            if versione_remota != VERSIONE_LOCALE:
                print("\n╔═════════════════════════════════════════════════════════════════════════╗")
                print(f"║ 📢 NUOVO AGGIORNAMENTO RILEVATO: v{versione_remota:<36} ║")
                print("╚═════════════════════════════════════════════════════════════════════════╝")
                if messaggio_server:
                    print(f"📢 Note: {messaggio_server}")
                
                if blocco_obbligatorio:
                    # Prende l'URL del file .py (url_aggiornamento) contenuto nel JSON e avvia il download vero
                    url_download = dati.get("url_aggiornamento")
                    esegui_autoupdate(url_download)
            else:
                print("✅ Il software è aggiornato all'ultima versione stabile.\n")
                time.sleep(0.5)
        else:
            print("⚠️ Risposta di GitHub non standard. Avvio in modalità offline protetta...\n")
    except Exception as e:
        print(f"⚠️ Impossibile verificare gli aggiornamenti ({e}). Avvio in modalità offline...\n")


def genera_parametri_client():
    scelta = random.choice(DISPOSITIVI_ANDROID)
    return {
        "device_model": scelta["device"],
        "system_version": scelta["system"],
        "app_version": f"{random.randint(9, 10)}.{random.randint(0, 5)}.{random.randint(0, 9)}"
    }

async def mostra_banner_animato():
    banner = r"""
        ,----,                                                                                   
      ,/   .`|                                                                                   
    ,`   .'  :                                     ,-.----.                                      
  ;    ;     /                    ,--,             \    /  \                          ,-.----.   
.'___,/    ,'  ,---.            ,--.'|             ;   :    \                         \    /  \  

|    :     |  '   ,'\ ,--,  ,--,|  |,              |   | .\ :               .--.--.   |   :    | 
;    |.';  ; /   /   ||'. \/ .`|`--'_       ,---.  .   : |: |   ,--.--.    /  /    '  |   | .\ : 
`----'  |  |.   ; ,. :'  \/  / ;,' ,'|     /     \ |   |  \ :  /       \  |  :  /`./  .   : |: | 
    '   :  ;_   | |: : \  \.' / '  | |    /    / ' |   : .  / .--.  .-. | |  :  ;_    |   |  \ : 

    |   |  ''   | .; :  \  ;  ; |  | :   .    ' /  ;   | |  \  \__\/: . .  \  \    `. |   : .  | 
    '   :  ||   :    | / \  \  \'  : |__ '   ; :__ |   | ;\  \ ," .--.; |   `----.   \:     |`-' 
    ;   |.'  \   \  /./__;   ;  \  | '.'|'   | '.'|:   ' | \.'/  /  ,.  |  /  /`--'  /:   : :    
    '---'     `----' |   :/\  \ ;  :    ;|   :    ::   : :-' ;  :   .'   \'--'.     / |   | :    
                     `---'  `--`|  ,   /  \   \  / |   |.'   |  ,     .-./  `--'---'  `---'.|    
                                 ---`-'    `----'  `---'      `--`---'                  `---`    
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    for riga in banner.splitlines():
        print(riga)
        await asyncio.sleep(0.01)
    print("\n" + "="*95 + "\n")

def carica_elaborati():
    if not os.path.exists(LOG_ELABORATI):
        return set()
    with open(LOG_ELABORATI, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())

def salva_elaborato(username):
    with open(LOG_ELABORATI, "a", encoding="utf-8") as f:
        f.write(f"{username}\n")

def resetta_elaborati():
    if os.path.exists(LOG_ELABORATI):
        os.remove(LOG_ELABORATI)
    print("🗑️ Memoria dei membri elaborati svuotata con successo!")

def carica_messaggi():
    if not os.path.exists(MESSAGGI_FILE):
        with open(MESSAGGI_FILE, "w", encoding="utf-8") as f:
            f.write("Ciao! Unisciti al nostro gruppo: {link}\n")
        return ["Ciao! Unisciti al nostro gruppo: {link}"]
    with open(MESSAGGI_FILE, "r", encoding="utf-8") as f:
        messaggi = [line.strip() for line in f if line.strip()]
    if not messaggi:
        return ["Ciao! Unisciti al nostro gruppo: {link}"]
    return messaggi

def carica_o_richiedi_api():
    if os.path.exists(ENV_FILE):
        api_id, api_hash = None, None
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    chiave, valore = line.split("=", 1)
                    if chiave.strip() == "API_ID":
                        api_id = int(valore.strip())
                    elif chiave.strip() == "API_HASH":
                        api_hash = valore.strip()
        if api_id and api_hash:
            return api_id, api_hash

    print("\n--- CONFIGURAZIONE API TELEGRAM ---")
    try:
        api_id = int(input("Inserisci API_ID: ").strip())
        api_hash = input("Inserisci API_HASH: ").strip()
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.write(f"API_ID={api_id}\nAPI_HASH={api_hash}\n")
        print(f"✅ Credenziali salvate in `{ENV_FILE}`.")
        return api_id, api_hash
    except ValueError:
        print("❌ API_ID deve essere un numero valido.")
        return None, None

CONNECTED_CLIENTS = {}

async def add_new_account(api_id, api_hash):
    global CONNECTED_CLIENTS
    print("\n--- AGGIUNGI NUOVO ACCOUNT (VoIP) ---")
    phone = input("Inserisci numero di telefono (es: +447584547674): ").strip().replace(" ", "")
    session_path = os.path.join(SESSIONS_DIR, phone)
    
    if phone in CONNECTED_CLIENTS:
        try: await CONNECTED_CLIENTS[phone].disconnect()
        except Exception: pass
        del CONNECTED_CLIENTS[phone]

    p = genera_parametri_client()
    client = TelegramClient(
        session_path, api_id, api_hash,
        device_model=p["device_model"],
        system_version=p["system_version"],
        app_version=p["app_version"]
    )
    
    try:
        await client.connect()
        await client.start(
            phone=lambda: phone,
            code_callback=lambda: input(f"📩 Inserisci il codice OTP inviato a {phone}: ").strip(),
            password=lambda: input("🔒 Inserisci la password della 2FA (invio se vuota): ").strip()
        )
        print(f"🎉 Account {phone} collegato con successo come {p['device_model']}!")
        CONNECTED_CLIENTS[phone] = client
    except Exception as e:
        print(f"❌ Errore durante l'autenticazione: {e}")
        try: await client.disconnect()
        except Exception: pass
        if os.path.exists(session_path + ".session"):
            os.remove(session_path + ".session")

async def sync_all_sessions(api_id, api_hash):
    global CONNECTED_CLIENTS
    if not os.path.exists(SESSIONS_DIR):
        return 0
    files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
    current_phones = [f.replace(".session", "") for f in files]
    
    for cached_phone in list(CONNECTED_CLIENTS.keys()):
        if cached_phone not in current_phones:
            try: await CONNECTED_CLIENTS[cached_phone].disconnect()
            except Exception: pass
            del CONNECTED_CLIENTS[cached_phone]

    print(f"🔄 Sincronizzazione di {len(files)} sessioni...")
    for file in files:
        phone = file.replace(".session", "")
        if phone in CONNECTED_CLIENTS:
            continue
        session_path = os.path.join(SESSIONS_DIR, phone)
        try:
            p = genera_parametri_client()
            client = TelegramClient(
                session_path, api_id, api_hash,
                device_model=p["device_model"],
                system_version=p["system_version"],
                app_version=p["app_version"]
            )
            await client.connect()
            if await client.is_user_authorized():
                CONNECTED_CLIENTS[phone] = client
                print(f"✅ Sessione {phone} attiva ({p['device_model']}).")
            else:
                await client.disconnect()
        except Exception as e:
            pass

def seleziona_profilo_velocita():
    print("\n--- SELEZIONE VELOCITÀ CAMPAGNA ---")
    print("1. ULTRA RAPIDO (Pausa singola: 2-5s  | Ogni 3 succ: Pausa 10s)")
    print("2. NORMALE      (Pausa singola: 10-25s | Ogni 3 succ: Pausa 30s)")
    print("3. SICURO       (Pausa singola: 30-60s | Ogni 3 succ: Pausa 90s)")
    
    scelta = input("Scegli la velocità (1-3): ").strip()
    if scelta == "1":
        return {"min_p": 2, "max_p": 5, "ciclo_p": 10}
    elif scelta == "2":
        return {"min_p": 10, "max_p": 25, "ciclo_p": 30}
    else:
        return {"min_p": 30, "max_p": 60, "ciclo_p": 90}

def disegna_dashboard_live(titolo):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔" + "═"*93 + "╗")
    print(f"║ 📊 DASHBOARD LIVE TOXICRASP - {titolo:<45} ║")
    print("╠" + "═"*93 + "╣")
    print(f"║ 🔥 TOTAL SUCCESS: {GLOBAL_SUCCESS:<10} | ❌ TOTAL FAILED: {GLOBAL_FAILED:<48} ║")
    print("╠" + "═"*93 + "╣")
    for phone, s in ACCOUNT_STATS.items():
        stato_pulito = str(s['status'])[:35]
        target_pulito = f"@{s['current']}"[:20]
        print(f"║ ► [{phone}] Succ: {s['succ']:<3} | Fall: {s['fall']:<3} | Target: {target_pulito:<20} | {stato_pulito:<32} ║")
    print("╚" + "═"*93 + "╝")

async def worker_aggiunta_parallela(phone, client, mia_lista, target_chat_id, tetto_massimo, profilo):
    global GLOBAL_SUCCESS, GLOBAL_FAILED
    aggiunte_effettuate = 0
    successi_locali_ciclo = 0
    
    for username_corrente in mia_lista:
        if aggiunte_effettuate >= tetto_massimo:
            break
            
        ACCOUNT_STATS[phone]["current"] = username_corrente
        ACCOUNT_STATS[phone]["status"] = "Risoluzione utente..."
        disegna_dashboard_live("AGGIUNTA DIRETTA")
        
        try:
            try:
                input_user = await client.get_input_entity(username_corrente)
            except (UsernameInvalidError, UserIdInvalidError, ValueError):
                ACCOUNT_STATS[phone]["fall"] += 1
                GLOBAL_FAILED += 1
                ACCOUNT_STATS[phone]["status"] = "❌ Username Non Valido"
                salva_elaborato(username_corrente)
                await asyncio.sleep(1)
                continue

            ACCOUNT_STATS[phone]["status"] = "Invio invito..."
            disegna_dashboard_live("AGGIUNTA DIRETTA")
            
            await client(InviteToChannelRequest(target_chat_id, [input_user]))
            
            ACCOUNT_STATS[phone]["succ"] += 1
            GLOBAL_SUCCESS += 1
            aggiunte_effettuate += 1
            successi_locali_ciclo += 1
            salva_elaborato(username_corrente)
            
            if successi_locali_ciclo >= 3:
                ACCOUNT_STATS[phone]["status"] = f"⏸️ Pausa ciclo ({profilo['ciclo_p']}s)"
                disegna_dashboard_live("AGGIUNTA DIRETTA")
                await asyncio.sleep(profilo["ciclo_p"])
                successi_locali_ciclo = 0
            else:
                pausa = random.randint(profilo["min_p"], profilo["max_p"])
                ACCOUNT_STATS[phone]["status"] = f"⏳ Attesa ({pausa}s)"
                disegna_dashboard_live("AGGIUNTA DIRETTA")
                await asyncio.sleep(pausa)
                
        except FloodWaitError as e:
            ACCOUNT_STATS[phone]["status"] = f"⚠️ FloodWait ({e.seconds}s)"
            disegna_dashboard_live("AGGIUNTA DIRETTA")
            await asyncio.sleep(e.seconds)
        except UserPrivacyRestrictedError:
            ACCOUNT_STATS[phone]["fall"] += 1
            GLOBAL_FAILED += 1
            ACCOUNT_STATS[phone]["status"] = "❌ Privacy Chiusa"
            salva_elaborato(username_corrente)
            await asyncio.sleep(1)
        except UserAlreadyParticipantError:
            ACCOUNT_STATS[phone]["status"] = "ℹ️ Già presente"
            salva_elaborato(username_corrente)
            await asyncio.sleep(1)
        except Exception as e:
            ACCOUNT_STATS[phone]["fall"] += 1
            GLOBAL_FAILED += 1
            err = str(e).lower()
            if "privacy" in err or "mutual" in err:
                ACCOUNT_STATS[phone]["status"] = "❌ Privacy/Contatti Mutui"
            elif "too many" in err or "limit" in err:
                ACCOUNT_STATS[phone]["status"] = "⚠️ Limite. Pausa 30m"
                await asyncio.sleep(1800)
            else:
                ACCOUNT_STATS[phone]["status"] = "❌ Errore Generico"
            salva_elaborato(username_corrente)
            await asyncio.sleep(1)
            
    ACCOUNT_STATS[phone]["status"] = "🏁 Completato"
    ACCOUNT_STATS[phone]["current"] = "Nessuno"
    disegna_dashboard_live("AGGIUNTA DIRETTA")

async def start_direct_add_campaign():
    global GLOBAL_SUCCESS, GLOBAL_FAILED, CONNECTED_CLIENTS, ACCOUNT_STATS
    if not CONNECTED_CLIENTS:
        print("❌ Nessun account operativo caricato!")
        return

    print("\n--- AVVIO OPERAZIONE PARALLELA (AGGIUNTA DIRETTA) ---")
    txt_file = input("File .txt membri (es: utenti.txt): ").strip()
    if not os.path.exists(txt_file):
        print("❌ File non trovato.")
        return

    try: target_chat_id = int(input("ID numerico gruppo target: ").strip())
    except ValueError: return

    try: tetto_massimo = int(input("Limite massimo aggiunte per account: ").strip())
    except ValueError: tetto_massimo = 15

    profilo = seleziona_profilo_velocita()
    phones_list = list(CONNECTED_CLIENTS.keys())
    
    elaborati = carica_elaborati()
    utenti_validi = []

    with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            match = re.search(r'@?([a-zA-Z0-9_]{5,32})$', line) or re.search(r'@([a-zA-Z0-9_]{5,32})', line)
            if match:
                username = match.group(1).lower()
                if not username.isdigit() and username not in ... and username not in elaborati:
                    utenti_validi.append(username)

    if not utenti_validi:
        print("❌ Nessun utente testuale valido trovato da elaborare.")
        return

    liste_suddivise = {phone: [] for phone in phones_list}
    for i, user in enumerate(utenti_validi):
        phone_assegnato = phones_list[i % len(phones_list)]
        liste_suddivise[phone_assegnato].append(user)

    ACCOUNT_STATS = {phone: {"succ": 0, "fall": 0, "current": "Pronto", "status": "Inizializzazione..."} for phone in phones_list}
    GLOBAL_SUCCESS = 0
    GLOBAL_FAILED = 0
    
    print(f"🚀 [Pronti] {len(utenti_validi)} utenti divisi su {len(phones_list)} account.")
    input("Premi INVIO per lanciare la dashboard live...")

    tasks = []
    for phone in phones_list:
        tasks.append(worker_aggiunta_parallela(phone, CONNECTED_CLIENTS[phone], liste_suddivise[phone], target_chat_id, tetto_massimo, profilo))

    await asyncio.gather(*tasks)
    print("\n🏁 Campagna Parallela Terminata!")
    input("\nPremi INVIO per tornare al menu...")

async def worker_pm_parallelo(phone, client, mia_lista, lista_messaggi, invite_link, tetto_massimo, profilo):
    global GLOBAL_SUCCESS, GLOBAL_FAILED
    inviati = 0
    successi_locali_ciclo = 0
    
    for username in mia_lista:
        if inviati >= tetto_massimo:
            break

        ACCOUNT_STATS[phone]["current"] = username
        ACCOUNT_STATS[phone]["status"] = "Invio messaggio privato..."
        disegna_dashboard_live("MESSAGGI PRIVATI")

        try:
            messaggio_base = random.choice(lista_messaggi)
            messaggio_formattato = messaggio_base.replace("{link}", invite_link)
            
            await client.send_message(username, messaggio_formattato)
            
            ACCOUNT_STATS[phone]["succ"] += 1
            GLOBAL_SUCCESS += 1
            inviati += 1
            successi_locali_ciclo += 1
            salva_elaborato(username)

            if successi_locali_ciclo >= 3:
                ACCOUNT_STATS[phone]["status"] = f"⏸️ Pausa ciclo ({profilo['ciclo_p']}s)"
                disegna_dashboard_live("MESSAGGI PRIVATI")
                await asyncio.sleep(profilo['ciclo_p'])
                successi_locali_ciclo = 0
            else:
                pausa = random.randint(profilo['min_p'], profilo['max_p'])
                ACCOUNT_STATS[phone]["status"] = f"⏳ Attesa ({pausa}s)"
                disegna_dashboard_live("MESSAGGI PRIVATI")
                await asyncio.sleep(pausa)

        except FloodWaitError as e:
            ACCOUNT_STATS[phone]["status"] = f"⚠️ FloodWait ({e.seconds}s)"
            disegna_dashboard_live("MESSAGGI PRIVATI")
            await asyncio.sleep(e.seconds)
        except PeerFloodError:
            ACCOUNT_STATS[phone]["status"] = "⚠️ PeerFlood! Pausa 1h"
            await asyncio.sleep(3600)
        except Exception as e:
            ACCOUNT_STATS[phone]["fall"] += 1
            GLOBAL_FAILED += 1
            ACCOUNT_STATS[phone]["status"] = "❌ Fallito/Non trovato"
            salva_elaborato(username)
            await asyncio.sleep(1)

    ACCOUNT_STATS[phone]["status"] = "🏁 Completato"
    ACCOUNT_STATS[phone]["current"] = "Nessuno"
    disegna_dashboard_live("MESSAGGI PRIVATI")

async def start_private_message_campaign():
    global GLOBAL_SUCCESS, GLOBAL_FAILED, CONNECTED_CLIENTS, ACCOUNT_STATS
    if not CONNECTED_CLIENTS:
        print("❌ Nessun account operativo caricato!")
        return

    print("\n--- AVVIO OPERAZIONE PARALLELA (MESSAGGI PRIVATI) ---")
    txt_file = input("File .txt dei membri (es: utenti.txt): ").strip()
    if not os.path.exists(txt_file):
        print("❌ File non trovato.")
        return

    invite_link = input("LINK DI INVITO: ").strip()
    try: tetto_massimo = int(input("Limite massimo messaggi per account: ").strip())
    except ValueError: tetto_massimo = 15

    profilo = seleziona_profilo_velocita()
    lista_messaggi = carica_messaggi()
    elaborati = carica_elaborati()
    utenti_validi = []

    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            match = re.search(r'@?([a-zA-Z0-9_]{5,32})$', line) or re.search(r'@([a-zA-Z0-9_]{5,32})', line)
            if match:
                username = match.group(1).lower()
                if not username.isdigit() and username not in elaborati:
                    utenti_validi.append(username)

    if not utenti_validi:
        print("❌ Nessun utente testuale valido trovato.")
        return

    phones_list = list(CONNECTED_CLIENTS.keys())
    liste_suddivise = {phone: [] for phone in phones_list}
    for i, user in enumerate(utenti_validi):
        phone_assegnato = phones_list[i % len(phones_list)]
        liste_suddivise[phone_assegnato].append(user)

    ACCOUNT_STATS = {phone: {"succ": 0, "fall": 0, "current": "Pronto", "status": "Inizializzazione..."} for phone in phones_list}
    GLOBAL_SUCCESS = 0
    GLOBAL_FAILED = 0

    print(f"🚀 [Pronti] {len(utenti_validi)} utenti avviati in parallelo.")
    input("Premi INVIO per lanciare la dashboard live...")

    tasks = []
    for phone in phones_list:
        tasks.append(worker_pm_parallelo(phone, CONNECTED_CLIENTS[phone], liste_suddivise[phone], lista_messaggi, invite_link, tetto_massimo, profilo))

    await asyncio.gather(*tasks)
    print("\n🏁 Campagna PM Parallela Terminata!")
    input("\nPremi INVIO per tornare al menu...")

async def main():
    # Il controllo aggiornamenti ed integrità avviene prima di lanciare il programma
    verifica_aggiornamenti_e_stato()
    
    await mostra_banner_animato()
    api_id, api_hash = carica_o_richiedi_api()
    if not api_id or not api_hash:
        return

    await sync_all_sessions(api_id, api_hash)

    while True:
        print("\n" + "="*45)
        print("=== MENU DI CONTROLLO TOXICRASP PARALLELO ===")
        print(f"[Account Operativi Connessi: {len(CONNECTED_CLIENTS)}]")
        print("="*45)
        print("1. Aggiungi Nuovo Account VoIP (.session)")
        print("2. Sincronizza / Ricarica tutte le sessioni")
        print("3. AVVIA CAMPAGNA SIMULTANEA: AGGIUNTA DIRETTA")
        print("4. AVVIA CAMPAGNA SIMULTANEA: INVIO MESSAGGI PRIVATI")
        print("5. SVUOTA MEMORIA UTENTI ELABORATI (Reset log)")
        print("6. Esci")
        print("="*45)
        
        scelta = input("Seleziona un'opzione (1-6): ").strip()
        if scelta == "1":
            await add_new_account(api_id, api_hash)
        elif scelta == "2":
            await sync_all_sessions(api_id, api_hash)
        elif scelta == "3":
            await start_direct_add_campaign()
        elif scelta == "4":
            await start_private_message_campaign()
        elif scelta == "5":
            resetta_elaborati()
        elif scelta == "6":
            for phone, client in CONNECTED_CLIENTS.items():
                try: await client.disconnect()
                except Exception: pass
            break
        else:
            print("❌ Opzione non valida.")

if __name__ == "__main__":
    asyncio.run(main())

    asyncio.run(main())
