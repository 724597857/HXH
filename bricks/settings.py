# 游戏全局配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
FONT_NAME = None  

# 玩家属性
LIVES = 3
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_COLOR = (200, 200, 200)

# 球属性
BALL_RADIUS = 10
BALL_COLOR = (255, 0, 0)
BALL_BASE_SPEED = 5

# 砖块属性
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_GAP = 5

# 道具系统
POWERUP_COLORS = {
    "expand": (0, 255, 0),
    "speed": (255, 165, 0),
    "shrink": (255, 0, 0),    # 红色-缩短
    "slow": (0, 0, 255),      # 蓝色-减速
    "life": (255, 192, 203)  # 粉色-生命道具
}
POWERUP_CHANCE = 0.3

# 关卡设计（5个关卡）
LEVELS = [
    {  # Level 1
        "layout": [
            "RRRRRRRR",
            "GGGGGGGG",
            "BBBBBBBB"
        ],
        "speed_multiplier": 1.0
    },
    {  # Level 2
        "layout": [
            "RGBRGBRG",
            "BRGBRGBR",
            "GRGBRGBR"
        ],
        "speed_multiplier": 1.2
    },
    {  # Level 3
        "layout": [
            "RBRBRBRB",
            "GRGRGRGR",
            "BRBRBRBR"
        ],
        "speed_multiplier": 1.4
    },
    {  # Level 4
        "layout": [
            "RRRRRRR",
            "R  R  R",
            "RRRRRRR"
        ],
        "speed_multiplier": 1.6
    },
    {  # Level 5
        "layout": [
            "RGBBRG",
            "BGRRGB",
            "RGGBBR"
        ],
        "speed_multiplier": 1.8
    }
]

COLOR_MAP = {
    "R": (255, 0, 0),
    "G": (0, 255, 0),
    "B": (0, 0, 255),
    " ": None  # 空砖块（用于特殊形状）
}