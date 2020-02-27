"""
@inproceedings{moattar2009simple,
  title={A simple but efficient real-time voice activity detection algorithm},
  author={Moattar, Mohammad H and Homayounpour, Mohammad M},
  booktitle={2009 17th European Signal Processing Conference},
  pages={2549--2553},
  year={2009},
  organization={IEEE}
}
"""

from vad import ActiveVoiceDetector

if __name__ == "__main__":
    active = ActiveVoiceDetector()
    active.vad()