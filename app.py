import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config.settings import settings
from data.synthetic_generator import generate_department_snapshot, generate_hr_data
from services.forecasting_service import apply_scenario, seasonal_forecast
from services.insight_service import calculate_payroll_scenario
from services.ollama_service import OllamaService

SCENARIO_FILE = Path("storage/current_scenario.json")
DEFAULT_SCENARIO = {"new_hires": 150, "salary_increase": 3.0, "smart_working": 3, "retention": 10.0}
BLUE, CYAN, PINK, PURPLE, GREEN = "#2f91ff", "#20d5dc", "#ff5d91", "#a76cff", "#45e0ad"
GRID = "rgba(119,158,194,.16)"


def load_css():
    path = Path("assets/style.css")
    if path.exists():
        st.markdown(f"<style>{path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def load_scenario():
    if "scenario" in st.session_state:
        return st.session_state["scenario"]
    if SCENARIO_FILE.exists():
        try:
            raw = json.loads(SCENARIO_FILE.read_text(encoding="utf-8"))
            scenario = {
                "new_hires": int(raw.get("new_hires", 150)),
                "salary_increase": float(raw.get("salary_increase", 3.0)),
                "smart_working": int(raw.get("smart_working", 3)),
                "retention": float(raw.get("retention", 10.0)),
            }
            st.session_state["scenario"] = scenario
            return scenario
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass
    return DEFAULT_SCENARIO.copy()


def save_scenario(scenario):
    SCENARIO_FILE.parent.mkdir(parents=True, exist_ok=True)
    SCENARIO_FILE.write_text(json.dumps(scenario, indent=2), encoding="utf-8")
    st.session_state["scenario"] = scenario


def chart_layout(height):
    return {
        "template": "plotly_dark",
        "height": height,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": "Segoe UI, Aptos, sans-serif", "color": "#c8d8e8"},
        "margin": {"l": 42, "r": 18, "t": 20, "b": 34},
        "legend": {"orientation": "h", "y": 1.12, "x": 0, "font": {"size": 10}},
        "xaxis": {"gridcolor": GRID, "zeroline": False},
        "yaxis": {"gridcolor": GRID, "zeroline": False},
        "hoverlabel": {"bgcolor": "#0b2036", "bordercolor": "#315778"},
    }


def panel_title(title, action=None):
    action_html = f'<span class="efi-action">{action}</span>' if action else ""
    st.markdown(f'<div class="efi-card-title"><strong>{title}</strong>{action_html}</div>', unsafe_allow_html=True)


def kpi(icon, label, value, delta, css_class, accent):
    st.markdown(
        f'''<div class="efi-kpi" style="--accent:{accent}">
        <div class="efi-kpi-top"><span class="efi-icon">{icon}</span><span class="efi-label">{label}</span></div>
        <div class="efi-value">{value}</div><div class="efi-kpi-foot"><span class="efi-delta {css_class}">{delta}</span>
        <span class="efi-small">vs anno precedente</span></div></div>''', unsafe_allow_html=True)


def headcount_chart(data, scenario):
    fc = seasonal_forecast(data.headcount, data.date.iloc[-1], 24)
    adjusted = apply_scenario(fc.median, "headcount", scenario["new_hires"], scenario["salary_increase"], scenario["smart_working"], scenario["retention"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.date, y=data.headcount, name="Storico", line={"color": BLUE, "width": 3}))
    fig.add_trace(go.Scatter(x=fc.dates, y=fc.upper, line={"width": 0}, showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=fc.dates, y=fc.lower, name="Intervallo di confidenza", fill="tonexty", fillcolor="rgba(109,85,189,.20)", line={"width": 0}))
    fig.add_trace(go.Scatter(x=fc.dates, y=fc.median, name="Forecast", line={"color": PURPLE, "width": 3, "dash": "dot"}))
    fig.add_trace(go.Scatter(x=fc.dates, y=adjusted, name="Scenario selezionato", line={"color": GREEN, "width": 2, "dash": "dash"}))
    fig.update_layout(**chart_layout(325))
    return fig


def absence_chart(data, horizon=12, height=280):
    fc = seasonal_forecast(data.absences, data.date.iloc[-1], horizon)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.date, y=data.absences, name="Storico", line={"color": BLUE, "width": 3}))
    fig.add_trace(go.Scatter(x=fc.dates, y=fc.upper, line={"width": 0}, showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=fc.dates, y=fc.lower, name="Intervallo di confidenza", fill="tonexty", fillcolor="rgba(255,93,145,.20)", line={"width": 0}))
    fig.add_trace(go.Scatter(x=fc.dates, y=fc.median, name="Forecast", line={"color": PINK, "width": 3, "dash": "dot"}))
    fig.update_layout(**chart_layout(height))
    return fig


