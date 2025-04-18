import os
import whisper
import logging
from celery import Task
from .celery_app import celery_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get model size from environment variable with fallback to "base"
DEFAULT_MODEL_SIZE = os.environ.get("DEFAULT_MODEL_SIZE", "base")

class WhisperTask(Task):
    _models = {}
    
    def __init__(self):
        super().__init__()
    
    def get_model(self, model_size=None):
        # Force using base model if requested
        model_size = model_size or DEFAULT_MODEL_SIZE
        
        # Only allow base model if specified in environment
        if os.environ.get("WHISPER_MODEL") == "base":
            model_size = "base"
            
        # Load model on first access or reuse existing
        if model_size not in self._models:
            logger.info(f"Loading Whisper model: {model_size}")
            self._models[model_size] = whisper.load_model(model_size)
            logger.info(f"Whisper model {model_size} loaded successfully")
        return self._models[model_size]

@celery_app.task(base=WhisperTask, bind=True, name="transcribe_audio", time_limit=1800)
def transcribe_audio(self, file_path, model_size=None):
    """
    Transcribe an audio file using Whisper.
    
    Args:
        file_path: Path to the audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
                   If WHISPER_MODEL is set to "base" in env, this parameter is ignored
    
    Returns:
        str: Transcription text
    """
    try:
        # Force using base model if configured in environment
        if os.environ.get("WHISPER_MODEL") == "base":
            model_size = "base"
            logger.info("Using base model as configured in environment")
        else:
            # Use provided model_size or default
            model_size = model_size or DEFAULT_MODEL_SIZE
            
        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        logger.info(f"Starting transcription for file: {file_path} with model: {model_size}")
        model = self.get_model(model_size)
        
        # Configure transcription options
        options = {
            "fp16": False,  # Use FP32 for broader hardware compatibility
            "language": None,  # Auto-detect language
            "task": "transcribe"
        }
        
        # Transcribe audio
        logger.info(f"Transcription started for {file_path}")
        result = model.transcribe(file_path, **options)
        logger.info(f"Transcription completed for {file_path}")
        
        # Cleanup audio file
        try:
            os.remove(file_path)
            logger.info(f"Removed audio file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to remove audio file: {e}")
        
        return result["text"]
    
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise Exception(f"Failed to transcribe audio: {str(e)}")