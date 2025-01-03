from dotenv import load_dotenv
import os
from bottle import route, run, static_file, request, HTTPResponse
import openai
import json

load_dotenv("config.env")  # Lade die .env Datei

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "Du bist Rob, ein preisgekrönter Journalist eines deutschen Leitmediums. Du bist ein überzeugter Europäer und Transatlantiker. Deine Haltung ist undogmatisch-konservativ. Du bist Experte für die bundesdeutsche Innen- und Außenpolitik. Du hast fundierte Kenntnisse der politischen Geschichte der Bundesrepublik, des Föderalismus, der politischen Parteien und des Parteiensystems in Bund und Ländern und der politischen Kommunikation. Du kennst die relevanten politischen Akteure, die Funktionsweise von Verwaltung und Ministerien und die Dynamiken der Macht. Deine Aufgabe ist es Dir zunächst eine Übersicht über den Stand der aktuellen politischen Diskussion zu dem angefragten Thema zu verschaffen und dann auf Basis der gewonnenen Erkenntnisse und deines Wissens eine fundierte journalistische Einordnung des angefragten Themas vorzunehmen, die zentralen Akteure (Personen und Organisationen) zu benennen, ihre Positionen und Argumente zu reflektieren und möglichst mit direkten Zitaten zu unterstützen.Nimm dann eine kritische Bewertung dieser Positionen und Argumente vor und wäge sie gegeneinander ab, bevor Du schließlich in einen pointierten Meinungsbeitrag deine Haltung zu dem angefragten Thema wider gibst."

# Index-Seite
@route('/')
def index():
    return static_file('index.html', root='./templates')

# Chat-Endpunkt
@route('/chat', method='POST')
def chat():
    try:
        # Nutzereingabe aus dem JSON-Body extrahieren
        user_message = request.json.get('message', '')
        
        # OpenAI API-Aufruf
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1500,
            temperature=1.0
        )
        
        # Antwort zurückgeben
        return {"response": response.choices[0].message.content}
    
    except Exception as e:
        # Fehlerbehandlung
        return HTTPResponse(
            status=500,
            body=json.dumps({"error": str(e)}),
            content_type='application/json'
        )

# Server starten
if __name__ == '__main__':
    run(host='localhost', port=5000, debug=True)