def payroll_chart(data, scenario):
    fc = seasonal_forecast(data.payroll, data.date.iloc[-1], 24)
    adjusted = apply_scenario(fc.median, "payroll", scenario["new_hires"], scenario["salary_increase"], scenario["smart_working"], scenario["retention"])
    recent = data.iloc[-24:]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=recent.date, y=recent.payroll, name="Storico", marker_color=BLUE))
    fig.add_trace(go.Bar(x=fc.dates, y=fc.median, name="Forecast", marker_color=PINK))
    fig.add_trace(go.Bar(x=fc.dates, y=adjusted - fc.median, base=fc.median, name="Scenario", marker_color=GREEN))
    layout = chart_layout(280)
    layout["barmode"] = "overlay"
    fig.update_layout(**layout)
    fig.update_yaxes(tickformat="~s")
    return fig


def donut_chart(departments):
    fig = go.Figure(go.Pie(labels=departments.department, values=departments.headcount, hole=.62,
        marker={"colors": [BLUE, CYAN, "#158fa4", "#bb945e", "#ff9b8e"], "line": {"color": "#0b2036", "width": 2}},
        textinfo="none", hovertemplate="%{label}: %{value:,}<extra></extra>"))
    fig.add_annotation(text=f"<b>{departments.headcount.sum():,}</b><br><span style='font-size:11px'>dipendenti</span>", showarrow=False, font={"size": 20, "color": "#f5f9ff"})
    layout = chart_layout(270)
    layout["showlegend"] = True
    layout["legend"] = {"orientation": "v", "x": .82, "y": .8, "font": {"size": 10}}
    fig.update_layout(**layout)
    return fig


def risk_gauge(score):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=score,
        number={"suffix": "/100", "font": {"size": 18, "color": "#f5f9ff"}},
        title={"text": "MEDIO", "font": {"size": 14, "color": "#f8d34e"}},
        gauge={"shape": "angular", "axis": {"range": [0, 100], "visible": False},
               "bar": {"color": "#f8d34e", "thickness": .28}, "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
               "steps": [{"range": [0, 35], "color": "#ff4f70"}, {"range": [35, 70], "color": "#ffad55"}, {"range": [70, 100], "color": "#38c691"}]}))
    layout = chart_layout(205)
    layout["margin"] = {"l": 25, "r": 25, "t": 15, "b": 0}
    fig.update_layout(**layout)
    return fig


