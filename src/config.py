WHISPER_CONFIG = {
    'models': {
        'default': 'small',
        'available': [
            # "tiny",
            # "base",
            "small",
            # "medium",
            # "large"
        ]
    },
    'paths': {
        'input': '../input',
        'output': '../output'
    },
    'timestamps': {
        'include': True,
        'format': 'full'
    },
    'output_format': 'html',  # 'txt' or 'html'
    'language': 'ja'
}