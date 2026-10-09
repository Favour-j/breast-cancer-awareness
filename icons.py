"""
Vector SVG icons library for Breast Cancer Surveillance Dashboard.
Completely single-line, clean, professional SVG strings with zero emojis.
"""

def icon(name: str, size: int = 16, color: str = "currentColor", stroke_width: float = 2.0, extra_class: str = "") -> str:
    """Return inline SVG vector markup for specified icon name, guaranteed single-line."""
    cls_attr = f' class="svg-icon {extra_class}"' if extra_class else ' class="svg-icon"'
    style_attr = 'style="vertical-align: -0.15em; display: inline-block; flex-shrink: 0;"'

    paths = {
        "ribbon": '<path d="M12 2c-3.1 0-5.5 2.4-5.5 5.5 0 2.6 1.6 4.9 3.8 5.6L5.5 22l6.5-4 6.5 4-4.8-8.9c2.2-.7 3.8-3 3.8-5.6C17.5 4.4 15.1 2 12 2z" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="7.5" r="2.2" fill="none" stroke="{c}" stroke-width="{w}"/>',
        "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>',
        "globe": '<circle cx="12" cy="12" r="10" fill="none" stroke="{c}" stroke-width="{w}"/><line x1="2" y1="12" x2="22" y2="12" stroke="{c}" stroke-width="{w}"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" fill="none" stroke="{c}" stroke-width="{w}"/>',
        "map_pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="10" r="3" fill="none" stroke="{c}" stroke-width="{w}"/>',
        "file_text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><polyline points="14 2 14 8 20 8" fill="none" stroke="{c}" stroke-width="{w}"/><line x1="16" y1="13" x2="8" y2="13" stroke="{c}" stroke-width="{w}"/><line x1="16" y1="17" x2="8" y2="17" stroke="{c}" stroke-width="{w}"/>',
        "trending_up": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><polyline points="17 6 23 6 23 12" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>',
        "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>',
        "shield_check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><polyline points="9 12 11 14 15 10" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>',
        "database": '<ellipse cx="12" cy="5" rx="9" ry="3" fill="none" stroke="{c}" stroke-width="{w}"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" fill="none" stroke="{c}" stroke-width="{w}"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" fill="none" stroke="{c}" stroke-width="{w}"/>',
        "alert_circle": '<circle cx="12" cy="12" r="10" fill="none" stroke="{c}" stroke-width="{w}"/><line x1="12" y1="8" x2="12" y2="12" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><line x1="12" y1="16" x2="12.01" y2="16" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>',
        "info": '<circle cx="12" cy="12" r="10" fill="none" stroke="{c}" stroke-width="{w}"/><line x1="12" y1="16" x2="12" y2="12" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><line x1="12" y1="8" x2="12.01" y2="8" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>',
        "check_circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><polyline points="22 4 12 14.01 9 11.01" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>',
        "search": '<circle cx="11" cy="11" r="8" fill="none" stroke="{c}" stroke-width="{w}"/><line x1="21" y1="21" x2="16.65" y2="16.65" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>',
        "book_open": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>',
        "bar_chart": '<line x1="18" y1="20" x2="18" y2="10" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><line x1="12" y1="20" x2="12" y2="4" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><line x1="6" y1="20" x2="6" y2="14" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>',
        "external_link": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15 3 21 3 21 9" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><line x1="10" y1="14" x2="21" y2="3" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    }

    raw = paths.get(name, paths["activity"])
    body = raw.replace("{c}", color).replace("{w}", str(stroke_width))
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24"{cls_attr} {style_attr}>{body}</svg>'
