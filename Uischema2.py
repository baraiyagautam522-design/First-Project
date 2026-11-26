import html
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Optional, List

load_dotenv()


class schema(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    Director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


parser = PydanticOutputParser(pydantic_object=schema)
tamplate = ChatPromptTemplate.from_messages([
    ("system", """
    Extract Movie Information from The Paragraph
    {formate}
    """),
    ("human", "{Paragraph}"),
])
model = ChatGroq(model="openai/gpt-oss-120b")


# ---------------------------------------------------------------- UI ---------
def e(value) -> str:
    """Escape model output before putting it inside HTML."""
    return html.escape(str(value))


st.set_page_config(page_title="CineScan - Movie Info Extractor", page_icon="🎬", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Source+Sans+3:wght@400;600&display=swap');

#MainMenu, footer, header {visibility: hidden;}
.stApp {
  background:
    radial-gradient(900px 500px at 85% -10%, rgba(255,64,129,.22), transparent 60%),
    radial-gradient(800px 500px at -10% 10%, rgba(255,193,7,.16), transparent 55%),
    #090c16;
  color: #e9edf5;
  font-family: 'Source Sans 3', sans-serif;
}
.block-container {max-width: 820px; padding-top: 2.2rem; padding-bottom: 4rem;}

/* hero */
.badge {display:inline-block; padding:5px 14px; border-radius:999px; font-size:.78rem; letter-spacing:.14em;
  text-transform:uppercase; color:#ffc107; border:1px solid rgba(255,193,7,.45); background:rgba(255,193,7,.08);}
.hero h1 {font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:3.2rem; line-height:1.05;
  margin:.9rem 0 .6rem; background:linear-gradient(95deg,#fff 10%,#ffc107 55%,#ff4081 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;}
.hero p {color:#9aa6b8; font-size:1.1rem; max-width:560px; margin:0 0 1.6rem;}
.strip {height:10px; margin:0 0 1.6rem; border-radius:3px; opacity:.55;
  background:repeating-linear-gradient(90deg,#fff 0 14px,transparent 14px 28px); -webkit-mask:linear-gradient(#000,#000);}

/* input */
.stTextArea label p {color:#c7d0de !important; font-weight:600; font-size:.95rem;}
.stTextArea textarea {background:rgba(255,255,255,.05) !important; color:#f2f5fa !important;
  border:1px solid rgba(255,255,255,.14) !important; border-radius:14px !important; padding:16px !important; font-size:1rem;}
.stTextArea textarea:focus {border-color:#ffc107 !important; box-shadow:0 0 0 3px rgba(255,193,7,.2) !important;}
.stTextArea textarea::placeholder {color:#6f7b8e !important;}

/* button */
div.stButton > button {width:100%; border:0; border-radius:14px; padding:.85rem 1rem; font-weight:700; font-size:1.05rem;
  font-family:'Bricolage Grotesque',sans-serif; color:#1b1200;
  background:linear-gradient(95deg,#ffc107,#ff9f43 50%,#ff4081); transition:transform .15s, box-shadow .15s;}
div.stButton > button:hover {transform:translateY(-2px); box-shadow:0 10px 30px rgba(255,100,100,.3); color:#1b1200;}
div.stButton > button:active {transform:translateY(0);}

/* result card */
.card {margin-top:2rem; padding:2rem; border-radius:22px; position:relative; overflow:hidden;
  background:linear-gradient(145deg,rgba(255,255,255,.08),rgba(255,255,255,.03));
  border:1px solid rgba(255,255,255,.12); box-shadow:0 30px 80px rgba(0,0,0,.45); animation:rise .55s ease both;}
.card::before {content:""; position:absolute; inset:0 0 auto 0; height:4px; background:linear-gradient(90deg,#ffc107,#ff4081,#7c4dff);}
@keyframes rise {from {opacity:0; transform:translateY(18px);} to {opacity:1; transform:none;}}
.top {display:flex; gap:24px; align-items:flex-start; justify-content:space-between;}
.year {font-size:.8rem; letter-spacing:.16em; text-transform:uppercase; color:#ffc107; font-weight:600;}
.title {font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:2.4rem; line-height:1.1; margin:.3rem 0 .9rem; color:#fff;}
.summary {color:#b4bfd0; line-height:1.65; font-size:1.02rem; margin:0;}
.ring {--p:0; flex:none; width:96px; height:96px; border-radius:50%; display:grid; place-items:center;
  background:conic-gradient(#ffc107 calc(var(--p) * 1%), rgba(255,255,255,.1) 0);}
.ring span {width:76px; height:76px; border-radius:50%; background:#12162a; display:grid; place-items:center;
  font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1.45rem; color:#fff;}
.ringlabel {text-align:center; font-size:.7rem; letter-spacing:.14em; text-transform:uppercase; color:#8793a6; margin-top:6px;}
.tiles {display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:14px; margin:1.8rem 0 1.4rem;}
.tile {padding:14px 16px; border-radius:14px; background:rgba(0,0,0,.25); border:1px solid rgba(255,255,255,.08);}
.label {font-size:.7rem; letter-spacing:.14em; text-transform:uppercase; color:#8793a6; margin-bottom:4px;}
.value {font-size:1.1rem; font-weight:600; color:#fff;}
.sec {margin-top:1.2rem;}
.pill {display:inline-block; margin:6px 8px 0 0; padding:6px 14px; border-radius:999px; font-size:.88rem; font-weight:600;
  color:#ffe29a; background:rgba(255,193,7,.1); border:1px solid rgba(255,193,7,.35);}
.actor {display:inline-flex; align-items:center; gap:10px; margin:8px 10px 0 0; padding:6px 16px 6px 6px; border-radius:999px;
  background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.1); color:#e9edf5; font-size:.92rem;}
.avatar {width:30px; height:30px; border-radius:50%; display:grid; place-items:center; font-weight:700; font-size:.8rem; color:#1b1200;
  background:linear-gradient(135deg,#ffc107,#ff4081);}
@media (max-width:640px) {.hero h1 {font-size:2.3rem;} .top {flex-direction:column-reverse;} .title {font-size:1.9rem;}}
</style>

<div class="hero">
  <span class="badge">AI Powered</span>
  <h1>CineScan</h1>
  <p>Paste any paragraph about a movie and watch it turn into a clean, structured profile.</p>
</div>
<div class="strip"></div>
""", unsafe_allow_html=True)

para = st.text_area(
    "Your paragraph",
    height=190,
    placeholder="e.g. Inception, released in 2010 and directed by Christopher Nolan, stars Leonardo DiCaprio "
                "and Elliot Page in a mind-bending heist through dreams...",
)

if st.button("🎬  Extract Movie Info"):
    if not para.strip():
        st.warning("Please paste a paragraph first.")
    else:
        with st.spinner("Rolling the film..."):
            final_prompt = tamplate.invoke(
                {"Paragraph": para, "formate": parser.get_format_instructions()}
            )
            output = model.invoke(final_prompt)

        try:
            movie = parser.parse(output.content)
        except Exception:
            st.error("Could not read the model's answer. Raw output is shown below.")
            st.code(output.content)
            st.stop()

        if movie.rating is not None:
            pct = movie.rating * 10 if movie.rating <= 10 else min(movie.rating, 100)
            ring = (f'<div><div class="ring" style="--p:{pct}"><span>{e(movie.rating)}</span></div>'
                    f'<div class="ringlabel">Rating</div></div>')
        else:
            ring = ""

        genres = "".join(f'<span class="pill">{e(g)}</span>' for g in movie.genre) or '<span class="value">N/A</span>'
        cast = "".join(
            f'<span class="actor"><span class="avatar">{e(c.strip()[:1].upper())}</span>{e(c)}</span>'
            for c in movie.cast
        ) or '<span class="value">N/A</span>'

        card = (
            '<div class="card">'
            '<div class="top"><div>'
            f'<div class="year">{e(movie.release_year) if movie.release_year else "Year unknown"}</div>'
            f'<div class="title">{e(movie.title)}</div>'
            f'<p class="summary">{e(movie.summary)}</p>'
            f'</div>{ring}</div>'
            '<div class="tiles">'
            f'<div class="tile"><div class="label">Director</div><div class="value">{e(movie.Director or "N/A")}</div></div>'
            f'<div class="tile"><div class="label">Release year</div><div class="value">{e(movie.release_year or "N/A")}</div></div>'
            '</div>'
            f'<div class="sec"><div class="label">Genre</div>{genres}</div>'
            f'<div class="sec"><div class="label">Cast</div>{cast}</div>'
            '</div>'
        )
        st.markdown(card, unsafe_allow_html=True)