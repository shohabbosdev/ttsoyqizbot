from environs import Env

env=Env()
env.read_env()

token = env('T_TOKEN')
ttsurl = env('TTS_URL')
api_token = env('API_TOKEN')
