"""
Default dark brand kit — developer-native dark theme.

No specific product. Use as a starting point for your own brand,
or to demo kalve without branding.
"""
from ..brand import BrandKit


DEFAULT_DARK = BrandKit(
    name="default_dark",
    product_name="Your Product",
    product_url="yoursite.com",
    hashtag="yourproduct",

    background_gradient=("#0F0F1A", "#1A1A2E", 180),

    inner_card_fill=(22, 22, 35, 255),
    inner_card_radius=48,
    inner_card_margin=60,

    text_primary=(240, 240, 245),
    text_secondary=(180, 180, 195),
    text_muted=(120, 120, 140),
    text_caption=(80, 80, 100),

    accent=(129, 140, 248),

    tiers={
        "tier1": {
            "pill_bg":   (49, 46, 129),
            "pill_text": (165, 180, 252),
        },
        "tier2": {
            "pill_bg":   (30, 58, 138),
            "pill_text": (147, 197, 253),
        },
        "tier3": {
            "pill_bg":   (127, 29, 29),
            "pill_text": (252, 165, 165),
        },
    },
)
