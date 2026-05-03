import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import io
import json
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Home Electronics & Network Diagnostic System – Built by Gesner Deslandes",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- AUTHENTICATION ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "maintenance_log" not in st.session_state:
    st.session_state.maintenance_log = []
if "scan_results" not in st.session_state:
    st.session_state.scan_results = None
if "devices" not in st.session_state:
    st.session_state.devices = {
        "Router (Living Room)": {"status": "Connected", "signal_strength": 68, "latency": 45, "last_check": datetime.now().strftime("%Y-%m-%d %H:%M"), "issues": []},
        "Smart TV (Living Room)": {"status": "Connected", "signal_strength": 72, "latency": 38, "last_check": datetime.now().strftime("%Y-%m-%d %H:%M"), "issues": []},
        "Security Camera (Front Door)": {"status": "Connected", "signal_strength": 55, "latency": 89, "last_check": datetime.now().strftime("%Y-%m-%d %H:%M"), "issues": ["Weak signal (55%)"]},
        "Laptop (Home Office)": {"status": "Connected", "signal_strength": 90, "latency": 22, "last_check": datetime.now().strftime("%Y-%m-%d %H:%M"), "issues": []},
        "Smart Plug (Kitchen)": {"status": "Offline", "signal_strength": 0, "latency": None, "last_check": datetime.now().strftime("%Y-%m-%d %H:%M"), "issues": ["Device offline – check power"]},
    }

