"""
Default light brand kit — clean minimal light theme.

No specific product. Use as a starting point for your own brand,
or to demo kalve without branding.
"""
from ..brand import BrandKit


DEFAULT_LIGHT = BrandKit(
    name="default_light",
    product_name="Your Product",
    product_url="yoursite.com",
    hashtag="yourproduct",

    background_gradient=("#F8F9FA", "#EEF0F2", 180),

    inner_card_fill=(255, 255, 255, 255),
    inner_card_radius=48,
    inner_card_margin=60,

    text_primary=(17, 24, 39),
    text_secondary=(55, 65, 81),
    text_muted=(107, 114, 128),
    text_caption=(156, 163, 175),

    accent=(79, 70, 229),

    tiers={
        "tier1": {
            "pill_bg":   (224, 231, 255),
            "pill_text": (67, 56, 202),
        },
        "tier2": {
            "pill_bg":   (219, 234, 254),
            "pill_text": (29, 78, 216),
        },
        "tier3": {
            "pill_bg":   (254, 226, 226),
            "pill_text": (185, 28, 28),
        },
    },
)
