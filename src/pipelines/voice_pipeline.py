from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    # FIXED: Add validation for empty/short audio
    if audio_bytes is None:
        st.error('No audio data provided')
        return None
    
    if len(audio_bytes) < 4000:  # Less than ~0.25 seconds at 16kHz
        st.warning('Audio is too short. Please record a longer phrase.')
        return None
    
    try:
        encoder = load_voice_encoder()
        
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        
        # FIXED: Check if audio has content
        if len(audio) == 0:
            st.error('No audio content detected')
            return None
        
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f'Voice recognition error: {str(e)}')  # FIXED: Better error message
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    # FIXED: Add validation for inputs
    if new_embedding is None:
        return None, 0.0
    
    if not candidates_dict:
        return None, 0.0
    
    best_sid = None
    best_score = -1.0
    
    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding is not None:  # FIXED: Check for None
            # FIXED: Ensure both are numpy arrays for dot product
            new_emb = np.array(new_embedding) if not isinstance(new_embedding, np.ndarray) else new_embedding
            stored_emb = np.array(stored_embedding) if not isinstance(stored_embedding, np.ndarray) else stored_embedding
            
            similarity = np.dot(new_emb, stored_emb)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid
    
    if best_score >= threshold:
        return best_sid, best_score
    
    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    # FIXED: Add validation
    if audio_bytes is None:
        st.error('No audio data provided')
        return {}
    
    if len(audio_bytes) < 8000:  # Less than ~0.5 seconds
        st.warning('Audio is too short for processing')
        return {}
    
    if not candidates_dict:
        st.warning('No voice profiles available for matching')
        return {}
    
    try:
        encoder = load_voice_encoder()
        
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        
        # FIXED: Check if audio has content
        if len(audio) == 0:
            st.error('No audio content detected')
            return {}
        
        # FIXED: Make top_db configurable but keep default
        segments = librosa.effects.split(audio, top_db=30)
        
        identified_results = {}
        
        for start, end in segments:
            # FIXED: Minimum segment length check (0.5 seconds)
            if (end - start) < sr * 0.5:
                continue
            
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)
            
            sid, score = identify_speaker(embedding, candidates_dict, threshold)
            
            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score
        
        return identified_results
    except Exception as e:
        st.error(f'Bulk audio processing error: {str(e)}')  # FIXED: Better error message
        return {}