import streamlit as st
import pyttsx3
import tempfile
import os
import base64
from gtts import gTTS
import pygame
from io import BytesIO
import time
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Advanced TTS Converter",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .voice-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class AdvancedTTS:
    """
    A class to handle both pyttsx3 (offline) and gTTS (online) engines.
    """
    def __init__(self):
        self.pyttsx3_engine = None
        self.available_voices = []
        self.setup_pyttsx3()
        st.audio.init()

    def setup_pyttsx3(self):
        """Initialize pyttsx3 engine and get available voices."""
        try:
            self.pyttsx3_engine = pyttsx3.init()
            voices = self.pyttsx3_engine.getProperty('voices')
            for i, voice in enumerate(voices):
                voice_info = {
                    'id': voice.id,
                    'name': voice.name,
                    'gender': 'Female' if 'female' in voice.name.lower() or 'zira' in voice.name.lower() else 'Male',
                    'index': i
                }
                self.available_voices.append(voice_info)
        except Exception as e:
            # Silently fail if no engine is found, will be handled in the UI
            self.pyttsx3_engine = None

    def get_gtts_languages(self):
        """Get a dictionary of available languages for Google TTS."""
        return {
            'English (US)': 'en', 'English (UK)': 'co.uk', 'English (Australia)': 'com.au',
            'English (India)': 'co.in', 'Spanish (Spain)': 'es', 'Spanish (Mexico)': 'com.mx',
            'French (France)': 'fr', 'French (Canada)': 'ca', 'German': 'de', 'Italian': 'it',
            'Portuguese (Brazil)': 'com.br', 'Portuguese (Portugal)': 'pt', 'Russian': 'ru',
            'Japanese': 'ja', 'Korean': 'ko', 'Chinese (Mandarin)': 'zh-cn', 'Arabic': 'ar',
            'Hindi': 'hi', 'Dutch': 'nl', 'Swedish': 'sv', 'Norwegian': 'no', 'Danish': 'da',
            'Finnish': 'fi', 'Polish': 'pl', 'Turkish': 'tr'
        }

    def text_to_speech_pyttsx3(self, text, voice_index, rate, volume):
        """Convert text to speech using pyttsx3 and return audio data."""
        try:
            if not self.pyttsx3_engine:
                return None, "pyttsx3 engine not available. Please ensure it's installed and configured on your system."

            voices = self.pyttsx3_engine.getProperty('voices')
            if voice_index < len(voices):
                self.pyttsx3_engine.setProperty('voice', voices[voice_index].id)

            self.pyttsx3_engine.setProperty('rate', rate)
            self.pyttsx3_engine.setProperty('volume', volume)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                temp_filename = tmp_file.name

            self.pyttsx3_engine.save_to_file(text, temp_filename)
            self.pyttsx3_engine.runAndWait()

            with open(temp_filename, 'rb') as f:
                audio_data = f.read()
            os.unlink(temp_filename)
            return audio_data, "Success"
        except Exception as e:
            return None, f"Error with pyttsx3: {str(e)}"

    def text_to_speech_gtts(self, text, tld, slow=False):
        """Convert text to speech using Google TTS and return audio data."""
        try:
            tts = gTTS(text=text, tld=tld, lang='en' if 'co' in tld or 'com' in tld else tld, slow=slow)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.getvalue(), "Success"
        except Exception as e:
            return None, f"Error with Google TTS: {str(e)}. Check your internet connection."

# --- Streamlit UI ---

@st.cache_resource
def get_tts_engine():
    """Cached function to initialize the TTS engine once."""
    return AdvancedTTS()

def create_download_link(audio_data, filename):
    """Create a base64-encoded download link for the audio file."""
    b64 = base64.b64encode(audio_data).decode()
    href = f'<a href="data:audio/wav;base64,{b64}" download="{filename}" style="text-decoration: none; color: #667eea; font-weight: bold;">📥 Download Audio File</a>'
    return href

