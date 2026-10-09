"""Shared appearance tokens and a device-preference bridge (no data access)."""
PALETTES = {
    'light': dict(bg='#F8FAFC', surface='#FFFFFF', sidebar='#EEF2F6', text='#0F172A', muted='#475569', border='#CBD5E1', land='#E2E8F0', crimson='#BE123C', teal='#0F766E', amber='#B45309', crimson_text='#BE123C', teal_text='#0F766E', amber_text='#92400E', rose_bg='#FFF1F2', rose_border='#FECDD3', teal_bg='#F0FDFA', teal_border='#99D5CE', amber_bg='#FFFBEB', amber_border='#FCD34D'),
    'dark': dict(bg='#0B1220', surface='#141F30', sidebar='#0F172A', text='#EAF0F7', muted='#C6D0DE', border='#405169', land='#253247', crimson='#BE123C', teal='#0F766E', amber='#B45309', crimson_text='#FB7185', teal_text='#7BD9D0', amber_text='#F5C583', rose_bg='#351625', rose_border='#642039', teal_bg='#102D30', teal_border='#205052', amber_bg='#302313', amber_border='#594022'),
}

def resolve_mode(choice, system):
    if choice in ('Light', 'Dark'):
        return choice.lower()
    return system if system in PALETTES else 'light'

THEME_JS = """
export default function({data, setStateValue}) {
    const media = window.matchMedia('(prefers-color-scheme: dark)');
    const update = () => {
        const mode = data.choice === 'System' ? (media.matches ? 'dark' : 'light') : data.choice.toLowerCase();
        document.documentElement.dataset.observatoryMode = mode;
        setStateValue('mode', mode);
    };
    update();
    media.addEventListener('change', update);
    return () => media.removeEventListener('change', update);
}
"""

def theme_css():
    def declarations(mode):
        return ';'.join(f'--obs-{k.replace("_", "-")}:{v}' for k,v in PALETTES[mode].items())
    tokens = ':root{' + declarations('light') + ';color-scheme:light}'
    tokens += '@media(prefers-color-scheme:dark){:root:not([data-observatory-mode]){' + declarations('dark') + ';color-scheme:dark}}'
    for mode in PALETTES:
        tokens += 'html[data-observatory-mode="' + mode + '"]{' + declarations(mode) + ';color-scheme:' + mode + '}'
    return tokens + """
    .stApp, .stApp [data-testid="stMarkdownContainer"], .stApp [data-testid="stText"] {color:var(--obs-text)}
    [data-testid="stAppViewContainer"], [data-testid="stMain"] {background:var(--obs-bg)!important}
    .stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6 {color:var(--obs-text)!important}
    .stApp strong,.stApp b {color:inherit}
    [data-testid="stHeader"] {background:var(--obs-bg)!important}
    [data-testid="stHeader"] *,[data-testid="stSidebarCollapseButton"] *,[data-testid="stExpandSidebarButton"] * {color:var(--obs-text)!important}
    [data-testid="stSidebar"] {background:var(--obs-sidebar)!important;color:var(--obs-text)}
    [data-testid="stTab"], [data-testid="stTab"] *,button[data-baseweb="tab"],button[data-baseweb="tab"] * {color:var(--obs-text)!important;opacity:1!important;font-weight:600!important}
    [role="tablist"] {overflow-x:auto;flex-wrap:nowrap}
    [role="tab"] {flex-shrink:0}
    [role="tab"][aria-selected="true"] {box-shadow:inset 0 -2px var(--obs-crimson);background:var(--obs-surface)!important}
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,.stApp label,.stApp label p {color:var(--obs-text)!important;opacity:1!important}
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p,.stApp [data-testid="stCaptionContainer"] p,.stApp small {color:var(--obs-muted)!important}
    /* React Aria controls in current Streamlit, plus older Base Web controls. */
    [data-testid="stSelectbox"] [data-rac], [data-testid="stMultiSelect"] [data-rac],
    [data-testid="stSelectbox"] input,[data-testid="stMultiSelect"] input,
    [data-baseweb="select"] > div,[data-baseweb="input"],[data-baseweb="base-input"],.stApp input,.stApp textarea {
        color:var(--obs-text)!important;background:var(--obs-surface)!important;border-color:var(--obs-border)!important;
        -webkit-text-fill-color:var(--obs-text)!important;opacity:1!important}
    [data-testid="stSelectbox"] svg,[data-testid="stMultiSelect"] svg {color:var(--obs-text)!important}
    .stApp input::placeholder,.stApp textarea::placeholder {color:var(--obs-muted)!important;-webkit-text-fill-color:var(--obs-muted)!important;opacity:1!important}
    [role="listbox"], [role="listbox"] [role="presentation"], [role="option"], [role="option"] *,
    [data-baseweb="popover"] ul,[data-baseweb="popover"] li {
        color:var(--obs-text)!important;background:var(--obs-surface)!important;-webkit-text-fill-color:var(--obs-text)!important;opacity:1!important}
    [role="option"]:hover,[role="option"][data-focused="true"],[role="option"][aria-selected="true"],
    [role="option"]:hover *,[role="option"][data-focused="true"] *,[role="option"][aria-selected="true"] * {background:var(--obs-land)!important;color:var(--obs-text)!important}
    .stApp [data-testid="stMultiSelect"] [data-tag],.stApp [data-testid="stMultiSelect"] [data-tag] * {background:var(--obs-land)!important;color:var(--obs-text)!important;-webkit-text-fill-color:var(--obs-text)!important}
    [data-baseweb="tag"],[data-baseweb="tag"] * {background:var(--obs-land)!important;color:var(--obs-text)!important}
    [data-testid="stRadio"] label,[data-testid="stRadio"] p {color:var(--obs-text)!important}
    [data-testid="stExpander"] details {background:var(--obs-surface)!important;border-color:var(--obs-border)!important}
    [data-testid="stExpander"] summary,[data-testid="stExpander"] summary *,[data-testid="stExpanderDetails"] {color:var(--obs-text)!important}
    [data-testid="stMetricLabel"] *,[data-testid="stMetricValue"] * {color:var(--obs-text)!important}
    [data-testid="stAlertContainer"] {background:var(--obs-amber-bg)!important}
    [data-testid="stAlert"] p {color:var(--obs-amber-text)!important}
    .stApp a {color:var(--obs-crimson-text)!important}
    .stApp code {color:var(--obs-crimson-text);background:var(--obs-land)}
    """