# ---------- LANGUAGE DICTIONARIES (renamed function to t() to avoid conflict) ----------
text = {
    "en": {
        "login_title": "🔐 System Login",
        "login_password": "Password",
        "login_button": "Login",
        "login_error": "Incorrect password. Please try again.",
        "logout_button": "🚪 Logout",
        "built_by": "Built by Gesner Deslandes – GlobalInternet.py",
        "company_name": "Home Diagnostic System",
        "nav_dashboard": "📊 Dashboard",
        "nav_scan": "🔍 Full System Scan",
        "nav_maintenance": "🛠️ Maintenance Reminders",
        "nav_report": "📥 Download Report",
        "nav_api": "📡 API Integration",
        "sidebar_contact": "📞 Contact Us",
        "sidebar_email": "✉️ deslandes78@gmail.com",
        "sidebar_phone": "📱 (509)-47385663",
        "sidebar_pricing_title": "💰 Software Pricing",
        "sidebar_monthly": "📅 Monthly subscription: $99 USD / month",
        "sidebar_full": "💎 Full package (one‑time): $2,499 USD",
        "sidebar_note": "Includes source code, setup, and 1 year support",
        "language_selector": "🌐 Language",
        "dashboard_title": "Home Electronics & Network Diagnostic Center",
        "status_online": "Online",
        "status_offline": "Offline",
        "device": "Device",
        "location": "Location",
        "signal": "Signal Strength",
        "latency": "Latency (ms)",
        "last_check": "Last Check",
        "issues": "Issues",
        "scan_btn": "🔍 Run Full System Scan",
        "scanning": "Scanning all devices...",
        "no_issues": "No issues detected",
        "issue_found": "Issue found!",
        "fix_instruction": "Fix Instruction",
        "maintenance_title": "Maintenance Reminders",
        "add_reminder": "➕ Add Maintenance Reminder",
        "device_name": "Device Name",
        "interval_days": "Reminder Interval (days)",
        "add_btn": "Add Reminder",
        "existing_reminders": "Existing Reminders",
        "next_due": "Next Due",
        "report_title": "System Health Report",
        "report_generate": "Generate & Download Report",
        "report_btn": "📥 Download CSV Report",
        "globe_alt": "GlobalInternet.py Logo",
        "api_title": "📡 API Integration – Ingest Device Logs",
        "api_instructions": "Paste device logs in JSON format (list of devices with status, signal_strength, latency) to analyze issues.",
        "api_example": "Example JSON",
        "api_input": "Device Logs (JSON)",
        "api_analyze": "Analyze Logs",
        "api_results": "Analysis Results",
    },
    "fr": {
        "login_title": "🔐 Connexion au système",
        "login_password": "Mot de passe",
        "login_button": "Se connecter",
        "login_error": "Mot de passe incorrect.",
        "logout_button": "🚪 Déconnexion",
        "built_by": "Construit par Gesner Deslandes – GlobalInternet.py",
        "company_name": "Système de diagnostic domestique",
        "nav_dashboard": "📊 Tableau de bord",
        "nav_scan": "🔍 Analyse complète",
        "nav_maintenance": "🛠️ Rappels de maintenance",
        "nav_report": "📥 Télécharger rapport",
        "nav_api": "📡 Intégration API",
        "sidebar_contact": "📞 Contactez‑nous",
        "sidebar_email": "✉️ deslandes78@gmail.com",
        "sidebar_phone": "📱 (509)-47385663",
        "sidebar_pricing_title": "💰 Tarifs du logiciel",
        "sidebar_monthly": "📅 Abonnement mensuel : 99 $US / mois",
        "sidebar_full": "💎 Licence complète (unique) : 2 499 $US",
        "sidebar_note": "Code source, installation et 1 an de support inclus",
        "language_selector": "🌐 Langue",
        "dashboard_title": "Centre de diagnostic électronique et réseau",
        "status_online": "En ligne",
        "status_offline": "Hors ligne",
        "device": "Appareil",
        "location": "Emplacement",
        "signal": "Force du signal",
        "latency": "Latence (ms)",
        "last_check": "Dernière vérification",
        "issues": "Problèmes",
        "scan_btn": "🔍 Lancer l'analyse complète",
        "scanning": "Analyse de tous les appareils...",
        "no_issues": "Aucun problème détecté",
        "issue_found": "Problème trouvé !",
        "fix_instruction": "Instruction de réparation",
        "maintenance_title": "Rappels de maintenance",
        "add_reminder": "➕ Ajouter un rappel",
        "device_name": "Nom de l'appareil",
        "interval_days": "Intervalle (jours)",
        "add_btn": "Ajouter",
        "existing_reminders": "Rappels existants",
        "next_due": "Prochaine échéance",
        "report_title": "Rapport d'état du système",
        "report_generate": "Générer et télécharger",
        "report_btn": "📥 Télécharger CSV",
        "globe_alt": "Logo GlobalInternet.py",
        "api_title": "📡 Intégration API – Ingérer des journaux d'appareils",
        "api_instructions": "Collez les journaux d'appareils au format JSON (liste d'appareils avec statut, signal_strength, latence) pour analyser les problèmes.",
        "api_example": "Exemple JSON",
        "api_input": "Journaux d'appareils (JSON)",
        "api_analyze": "Analyser les journaux",
        "api_results": "Résultats d'analyse",
    },
    "es": {
        "login_title": "🔐 Inicio de sesión",
        "login_password": "Contraseña",
        "login_button": "Iniciar sesión",
        "login_error": "Contraseña incorrecta.",
        "logout_button": "🚪 Cerrar sesión",
        "built_by": "Construido por Gesner Deslandes – GlobalInternet.py",
        "company_name": "Sistema de diagnóstico del hogar",
        "nav_dashboard": "📊 Tablero",
        "nav_scan": "🔍 Análisis completo",
        "nav_maintenance": "🛠️ Recordatorios de mantenimiento",
        "nav_report": "📥 Descargar informe",
        "nav_api": "📡 Integración API",
        "sidebar_contact": "📞 Contáctenos",
        "sidebar_email": "✉️ deslandes78@gmail.com",
        "sidebar_phone": "📱 (509)-47385663",
        "sidebar_pricing_title": "💰 Precios del software",
        "sidebar_monthly": "📅 Suscripción mensual: $99 USD / mes",
        "sidebar_full": "💎 Licencia completa (única): $2,499 USD",
        "sidebar_note": "Incluye código fuente, instalación y 1 año de soporte",
        "language_selector": "🌐 Idioma",
        "dashboard_title": "Centro de diagnóstico electrónico y de red",
        "status_online": "En línea",
        "status_offline": "Fuera de línea",
        "device": "Dispositivo",
        "location": "Ubicación",
        "signal": "Intensidad de la señal",
        "latency": "Latencia (ms)",
        "last_check": "Última verificación",
        "issues": "Problemas",
        "scan_btn": "🔍 Ejecutar análisis completo",
        "scanning": "Escaneando todos los dispositivos...",
        "no_issues": "No se detectaron problemas",
        "issue_found": "¡Problema encontrado!",
        "fix_instruction": "Instrucción de reparación",
        "maintenance_title": "Recordatorios de mantenimiento",
        "add_reminder": "➕ Agregar recordatorio",
        "device_name": "Nombre del dispositivo",
        "interval_days": "Intervalo (días)",
        "add_btn": "Agregar",
        "existing_reminders": "Recordatorios existentes",
        "next_due": "Próxima fecha",
        "report_title": "Informe de estado del sistema",
        "report_generate": "Generar y descargar",
        "report_btn": "📥 Descargar CSV",
        "globe_alt": "Logo GlobalInternet.py",
        "api_title": "📡 Integración API – Ingerir registros de dispositivos",
        "api_instructions": "Pegue los registros de dispositivos en formato JSON (lista de dispositivos con estado, signal_strength, latencia) para analizar problemas.",
        "api_example": "Ejemplo JSON",
        "api_input": "Registros de dispositivos (JSON)",
        "api_analyze": "Analizar registros",
        "api_results": "Resultados del análisis",
    }
}