st.set_page_config(page_title="HR Future Insights", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
load_css()

@st.cache_data
def load_data():
    return generate_hr_data(seed=settings.synthetic_seed), generate_department_snapshot(settings.synthetic_seed)

hr_data, departments = load_data()
scenario = load_scenario()
last, previous = hr_data.iloc[-1], hr_data.iloc[-13]

st.markdown('''<div class="efi-header"><div class="efi-brand"><div class="efi-mark">▲</div><div><b>ENGINEERING</b><small>THE DIGITAL TRANSFORMATION COMPANY</small></div></div>
<div class="efi-product"><b>HR Future Insights</b><span>AI-Powered Workforce Forecasting Platform</span></div>
<div class="efi-tagline">Dai dati di oggi alle persone di domani</div><div class="efi-profile"><span class="efi-search">⌕&nbsp;&nbsp; Cerca...</span><span class="efi-avatar">HR</span><span>HR Analytics</span></div></div>
<div class="efi-tabs"><span class="active">Overview</span><span>Headcount</span><span>Assenze</span><span>Payroll</span><span>Turnover</span><span>Analisi Reparti</span></div>''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="efi-side-brand">HR FUTURE<br><b>INSIGHTS</b></div>', unsafe_allow_html=True)
    st.page_link("app.py", label="Dashboard", icon="🏠")
    st.page_link("pages/1_Forecasting.py", label="Forecasting", icon="📈")
    st.page_link("pages/3_AI_Chat.py", label="AI Assistant", icon="✨")
    st.page_link("pages/2_Scenarios.py", label="Scenari", icon="🎛️")
    st.markdown('<div class="efi-side-bottom">AI for a<br><b>smarter tomorrow</b></div>', unsafe_allow_html=True)

cols = st.columns([1, 1, 1, 1, 1.25])
with cols[0]: kpi("👥", "Headcount", f"{int(last.headcount):,}".replace(",", "."), f"↗ {(last.headcount/previous.headcount-1)*100:+.1f}%".replace(".", ","), "positive", BLUE)
with cols[1]: kpi("▣", "Assenze", f"{int(last.absences)} gg/mese", f"↗ {(last.absences/previous.absences-1)*100:+.1f}%".replace(".", ","), "negative", PINK)
with cols[2]: kpi("⟳", "Turnover", f"{last.turnover:.1f}%".replace(".", ","), f"↘ {last.turnover-previous.turnover:+.1f} pp".replace(".", ","), "positive", CYAN)
with cols[3]: kpi("▤", "Costo del personale", f"€ {last.payroll/1e6:.1f} M".replace(".", ","), f"↗ {(last.payroll/previous.payroll-1)*100:+.1f}%".replace(".", ","), "positive", BLUE)
with cols[4]:
    st.markdown('<div class="efi-panel gauge-panel">', unsafe_allow_html=True); panel_title("Indice di rischio HR")
    st.plotly_chart(risk_gauge(48), use_container_width=True, config={"displayModeBar": False}); st.markdown('</div>', unsafe_allow_html=True)

main, ai = st.columns([3.25, 1.15], gap="medium")
with main:
    a, b = st.columns([2.1, 1], gap="medium")
    with a:
        st.markdown('<div class="efi-panel">', unsafe_allow_html=True); panel_title("Andamento Headcount", "Prossimi 24 mesi⌄")
        st.plotly_chart(headcount_chart(hr_data, scenario), use_container_width=True, config={"displayModeBar": False}); st.markdown('</div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="efi-panel">', unsafe_allow_html=True); panel_title("Distribuzione Headcount per area")
        st.plotly_chart(donut_chart(departments), use_container_width=True, config={"displayModeBar": False}); st.markdown('</div>', unsafe_allow_html=True)
    c, d = st.columns(2, gap="medium")
    with c:
        st.markdown('<div class="efi-panel">', unsafe_allow_html=True); panel_title("Previsione Assenze", "Prossimi 12 mesi⌄")
        st.plotly_chart(absence_chart(hr_data), use_container_width=True, config={"displayModeBar": False}); st.markdown('</div>', unsafe_allow_html=True)
    with d:
        st.markdown('<div class="efi-panel">', unsafe_allow_html=True); panel_title("Costo del personale", "Prossimi 24 mesi⌄")
        st.plotly_chart(payroll_chart(hr_data, scenario), use_container_width=True, config={"displayModeBar": False}); st.markdown('</div>', unsafe_allow_html=True)
    e, f = st.columns([1, 1.35], gap="medium")
    with e:
        st.markdown('<div class="efi-panel efi-turnover">', unsafe_allow_html=True); panel_title("Turnover per reparto", "vs anno precedente")
        for _, row in departments.sort_values("turnover", ascending=False).iterrows():
            width = min(float(row.turnover)/13*100, 100); color = PINK if row.turnover >= 10 else "#ffae58" if row.turnover >= 7 else GREEN
            st.markdown(f'<div class="efi-bar-row"><span>{row.department}</span><div class="efi-bar-track"><i style="width:{width:.0f}%;background:{color}"></i></div><b>{row.turnover:.1f}%</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with f:
        st.markdown('<div class="efi-panel efi-scenario">', unsafe_allow_html=True); panel_title("Scenario Simulator")
        left, right = st.columns([1.25, 1])
        with left:
            hires=st.slider("Nuove assunzioni",0,500,int(scenario["new_hires"]),10,key="dash_hires")
            salary=st.slider("Incremento salariale",0.0,10.0,float(scenario["salary_increase"]),.5,key="dash_salary")
            smart=st.slider("Smart Working",0,5,int(scenario["smart_working"]),key="dash_smart")
            retention=st.slider("Riduzione turnover",0.0,30.0,float(scenario["retention"]),1.0,key="dash_retention")
            if st.button("⚒  Genera Scenario", type="primary", use_container_width=True):
                save_scenario({"new_hires":hires,"salary_increase":salary,"smart_working":smart,"retention":retention}); st.rerun()
        with right:
            impact=calculate_payroll_scenario(float(last.payroll),hires,salary)
            st.markdown(f'''<div class="efi-impact"><b>Impatto previsto (12 mesi)</b><p><span>👥 Headcount</span><strong class="green">+{hires}</strong></p>
            <p><span>▤ Costo personale</span><strong class="red">+{impact['delta_percentage']:.1f}%</strong></p><p><span>◉ Assenze</span><strong class="green">-{smart*1.2:.1f}%</strong></p>
            <p><span>⟳ Turnover</span><strong class="green">-{retention:.1f}%</strong></p></div>'''.replace(".",","), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with ai:
    st.markdown('<div class="efi-panel efi-ai">', unsafe_allow_html=True); panel_title("✦  AI HR Assistant", "Nuova conversazione")
    st.markdown('<div class="efi-chat-user">Qual è il trend delle assenze<br>per i prossimi 6 mesi?</div><div class="efi-chat-time">10:24</div><div class="efi-chat-ai"><b>✦</b><div>Ecco l\'analisi delle assenze prevista per i prossimi 6 mesi.</div></div>', unsafe_allow_html=True)
    mini = absence_chart(hr_data, 6, 210)
    mini_layout = chart_layout(210); mini_layout["margin"] = {"l":34,"r":8,"t":12,"b":26}; mini.update_layout(**mini_layout)
    st.plotly_chart(mini, use_container_width=True, config={"displayModeBar": False})
    fc=seasonal_forecast(hr_data.absences,hr_data.date.iloc[-1],6); growth=(fc.median[-1]/max(float(last.absences),1)-1)*100
    st.markdown(f'<div class="efi-ai-text">È previsto un andamento delle assenze pari a <b>{growth:+.1f}%</b> sul periodo simulato. Il dato è sintetico e richiede validazione.</div><div class="efi-recommend"><b>Raccomandazioni</b><p>• Pianificare risorse aggiuntive nei mesi di picco</p><p>• Monitorare IT e Operations</p><p>• Valutare iniziative di wellbeing</p></div><div class="efi-chat-input">Scrivi la tua domanda... <span>➤</span></div>'.replace(".",","), unsafe_allow_html=True)
    models=OllamaService().list_models(); st.caption(f"Ollama locale: {'operativo · '+str(len(models))+' modelli' if models else 'non disponibile'}")
    st.page_link("pages/3_AI_Chat.py",label="Apri AI Assistant",icon="✨",use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div class="efi-footer"><span>© 2026 Engineering · HR Future Insights</span><span>Powered by Timestral & Ollama&nbsp;&nbsp;|&nbsp;&nbsp;Built for a smarter tomorrow</span></div>',unsafe_allow_html=True)
