import streamlit as st
import time
import datetime
import os
from io import BytesIO
import streamlit.components.v1 as components
import zipfile
import random

SAVE_DIR = "proctor_session_data"
os.makedirs(SAVE_DIR, exist_ok=True)

def proctor_mode_ui():
    if "photos" not in st.session_state:
        st.session_state.photos = []
    if "tab_switch_events" not in st.session_state:
        st.session_state.tab_switch_events = []
    if "last_capture_time" not in st.session_state:
        st.session_state.last_capture_time = 0
    if "last_cam_photo" not in st.session_state:
        st.session_state.last_cam_photo = None

    tab_switch_js = """
    <script>
    document.addEventListener('visibilitychange', function() {
        if(document.hidden){
            alert("🚨 You switched tabs or minimized! This has been logged.");
        }
    });
    </script>
    """
    components.html(tab_switch_js, height=0)

    with st.expander("📋 Proctoring Instructions", expanded=True):
        st.markdown("""
        - Keep your face visible to the webcam.
        - The app captures a photo every 30 seconds.
        - If you switch tabs or minimize, you will be alerted and must log it manually.
        - At the end, download all photos and logs as a ZIP file.
        """)

    # --- Live Webcam (Proctor Mode) ---
    cam_photo = st.camera_input("", key="proctor_cam_input")
    auto_capture = False
    if cam_photo:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_auto")
        # Only add if new photo (avoid duplicates)
        if not st.session_state.last_cam_photo or cam_photo.getvalue() != st.session_state.last_cam_photo.getvalue():
            st.session_state.photos.append((timestamp, cam_photo))
            with open(f"{SAVE_DIR}/photo_{timestamp}.png", "wb") as f:
                f.write(cam_photo.getbuffer())
            st.session_state.last_cam_photo = cam_photo
            st.session_state.last_capture_time = time.time()
            auto_capture = True
    # Show small live preview if available
    if st.session_state.last_cam_photo:
        st.image(st.session_state.last_cam_photo, width=100, caption="Live Preview")

    # --- Auto photo capture every 30 seconds (simulate with info) ---
    current_time = time.time()
    interval = 30
    if st.session_state.last_cam_photo:
        elapsed = current_time - st.session_state.last_capture_time
        if elapsed > interval:
            st.info(f"⏱️ It's time for an auto-capture! Please move or blink to refresh the webcam.")
            # The next cam_photo will be auto-captured by user interaction

    # --- Tab Switch Monitoring ---
    st.header("🧠 Tab Switch Monitoring")
    if st.button("🚨 I switched tab or minimized"):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.tab_switch_events.append(ts)
        with open(f"{SAVE_DIR}/tab_switch_log.txt", "a") as f:
            f.write(f"{ts}\n")
        st.warning(f"⚠️ Logged tab switch at {ts}")

    # Display tab switch events on frontend
    if st.session_state.tab_switch_events:
        st.subheader("🕒 Logged Tab Switch Events")
        for e in st.session_state.tab_switch_events:
            st.write(f"🔹 {e}")

    # --- Exam Termination Logic ---
    if len(st.session_state.tab_switch_events) > 3:
        st.error("🚨 Exam terminated: Too many tab switches detected.")
        # Generate interview report
        report = f"""
        # Interview Proctoring Report\n\n
        **Status:** Terminated due to excessive tab switches.\n
        **Tab Switch Events:**\n
        """ + "\n".join(st.session_state.tab_switch_events) + "\n\n" + \
        f"**Captured Photos:** {len(st.session_state.photos)}\n\n" + \
        "**Coding Section:**\n" + \
        f"Language: {st.session_state.get('proctor_lang_select', 'N/A')}\n" + \
        f"Question: {coding_question}\n" + \
        f"User Code:\n\n{code_input}\n\n" + \
        (f"Output:\n\n{code_output}\n\n" if code_output else "") + \
        (f"Error:\n\n{code_error}\n\n" if code_error else "")
        st.markdown(report)
        st.stop()

    # Display previews (small)
    if st.session_state.photos:
        st.subheader("🖼️ Captured Photos (Preview)")
        cols = st.columns(6)
        for idx, (ts, img) in enumerate(st.session_state.photos[-6:]):
            with cols[idx % 6]:
                st.image(img, caption=ts, width=80)

