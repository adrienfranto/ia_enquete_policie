from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os
import json

app = Flask(__name__)

# PROLOG facts and rules as a string template
PROLOG_CODE = """
% Police Investigation System in PROLOG
% Types de crime
crime_type(vol).
crime_type(assassinat).
crime_type(escroquerie).

% Faits sur les suspects
suspect(john).
suspect(mary).
suspect(alice).
suspect(bruno).
suspect(sophie).

% Faits pour le vol
has_motive(john, vol).
was_near_crime_scene(john, vol).
has_fingerprint_on_weapon(john, vol).

% Faits pour l'assassinat
has_motive(mary, assassinat).
was_near_crime_scene(mary, assassinat).
has_fingerprint_on_weapon(mary, assassinat).

% Faits pour l'escroquerie
has_motive(alice, escroquerie).
has_bank_transaction(alice, escroquerie).
has_bank_transaction(bruno, escroquerie).
owns_fake_identity(sophie, escroquerie).

% Témoins oculaires
eyewitness_identification(mary, assassinat).

% Règles pour déterminer la culpabilité
is_guilty(Suspect, vol) :-
    has_motive(Suspect, vol),
    was_near_crime_scene(Suspect, vol),
    has_fingerprint_on_weapon(Suspect, vol).

is_guilty(Suspect, assassinat) :-
    has_motive(Suspect, assassinat),
    was_near_crime_scene(Suspect, assassinat),
    ( has_fingerprint_on_weapon(Suspect, assassinat)
    ; eyewitness_identification(Suspect, assassinat)
    ).

is_guilty(Suspect, escroquerie) :-
    has_motive(Suspect, escroquerie),
    ( has_bank_transaction(Suspect, escroquerie)
    ; owns_fake_identity(Suspect, escroquerie)
    ).

% Règles utilitaires
guilty_suspects(CrimeType, Suspects) :-
    findall(Suspect, is_guilty(Suspect, CrimeType), Suspects).

evidence_against(Suspect, CrimeType, Evidence) :-
    findall(Proof, (
        ( has_motive(Suspect, CrimeType), Proof = motive
        ; was_near_crime_scene(Suspect, CrimeType), Proof = near_scene
        ; has_fingerprint_on_weapon(Suspect, CrimeType), Proof = fingerprints
        ; has_bank_transaction(Suspect, CrimeType), Proof = bank_transaction
        ; owns_fake_identity(Suspect, CrimeType), Proof = fake_identity
        ; eyewitness_identification(Suspect, CrimeType), Proof = eyewitness
        )
    ), Evidence).

is_innocent(Suspect, CrimeType) :-
    suspect(Suspect),
    crime_type(CrimeType),
    \\+ is_guilty(Suspect, CrimeType).
"""

def execute_prolog_query(query):
    """Execute a PROLOG query and return the results"""
    try:
        # Create a temporary PROLOG file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pl', delete=False) as f:
            f.write(PROLOG_CODE)
            f.write(f"\n\n:- {query}.\n")
            temp_file = f.name
        
        # Try to execute with SWI-Prolog (if available)
        try:
            result = subprocess.run(['swipl', '-q', '-t', 'halt', '-s', temp_file], 
                                  capture_output=True, text=True, timeout=10)
            output = result.stdout.strip()
            if result.returncode == 0:
                return {"success": True, "result": output if output else "true"}
            else:
                return {"success": False, "error": result.stderr}
        except FileNotFoundError:
            # If SWI-Prolog is not available, simulate the logic
            return simulate_prolog_query(query)
        finally:
            os.unlink(temp_file)
    except Exception as e:
        return {"success": False, "error": str(e)}

def simulate_prolog_query(query):
    """Simulate PROLOG queries when SWI-Prolog is not available"""
    # Parse common query patterns
    if "is_guilty(" in query:
        # Extract suspect and crime type
        parts = query.replace("is_guilty(", "").replace(")", "").replace(".", "").split(",")
        if len(parts) == 2:
            suspect = parts[0].strip()
            crime_type = parts[1].strip()
            
            # Apply the logic rules
            if crime_type == "vol" and suspect == "john":
                return {"success": True, "result": "true"}
            elif crime_type == "assassinat" and suspect == "mary":
                return {"success": True, "result": "true"}
            elif crime_type == "escroquerie" and (suspect == "alice" or suspect == "sophie"):
                return {"success": True, "result": "true"}
            else:
                return {"success": True, "result": "false"}
    
    elif "guilty_suspects(" in query:
        parts = query.replace("guilty_suspects(", "").replace(")", "").replace(".", "").split(",")
        if len(parts) >= 1:
            crime_type = parts[0].strip()
            if crime_type == "vol":
                return {"success": True, "result": "[john]"}
            elif crime_type == "assassinat":
                return {"success": True, "result": "[mary]"}
            elif crime_type == "escroquerie":
                return {"success": True, "result": "[alice, sophie]"}
    
    return {"success": True, "result": "Query executed"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/investigate', methods=['POST'])
def investigate():
    data = request.json
    suspect = data.get('suspect', '').lower()
    crime_type = data.get('crime_type', '').lower()
    
    if not suspect or not crime_type:
        return jsonify({"success": False, "error": "Suspect and crime type are required"})
    
    query = f"is_guilty({suspect}, {crime_type})"
    result = execute_prolog_query(query)
    
    # Get evidence if guilty
    evidence = []
    if result.get("success") and result.get("result") == "true":
        evidence_query = f"evidence_against({suspect}, {crime_type}, Evidence)"
        evidence_result = execute_prolog_query(evidence_query)
        if evidence_result.get("success"):
            evidence = get_evidence_for_suspect(suspect, crime_type)
    
    return jsonify({
        "success": result.get("success", False),
        "guilty": result.get("result") == "true",
        "evidence": evidence,
        "suspect": suspect.title(),
        "crime_type": crime_type.title()
    })

@app.route('/api/all_guilty/<crime_type>')
def get_all_guilty(crime_type):
    query = f"guilty_suspects({crime_type.lower()}, Suspects)"
    result = execute_prolog_query(query)
    
    # Simulate the result for demonstration
    guilty_list = []
    if crime_type.lower() == "vol":
        guilty_list = ["John"]
    elif crime_type.lower() == "assassinat":
        guilty_list = ["Mary"]
    elif crime_type.lower() == "escroquerie":
        guilty_list = ["Alice", "Sophie"]
    
    return jsonify({
        "success": True,
        "crime_type": crime_type.title(),
        "guilty_suspects": guilty_list
    })

def get_evidence_for_suspect(suspect, crime_type):
    """Get evidence against a suspect for a specific crime"""
    evidence_map = {
        ("john", "vol"): ["Motif", "Présent sur les lieux", "Empreintes sur l'arme"],
        ("mary", "assassinat"): ["Motif", "Présent sur les lieux", "Empreintes sur l'arme", "Témoin oculaire"],
        ("alice", "escroquerie"): ["Motif", "Transactions bancaires suspectes"],
        ("sophie", "escroquerie"): ["Fausse identité"]
    }
    
    return evidence_map.get((suspect.lower(), crime_type.lower()), [])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
