"""
Electronic Accessories Chatbot - Streamlit app.
Shows brands, features, price, warranty, colors, ratings and delivery date.
Run:  streamlit run app.py
Note: all product data below is sample data - replace it with your real catalog.
"""
import html
import re
from datetime import date, timedelta

import pandas as pd
import streamlit as st

CURRENCY = "₹"

# ------------------------------------------------------------------ DATA
PRODUCTS = {
    "earbuds": [
        {"brand": "Sony", "model": "WF-C700N", "price": 8990, "rating": 4.5,
         "warranty": "1 year", "colors": ["Black", "White", "Lavender"],
         "features": ["Active noise cancelling", "Up to 15h battery", "IPX4"],
         "delivery_days": 3},
        {"brand": "boAt", "model": "Airdopes 141", "price": 1299, "rating": 4.0,
         "warranty": "1 year", "colors": ["Black", "Blue", "Red"],
         "features": ["42h playback", "ENx noise reduction", "Low-latency mode"],
         "delivery_days": 2},
        {"brand": "Apple", "model": "AirPods (3rd gen)", "price": 17900, "rating": 4.7,
         "warranty": "1 year", "colors": ["White"],
         "features": ["Spatial audio", "MagSafe case", "Sweat resistant"],
         "delivery_days": 4},
    ],
    "headphones": [
        {"brand": "Sony", "model": "WH-CH720N", "price": 9990, "rating": 4.5,
         "warranty": "1 year", "colors": ["Black", "Blue", "White"],
         "features": ["Noise cancelling", "35h battery", "Lightweight"],
         "delivery_days": 3},
        {"brand": "JBL", "model": "Tune 770NC", "price": 7999, "rating": 4.3,
         "warranty": "1 year", "colors": ["Black", "Blue", "White"],
         "features": ["Adaptive noise cancelling", "70h battery", "Multi-point"],
         "delivery_days": 3},
        {"brand": "boAt", "model": "Rockerz 450", "price": 1499, "rating": 4.0,
         "warranty": "1 year", "colors": ["Black", "Red", "Green"],
         "features": ["15h battery", "40mm drivers", "Foldable"],
         "delivery_days": 2},
    ],
    "smartwatch": [
        {"brand": "Apple", "model": "Watch SE", "price": 29900, "rating": 4.7,
         "warranty": "1 year", "colors": ["Midnight", "Starlight", "Silver"],
         "features": ["Heart-rate monitor", "Crash detection", "Water resistant"],
         "delivery_days": 4},
        {"brand": "Samsung", "model": "Galaxy Watch 6", "price": 24999, "rating": 4.4,
         "warranty": "1 year", "colors": ["Graphite", "Silver", "Gold"],
         "features": ["Sleep tracking", "ECG", "AMOLED display"],
         "delivery_days": 3},
        {"brand": "Noise", "model": "ColorFit Pro 4", "price": 2999, "rating": 4.0,
         "warranty": "1 year", "colors": ["Black", "Blue", "Pink"],
         "features": ["BT calling", "100+ sports modes", "7-day battery"],
         "delivery_days": 2},
    ],
    "powerbank": [
        {"brand": "Mi", "model": "Power Bank 3i 20000mAh", "price": 2199, "rating": 4.4,
         "warranty": "6 months", "colors": ["Black", "Silver"],
         "features": ["20000mAh", "18W fast charge", "Dual output"],
         "delivery_days": 2},
        {"brand": "Anker", "model": "PowerCore 10000", "price": 2999, "rating": 4.6,
         "warranty": "18 months", "colors": ["Black", "Blue"],
         "features": ["10000mAh", "Compact", "PowerIQ tech"],
         "delivery_days": 3},
        {"brand": "Ambrane", "model": "Stylo 10K", "price": 1099, "rating": 3.9,
         "warranty": "1 year", "colors": ["Black", "Blue", "Red"],
         "features": ["10000mAh", "20W output", "Type-C"],
         "delivery_days": 2},
    ],
    "charger": [
        {"brand": "Samsung", "model": "45W Super Fast Charger", "price": 1999, "rating": 4.5,
         "warranty": "1 year", "colors": ["Black", "White"],
         "features": ["45W PD", "USB-C", "Overheat protection"],
         "delivery_days": 2},
        {"brand": "Anker", "model": "Nano 3 30W", "price": 2499, "rating": 4.6,
         "warranty": "18 months", "colors": ["Black", "White"],
         "features": ["30W GaN", "Tiny size", "Multi-device safe"],
         "delivery_days": 3},
        {"brand": "Mi", "model": "33W SonicCharge", "price": 999, "rating": 4.2,
         "warranty": "6 months", "colors": ["White"],
         "features": ["33W", "Cable included", "Wide compatibility"],
         "delivery_days": 2},
    ],
    "mouse": [
        {"brand": "Logitech", "model": "M331 Silent", "price": 1295, "rating": 4.5,
         "warranty": "3 years", "colors": ["Black", "Blue", "Red"],
         "features": ["90% quieter clicks", "Wireless 2.4GHz", "24-month battery"],
         "delivery_days": 3},
        {"brand": "HP", "model": "X1000", "price": 399, "rating": 4.0,
         "warranty": "1 year", "colors": ["Black"],
         "features": ["Wired", "1000 DPI", "Ergonomic"],
         "delivery_days": 2},
        {"brand": "Razer", "model": "DeathAdder Essential", "price": 2499, "rating": 4.4,
         "warranty": "2 years", "colors": ["Black"],
         "features": ["6400 DPI", "Gaming-grade sensor", "Ergonomic"],
         "delivery_days": 4},
    ],
}

