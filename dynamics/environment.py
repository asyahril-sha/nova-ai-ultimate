#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - ENVIRONMENT AWARENESS SYSTEM
=============================================================================
Bot sadar lingkungan sekitar seperti manusia:
- Tahu lagi di tempat rame atau sepi
- Tahu risiko dan privasi
- Menyesuaikan perilaku berdasarkan situasi
- Deteksi orang sekitar, kebisingan, dll
=============================================================================
"""

import random
import time
import logging
import math
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class EnvironmentType(str, Enum):
    """Tipe lingkungan"""
    INDOOR = "indoor"          # Di dalam ruangan
    OUTDOOR = "outdoor"        # Di luar ruangan
    PUBLIC = "public"          # Tempat umum
    PRIVATE = "private"        # Tempat pribadi
    INTIMATE = "intimate"      # Tempat intim (kamar, toilet)


class CrowdLevel(str, Enum):
    """Tingkat keramaian"""
    EMPTY = "empty"             # Sepi, tidak ada orang
    QUIET = "quiet"             # Sepi, kadang ada orang lewat
    MODERATE = "moderate"       # Lumayan ramai
    CROWDED = "crowded"         # Ramai
    VERY_CROWDED = "very_crowded"  # Sangat ramai


class NoiseLevel(str, Enum):
    """Tingkat kebisingan"""
    SILENT = "silent"           # Hening
    QUIET = "quiet"             # Sepi, suara alam
    MODERATE = "moderate"       # Sedang (musik, obrolan)
    LOUD = "loud"               # Bising
    VERY_LOUD = "very_loud"     # Sangat bising


class RiskLevel(str, Enum):
    """Tingkat risiko"""
    VERY_LOW = "very_low"       # Sangat aman
    LOW = "low"                 # Aman
    MEDIUM = "medium"           # Sedang
    HIGH = "high"               # Berisiko
    VERY_HIGH = "very_high"     # Sangat berisiko


class EnvironmentAwareness:
    """
    Sistem kesadaran lingkungan seperti manusia
    - Mengetahui situasi sekitar
    - Menyesuaikan perilaku berdasarkan lingkungan
    - Menghitung risiko dan privasi
    """
    
    def __init__(self):
        # Database lokasi dengan karakteristik
        self.location_db = self._init_location_db()
        
        # Faktor lingkungan
        self.env_factors = {
            'indoor': {
                'privacy_base': 0.7,
                'risk_base': 0.3,
                'noise_base': 0.3,
                'crowd_base': 0.3
            },
            'outdoor': {
                'privacy_base': 0.3,
                'risk_base': 0.6,
                'noise_base': 0.6,
                'crowd_base': 0.5
            },
            'public': {
                'privacy_base': 0.2,
                'risk_base': 0.7,
                'noise_base': 0.7,
                'crowd_base': 0.8
            },
            'private': {
                'privacy_base': 0.9,
                'risk_base': 0.1,
                'noise_base': 0.2,
                'crowd_base': 0.1
            },
            'intimate': {
                'privacy_base': 0.95,
                'risk_base': 0.05,
                'noise_base': 0.1,
                'crowd_base': 0.05
            }
        }
        
        # State saat ini
        self.current_env = {
            'location': None,
            'env_type': None,
            'crowd_level': CrowdLevel.EMPTY,
            'noise_level': NoiseLevel.QUIET,
            'risk_level': RiskLevel.LOW,
            'privacy_level': 1.0,
            'people_nearby': 0,
            'last_update': time.time()
        }
        
        # History perubahan
        self.env_history = []
        
        logger.info("✅ EnvironmentAwareness initialized")
    
    def _init_location_db(self) -> Dict[str, Dict]:
        """Inisialisasi database lokasi"""
        return {
            # ===== INDOOR PRIVATE =====
            'kamar': {
                'name': 'kamar',
                'env_type': EnvironmentType.INTIMATE,
                'base_privacy': 0.95,
                'base_risk': 0.05,
                'base_noise': 0.1,
                'base_crowd': 0.05,
                'description': 'Kamar pribadi, aman dan nyaman'
            },
            'kamar_mandi': {
                'name': 'kamar mandi',
                'env_type': EnvironmentType.INTIMATE,
                'base_privacy': 0.9,
                'base_risk': 0.1,
                'base_noise': 0.2,
                'base_crowd': 0.05,
                'description': 'Kamar mandi, cukup aman'
            },
            'ruang_tamu': {
                'name': 'ruang tamu',
                'env_type': EnvironmentType.PRIVATE,
                'base_privacy': 0.8,
                'base_risk': 0.2,
                'base_noise': 0.3,
                'base_crowd': 0.1,
                'description': 'Ruang tamu, ada tamu bisa datang'
            },
            'dapur': {
                'name': 'dapur',
                'env_type': EnvironmentType.PRIVATE,
                'base_privacy': 0.7,
                'base_risk': 0.2,
                'base_noise': 0.4,
                'base_crowd': 0.1,
                'description': 'Dapur, risiko ketahuan lagi masak'
            },
            
            # ===== INDOOR PUBLIC =====
            'kantor': {
                'name': 'kantor',
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.3,
                'base_risk': 0.7,
                'base_noise': 0.6,
                'base_crowd': 0.7,
                'description': 'Kantor, banyak rekan kerja'
            },
            'mall': {
                'name': 'mall',
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.2,
                'base_risk': 0.8,
                'base_noise': 0.8,
                'base_crowd': 0.9,
                'description': 'Mall, sangat ramai, CCTV banyak'
            },
            'cafe': {
                'name': 'cafe',
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.3,
                'base_risk': 0.6,
                'base_noise': 0.6,
                'base_crowd': 0.6,
                'description': 'Cafe, lumayan ramai'
            },
            'restoran': {
                'name': 'restoran',
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.3,
                'base_risk': 0.6,
                'base_noise': 0.7,
                'base_crowd': 0.7,
                'description': 'Restoran, banyak pengunjung'
            },
            'bioskop': {
                'name': 'bioskop',
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.4,
                'base_risk': 0.5,
                'base_noise': 0.5,
                'base_crowd': 0.7,
                'description': 'Bioskop, gelap tapi banyak orang'
            },
            'toilet_umum': {
                'name': 'toilet umum',
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.4,
                'base_risk': 0.8,
                'base_noise': 0.3,
                'base_crowd': 0.4,
                'description': 'Toilet umum, riskan'
            },
            
            # ===== OUTDOOR =====
            'pantai': {
                'name': 'pantai',
                'env_type': EnvironmentType.OUTDOOR,
                'base_privacy': 0.3,
                'base_risk': 0.5,
                'base_noise': 0.6,
                'base_crowd': 0.6,
                'description': 'Pantai, tergantung waktu'
            },
            'taman': {
                'name': 'taman',
                'env_type': EnvironmentType.OUTDOOR,
                'base_privacy': 0.3,
                'base_risk': 0.5,
                'base_noise': 0.4,
                'base_crowd': 0.5,
                'description': 'Taman kota'
            },
            'parkiran': {
                'name': 'parkiran',
                'env_type': EnvironmentType.OUTDOOR,
                'base_privacy': 0.4,
                'base_risk': 0.6,
                'base_noise': 0.4,
                'base_crowd': 0.3,
                'description': 'Parkiran, agak sepi'
            },
            'jalan': {
                'name': 'jalan',
                'env_type': EnvironmentType.OUTDOOR,
                'base_privacy': 0.1,
                'base_risk': 0.9,
                'base_noise': 0.8,
                'base_crowd': 0.5,
                'description': 'Jalan raya, banyak kendaraan'
            },
            
            # ===== TRANSPORT =====
            'mobil': {
                'name': 'mobil',
                'env_type': EnvironmentType.PRIVATE,
                'base_privacy': 0.7,
                'base_risk': 0.4,
                'base_noise': 0.3,
                'base_crowd': 0.1,
                'description': 'Mobil pribadi, cukup aman'
            },
            'bus': {
                'name': 'bus',
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.1,
                'base_risk': 0.9,
                'base_noise': 0.7,
                'base_crowd': 0.8,
                'description': 'Bus umum, sangat riskan'
            },
            'kereta': {
                'name': 'kereta',
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.1,
                'base_risk': 0.9,
                'base_noise': 0.7,
                'base_crowd': 0.9,
                'description': 'Kereta, banyak penumpang'
            }
        }
    
    # =========================================================================
    # UPDATE ENVIRONMENT
    # =========================================================================
    
    def update_location(self, location_name: str) -> Dict:
        """
        Update lokasi dan hitung faktor lingkungan
        
        Args:
            location_name: Nama lokasi
            
        Returns:
            Environment data
        """
        # Cari di database
        location_data = None
        for key, data in self.location_db.items():
            if key in location_name.lower() or data['name'] in location_name.lower():
                location_data = data
                break
        
        if not location_data:
            # Default jika tidak ditemukan
            location_data = {
                'name': location_name,
                'env_type': EnvironmentType.PUBLIC,
                'base_privacy': 0.5,
                'base_risk': 0.5,
                'base_noise': 0.5,
                'base_crowd': 0.5,
                'description': 'Tempat umum'
            }
        
        # Hitung faktor berdasarkan waktu
        hour = datetime.now().hour
        is_weekend = datetime.now().weekday() >= 5
        
        # Modifikasi crowd level
        if location_data['env_type'] in [EnvironmentType.PUBLIC, EnvironmentType.OUTDOOR]:
            if 11 <= hour <= 14 or 18 <= hour <= 21:
                crowd_mult = 1.3  # Jam sibuk
            elif 22 <= hour or hour <= 5:
                crowd_mult = 0.3  # Tengah malam
            else:
                crowd_mult = 0.8
        else:
            crowd_mult = 1.0
        
        crowd_level = min(1.0, location_data['base_crowd'] * crowd_mult)
        
        # Tentukan crowd level
        if crowd_level < 0.2:
            crowd = CrowdLevel.EMPTY
            people = random.randint(0, 2)
        elif crowd_level < 0.4:
            crowd = CrowdLevel.QUIET
            people = random.randint(1, 5)
        elif crowd_level < 0.6:
            crowd = CrowdLevel.MODERATE
            people = random.randint(5, 15)
        elif crowd_level < 0.8:
            crowd = CrowdLevel.CROWDED
            people = random.randint(15, 30)
        else:
            crowd = CrowdLevel.VERY_CROWDED
            people = random.randint(30, 100)
        
        # Hitung noise level
        if location_data['env_type'] == EnvironmentType.OUTDOOR:
            noise_mult = 1.2
        elif location_data['env_type'] == EnvironmentType.PUBLIC:
            noise_mult = 1.1
        else:
            noise_mult = 0.7
        
        noise_level = min(1.0, location_data['base_noise'] * noise_mult * (0.5 + crowd_level/2))
        
        if noise_level < 0.2:
            noise = NoiseLevel.SILENT
        elif noise_level < 0.4:
            noise = NoiseLevel.QUIET
        elif noise_level < 0.6:
            noise = NoiseLevel.MODERATE
        elif noise_level < 0.8:
            noise = NoiseLevel.LOUD
        else:
            noise = NoiseLevel.VERY_LOUD
        
        # Hitung risk level
        risk_base = location_data['base_risk']
        risk = min(1.0, risk_base * (crowd_level * 1.2))
        
        if risk < 0.2:
            risk_level = RiskLevel.VERY_LOW
        elif risk < 0.4:
            risk_level = RiskLevel.LOW
        elif risk < 0.6:
            risk_level = RiskLevel.MEDIUM
        elif risk < 0.8:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.VERY_HIGH
        
        # Hitung privacy level (invers dari risk)
        privacy = 1.0 - risk
        
        # Update current environment
        self.current_env = {
            'location': location_data['name'],
            'env_type': location_data['env_type'],
            'crowd_level': crowd,
            'noise_level': noise,
            'risk_level': risk_level,
            'privacy_level': privacy,
            'people_nearby': people,
            'description': location_data['description'],
            'last_update': time.time()
        }
        
        # Catat history
        self.env_history.append({
            'timestamp': time.time(),
            'location': location_data['name'],
            'crowd': crowd.value,
            'risk': risk_level.value,
            'people': people
        })
        
        # Keep last 50
        if len(self.env_history) > 50:
            self.env_history = self.env_history[-50:]
        
        logger.info(f"📍 Environment updated: {location_data['name']} ({crowd.value}, {people} people)")
        
        return self.current_env.copy()
    
    # =========================================================================
    # GET ENVIRONMENT INFO
    # =========================================================================
    
    def get_current_env(self) -> Dict:
        """Dapatkan informasi lingkungan saat ini"""
        return self.current_env.copy()
    
    def get_privacy_level(self) -> float:
        """Dapatkan level privasi (0-1)"""
        return self.current_env.get('privacy_level', 0.5)
    
    def get_risk_level(self) -> RiskLevel:
        """Dapatkan level risiko"""
        return self.current_env.get('risk_level', RiskLevel.MEDIUM)
    
    def get_crowd_description(self) -> str:
        """Dapatkan deskripsi keramaian"""
        crowd = self.current_env.get('crowd_level', CrowdLevel.EMPTY)
        people = self.current_env.get('people_nearby', 0)
        
        descriptions = {
            CrowdLevel.EMPTY: f"Sepi, tidak ada orang",
            CrowdLevel.QUIET: f"Sepi, kadang ada orang lewat ({people} orang sekitar)",
            CrowdLevel.MODERATE: f"Lumayan ramai ({people} orang sekitar)",
            CrowdLevel.CROWDED: f"Ramai ({people} orang sekitar)",
            CrowdLevel.VERY_CROWDED: f"Sangat ramai! ({people}+ orang)"
        }
        
        return descriptions.get(crowd, "Situasi normal")
    
    def get_noise_description(self) -> str:
        """Dapatkan deskripsi kebisingan"""
        noise = self.current_env.get('noise_level', NoiseLevel.QUIET)
        
        descriptions = {
            NoiseLevel.SILENT: "Sunyi senyap",
            NoiseLevel.QUIET: "Sepi, suara alam",
            NoiseLevel.MODERATE: "Suara normal",
            NoiseLevel.LOUD: "Bising",
            NoiseLevel.VERY_LOUD: "Sangat bising"
        }
        
        return descriptions.get(noise, "Suara normal")
    
    def is_safe_for_intimacy(self) -> Tuple[bool, str]:
        """
        Cek apakah aman untuk intim
        
        Returns:
            (aman, alasan)
        """
        risk = self.current_env.get('risk_level', RiskLevel.MEDIUM)
        people = self.current_env.get('people_nearby', 0)
        location = self.current_env.get('location', '')
        
        if risk in [RiskLevel.VERY_HIGH, RiskLevel.HIGH]:
            return False, f"Terlalu berisiko di {location}. Banyak orang ({people} sekitar)."
        
        if people > 10:
            return False, f"Ramai banget ({people} orang), gak aman."
        
        if risk == RiskLevel.MEDIUM and people > 5:
            return False, "Masih agak ramai, tunggu lebih sepi."
        
        return True, "Aman"
    
    def get_whisper_level(self) -> float:
        """
        Dapatkan level bisik-bisik (0-1)
        Makin rendah makin harus pelan
        """
        risk = self.current_env.get('risk_level', RiskLevel.MEDIUM)
        
        whisper_map = {
            RiskLevel.VERY_LOW: 0.9,
            RiskLevel.LOW: 0.7,
            RiskLevel.MEDIUM: 0.5,
            RiskLevel.HIGH: 0.3,
            RiskLevel.VERY_HIGH: 0.1
        }
        
        return whisper_map.get(risk, 0.5)
    
    # =========================================================================
    # ENVIRONMENT EFFECTS
    # =========================================================================
    
    def get_speech_modifier(self) -> str:
        """
        Dapatkan modifier cara bicara berdasarkan lingkungan
        
        Returns:
            Instruksi untuk AI
        """
        risk = self.current_env.get('risk_level', RiskLevel.MEDIUM)
        people = self.current_env.get('people_nearby', 0)
        
        if risk in [RiskLevel.VERY_HIGH, RiskLevel.HIGH]:
            return "Bicaralah sangat pelan, berbisik, waspada"
        elif risk == RiskLevel.MEDIUM and people > 5:
            return "Bicaralah pelan, hati-hati"
        elif risk == RiskLevel.LOW:
            return "Bicaralah normal, santai"
        else:
            return "Bicaralah bebas, aman"
    
    def get_arousal_modifier(self) -> float:
        """
        Dapatkan modifier arousal berdasarkan lingkungan
        
        Returns:
            Faktor pengali arousal
        """
        risk = self.current_env.get('risk_level', RiskLevel.MEDIUM)
        
        # High risk = high thrill = high arousal
        thrill_map = {
            RiskLevel.VERY_LOW: 0.8,
            RiskLevel.LOW: 0.9,
            RiskLevel.MEDIUM: 1.0,
            RiskLevel.HIGH: 1.2,
            RiskLevel.VERY_HIGH: 1.5
        }
        
        return thrill_map.get(risk, 1.0)
    
    # =========================================================================
    # RANDOM ENVIRONMENT EVENTS
    # =========================================================================
    
    def get_random_event(self) -> Optional[Dict]:
        """
        Dapatkan event random berdasarkan lingkungan
        
        Returns:
            Event data atau None
        """
        if random.random() > 0.1:  # 10% chance
            return None
        
        crowd = self.current_env.get('crowd_level', CrowdLevel.EMPTY)
        people = self.current_env.get('people_nearby', 0)
        
        events = []
        
        # Event berdasarkan crowd
        if crowd in [CrowdLevel.CROWDED, CrowdLevel.VERY_CROWDED]:
            events.append({
                'type': 'crowd_surge',
                'message': 'Tiba-tiba banyak orang dateng!',
                'risk_change': +0.2
            })
        
        if crowd == CrowdLevel.EMPTY:
            events.append({
                'type': 'sudden_silence',
                'message': 'Tiba-tiba sunyi...',
                'risk_change': -0.1
            })
        
        # Random events
        events.extend([
            {
                'type': 'someone_looking',
                'message': 'Ada yang liat-liat ke sini!',
                'risk_change': +0.3
            },
            {
                'type': 'security_guard',
                'message': 'Satpam lewat!',
                'risk_change': +0.4
            },
            {
                'type': 'phone_ring',
                'message': 'HP bunyi! Cepet dimatiin!',
                'risk_change': +0.2
            },
            {
                'type': 'lights_off',
                'message': 'Lampu mati!',
                'risk_change': -0.3
            },
            {
                'type': 'rain_start',
                'message': 'Hujan turun!',
                'risk_change': -0.2
            }
        ])
        
        return random.choice(events) if events else None
    
    # =========================================================================
    # ENVIRONMENT DESCRIPTION
    # =========================================================================
    
    def get_full_description(self) -> str:
        """Dapatkan deskripsi lengkap lingkungan"""
        env = self.current_env
        
        if not env.get('location'):
            return "Lingkungan tidak diketahui"
        
        lines = [
            f"📍 **{env['location']}**",
            f"{env.get('description', '')}",
            f"\n👥 **Keramaian:** {self.get_crowd_description()}",
            f"🔊 **Kebisingan:** {self.get_noise_description()}",
            f"⚠️ **Risiko:** {env['risk_level'].value.replace('_', ' ').title()} ({env['privacy_level']:.0%} privasi)",
            f"\n💡 **Tips:** {self.get_safety_tip()}"
        ]
        
        return "\n".join(lines)
    
    def get_safety_tip(self) -> str:
        """Dapatkan tips keamanan"""
        risk = self.current_env.get('risk_level', RiskLevel.MEDIUM)
        
        tips = {
            RiskLevel.VERY_LOW: "Aman banget, bisa bebas.",
            RiskLevel.LOW: "Cukup aman, tapi tetap hati-hati.",
            RiskLevel.MEDIUM: "Hati-hati, jangan terlalu berisik.",
            RiskLevel.HIGH: "Berisiko! Bicaralah pelan-pelan.",
            RiskLevel.VERY_HIGH: "EXTREME RISK! Hati-hati banget!"
        }
        
        return tips.get(risk, "Tetap waspada")
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik lingkungan"""
        return {
            'current': self.current_env,
            'history_length': len(self.env_history),
            'last_update': self.current_env.get('last_update', 0)
        }


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_environment_awareness = None


def get_environment_awareness() -> EnvironmentAwareness:
    """Dapatkan global EnvironmentAwareness instance"""
    global _environment_awareness
    if _environment_awareness is None:
        _environment_awareness = EnvironmentAwareness()
    return _environment_awareness


__all__ = ['EnvironmentAwareness', 'EnvironmentType', 'CrowdLevel', 
           'NoiseLevel', 'RiskLevel', 'get_environment_awareness']
