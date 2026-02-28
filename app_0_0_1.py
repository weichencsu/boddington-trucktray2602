import streamlit as st
from multipage import MultiPage
from spages import Golding830E2507
from streamlit.components.v1 import html

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


# 主页面
###############################################################################
def main_page():
    MAGE_EMOJI_URL = "streamlitbis.png"
    st.set_page_config(page_title='Bisalloy Digital App', page_icon=MAGE_EMOJI_URL, initial_sidebar_state = 'expanded')
    st.markdown(
            f"""
            <style>
                .reportview-container .main .block-container{{
                    max-width: 1800px;
                    padding-top: 0rem;
                    padding-right: 1rem;
                    padding-left: 1rem;
                    padding-bottom: 0rem;
                }}
    
            </style>
            """,
            unsafe_allow_html=True,
        )
    
    
    ####### Actual App Content ########
    app = MultiPage()
    # add applications
    app.add_page('🔵  Boddington Linerless Tray', Golding830E2507.app)
    #app.add_page('🟢  SAG Mill #2', SAG25NOV.app)
    app.run()

    # 在侧边栏显示已登录的用户信息
    if 'name' in st.session_state:
        st.sidebar.markdown("User Information")
        st.sidebar.caption(f"username: {st.session_state['name']}")
        st.sidebar.caption(f"account: {st.session_state['username']}")

    if st.sidebar.button("logout"):
        st.session_state['logged_in'] = False
        st.session_state.pop('name', None)
        st.session_state.pop('username', None)
        st.rerun()


# 登录页面
###############################################################################
def login_page():
    MAGE_EMOJI_URL = "streamlitbis.png"
    st.set_page_config(page_title='OptiWear®',page_icon=MAGE_EMOJI_URL, initial_sidebar_state = 'expanded', layout="centered")
    #page_icon = favicon,

    st.markdown(
                f"""
                <style>
                    .reportview-container .main .block-container{{
                        max-width: 1800px;
                        padding-top: 0rem;
                        padding-right: 1rem;
                        padding-left: 1rem;
                        padding-bottom: 0rem;
                    }}
        
                </style>
                """,
                unsafe_allow_html=True,
            )


    st.logo("bisalloy.png")
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    name, authentication_status, username = authenticator.login(':material/Apps: :rainbow[Bisalloy Digital App]', 'main')

    if authentication_status:
        
        st.success(f"Welcome Back!  {name}!")
        st.session_state['logged_in'] = True
        st.session_state['name'] = name  # 存储用户姓名
        st.session_state['username'] = username  # 存储用户名
        st.rerun()  # 刷新页面，跳转到主页面
                    #st.markdown(
                    #    '<nobr><p style="text-align: left;font-family:sans serif; color:#262730; font-size: 23px;">'
                    #    'Welcome to the app gallary. We share the past and most <br> '
                    #    'exciting IoT apps that have been deployed by our team. <br>'
                    #    'Simply click on each app’s URL to view the app.</p></nobr>',
                        #    unsafe_allow_html=True)

    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')