ALIASES = {
    "earbuds": ["earbuds", "earbud", "airpods", "tws", "earphones", "earphone"],
    "headphones": ["headphones", "headphone", "headset"],
    "smartwatch": ["smartwatch", "smart watch", "watch", "watches"],
    "powerbank": ["powerbank", "power bank", "power banks"],
    "charger": ["charger", "chargers", "adapter"],
    "mouse": ["mouse", "mice"],
}

# ---------- Look & feel per category ----------
CAT_THEME = {
    "earbuds":    ("🎶", "#4a148c", "#ab47bc"),
    "headphones": ("🎧", "#0d47a1", "#42a5f5"),
    "smartwatch": ("⌚", "#004d40", "#26a69a"),
    "powerbank":  ("🔋", "#e65100", "#ffa726"),
    "charger":    ("🔌", "#b71c1c", "#ef5350"),
    "mouse":      ("🖱️", "#263238", "#78909c"),
}

COLOR_HEX = {
    "Black": "#212121", "White": "#f5f5f5", "Lavender": "#b39ddb", "Blue": "#1e88e5",
    "Red": "#e53935", "Midnight": "#1a237e", "Starlight": "#f3e5ab", "Silver": "#b0bec5",
    "Graphite": "#455a64", "Gold": "#ffc107", "Pink": "#f06292", "Green": "#43a047",
}


# ------------------------------------------------------------- HELPERS
def add_business_days(start, days):
    """Add days to a date, skipping Sundays (no deliveries)."""
    current = start
    while days > 0:
        current += timedelta(days=1)
        if current.weekday() != 6:
            days -= 1
    return current


def fmt_price(p):
    return f"{CURRENCY}{p:,}"


def has_word(text, phrase):
    """Whole-word match, so 'mi' does not match inside 'premium'."""
    return re.search(r"\b" + re.escape(phrase) + r"\b", text) is not None


def find_category(text):
    for cat, words in ALIASES.items():
        if any(has_word(text, w) for w in words):
            return cat
    return None


def find_brand(text, category=None):
    cats = [category] if category else PRODUCTS.keys()
    for cat in cats:
        for p in PRODUCTS[cat]:
            if has_word(text, p["brand"].lower()):
                return p["brand"]
    return None


def all_products():
    return [(cat, p) for cat, items in PRODUCTS.items() for p in items]


def delivery_date(p, start=None):
    return add_business_days(start or date.today(), p["delivery_days"])


def product_md(p, category):
    d = delivery_date(p)
    return (
        f"**{p['brand']} {p['model']}** _({category})_\n"
        f"- Price: {fmt_price(p['price'])}\n"
        f"- Rating: {p['rating']}/5\n"
        f"- Warranty: {p['warranty']}\n"
        f"- Colors: {', '.join(p['colors'])}\n"
        f"- Features: {', '.join(p['features'])}\n"
        f"- Delivery: {d.strftime('%a, %d %b %Y')} "
        f"(if ordered today, {p['delivery_days']} business days)\n"
    )


