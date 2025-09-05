# config.py - Configuration management
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class AssistantConfig:
    """Configuration for the Voice Assistant"""
    
    # LLM Configuration
    model_name: str = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    provider: str = os.getenv("LLM_PROVIDER", "groq")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))
    
    # Speech Recognition Configuration
    max_record_seconds: int = int(os.getenv("MAX_RECORD_SECONDS", "10"))
    energy_threshold: int = int(os.getenv("ENERGY_THRESHOLD", "300"))
    pause_threshold: float = float(os.getenv("PAUSE_THRESHOLD", "0.8"))
    dynamic_energy: bool = os.getenv("DYNAMIC_ENERGY", "true").lower() == "true"
    
    # Text-to-Speech Configuration
    tts_rate: int = int(os.getenv("TTS_RATE", "180"))
    tts_volume: float = float(os.getenv("TTS_VOLUME", "0.9"))
    tts_voice: Optional[str] = os.getenv("TTS_VOICE", None)
    
    # Session Configuration
    history_max_turns: int = int(os.getenv("HISTORY_MAX_TURNS", "10"))
    session_timeout_minutes: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
    max_concurrent_sessions: int = int(os.getenv("MAX_CONCURRENT_SESSIONS", "10"))
    
    # Audio Device Configuration
    audio_device: str = os.getenv("AUDIO_DEVICE", "auto")
    sample_rate: int = int(os.getenv("SAMPLE_RATE", "16000"))
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_reload: bool = os.getenv("API_RELOAD", "true").lower() == "true"
    cors_origins: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: Optional[str] = os.getenv("LOG_FILE", None)
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is required but not set")
        
        if self.max_record_seconds <= 0:
            raise ValueError("MAX_RECORD_SECONDS must be positive")
        
        if not 0 <= self.tts_volume <= 1:
            raise ValueError("TTS_VOLUME must be between 0 and 1")
        
        if self.tts_rate <= 0:
            raise ValueError("TTS_RATE must be positive")
    
    @classmethod
    def from_env_file(cls, env_file: str = ".env"):
        """Load configuration from a specific .env file"""
        from dotenv import load_dotenv
        load_dotenv(env_file, override=True)
        return cls()
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }
    
    def get_llm_config(self) -> dict:
        """Get LLM-specific configuration"""
        return {
            "model_name": self.model_name,
            "provider": self.provider,
            "api_key": self.groq_api_key,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def get_stt_config(self) -> dict:
        """Get STT-specific configuration"""
        return {
            "max_record_seconds": self.max_record_seconds,
            "energy_threshold": self.energy_threshold,
            "pause_threshold": self.pause_threshold,
            "dynamic_energy": self.dynamic_energy,
            "audio_device": self.audio_device,
            "sample_rate": self.sample_rate
        }
    
    def get_tts_config(self) -> dict:
        """Get TTS-specific configuration"""
        return {
            "rate": self.tts_rate,
            "volume": self.tts_volume,
            "voice": self.tts_voice
        }

# Global configuration instance
config = AssistantConfig()