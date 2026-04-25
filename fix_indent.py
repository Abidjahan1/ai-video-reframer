import re
content = open(r'O:\pythonproject\smart-video-reframer\gui\controller.py', 'r', encoding='utf-8').read()

new_section = '''def _on_play_pause(self):
    """
    Handle Play/Pause button click.
    """
    if self.video_display is None:
        return

    if self.video_display.is_playing:
        self.video_display.pause()
        if hasattr(self.main_window, 'play_btn'):
            self.main_window.play_btn.configure(text="▶ Play")
        self.logger.info("Playback paused")
    else:
        self.video_display.play()
        if hasattr(self.main_window, 'play_btn'):
            self.main_window.play_btn.configure(text="⏸ Pause")
        self.logger.info("Playback started")

def _on_timeline_change'''

pattern = r'def _on_play_pause\(self\):.*?def _on_timeline_change'
content = re.sub(pattern, new_section, content, flags=re.DOTALL)

open(r'O:\pythonproject\smart-video-reframer\gui\controller.py', 'w', encoding='utf-8').write(content)
print('Fixed')