def list_md(category):
    lines = [f"**Available {category} brands:**\n"]
    for p in PRODUCTS[category]:
        lines.append(f"- {p['brand']} {p['model']} | {fmt_price(p['price'])} | "
                     f"{p['rating']}★ | warranty {p['warranty']}")
    lines.append(f"\nTip: say 'compare {category}' for full details.")
    return "\n".join(lines)


def best_value_pick(category):
    # rating points minus a price penalty, so cheap items don't dominate
    return max(PRODUCTS[category], key=lambda x: x["rating"] - x["price"] / 20000)


def compare_md(category):
    items = sorted(PRODUCTS[category], key=lambda x: -x["rating"])
    parts = [f"**Comparison of {category} (best rated first):**\n"]
    parts += [product_md(p, category) for p in items]
    best = items[0]
    cheapest = min(items, key=lambda x: x["price"])
    parts.append(f"**Best rated:** {best['brand']} {best['model']}  \n"
                 f"**Cheapest:** {cheapest['brand']} {cheapest['model']} ({fmt_price(cheapest['price'])})")
    return "\n".join(parts)


HELP = """I can help with: **earbuds, headphones, smartwatch, powerbank, charger, mouse**.

Try:
- `earbuds` - list brands
- `compare headphones` - full comparison
- `best smartwatch` - top-rated pick
- `best value powerbank` - good quality for the price
- `cheapest charger` - lowest price
- `Sony headphones` - details of a brand
- `delivery Anker charger` - delivery date if ordered now
- `categories` - show all categories
"""


# ---------------------------------------------------------------- CHATBOT
def chatbot_reply(user_input):
    """Return {'text', 'action', 'category', 'brand'} for one user message."""
    text = user_input.lower().strip()
    out = {"text": "", "action": "UNKNOWN", "category": None, "brand": None}

    if text in ("exit", "quit", "bye"):
        out.update(action="GOODBYE", text="Thanks for visiting. Goodbye!")
        return out
    if text in ("help", "?", "hi", "hello", "hey"):
        out.update(action="HELP", text=HELP)
        return out
    if "categories" in text or "what do you sell" in text:
        out.update(action="CATEGORIES", text="**Categories:** " + ", ".join(PRODUCTS.keys()))
        return out

    category = find_category(text)
    brand = find_brand(text, category)
    out.update(category=category, brand=brand)

    if not category and not brand:
        out["text"] = "Sorry, I didn't get that. Type 'help' to see what I can do."
        return out

    # brand without category -> show that brand across all categories
    if brand and not category:
        out["action"] = "BRAND_ALL"
        cards = [product_md(p, cat) for cat, p in all_products() if p["brand"] == brand]
        out["text"] = f"**Products from {brand}:**\n\n" + "\n".join(cards)
        return out

    if "compare" in text or "better" in text:          # also covers "which is better"
        out.update(action="COMPARE", text=compare_md(category))
    elif "value" in text:                               # also covers "best value"
        p = best_value_pick(category)
        out.update(action="BEST_VALUE", text=f"**Best value {category}:**\n\n" + product_md(p, category))
    elif "best" in text:
        p = max(PRODUCTS[category], key=lambda x: x["rating"])
        out.update(action="BEST", text=f"**Top-rated {category}:**\n\n" + product_md(p, category))
    elif "cheap" in text or "lowest" in text or "budget" in text:
        p = min(PRODUCTS[category], key=lambda x: x["price"])
        out.update(action="CHEAPEST", text=f"**Cheapest {category}:**\n\n" + product_md(p, category))
    elif "deliver" in text:
        items = [p for p in PRODUCTS[category] if not brand or p["brand"] == brand]
        out.update(action="DELIVERY", text="\n".join(product_md(p, category) for p in items))
    elif brand:
        items = [p for p in PRODUCTS[category] if p["brand"] == brand]
        out.update(action="BRAND_DETAIL", text="\n".join(product_md(p, category) for p in items))
    else:
        out.update(action="LIST", text=list_md(category))
    return out


# =====================================================================
#                          STREAMLIT UI
# =====================================================================
st.set_page_config(page_title="Accessories Shop Assistant", page_icon="🎧", layout="wide")

WELCOME = ("Hi! Ask me about brands, price, features, warranty, colors and delivery dates. "
           "Type **help** for examples.")

SAMPLE_PROMPTS = [
    "earbuds", "compare headphones", "best smartwatch", "best value powerbank",
    "cheapest charger", "Sony headphones", "delivery Anker charger", "help",
]