def t(key):
    return text[st.session_state.lang].get(key, key)

# ---------- INITIALISE MAINTENANCE REMINDERS (demo) ----------
if not st.session_state.maintenance_log:
    st.session_state.maintenance_log = [
        {"device": "Router (Living Room)", "last_maintenance": datetime.now().strftime("%Y-%m-%d"), "interval_days": 30, "next_due": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")},
        {"device": "Security Camera (Front Door)", "last_maintenance": datetime.now().strftime("%Y-%m-%d"), "interval_days": 45, "next_due": (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d")},
    ]

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    .stApp, [data-testid="stSidebar"] {
        background: #1a1a2e !important;
        color: white !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio div[role="radio"] span {
        color: white !important;
    }
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }
    .main-header {
        background: linear-gradient(135deg, #0f3460, #16213e);
        padding: 1rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #00ffcc;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        background-color: rgba(255,255,255,0.05);
        border-radius: 20px;
        color: #aaa;
    }
    .stButton button {
        background-color: #00ffcc;
        color: #0f3460;
        border-radius: 30px;
        padding: 0.3rem 1.2rem;
        font-weight: bold;
        border: none;
    }
    .stButton button:hover {
        background-color: #00e6bb;
        color: #0a1a2e;
    }
    h1, h2, h3, .stMarkdown, .stMetric {
        color: white !important;
    }
    .metric-card {
        background: #0f3460;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #00ffcc;
    }
    .rotating-symbol {
        font-size: 120px;
        display: block;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: spin 8s linear infinite;
    }
    @keyframes spin {
        100% { transform: rotate(360deg); }
    }
    .sidebar-globe {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: spin 8s linear infinite;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #0f3460 !important;
        color: white !important;
        border: 1px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN PAGE ----------
if not st.session_state.authenticated:
    st.markdown('<div class="main-header"><div class="rotating-symbol">⚡⚙️🔧</div><h1>{}</h1></div>'.format(t("login_title")), unsafe_allow_html=True)
    password = st.text_input(t("login_password"), type="password")
    if st.button(t("login_button")):
        if password == "20082010":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error(t("login_error"))
    st.stop()

# ---------- LOGGED IN – MAIN INTERFACE ----------
lang_options = {"English": "en", "Français": "fr", "Español": "es"}
selected_lang = st.sidebar.selectbox(t("language_selector"), list(lang_options.keys()))
st.session_state.lang = lang_options[selected_lang]

page = st.sidebar.radio(
    "Navigation",
    [t("nav_dashboard"), t("nav_scan"), t("nav_maintenance"), t("nav_report"), t("nav_api")],
    label_visibility="hidden"
)

# ---------- SIDEBAR: GLOBE LOGO, CONTACT, PRICING ----------
st.sidebar.markdown('<div class="sidebar-globe">🌐</div>', unsafe_allow_html=True)
st.sidebar.markdown(f"## {t('company_name')}")
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t('sidebar_contact')}")
st.sidebar.markdown(t("sidebar_email"))
st.sidebar.markdown(t("sidebar_phone"))
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t('sidebar_pricing_title')}")
st.sidebar.markdown(t("sidebar_monthly"))
st.sidebar.markdown(t("sidebar_full"))
st.sidebar.caption(t("sidebar_note"))
st.sidebar.markdown("---")

if st.sidebar.button(t("logout_button"), width='stretch'):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"*{t('built_by')}*")

# Helper functions
def analyze_device_logs(devices_list):
    """Analyze a list of device logs (dict) and return a DataFrame with issues and fixes."""
    results = []
    for device in devices_list:
        name = device.get("name", "Unknown Device")
        status = device.get("status", "Unknown")
        signal = device.get("signal_strength")
        latency = device.get("latency")
        issues = []
        fix = ""
        if signal is not None and signal < 60:
            issues.append("Weak signal (below 60%)")
            fix = "Move device closer to router or add a Wi‑Fi extender."
        if latency is not None and latency > 80:
            issues.append("High latency (>80 ms)")
            fix = "Check for interference, reduce network congestion, or restart router."
        if status == "Offline":
            issues.append("Device offline")
            fix = "Check power connection, restart device, or verify network settings."
        if not issues:
            issues.append("No issues")
            fix = "No action needed."
        results.append({
            "Device": name,
            "Status": status,
            "Signal Strength (%)": signal if signal is not None else "",
            "Latency (ms)": latency if latency is not None else "",
            "Issues": ", ".join(issues),
            "Fix Instruction": fix
        })
    return pd.DataFrame(results)

def simulate_scan():
    results = []
    for device, info in st.session_state.devices.items():
        issues = []
        fix = ""
        if info["signal_strength"] is not None and info["signal_strength"] < 60:
            issues.append("Weak signal (below 60%)")
            fix = "Move device closer to router or add a Wi‑Fi extender."
        if info["latency"] is not None and info["latency"] > 80:
            issues.append("High latency (>80 ms)")
            fix = "Check for interference, reduce network congestion, or restart router."
        if info["status"] == "Offline":
            issues.append("Device offline")
            fix = "Check power connection, restart device, or verify network settings."
        if not issues:
            issues.append("No issues")
            fix = "No action needed."
        latency_val = info["latency"] if info["latency"] is not None else None
        results.append({
            "Device": device,
            "Location": device.split("(")[-1].replace(")", "") if "(" in device else "Unknown",
            "Status": info["status"],
            "Signal Strength (%)": info["signal_strength"] if info["signal_strength"] is not None else None,
            "Latency (ms)": latency_val,
            "Issues": ", ".join(issues),
            "Fix Instruction": fix
        })
    return pd.DataFrame(results)

# ---------- DASHBOARD ----------
if page == t("nav_dashboard"):
    st.markdown(f'<div class="main-header"><div class="rotating-symbol">⚡⚙️🔧</div><h1>{t("dashboard_title")}</h1></div>', unsafe_allow_html=True)
    
    st.subheader("📡 Current Device Status")
    df_status = pd.DataFrame.from_dict(st.session_state.devices, orient="index").reset_index()
    df_status.rename(columns={"index": "Device"}, inplace=True)
    st.dataframe(df_status[["Device", "status", "signal_strength", "latency", "last_check", "issues"]], use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        online_count = sum(1 for d in st.session_state.devices.values() if d["status"] == "Connected")
        st.metric("Devices Online", f"{online_count}/{len(st.session_state.devices)}")
    with col2:
        signals = [d["signal_strength"] for d in st.session_state.devices.values() if d["signal_strength"] is not None]
        avg_signal = sum(signals) / len(signals) if signals else 0
        st.metric("Average Signal Strength", f"{avg_signal:.1f}%")
    with col3:
        issues_count = sum(1 for d in st.session_state.devices.values() if d["issues"])
        st.metric("Active Issues", issues_count)

# ---------- FULL SYSTEM SCAN ----------
elif page == t("nav_scan"):
    st.markdown(f'<div class="main-header"><h1>🔍 {t("nav_scan")}</h1></div>', unsafe_allow_html=True)
    if st.button(t("scan_btn")):
        with st.spinner(t("scanning")):
            time.sleep(2)
            st.session_state.scan_results = simulate_scan()
        st.success("Scan complete!")
    
    if st.session_state.scan_results is not None:
        st.subheader("🔎 Scan Report")
        st.dataframe(st.session_state.scan_results, use_container_width=True)
        issues_df = st.session_state.scan_results[st.session_state.scan_results["Issues"] != "No issues"]
        if not issues_df.empty:
            st.warning("⚠️ Issues detected! See instructions above.")
            for _, row in issues_df.iterrows():
                with st.expander(f"Fix for {row['Device']} – {row['Issues']}"):
                    st.markdown(f"**Location:** {row['Location']}\n\n**Fix:** {row['Fix Instruction']}")
        else:
            st.success("✅ All devices are healthy!")

# ---------- MAINTENANCE REMINDERS ----------
elif page == t("nav_maintenance"):
    st.markdown(f'<div class="main-header"><h1>🛠️ {t("nav_maintenance")}</h1></div>', unsafe_allow_html=True)
    
    with st.expander(t("add_reminder")):
        with st.form("add_reminder_form"):
            device_name = st.text_input(t("device_name"))
            interval = st.number_input(t("interval_days"), min_value=1, value=30, step=1)
            if st.form_submit_button(t("add_btn")):
                if device_name:
                    new_entry = {
                        "device": device_name,
                        "last_maintenance": datetime.now().strftime("%Y-%m-%d"),
                        "interval_days": interval,
                        "next_due": (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d")
                    }
                    st.session_state.maintenance_log.append(new_entry)
                    st.rerun()
    
    st.subheader(t("existing_reminders"))
    if st.session_state.maintenance_log:
        df_reminders = pd.DataFrame(st.session_state.maintenance_log)
        st.dataframe(df_reminders[["device", "last_maintenance", "interval_days", "next_due"]], use_container_width=True)
        today = datetime.now().date()
        for idx, row in df_reminders.iterrows():
            due_date = datetime.strptime(row["next_due"], "%Y-%m-%d").date()
            if due_date < today:
                st.warning(f"⏰ Overdue: {row['device']} maintenance was due on {row['next_due']}.")
            elif (due_date - today).days <= 7:
                st.info(f"📅 Upcoming: {row['device']} maintenance due on {row['next_due']}.")
    else:
        st.info("No maintenance reminders set.")

# ---------- DOWNLOAD REPORT ----------
elif page == t("nav_report"):
    st.markdown(f'<div class="main-header"><h1>📥 {t("nav_report")}</h1></div>', unsafe_allow_html=True)
    st.write(t("report_title"))
    
    if st.button(t("report_btn")):
        report_data = []
        for device, info in st.session_state.devices.items():
            report_data.append({
                "Device": device,
                "Status": info["status"],
                "Signal Strength (%)": info["signal_strength"] if info["signal_strength"] is not None else "",
                "Latency (ms)": info["latency"] if info["latency"] is not None else "",
                "Last Check": info["last_check"],
                "Detected Issues": ", ".join(info["issues"]),
                "Recommended Fix": "Check connectivity" if "Offline" in info["issues"] else ("Improve signal" if info.get("signal_strength", 100) < 60 else "No action needed")
            })
        df_report = pd.DataFrame(report_data)
        
        if st.session_state.maintenance_log:
            df_rem = pd.DataFrame(st.session_state.maintenance_log)
            df_rem = df_rem.rename(columns={"device": "Device", "last_maintenance": "Last Maintenance", "next_due": "Next Maintenance Due"})
            df_report = df_report.merge(df_rem, on="Device", how="left")
        
        csv_buffer = io.StringIO()
        df_report.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Full System Report (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"home_diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_report"
        )
        st.success("Report generated! Check your downloads folder.")

# ---------- API INTEGRATION PAGE ----------
elif page == t("nav_api"):
    st.markdown(f'<div class="main-header"><h1>{t("api_title")}</h1></div>', unsafe_allow_html=True)
    st.markdown(t("api_instructions"))
    
    # Show example JSON
    example_json = [
        {"name": "Router (Living Room)", "status": "Connected", "signal_strength": 68, "latency": 45},
        {"name": "Smart TV (Living Room)", "status": "Connected", "signal_strength": 72, "latency": 38},
        {"name": "Security Camera (Front Door)", "status": "Connected", "signal_strength": 55, "latency": 89},
        {"name": "Laptop (Home Office)", "status": "Connected", "signal_strength": 90, "latency": 22},
        {"name": "Smart Plug (Kitchen)", "status": "Offline", "signal_strength": 0, "latency": None}
    ]
    st.code(json.dumps(example_json, indent=2), language="json")
    
    # Input area for JSON
    json_input = st.text_area(t("api_input"), height=200, placeholder='[{"name": "Device1", "status": "Connected", "signal_strength": 45, "latency": 120}]')
    
    if st.button(t("api_analyze")):
        try:
            data = json.loads(json_input)
            if isinstance(data, list):
                df_analysis = analyze_device_logs(data)
                st.subheader(t("api_results"))
                st.dataframe(df_analysis, use_container_width=True)
                # Show issues summary
                issues_df = df_analysis[df_analysis["Issues"] != "No issues"]
                if not issues_df.empty:
                    st.warning("⚠️ Issues detected in the ingested logs!")
                    for _, row in issues_df.iterrows():
                        with st.expander(f"Fix for {row['Device']} – {row['Issues']}"):
                            st.markdown(row['Fix Instruction'])
                else:
                    st.success("✅ All ingested devices are healthy!")
            else:
                st.error("JSON must contain a list of devices.")
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")

# ---------- FOOTER ----------
footer_html = f"""
<div class="footer">
    <p>© {datetime.now().year} – {t('built_by')}</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
