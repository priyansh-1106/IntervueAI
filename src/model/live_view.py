def build_pip_html (ai_photo_url ):
    html =f"""
    <div style="position:relative; width:100%; aspect-ratio:16/10; border-radius:16px; overflow:hidden; background:#0b0f1e;">
        <img src="{ai_photo_url }"
             style="width:100%; height:100%; object-fit:cover; display:block;" />

        <video id="ia_webcam" autoplay muted playsinline
               style="position:absolute; bottom:16px; right:16px;
                      width:26%; max-width:220px; aspect-ratio:4/3; object-fit:cover;
                      transform:scaleX(-1); border-radius:12px;
                      border:3px solid #2f6fed; box-shadow:0 4px 14px rgba(0,0,0,0.4);
                      background:#000;">
        </video>

        <div id="ia_cam_error" style="position:absolute; bottom:16px; right:16px;
             width:26%; max-width:220px; padding:10px; border-radius:12px;
             background:#12172b; color:#aab2c8; font-size:12px; text-align:center;
             display:none;">
            Camera not available
        </div>
    </div>

    <script>
        const video = document.getElementById("ia_webcam");
        const errorBox = document.getElementById("ia_cam_error");

        navigator.mediaDevices.getUserMedia({{ video: true, audio: false }})
            .then(function (stream) {{
                video.srcObject = stream;
                video.onloadedmetadata = function () {{
                    video.play().catch(function () {{}});
                }};
                window.addEventListener("beforeunload", function () {{
                    stream.getTracks().forEach(function (track) {{ track.stop(); }});
                }});
            }})
            .catch(function (error) {{
                video.style.display = "none";
                errorBox.style.display = "block";
            }});
    </script>
    """
    return html 


def build_tab_switch_tracker_html ():
    html ="""
    <script>
        if (!window.ia_listener_added) {
            window.ia_listener_added = true;
            document.addEventListener("visibilitychange", function () {
                if (document.hidden) {
                    let current = parseInt(localStorage.getItem("ia_tab_switches") || "0");
                    localStorage.setItem("ia_tab_switches", current + 1);
                }
            });
        }
    </script>
    """
    return html 


def build_auto_speak_html (question_text ):
    safe_text =question_text .replace ("\\","\\\\").replace ('"','\\"').replace ("\n"," ")
    html =f"""
    <script>
        if ("speechSynthesis" in window) {{
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance("{safe_text }");
            utterance.rate = 0.98;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        }}
    </script>
    """
    return html 
