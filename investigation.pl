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

% Témoins oculaires (pour certains cas)
eyewitness_identification(mary, assassinat).

% Règles pour déterminer la culpabilité

% Règle pour le vol - nécessite motif, présence sur les lieux et preuves physiques
is_guilty(Suspect, vol) :-
    has_motive(Suspect, vol),
    was_near_crime_scene(Suspect, vol),
    has_fingerprint_on_weapon(Suspect, vol).

% Règle pour l'assassinat - nécessite motif, présence et soit empreintes soit témoin
is_guilty(Suspect, assassinat) :-
    has_motive(Suspect, assassinat),
    was_near_crime_scene(Suspect, assassinat),
    ( has_fingerprint_on_weapon(Suspect, assassinat)
    ; eyewitness_identification(Suspect, assassinat)
    ).

% Règle pour l'escroquerie - nécessite soit transactions bancaires soit fausse identité
is_guilty(Suspect, escroquerie) :-
    has_motive(Suspect, escroquerie),
    ( has_bank_transaction(Suspect, escroquerie)
    ; owns_fake_identity(Suspect, escroquerie)
    ).

% Règle pour obtenir tous les suspects coupables d'un type de crime
guilty_suspects(CrimeType, Suspects) :-
    findall(Suspect, is_guilty(Suspect, CrimeType), Suspects).

% Règle pour obtenir toutes les preuves contre un suspect
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

% Règle pour vérifier si un suspect est innocent
is_innocent(Suspect, CrimeType) :-
    suspect(Suspect),
    crime_type(CrimeType),
    \+ is_guilty(Suspect, CrimeType).

% Entrée principale pour test en ligne de commande
main :-
    current_input(Input),
    read(Input, crime(Suspect, CrimeType)),
    (   is_guilty(Suspect, CrimeType) ->
        writeln(guilty)
    ;   writeln(not_guilty)
    ),
    halt.