# 主程序
# Test Auto Deploy
###############################################################################
def main():
    # 初始化登录状态
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # 根据登录状态显示不同页面
    if st.session_state['logged_in']:
        #app.run()
        main_page()

    else:
        html_code = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Next Gen Truck Tray Intelligence</title>
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
                    <style>
                        :root {
                            --bg-color: #f0f4f8;
                            --text-primary: #1a2744;
                            --text-secondary: #2d5a87;
                            --accent-cyan: #00d4ff;
                            --accent-blue: #0066ff;
                            --accent-light: #66e0ff;
                            --glow-color: rgba(0, 212, 255, 0.5);
                            --shadow-color: rgba(26, 39, 68, 0.1);
                        }

                        * {
                            margin: 0;
                            padding: 0;
                            box-sizing: border-box;
                        }

                        body {
                            background: linear-gradient(135deg, #f0f4f8 0%, #e1e8f0 100%);
                            min-height: 100vh;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            font-family: 'Rajdhani', sans-serif;
                            overflow: hidden;
                            padding: 20px;
                        }

                        .container {
                            text-align: center;
                            position: relative;
                            max-width: 900px;
                            padding: 40px;
                        }

                        /* Background Grid Pattern */
                        .grid-bg {
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            background-image: 
                                linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
                                linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
                            background-size: 50px 50px;
                            animation: gridMove 20s linear infinite;
                            z-index: -1;
                        }

                        @keyframes gridMove {
                            0% { transform: translate(0, 0); }
                            100% { transform: translate(50px, 50px); }
                        }

                        /* Main Title */
                        .title {
                            font-family: 'Orbitron', sans-serif;
                            font-size: 3.5rem;
                            font-weight: 900;
                            text-transform: uppercase;
                            letter-spacing: 4px;
                            margin-bottom: 10px;
                            position: relative;
                            display: inline-block;
                        }

                        .title-line {
                            display: block;
                            overflow: hidden;
                        }

                        .title-char {
                            display: inline-block;
                            opacity: 0;
                            transform: translateY(30px);
                            background: linear-gradient(180deg, var(--text-primary) 0%, var(--text-secondary) 100%);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            animation: charReveal 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
                            position: relative;
                        }

                        .title-char::after {
                            content: attr(data-char);
                            position: absolute;
                            top: 0;
                            left: 0;
                            background: linear-gradient(180deg, var(--accent-cyan) 0%, var(--accent-blue) 100%);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            opacity: 0;
                            animation: charGlow 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
                            animation-delay: calc(var(--char-index) * 0.05s + 0.4s);
                        }

                        @keyframes charReveal {
                            to {
                                opacity: 1;
                                transform: translateY(0);
                            }
                        }

                        @keyframes charGlow {
                            0% { opacity: 0; filter: blur(10px); }
                            50% { opacity: 1; filter: blur(5px); }
                            100% { opacity: 0.3; filter: blur(0px); }
                        }

                        /* Subtitle */
                        .subtitle {
                            font-size: 1.5rem;
                            font-weight: 500;
                            color: var(--text-secondary);
                            letter-spacing: 8px;
                            text-transform: uppercase;
                            margin-top: 15px;
                            opacity: 0;
                            animation: fadeIn 1s ease forwards;
                            animation-delay: 1.5s;
                            position: relative;
                            display: inline-block;
                        }

                        .subtitle::before,
                        .subtitle::after {
                            content: '';
                            position: absolute;
                            top: 50%;
                            width: 60px;
                            height: 2px;
                            background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
                            animation: lineExpand 1s ease forwards;
                            animation-delay: 1.8s;
                        }

                        .subtitle::before {
                            left: -80px;
                            transform: translateX(-100%);
                        }

                        .subtitle::after {
                            right: -80px;
                            transform: translateX(100%);
                        }

                        @keyframes lineExpand {
                            to {
                                transform: translateX(0);
                            }
                        }

                        @keyframes fadeIn {
                            to {
                                opacity: 1;
                            }
                        }

                        /* Digital Particles */
                        .particles {
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            pointer-events: none;
                            overflow: hidden;
                        }

                        .particle {
                            position: absolute;
                            width: 4px;
                            height: 4px;
                            background: var(--accent-cyan);
                            border-radius: 50%;
                            opacity: 0;
                            box-shadow: 0 0 10px var(--glow-color);
                        }

                        /* Data Stream Effect */
                        .data-stream {
                            position: absolute;
                            width: 2px;
                            height: 100px;
                            background: linear-gradient(180deg, transparent, var(--accent-cyan), transparent);
                            opacity: 0;
                            animation: dataFall 3s ease-in-out infinite;
                        }

                        @keyframes dataFall {
                            0% {
                                transform: translateY(-100px);
                                opacity: 0;
                            }
                            20% {
                                opacity: 1;
                            }
                            80% {
                                opacity: 1;
                            }
                            100% {
                                transform: translateY(400px);
                                opacity: 0;
                            }
                        }

                        /* Pulse Ring */
                        .pulse-ring {
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            width: 100px;
                            height: 100px;
                            border: 2px solid var(--accent-cyan);
                            border-radius: 50%;
                            opacity: 0;
                            animation: pulse 2s ease-out infinite;
                        }

                        .pulse-ring:nth-child(2) {
                            animation-delay: 0.5s;
                        }

                        .pulse-ring:nth-child(3) {
                            animation-delay: 1s;
                        }

                        @keyframes pulse {
                            0% {
                                width: 100px;
                                height: 100px;
                                opacity: 0.8;
                            }
                            100% {
                                width: 600px;
                                height: 600px;
                                opacity: 0;
                            }
                        }

                        /* Scan Line */
                        .scan-line {
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 2px;
                            background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
                            opacity: 0.3;
                            animation: scanDown 4s ease-in-out infinite;
                            animation-delay: 2s;
                        }

                        @keyframes scanDown {
                            0%, 100% {
                                top: 0%;
                                opacity: 0;
                            }
                            10% {
                                opacity: 0.5;
                            }
                            90% {
                                opacity: 0.5;
                            }
                            100% {
                                top: 100%;
                                opacity: 0;
                            }
                        }

                        /* Responsive */
                        @media (max-width: 768px) {
                            .title {
                                font-size: 2rem;
                                letter-spacing: 2px;
                            }
                            .subtitle {
                                font-size: 1rem;
                                letter-spacing: 4px;
                            }
                            .subtitle::before,
                            .subtitle::after {
                                width: 30px;
                            }
                            .subtitle::before {
                                left: -50px;
                            }
                            .subtitle::after {
                                right: -50px;
                            }
                        }

                        @media (max-width: 480px) {
                            .title {
                                font-size: 1.5rem;
                            }
                            .subtitle {
                                font-size: 0.8rem;
                                letter-spacing: 2px;
                            }
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="grid-bg"></div>
                        <div class="scan-line"></div>
                        
                        <div class="pulse-ring"></div>
                        <div class="pulse-ring"></div>
                        <div class="pulse-ring"></div>
                        
                        <div class="particles" id="particles"></div>
                        
                        <h1 class="title">
                            <span class="title-line" id="line1"></span>
                            <span class="title-line" id="line2"></span>
                        </h1>
                        
                        <p class="subtitle">Digital Intelligence System</p>
                    </div>

                    <script>
                        // Split text into characters with animation delays
                        function animateText() {
                            const line1 = document.getElementById('line1');
                            const line2 = document.getElementById('line2');
                            
                            const text1 = "NEXT GEN";
                            const text2 = "TRUCK TRAY INTELLIGENCE";
                            
                            // Create characters for line 1
                            text1.split('').forEach((char, index) => {
                                const span = document.createElement('span');
                                span.className = 'title-char';
                                span.textContent = char === ' ' ? '\u00A0' : char;
                                span.setAttribute('data-char', char === ' ' ? '\u00A0' : char);
                                span.style.setProperty('--char-index', index);
                                span.style.animationDelay = `${index * 0.05}s`;
                                line1.appendChild(span);
                            });
                            
                            // Create characters for line 2
                            text2.split('').forEach((char, index) => {
                                const span = document.createElement('span');
                                span.className = 'title-char';
                                span.textContent = char === ' ' ? '\u00A0' : char;
                                span.setAttribute('data-char', char === ' ' ? '\u00A0' : char);
                                span.style.setProperty('--char-index', text1.length + index);
                                span.style.animationDelay = `${(text1.length + index) * 0.05}s`;
                                line2.appendChild(span);
                            });
                        }

                        // Create floating particles
                        function createParticles() {
                            const container = document.getElementById('particles');
                            const particleCount = 30;
                            
                            for (let i = 0; i < particleCount; i++) {
                                const particle = document.createElement('div');
                                particle.className = 'particle';
                                particle.style.left = `${Math.random() * 100}%`;
                                particle.style.top = `${Math.random() * 100}%`;
                                particle.style.animationDelay = `${Math.random() * 3}s`;
                                particle.style.opacity = Math.random() * 0.5 + 0.2;
                                
                                // Random movement animation
                                const duration = Math.random() * 3 + 2;
                                particle.style.transition = `all ${duration}s ease-in-out`;
                                
                                container.appendChild(particle);
                                
                                // Animate particles
                                setInterval(() => {
                                    const newX = Math.random() * 100;
                                    const newY = Math.random() * 100;
                                    particle.style.left = `${newX}%`;
                                    particle.style.top = `${newY}%`;
                                }, duration * 1000);
                            }
                        }

                        // Create data streams
                        function createDataStreams() {
                            const container = document.querySelector('.container');
                            const streamCount = 8;
                            
                            for (let i = 0; i < streamCount; i++) {
                                const stream = document.createElement('div');
                                stream.className = 'data-stream';
                                stream.style.left = `${Math.random() * 100}%`;
                                stream.style.animationDelay = `${Math.random() * 3}s`;
                                stream.style.height = `${Math.random() * 100 + 50}px`;
                                container.appendChild(stream);
                            }
                        }

                        // Initialize
                        document.addEventListener('DOMContentLoaded', () => {
                            animateText();
                            createParticles();
                            createDataStreams();
                        });
                    </script>
                </body>
                </html>
            """

        html(html_code, height=220)
        login_page()  # 显示登录页面




# Run application
if __name__ == '__main__':
    main()
