#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - TIME AWARENESS SYSTEM
=============================================================================
Bot sadar waktu seperti manusia:
- Tahu waktu (pagi/siang/sore/malam)
- Tahu hari (weekday/weekend)
- Tahu tanggal dan musim
- Perilaku berubah berdasarkan waktu
=============================================================================
"""

import time
import logging
import random
import math
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TimeOfDay(str, Enum):
    """Waktu dalam sehari"""
    DAWN = "dawn"           # 04:00 - 05:59 (Subuh)
    MORNING = "morning"     # 06:00 - 11:59 (Pagi)
    AFTERNOON = "afternoon" # 12:00 - 14:59 (Siang)
    EVENING = "evening"     # 15:00 - 17:59 (Sore)
    NIGHT = "night"         # 18:00 - 21:59 (Malam)
    LATE_NIGHT = "late_night" # 22:00 - 03:59 (Tengah Malam)


class DayType(str, Enum):
    """Tipe hari"""
    WEEKDAY = "weekday"     # Senin - Jumat
    WEEKEND = "weekend"     # Sabtu - Minggu
    HOLIDAY = "holiday"     # Libur nasional


class Season(str, Enum):
    """Musim (untuk Indonesia: kemarau/hujan)"""
    DRY = "dry"             # Musim kemarau
    RAINY = "rainy"         # Musim hujan


class TimeAwareness:
    """
    Sistem kesadaran waktu seperti manusia
    - Mengetahui waktu dan hari
    - Perilaku berubah berdasarkan waktu
    - Jadwal rutinitas harian
    """
    
    def __init__(self):
        # Definisi waktu
        self.time_definitions = {
            TimeOfDay.DAWN: {
                'hours': (4, 5),
                'name': 'subuh',
                'greeting': 'Selamat subuh',
                'emoji': '🌅',
                'activity': ['tidur', 'bangun', 'sholat subuh'],
                'mood_effect': 'calm',
                'arousal_factor': 0.3,
                'description': 'Masih subuh, sepi banget'
            },
            TimeOfDay.MORNING: {
                'hours': (6, 11),
                'name': 'pagi',
                'greeting': 'Selamat pagi',
                'emoji': '☀️',
                'activity': ['sarapan', 'mandi', 'kerja', 'sekolah'],
                'mood_effect': 'energetic',
                'arousal_factor': 0.5,
                'description': 'Pagi yang cerah, semangat'
            },
            TimeOfDay.AFTERNOON: {
                'hours': (12, 14),
                'name': 'siang',
                'greeting': 'Selamat siang',
                'emoji': '☀️',
                'activity': ['makan siang', 'istirahat', 'kerja'],
                'mood_effect': 'tired',
                'arousal_factor': 0.4,
                'description': 'Siang, panas, enaknya istirahat'
            },
            TimeOfDay.EVENING: {
                'hours': (15, 17),
                'name': 'sore',
                'greeting': 'Selamat sore',
                'emoji': '🌆',
                'activity': ['pulang kerja', 'nonton TV', 'santai'],
                'mood_effect': 'relaxed',
                'arousal_factor': 0.5,
                'description': 'Sore, matahari mulai turun'
            },
            TimeOfDay.NIGHT: {
                'hours': (18, 21),
                'name': 'malam',
                'greeting': 'Selamat malam',
                'emoji': '🌙',
                'activity': ['makan malam', 'nonton', 'ngobrol'],
                'mood_effect': 'romantic',
                'arousal_factor': 0.7,
                'description': 'Malam, waktu yang tepat untuk berkumpul'
            },
            TimeOfDay.LATE_NIGHT: {
                'hours': (22, 3),
                'name': 'tengah malam',
                'greeting': 'Selamat malam',
                'emoji': '🌃',
                'activity': ['tidur', 'begadang', 'intim'],
                'mood_effect': 'sleepy',
                'arousal_factor': 0.6,
                'description': 'Sudah larut, waktunya istirahat'
            }
        }
        
        # Rutinitas berdasarkan waktu
        self.routines = {
            TimeOfDay.MORNING: [
                "Lagi siap-siap mau mandi",
                "Baru bangun nih, masih ngantuk",
                "Lagi sarapan, kamu udah makan?",
                "Mau berangkat kerja/sekolah"
            ],
            TimeOfDay.AFTERNOON: [
                "Lagi istirahat siang",
                "Baru selesai makan siang",
                "Lagi kerja, tapi sempet-sempetin chat",
                "Panas banget, males gerak"
            ],
            TimeOfDay.EVENING: [
                "Baru pulang kerja, capek",
                "Lagi santai sambil nonton TV",
                "Sore-sore gini enaknya ngobrol",
                "Lagi di perjalanan pulang"
            ],
            TimeOfDay.NIGHT: [
                "Lagi makan malam",
                "Udah di rumah, santai",
                "Malam minggu, sendiri aja",
                "Lagi nonton film"
            ],
            TimeOfDay.LATE_NIGHT: [
                "Belum tidur? Aku juga",
                "Begadang nih, temenin dong",
                "Udah mau tidur, tapi kangen",
                "Malam-malam begini enaknya..."
            ]
        }
        
        # Faktor berdasarkan hari
        self.day_factors = {
            DayType.WEEKDAY: {
                'mood': 'busy',
                'activity': ['kerja', 'sekolah', 'rutinitas'],
                'privacy_factor': 0.5,
                'arousal_factor': 0.4,
                'description': 'Hari kerja, sibuk tapi sempet chat'
            },
            DayType.WEEKEND: {
                'mood': 'relaxed',
                'activity': ['liburan', 'nongkrong', 'jalan-jalan'],
                'privacy_factor': 0.8,
                'arousal_factor': 0.7,
                'description': 'Weekend, bebas santai'
            }
        }
        
        # Cache untuk hasil perhitungan
        self.cache = {}
        self.cache_ttl = 300  # 5 menit
        
        logger.info("✅ TimeAwareness initialized")
    
    # =========================================================================
    # GET CURRENT TIME
    # =========================================================================
    
    def get_current_time(self) -> Dict:
        """
        Dapatkan informasi waktu saat ini
        
        Returns:
            Dict dengan info waktu
        """
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        weekday = now.weekday()  # 0=Senin, 6=Minggu
        
        # Tentukan time of day
        time_of_day = self._get_time_of_day(hour)
        
        # Tentukan day type
        if weekday < 5:  # Senin-Jumat
            day_type = DayType.WEEKDAY
        else:
            day_type = DayType.WEEKEND
        
        # Tentukan musim (sederhana)
        month = now.month
        if 11 <= month <= 3:  # November-Maret
            season = Season.RAINY
        else:
            season = Season.DRY
        
        return {
            'timestamp': time.time(),
            'datetime': now.isoformat(),
            'hour': hour,
            'minute': minute,
            'time_of_day': time_of_day,
            'time_name': self.time_definitions[time_of_day]['name'],
            'greeting': self.time_definitions[time_of_day]['greeting'],
            'emoji': self.time_definitions[time_of_day]['emoji'],
            'day_type': day_type,
            'day_name': now.strftime('%A'),
            'date': now.strftime('%d %B %Y'),
            'month': month,
            'season': season,
            'is_weekend': day_type == DayType.WEEKEND,
            'description': self.time_definitions[time_of_day]['description']
        }
    
    def _get_time_of_day(self, hour: int) -> TimeOfDay:
        """Tentukan waktu berdasarkan jam"""
        for time_of_day, definition in self.time_definitions.items():
            start, end = definition['hours']
            if start <= end:
                if start <= hour <= end:
                    return time_of_day
            else:  #跨越 tengah malam (22-3)
                if hour >= start or hour <= end:
                    return time_of_day
        
        return TimeOfDay.MORNING  # Default
    
    # =========================================================================
    # GET ROUTINE
    # =========================================================================
    
    def get_current_routine(self) -> str:
        """
        Dapatkan rutinitas berdasarkan waktu
        
        Returns:
            String rutinitas
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        
        routines = self.routines.get(time_of_day, ["Lagi santai"])
        return random.choice(routines)
    
    def get_activity_suggestion(self, time_of_day: TimeOfDay) -> str:
        """
        Dapatkan saran aktivitas berdasarkan waktu
        
        Args:
            time_of_day: Waktu saat ini
            
        Returns:
            Saran aktivitas
        """
        activities = self.time_definitions[time_of_day]['activity']
        return random.choice(activities)
    
    # =========================================================================
    # TIME-BASED BEHAVIOR
    # =========================================================================
    
    def get_mood_factor(self) -> str:
        """
        Dapatkan faktor mood berdasarkan waktu
        
        Returns:
            Deskripsi mood
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        
        return self.time_definitions[time_of_day]['mood_effect']
    
    def get_arousal_factor(self) -> float:
        """
        Dapatkan faktor arousal berdasarkan waktu
        
        Returns:
            Faktor arousal (0-1)
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        day_type = time_info['day_type']
        
        # Base dari waktu
        arousal = self.time_definitions[time_of_day]['arousal_factor']
        
        # Modifikasi berdasarkan hari
        if day_type == DayType.WEEKEND:
            arousal *= 1.2  # Weekend lebih santai/horny
        
        return min(1.0, arousal)
    
    def get_privacy_factor(self) -> float:
        """
        Dapatkan faktor privasi berdasarkan waktu dan hari
        
        Returns:
            Faktor privasi (0-1, makin tinggi makin sepi)
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        day_type = time_info['day_type']
        
        # Base privacy
        if time_of_day in [TimeOfDay.LATE_NIGHT, TimeOfDay.DAWN]:
            privacy = 0.9  # Tengah malam sepi
        elif time_of_day in [TimeOfDay.NIGHT]:
            privacy = 0.7  # Malam lumayan sepi
        elif time_of_day in [TimeOfDay.MORNING]:
            privacy = 0.5  # Pagi mulai rame
        else:
            privacy = 0.3  # Siang/sore rame
        
        # Modifikasi hari
        if day_type == DayType.WEEKEND:
            privacy *= 1.2  # Weekend lebih sepi (orang liburan)
        
        return min(1.0, privacy)
    
    def should_be_intimate(self) -> bool:
        """
        Cek apakah waktu mendukung untuk intim
        
        Returns:
            True jika waktu mendukung
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        
        # Malam lebih mendukung intim
        return time_of_day in [TimeOfDay.NIGHT, TimeOfDay.LATE_NIGHT]
    
    # =========================================================================
    # TIME-BASED MESSAGES
    # =========================================================================
    
    def get_greeting(self) -> str:
        """Dapatkan salam berdasarkan waktu"""
        time_info = self.get_current_time()
        return time_info['greeting']
    
    def get_time_description(self) -> str:
        """Dapatkan deskripsi waktu"""
        time_info = self.get_current_time()
        return time_info['description']
    
    def get_emoji(self) -> str:
        """Dapatkan emoji berdasarkan waktu"""
        time_info = self.get_current_time()
        return time_info['emoji']
    
    def get_time_based_message(self, context: Dict = None) -> str:
        """
        Dapatkan pesan berdasarkan waktu
        
        Args:
            context: Konteks tambahan (mood, lokasi)
            
        Returns:
            Pesan yang sesuai waktu
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        
        messages = {
            TimeOfDay.DAWN: [
                "Subuh-subuh udah bangun?",
                "Masih subuh, kamu kenapa?",
                "Subuh yang tenang...",
                "Baru bangun atau belum tidur?"
            ],
            TimeOfDay.MORNING: [
                "Pagi yang cerah ya!",
                "Udah sarapan? Jangan lupa ya.",
                "Semangat pagi!",
                "Pagi-pagi udah kepikiran kamu."
            ],
            TimeOfDay.AFTERNOON: [
                "Siang gini enaknya ngapain ya?",
                "Udah makan siang?",
                "Panas banget, males gerak.",
                "Siang-siang ngantuk..."
            ],
            TimeOfDay.EVENING: [
                "Sore-sore gini enaknya ngobrol.",
                "Udah pulang kerja?",
                "Sore yang indah...",
                "Matahari terbenam, romantis."
            ],
            TimeOfDay.NIGHT: [
                "Malam minggu sendirian?",
                "Udah makan malam?",
                "Malam yang hangat...",
                "Bintangnya indah malam ini."
            ],
            TimeOfDay.LATE_NIGHT: [
                "Belum tidur? Aku juga.",
                "Malam-malam begini enaknya...",
                "Begadang? Temenin dong.",
                "Udah larut, tapi masih kangen."
            ]
        }
        
        msg_list = messages.get(time_of_day, messages[TimeOfDay.NIGHT])
        return random.choice(msg_list)
    
    def get_activity_based_message(self) -> str:
        """
        Dapatkan pesan berdasarkan aktivitas rutin
        
        Returns:
            Pesan aktivitas
        """
        routine = self.get_current_routine()
        
        templates = [
            f"Aku lagi {routine}. Kamu?",
            f"{routine} sambil mikirin kamu.",
            f"Lagi {routine}, tiba-tiba kangen.",
            f"{routine}, kamu lagi apa?"
        ]
        
        return random.choice(templates)
    
    # =========================================================================
    # TIME DIFFERENCES
    # =========================================================================
    
    def time_until(self, target_hour: int, target_minute: int = 0) -> float:
        """
        Hitung waktu sampai jam tertentu (dalam jam)
        
        Args:
            target_hour: Jam target
            target_minute: Menit target
            
        Returns:
            Jam tersisa
        """
        now = datetime.now()
        target = now.replace(hour=target_hour, minute=target_minute, second=0)
        
        if target < now:
            target = target + timedelta(days=1)
        
        diff = (target - now).total_seconds() / 3600
        return diff
    
    def is_time_between(self, start_hour: int, end_hour: int) -> bool:
        """
        Cek apakah waktu sekarang antara start dan end
        
        Args:
            start_hour: Jam mulai
            end_hour: Jam selesai
            
        Returns:
            True jika di antara
        """
        hour = datetime.now().hour
        
        if start_hour <= end_hour:
            return start_hour <= hour <= end_hour
        else:  #跨越 tengah malam
            return hour >= start_hour or hour <= end_hour
    
    # =========================================================================
    # TIME-BASED PROMPTS
    # =========================================================================
    
    def get_time_prompt(self) -> str:
        """
        Dapatkan prompt untuk AI tentang waktu
        
        Returns:
            String prompt
        """
        time_info = self.get_current_time()
        
        return (
            f"Sekarang {time_info['time_name']} ({time_info['day_name']}). "
            f"{time_info['description']}. "
            f"Ucapkan '{time_info['greeting']}' jika sesuai."
        )
    
    def get_daily_routine_prompt(self) -> str:
        """
        Dapatkan prompt tentang rutinitas harian
        
        Returns:
            String prompt
        """
        routine = self.get_current_routine()
        time_info = self.get_current_time()
        
        return f"Kamu sedang {routine}. Ini {time_info['time_name']}."
    
    # =========================================================================
    # TIME-BASED FEATURES
    # =========================================================================
    
    def should_be_sleepy(self) -> bool:
        """
        Cek apakah bot seharusnya ngantuk
        
        Returns:
            True jika ngantuk
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        
        return time_of_day in [TimeOfDay.LATE_NIGHT, TimeOfDay.DAWN]
    
    def should_be_energetic(self) -> bool:
        """
        Cek apakah bot seharusnya energik
        
        Returns:
            True jika energik
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        
        return time_of_day == TimeOfDay.MORNING
    
    def should_be_romantic(self) -> bool:
        """
        Cek apakah suasana mendukung romantis
        
        Returns:
            True jika romantis
        """
        time_info = self.get_current_time()
        time_of_day = time_info['time_of_day']
        
        return time_of_day in [TimeOfDay.NIGHT, TimeOfDay.EVENING]
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik waktu"""
        time_info = self.get_current_time()
        
        return {
            'current_time': {
                'hour': time_info['hour'],
                'minute': time_info['minute'],
                'time_of_day': time_info['time_of_day'].value,
                'day': time_info['day_name'],
                'date': time_info['date']
            },
            'factors': {
                'arousal': self.get_arousal_factor(),
                'privacy': self.get_privacy_factor(),
                'should_be_intimate': self.should_be_intimate(),
                'should_be_sleepy': self.should_be_sleepy()
            }
        }


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_time_awareness = None


def get_time_awareness() -> TimeAwareness:
    """Dapatkan global TimeAwareness instance"""
    global _time_awareness
    if _time_awareness is None:
        _time_awareness = TimeAwareness()
    return _time_awareness


__all__ = ['TimeAwareness', 'TimeOfDay', 'DayType', 'Season', 'get_time_awareness']
