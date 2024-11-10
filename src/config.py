WHISPER_CONFIG = {
    'models': {
        'default': 'small',
        'available': [
            # "tiny",
            # "base",
            "small",
            # "medium",
            # "large",
            # "large-v2",
            # "large-v3",
            # "turbo",
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
    'language': 'ja',
    'device': 'cpu',
    'compute_type': 'int8'
}