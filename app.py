import os
from pathlib import Path
import importlib.util

import streamlit as st

import auth
import admin_login
import admin_panel
import doctor_login
import farmer_dashboard
import support
import vet_dashboard

# Suppress TensorFlow logging if models are loaded by prediction modules
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

ROOT = Path(__file__).resolve().parent

MODULE_PATHS = {
    'Breed Prediction': ROOT / 'breed_predict.py',
    'Disease Prediction': ROOT / 'disease_predict.py',
    'My Requests': ROOT / 'pages' / 'my_requests.py'
}


def load_module(name: str, path: Path):
    """Lazily import a module from a file path and cache it in session state."""
    if 'loaded_modules' not in st.session_state:
        st.session_state.loaded_modules = {}

    if name in st.session_state.loaded_modules:
        return st.session_state.loaded_modules[name]

    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {name} from {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    st.session_state.loaded_modules[name] = module
    return module


def ensure_session_state():
    defaults = {
        'logged_in': False,
        'role': None,
        'user_id': None,
        'user_name': None,
        'page': 'Home'
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def apply_global_styles():
    st.markdown(
        r'''
        <style>
            body {
                background: #f5f7ff;
            }
            .stApp {
                color: #1b1f3b;
            }
            .hero-card {
                background: linear-gradient(135deg, rgba(102,126,234,0.12), rgba(118,75,162,0.08));
                border-radius: 28px;
                padding: 2rem 2rem 1.5rem;
                box-shadow: 0 24px 80px rgba(33, 45, 94, 0.08);
                border: 1px solid rgba(102, 126, 234, 0.14);
                margin-bottom: 1rem;
            }
            .feature-card {
                background: #ffffff;
                border-radius: 24px;
                padding: 1.5rem;
                box-shadow: 0 18px 45px rgba(16, 24, 72, 0.08);
                border: 1px solid rgba(99, 102, 241, 0.12);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .feature-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 24px 72px rgba(16, 24, 72, 0.12);
            }
            .feature-icon {
                font-size: 2.25rem;
                margin-bottom: 0.75rem;
                color: #4f46e5;
            }
            .stButton>button {
                border-radius: 999px;
                padding: 0.8rem 1.5rem;
                font-weight: 600;
                background: linear-gradient(90deg, #4338ca, #8b5cf6);
                color: white;
                border: none;
            }
            .stButton>button:hover {
                filter: brightness(1.05);
            }
            section[data-testid='stSidebar'] .css-1d391kg {
                background: linear-gradient(180deg, #4338ca, #5b21b6);
            }
            section[data-testid='stSidebar'] .css-1d391kg h1,
            section[data-testid='stSidebar'] .css-1d391kg p,
            section[data-testid='stSidebar'] .css-1d391kg span {
                color: #f8fafc;
            }
        </style>
        ''',
        unsafe_allow_html=True,
    )


def render_home():
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.markdown('## 🐄 Smart Vet Care', unsafe_allow_html=True)
    st.markdown('### AI-powered cattle breed and disease detection for farmers and veterinarians.')
    st.write('Welcome to an intelligent livestock care platform that makes veterinary guidance accessible and fast.')
    st.markdown('<div style="display:flex; gap:16px; flex-wrap:wrap; margin-top:1.25rem;">', unsafe_allow_html=True)
    st.markdown('<div style="flex:1; min-width:220px; background:rgba(255,255,255,0.95); border-radius:18px; padding:1rem;">✅ Fast image-based predictions</div>', unsafe_allow_html=True)
    st.markdown('<div style="flex:1; min-width:220px; background:rgba(255,255,255,0.95); border-radius:18px; padding:1rem;">✅ Instant AI guidance for disease care</div>', unsafe_allow_html=True)
    st.markdown('<div style="flex:1; min-width:220px; background:rgba(255,255,255,0.95); border-radius:18px; padding:1rem;">✅ History tracking and consultation requests</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write('---')

    st.markdown('#### What you can do:')
    cols = st.columns(3)
    cards = [
        ('🐮', 'Breed Detection', 'Identify cattle breeds from uploaded images.'),
        ('🦠', 'Disease Detection', 'Detect FMD, LSD or healthy cattle in seconds.'),
        ('💬', 'Vet Consultation', 'Submit cases directly for expert review.')
    ]
    for col, (icon, title, desc) in zip(cols, cards):
        col.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><h4>{title}</h4><p style="color:#4b5563;">{desc}</p></div>', unsafe_allow_html=True)

    st.write('---')
    st.markdown('#### Quick start')
    st.write('1. Create a farmer account or login with existing credentials.')
    st.write('2. Open the Farmer Dashboard to access prediction tools.')
    st.write('3. Submit a consultation request when you need veterinary advice.')
    st.write('4. Doctors and admins can login through the sidebar.')


def main():
    st.set_page_config(
        page_title='Smart Vet Care',
        page_icon='🐄',
        layout='wide'
    )

    apply_global_styles()
    ensure_session_state()

    if st.session_state.logged_in:
        if st.session_state.role == 'doctor':
            default_pages = ['Vet Dashboard']
        elif st.session_state.role == 'admin':
            default_pages = ['Admin Panel']
        else:
            default_pages = [
                'Farmer Dashboard',
                'Breed Prediction',
                'Disease Prediction',
                'Support',
                'My Requests'
            ]
    else:
        default_pages = ['Home', 'Login', 'Register', 'Doctor Login', 'Admin Login']

    sidebar_title = 'Navigation'
    st.sidebar.title('Smart Vet Care')
    st.sidebar.markdown('Manage cattle breed, disease, and consultation workflows.')

    if st.session_state.logged_in:
        st.sidebar.markdown(f'**Logged in as:** {st.session_state.user_name}')
        st.sidebar.markdown(f'**Role:** {st.session_state.role.capitalize()}')
        if st.sidebar.button('Logout'):
            logout()

    page = st.sidebar.selectbox('Choose a page', default_pages, index=max(0, default_pages.index(st.session_state.page)) if st.session_state.page in default_pages else 0)
    st.session_state.page = page

    if not st.session_state.logged_in:
        if page == 'Home':
            render_home()
        elif page == 'Login':
            auth.login()
            if st.session_state.logged_in:
                if st.session_state.role == 'doctor':
                    st.session_state.page = 'Vet Dashboard'
                elif st.session_state.role == 'admin':
                    st.session_state.page = 'Admin Panel'
                else:
                    st.session_state.page = 'Farmer Dashboard'
                st.rerun()
        elif page == 'Register':
            auth.register()
        elif page == 'Doctor Login':
            doctor_login.app()
            if st.session_state.logged_in and st.session_state.role == 'doctor':
                st.session_state.page = 'Vet Dashboard'
                st.rerun()
        elif page == 'Admin Login':
            admin_login.app()
            if st.session_state.logged_in and st.session_state.role == 'admin':
                st.session_state.page = 'Admin Panel'
                st.rerun()
    else:
        if st.session_state.role == 'doctor':
            if page == 'Vet Dashboard':
                vet_dashboard.app()
            else:
                st.warning('Unknown page for doctor role.')
        elif st.session_state.role == 'admin':
            if page == 'Admin Panel':
                admin_panel.app()
            else:
                st.warning('Unknown page for admin role.')
        else:
            if page == 'Farmer Dashboard':
                farmer_dashboard.app()
            elif page == 'Breed Prediction':
                module = load_module('breed_predict', MODULE_PATHS['Breed Prediction'])
                module.app()
            elif page == 'Disease Prediction':
                module = load_module('disease_predict', MODULE_PATHS['Disease Prediction'])
                module.app()
            elif page == 'Support':
                support.app()
            elif page == 'My Requests':
                module = load_module('my_requests', MODULE_PATHS['My Requests'])
                module.app()
            else:
                st.warning('Page not found. Please choose a valid item from the sidebar.')


if __name__ == '__main__':
    main()
