import streamlit as st
import speech_recognition as sr
import os

# Fonction de transcription avec gestion des API et langues
def transcribe_speech(api_choice, language):
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        with st.spinner("Écoute en cours..."):
            audio_text = r.listen(source)
        
        st.info("Transcription en cours...")
        try:
            if api_choice == "Google":
                text = r.recognize_google(audio_text, language=language)
            elif api_choice == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language)
            else:
                return "API non prise en charge."
            return text
        except sr.UnknownValueError:
            return "Désolé, je n'ai pas compris votre discours."
        except sr.RequestError as e:
            return f"Erreur avec l'API sélectionnée : {e}"
        except Exception as e:
            return f"Une erreur inattendue s'est produite : {e}"

# Fonction pour enregistrer la transcription dans un fichier
def save_transcription(text):
    file_name = st.text_input("Entrez le nom du fichier (sans extension) :", "transcription")
    if st.button("Enregistrer"):
        if not file_name.strip():
            st.error("Le nom du fichier ne peut pas être vide.")
            return
        try:
            with open(f"{file_name.strip()}.txt", "w") as file:
                file.write(text)
            st.success(f"Transcription enregistrée sous le nom {file_name.strip()}.txt")
        except Exception as e:
            st.error(f"Erreur lors de l'enregistrement : {e}")

# Fonction principale
def main():
    st.title("Application de Reconnaissance Vocale")
    
    # Sélection de l'API
    st.sidebar.header("Paramètres")
    api_choice = st.sidebar.selectbox(
        "Sélectionnez l'API de reconnaissance vocale :",
        ("Google", "Sphinx")
    )
    
    # Sélection de la langue
    language = st.sidebar.selectbox(
        "Sélectionnez la langue :",
        ["fr-FR", "en-US", "es-ES", "de-DE"],
        format_func=lambda lang: {
            "fr-FR": "Français",
            "en-US": "Anglais",
            "es-ES": "Espagnol",
            "de-DE": "Allemand"
        }[lang]
    )
    
    # Pause et reprise
    st.sidebar.write("**Pause/Reprise :** Utilisez les options ci-dessous pour gérer l'écoute.")
    pause_recognition = st.sidebar.checkbox("Mettre en pause l'écoute")
    if pause_recognition:
        st.warning("L'écoute est actuellement en pause.")
    else:
        st.info("L'écoute est active.")
    
    # Bouton pour lancer la reconnaissance vocale
    if st.button("Commencer l'enregistrement"):
        if not pause_recognition:
            text = transcribe_speech(api_choice, language)
            if text:
                st.write("Transcription :", text)
                save_transcription(text)
        else:
            st.warning("Veuillez désactiver la pause pour commencer l'enregistrement.")

if __name__ == "__main__":
    main()