def main():
    """Main function to run the Streamlit app."""
    st.markdown('<h1 class="main-header">🎤 Advanced Text-to-Speech Converter</h1><h3 class="main-header" >AyushVerma@2025 | Project14</h3>', unsafe_allow_html=True)

    tts_engine = get_tts_engine()

    # --- Sidebar ---
    with st.sidebar:
        social_button_html = """
        <div style="margin-bottom: 20px;">
            <div class="social-button-wrapper">
                <div class="social-button-main">
                    <button class="main-button">
                        <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                        </svg>
                        Ayush's Socials
                    </button>
                </div>
                <div class="social-links">
                    <a href="https://www.linkedin.com/in/ayush-verma-a076a7360/" target="_blank" class="social-link" title="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
                    <a href="https://github.com/Ayush2426" target="_blank" class="social-link" title="GitHub"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg></a>
                    <a href="https://ayushhh-portfolio-2025-oalo.vercel.app/" target="_blank" class="social-link" title="Portfolio"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-3.086-3.086a2 2 0 00-2.828 0L6 21"/></svg></a>
                    <a href="mailto:ayushhhverma07@gmail.com" target="_blank" class="social-link" title="Email"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>
                </div>
            </div>
        </div>
        </br>
        <style>
                .infoCarrier{
            width: 100%;
            display: flex;
            justify-content: center;
            align-item: center;
            font-family: "Poppins", sans-serif;
            font-size: .8rem;
            color: rgb(145, 0, 212);
            margin: 5px;
        }
            .social-button-wrapper { position: relative; width: 100%; height: 40px; }
            .social-button-main { position: relative; z-index: 2; transition: opacity 0.2s ease; }
            .main-button { width: 100%; height: 40px; padding: 8px 16px; display: flex; align-items: center; justify-content: center; gap: 8px; background: rgba(31, 41, 55, 0.5); color: white; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; backdrop-filter: blur(12px); transition: all 0.2s ease; cursor: pointer; font-size: 14px; font-weight: 500; font-family: inherit; }
            .main-button:hover { background: rgba(55, 65, 81, 0.7); }
            .link-icon { width: 16px; height: 16px; }
            .social-links { position: absolute; top: 0; left: 0; height: 40px; display: flex; overflow: hidden; border-radius: 8px; width: 48px; transition: width 0.4s cubic-bezier(0.23, 1, 0.32, 1); z-index: 1; }
            .social-link { height: 40px; width: 48px; min-width: 48px; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.3); color: white; border-right: 1px solid rgba(255, 255, 255, 0.1); text-decoration: none; transition: all 0.3s ease; opacity: 0; transform: translateX(-20px); }
            .social-link:last-child { border-right: none; }
            .social-link:hover { background: rgba(0, 0, 0, 0.5); }
            .social-link svg { width: 20px; height: 20px; }
            .social-button-wrapper:hover .social-button-main { opacity: 0; pointer-events: none; }
            .social-button-wrapper:hover .social-links { width: 192px; }
            .social-button-wrapper:hover .social-link { opacity: 1; transform: translateX(0); }
            .social-button-wrapper:hover .social-link:nth-child(1) { transition-delay: 0ms; }
            .social-button-wrapper:hover .social-link:nth-child(2) { transition-delay: 70ms; }
            .social-button-wrapper:hover .social-link:nth-child(3) { transition-delay: 140ms; }
            .social-button-wrapper:hover .social-link:nth-child(4) { transition-delay: 210ms; }
        </style>
        """
        components.html(social_button_html, height=60)

        st.markdown("## ⚙️ Settings")
        engine_choice = st.selectbox("🔧 Select TTS Engine:", ["Google TTS (Online)", "pyttsx3 (Offline)"])
        st.markdown("---")

        if engine_choice == "pyttsx3 (Offline)":
            st.markdown("### 🎭 Voice Settings")
            if tts_engine.available_voices:
                voice_options = [f"{v['name']} ({v['gender']})" for v in tts_engine.available_voices]
                selected_voice = st.selectbox("🎙️ Select Voice:", voice_options)
                voice_index = voice_options.index(selected_voice)
                rate = st.slider("🏃 Speech Rate (words/min):", 50, 400, 200, 10)
                volume = st.slider("🔊 Volume:", 0.0, 1.0, 0.9, 0.1)
            else:
                st.error("pyttsx3 engine not found or no voices available.")
                voice_index, rate, volume = 0, 200, 0.9 # Default values
        else:
            st.markdown("### 🌍 Language & Accent")
            languages = tts_engine.get_gtts_languages()
            selected_lang_name = st.selectbox("🗣️ Select Language/Accent:", list(languages.keys()))
            selected_tld = languages[selected_lang_name]
            slow_speech = st.checkbox("🐌 Slow Speech", value=False)

    # --- Main Content Area ---
    col1, col2 = st.columns([2.5, 1.5])

    with col1:
        st.markdown("## 📝 Text Input")
        input_method = st.radio("Choose input method:", ["Type Text", "Upload Text File"], horizontal=True, label_visibility="collapsed")

        if 'text_input' not in st.session_state:
            st.session_state.text_input = ""

        if input_method == "Type Text":
            st.session_state.text_input = st.text_area("Enter text to convert:", value=st.session_state.text_input, height=150, placeholder="Type your text here...")
        else:
            uploaded_file = st.file_uploader("Upload a .txt or .md file:", type=['txt', 'md'])
            if uploaded_file:
                st.session_state.text_input = str(uploaded_file.read(), "utf-8")
                st.text_area("File content:", value=st.session_state.text_input, height=250, disabled=True)

    with col2:
        st.markdown("## 🎯 Quick Actions")
        sample_texts = {
            "Greeting": "Hello! Welcome to this advanced text-to-speech converter.",
            "Technical": "Artificial intelligence is revolutionizing technology.",
            "Creative": "In a land of myth, and a time of magic, the destiny of a great kingdom rests on the shoulders of a young boy.",
        }
        for name, sample in sample_texts.items():
            if st.button(f"📄 Use '{name}' sample", key=f"sample_{name}", use_container_width=True):
                st.session_state.text_input = sample
                st.rerun()

    if st.session_state.text_input:
        char_count = len(st.session_state.text_input)
        word_count = len(st.session_state.text_input.split())
        st.info(f"📊 Characters: {char_count} | Words: {word_count}")

    # --- Conversion Button ---
    st.markdown("---")
    _, mid_col, _ = st.columns([1, 1, 1])
    with mid_col:
        convert_button = st.button("🎵 Convert to Speech", type="primary", use_container_width=True, disabled=not st.session_state.text_input.strip())

    # --- Conversion Logic and Output ---
    if convert_button:
        with st.spinner("🔄 Converting text to speech..."):
            text_to_convert = st.session_state.text_input.strip()
            if engine_choice == "pyttsx3 (Offline)":
                if not tts_engine.available_voices:
                    st.error("Cannot convert: pyttsx3 voices are not available.")
                else:
                    audio_data, status = tts_engine.text_to_speech_pyttsx3(text_to_convert, voice_index, rate, volume)
                    filename = f"tts_pyttsx3_{int(time.time())}.wav"
            else: # Google TTS
                audio_data, status = tts_engine.text_to_speech_gtts(text_to_convert, selected_tld, slow_speech)
                filename = f"tts_gtts_{int(time.time())}.mp3"

            if 'audio_data' in locals() and audio_data and status == "Success":
                st.markdown('<div class="success-message">✅ Conversion Successful!</div>', unsafe_allow_html=True)
                st.audio(audio_data, format='audio/wav' if 'pyttsx3' in filename else 'audio/mp3')
                st.markdown(create_download_link(audio_data, filename), unsafe_allow_html=True)
                file_size_kb = len(audio_data) / 1024
                st.info(f"📁 File size: {file_size_kb:.1f} KB | Format: {'WAV' if 'pyttsx3' in filename else 'MP3'}")
            elif 'status' in locals():
                st.error(f"❌ Conversion failed: {status}")


    # --- Information Section ---
    st.markdown("---")
    with st.expander("ℹ️ About This Application & Available Voices", expanded=False):
        st.markdown("""
        ### 🚀 Features
        - **Dual TTS Engines**: Choose between **pyttsx3** for fast, offline generation and **Google TTS** for high-quality, online voices.
        - **Voice Variety**: Access system-installed voices (male/female) and numerous languages/accents from Google.
        - **Full Customization**: Adjust speech rate and volume for the perfect output.
        - **Flexible Input**: Type text directly or upload `.txt` and `.md` files.
        - **Downloadable Audio**: Save the generated speech as a `.wav` or `.mp3` file.
        """)
        if engine_choice == "pyttsx3 (Offline)" and tts_engine.available_voices:
            st.markdown("### 🎭 Available System Voices (pyttsx3)")
            for voice in tts_engine.available_voices:
                st.markdown(f"""
                <div class="voice-card">
                    <strong>{voice['name']}</strong><br>
                    <small>Gender: {voice['gender']} | Index: {voice['index']}</small>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