PAGES = ["🏠 Home", "💬 Chat", "🛒 Product Finder", "⚖️ Compare", "📦 Delivery Estimator"]


# ---------- Images: SVGs generated in code, so no image files are needed ----------
def svg_img(svg, radius=14):
    import base64
    b64 = base64.b64encode(svg.encode("utf-8")).decode()
    return (f'<img src="data:image/svg+xml;base64,{b64}" '
            f'style="width:100%;border-radius:{radius}px;" />')


def hero_svg():
    icons = "".join(
        f'<text x="{x}" y="120" font-size="54">{e}</text>'
        for x, e in zip((560, 625, 690, 755, 820), ("🎧", "⌚", "🔋", "🔌", "🖱️"))
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 230">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#1a237e"/><stop offset="1" stop-color="#00acc1"/></linearGradient></defs>
<rect width="900" height="230" fill="url(#g)"/>
<circle cx="760" cy="60" r="130" fill="#fff" opacity="0.08"/>
{icons}
<text x="50" y="105" font-family="sans-serif" font-size="44" font-weight="bold" fill="#fff">Accessories Shop Assistant</text>
<text x="50" y="145" font-family="sans-serif" font-size="20" fill="#e0f7fa">Compare brands, prices, ratings, warranty and delivery dates</text>
<rect x="50" y="165" width="390" height="34" rx="17" fill="#ffffff" opacity="0.2"/>
<text x="68" y="188" font-family="sans-serif" font-size="16" fill="#fff">6 categories  |  18 products  |  sample data</text>
</svg>"""


def feature_svg(emoji, title, sub, c1, c2):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 170">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
<rect width="300" height="170" fill="url(#g)"/>
<circle cx="250" cy="40" r="70" fill="#fff" opacity="0.12"/>
<text x="24" y="85" font-size="52">{emoji}</text>
<text x="24" y="124" font-family="sans-serif" font-size="22" font-weight="bold" fill="#fff">{html.escape(title)}</text>
<text x="24" y="148" font-family="sans-serif" font-size="13" fill="#fff" opacity="0.9">{html.escape(sub)}</text>
</svg>"""


def product_svg(p, category):
    emoji, c1, c2 = CAT_THEME[category]
    title = html.escape(f"{p['brand']} {p['model']}")
    if len(title) > 30:
        title = title[:29] + "…"
    dots = "".join(
        f'<circle cx="{30 + i * 26}" cy="150" r="10" fill="{COLOR_HEX.get(c, "#9e9e9e")}" '
        f'stroke="#ffffff" stroke-width="2"/>'
        for i, c in enumerate(p["colors"])
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 175">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
<rect width="300" height="175" fill="url(#g)"/>
<circle cx="250" cy="35" r="65" fill="#fff" opacity="0.12"/>
<text x="22" y="66" font-size="44">{emoji}</text>
<text x="22" y="98" font-family="sans-serif" font-size="16" font-weight="bold" fill="#fff">{title}</text>
<text x="22" y="124" font-family="sans-serif" font-size="20" font-weight="bold" fill="#fff">{html.escape(fmt_price(p["price"]))}</text>
<text x="190" y="124" font-family="sans-serif" font-size="16" fill="#fff">★ {p["rating"]}</text>
{dots}
</svg>"""


def flow_svg():
    boxes = [
        (20, "1  You ask", "category, brand or budget", "#e3f2fd", "#1565c0"),
        (330, "2  Bot matches", "category + brand + intent", "#fff3e0", "#e65100"),
        (640, "3  You decide", "compare, price, delivery", "#e8f5e9", "#2e7d32"),
    ]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 200">',
             '<rect width="900" height="200" fill="#f7f9fc"/>']
    for x, t, s, bg, fg in boxes:
        parts.append(f'<rect x="{x}" y="40" width="240" height="120" rx="16" fill="{bg}" stroke="{fg}" stroke-width="2"/>')
        parts.append(f'<text x="{x + 20}" y="90" font-family="sans-serif" font-size="24" font-weight="bold" fill="{fg}">{t}</text>')
        parts.append(f'<text x="{x + 20}" y="124" font-family="sans-serif" font-size="16" fill="#444">{s}</text>')
    for x in (268, 578):
        parts.append(f'<polygon points="{x},85 {x + 40},100 {x},115" fill="#90a4ae"/>')
    parts.append("</svg>")
    return "".join(parts)


# ---------- Session state ----------
def reset_chat():
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
    st.session_state.last_analysis = None


def init_session():
    if "messages" not in st.session_state:
        reset_chat()


def send_message(user_text):
    out = chatbot_reply(user_text)
    name = st.session_state.get("user_name", "").strip()
    reply = out["text"]
    if name and out["action"] == "HELP":
        reply = f"Hi {name}! " + reply
    analysis = {"action": out["action"], "category": out["category"], "brand": out["brand"]}
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.messages.append({"role": "assistant", "content": reply, "meta": analysis})
    st.session_state.last_analysis = analysis


def show_analysis(a):
    c1, c2, c3 = st.columns(3)
    c1.metric("Action", a["action"])
    c2.metric("Category", a["category"] or "-")
    c3.metric("Brand", a["brand"] or "-")


# ---------- Pages ----------
def page_home():
    st.markdown(svg_img(hero_svg(), 18), unsafe_allow_html=True)
    st.write("")
    products = all_products()
    brands = {p["brand"] for _, p in products}
    n_user = sum(1 for m in st.session_state.messages if m["role"] == "user")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Categories", len(PRODUCTS))
    m2.metric("Products", len(products))
    m3.metric("Brands", len(brands))
    m4.metric("Messages you sent", n_user)

    st.subheader("What can you shop for?")
    cats = list(PRODUCTS.keys())
    for row in (cats[:3], cats[3:]):
        cols = st.columns(3)
        for col, cat in zip(cols, row):
            emoji, c1, c2 = CAT_THEME[cat]
            low = min(p["price"] for p in PRODUCTS[cat])
            sub = f"{len(PRODUCTS[cat])} products, from {fmt_price(low)}"
            col.markdown(svg_img(feature_svg(emoji, cat.capitalize(), sub, c1, c2)), unsafe_allow_html=True)
        st.write("")

    st.subheader("How it works")
    st.markdown(svg_img(flow_svg()), unsafe_allow_html=True)
    st.info("Use the sidebar to **chat**, filter products in the **Product Finder**, "
            "see side-by-side tables in **Compare**, or check a date in the **Delivery Estimator**.")


def page_chat():
    st.subheader("💬 Chat with the shop assistant")

    cols = st.columns(4)
    for i, p in enumerate(SAMPLE_PROMPTS):
        if cols[i % 4].button(p, key=f"sample_{i}", use_container_width=True):
            st.session_state.queued = p

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m.get("meta"):
                with st.expander("🔍 What the bot understood"):
                    show_analysis(m["meta"])

    user_input = st.chat_input("Ask e.g. 'compare headphones' or 'cheapest charger'...")
    if "queued" in st.session_state:
        user_input = st.session_state.pop("queued")
    if user_input:
        send_message(user_input)
        st.rerun()


def page_finder():
    st.subheader("🛒 Product Finder")
    st.caption("Set the filters and the matching products update instantly.")
    items = all_products()
    prices = [p["price"] for _, p in items]

    f1, f2 = st.columns(2)
    cats = f1.multiselect("Categories", list(PRODUCTS.keys()), default=list(PRODUCTS.keys()))
    pool = [(c, p) for c, p in items if c in cats]
    brand_options = sorted({p["brand"] for _, p in pool})
    brands = f2.multiselect("Brands (leave empty for all)", brand_options)

    g1, g2, g3 = st.columns(3)
    price_range = g1.slider("Price range (Rs)", min(prices), max(prices),
                            (min(prices), max(prices)), step=100)
    min_rating = g2.slider("Minimum rating", 0.0, 5.0, 0.0, step=0.1)
    max_days = g3.slider("Max delivery (business days)", 2, 4, 4)

    h1, h2 = st.columns(2)
    color_options = sorted({c for _, p in pool for c in p["colors"]})
    colors = h1.multiselect("Colors (leave empty for any)", color_options)
    sort_by = h2.selectbox("Sort by", ["Rating (high to low)", "Price (low to high)",
                                       "Price (high to low)", "Fastest delivery"])

    results = [
        (c, p) for c, p in pool
        if price_range[0] <= p["price"] <= price_range[1]
        and p["rating"] >= min_rating
        and p["delivery_days"] <= max_days
        and (not brands or p["brand"] in brands)
        and (not colors or set(colors) & set(p["colors"]))
    ]
    sorters = {
        "Rating (high to low)": lambda cp: -cp[1]["rating"],
        "Price (low to high)": lambda cp: cp[1]["price"],
        "Price (high to low)": lambda cp: -cp[1]["price"],
        "Fastest delivery": lambda cp: cp[1]["delivery_days"],
    }
    results.sort(key=sorters[sort_by])

    st.markdown(f"**{len(results)} product(s) match**")
    if not results:
        st.warning("No products match these filters. Try widening the price range or lowering the rating.")
        return
    for start in range(0, len(results), 3):
        cols = st.columns(3)
        for col, (cat, p) in zip(cols, results[start:start + 3]):
            col.markdown(svg_img(product_svg(p, cat)), unsafe_allow_html=True)
            d = delivery_date(p).strftime("%a, %d %b")
            col.caption(f"Warranty: {p['warranty']} | Delivery by {d}")
            col.write(", ".join(p["features"]))


def page_compare():
    st.subheader("⚖️ Compare")
    cat = st.selectbox("Category", list(PRODUCTS.keys()), key="cmp_cat")
    rows = [{
        "Brand": p["brand"], "Model": p["model"], "Price": p["price"], "Rating": p["rating"],
        "Warranty": p["warranty"], "Delivery (days)": p["delivery_days"],
        "Colors": ", ".join(p["colors"]), "Features": ", ".join(p["features"]),
    } for p in PRODUCTS[cat]]
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True, use_container_width=True)

    best = max(PRODUCTS[cat], key=lambda x: x["rating"])
    cheap = min(PRODUCTS[cat], key=lambda x: x["price"])
    value = best_value_pick(cat)
    k1, k2, k3 = st.columns(3)
    k1.metric("Best rated", f"{best['brand']} {best['model']}", f"{best['rating']}/5")
    k2.metric("Cheapest", f"{cheap['brand']} {cheap['model']}", fmt_price(cheap["price"]))
    k3.metric("Best value", f"{value['brand']} {value['model']}")

    c1, c2 = st.columns(2)
    c1.markdown("**Price (Rs)**")
    c1.bar_chart(df.set_index("Model")[["Price"]])
    c2.markdown("**Rating (out of 5)**")
    c2.bar_chart(df.set_index("Model")[["Rating"]])


def page_delivery():
    st.subheader("📦 Delivery Estimator")
    st.caption("Deliveries are made Monday to Saturday (Sundays are skipped).")
    c1, c2 = st.columns(2)
    cat = c1.selectbox("Category", list(PRODUCTS.keys()), key="dl_cat")
    items = PRODUCTS[cat]
    idx = c2.selectbox("Product", range(len(items)),
                       format_func=lambda i: f"{items[i]['brand']} {items[i]['model']}", key="dl_prod")
    p = items[idx]
    order_date = st.date_input("Order date", value=date.today())
    eta = add_business_days(order_date, p["delivery_days"])

    st.markdown(svg_img(product_svg(p, cat)), unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    k1.metric("Order date", order_date.strftime("%a, %d %b %Y"))
    k2.metric("Business days", p["delivery_days"])
    k3.metric("Estimated delivery", eta.strftime("%a, %d %b %Y"))
    st.success(f"If you order the {p['brand']} {p['model']} on {order_date.strftime('%d %b %Y')}, "
               f"it should arrive by {eta.strftime('%A, %d %b %Y')}.")


# ---------- Sidebar + routing ----------
init_session()

with st.sidebar:
    st.title("🎧 Accessories Shop")
    page = st.radio("Go to", PAGES, key="page")
    st.text_input("Your name (optional)", key="user_name", placeholder="e.g. Pallavi")
    st.divider()
    if st.button("🔄 Reset conversation", use_container_width=True):
        reset_chat()
        st.rerun()
    la = st.session_state.last_analysis
    if la:
        st.markdown("**Last message**")
        st.write(f"Action: `{la['action']}`")
        st.write(f"Category: `{la['category'] or '-'}`  Brand: `{la['brand'] or '-'}`")
    st.caption("Sample data only.")

if page == PAGES[0]:
    page_home()
elif page == PAGES[1]:
    page_chat()
elif page == PAGES[2]:
    page_finder()
elif page == PAGES[3]:
    page_compare()
else:
    page_delivery()