<<<<<<< HEAD
    # --- Coding Question Section ---
    dsa_questions = [
        ("Python", "Write a Python function to check if a string is a palindrome."),
        ("Python", "Write a Python function to find the nth Fibonacci number."),
    ]
    # Hidden test cases for each question
    hidden_tests = {
        dsa_questions[0][1]: [  # Palindrome
            ("racecar", True),
            ("hello", False),
            ("Aibohphobia", True),
            ("", True),
            ("12321", True),
        ],
        dsa_questions[1][1]: [  # Fibonacci
            (1, 1),
            (2, 1),
            (5, 5),
            (10, 55),
            (0, 0),
        ],
    }
    lang, coding_question = random.choice(dsa_questions)
    st.header(f"💻 Coding Challenge (Proctor Mode) [Python]")
    st.info(f"**Question:** {coding_question}")
    # Use session state to persist code
    if 'proctor_code_input' not in st.session_state:
        st.session_state['proctor_code_input'] = ''
    code_input = st.text_area(f"✍️ Write your code here (Python)", value=st.session_state['proctor_code_input'], height=200, key="proctor_code_input")
    code_output = None
    code_error = None
    test_results = None
    lang_options = ["Python"]
    selected_lang = st.selectbox("Select Language", lang_options, index=0, key="proctor_lang_select")
    if st.button("▶️ Run Code", key="proctor_run_code"):
        import io
        import contextlib
        user_code = code_input
        # Prepare to run hidden tests
        test_results = []
        if selected_lang == "Python":
            # Determine function name expected for each question
            if "palindrome" in coding_question.lower():
                func_name = "is_palindrome"
                test_cases = hidden_tests[coding_question]
                # User must define is_palindrome(s: str) -> bool
                code_to_exec = user_code + "\nresult = is_palindrome"
                for idx, (inp, expected) in enumerate(test_cases):
                    f = io.StringIO()
                    try:
                        local_vars = {}
                        exec(user_code, local_vars)
                        result = local_vars[func_name](inp)
                        passed = result == expected
                        test_results.append((idx+1, passed))
                    except Exception as e:
                        test_results.append((idx+1, False, str(e)))
            elif "fibonacci" in coding_question.lower():
                func_name = "fibonacci"
                test_cases = hidden_tests[coding_question]
                # User must define fibonacci(n: int) -> int
                for idx, (inp, expected) in enumerate(test_cases):
                    f = io.StringIO()
                    try:
                        local_vars = {}
                        exec(user_code, local_vars)
                        result = local_vars[func_name](inp)
                        passed = result == expected
                        test_results.append((idx+1, passed))
                    except Exception as e:
                        test_results.append((idx+1, False, str(e)))
            else:
                code_error = "Unknown question type."
    if code_output:
        st.success("Output:")
        st.code(code_output)
    if code_error:
        st.error(f"Error: {code_error}")
    if test_results is not None:
        st.subheader("🕵️ Hidden Test Cases Results")
        for idx, *result in test_results:
            if result[0]:
                st.success(f"Test Case {idx}: Passed")
            else:
                err = result[1] if len(result) > 1 else None
                if err:
                    st.error(f"Test Case {idx}: Error ({err})")
                else:
                    st.error(f"Test Case {idx}: Failed")
=======
    # --- Coding Question Section (Python only) ---
    questions = [
        "Write a Python function to check if a string is a palindrome.",
        "Write a Python function to find the nth Fibonacci number."
    ]
    coding_question = random.choice(questions)
    st.header("💻 Coding Challenge (Python)")
    st.info(f"**Question:** {coding_question}")
    # Persist user code
    default_code = st.session_state.get("proctor_code_input", "")
    code_input = st.text_area("✍️ Write your Python code here", value=default_code, height=200, key="proctor_code_input")
    code_output = None
    code_error = None
    if st.button("▶️ Run Code", key="proctor_run_code"):
        import io, contextlib
        try:
            # Execute user code and capture stdout
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                exec(code_input, {})
            code_output = f.getvalue()
        except Exception as e:
            code_error = str(e)
    if code_output is not None:
        st.subheader("Output")
        st.code(code_output)
    if code_error is not None:
        st.subheader("Error")
        st.error(code_error)
>>>>>>> 817da3f928a9f49abdcd427c309282572cb3a50c
