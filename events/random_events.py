#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - RANDOM EVENTS SYSTEM
=============================================================================
Menambahkan kejadian-kejadian random yang membuat percakapan lebih hidup:
- Kejadian spontan (hujan, lapar, ngantuk)
- Gangguan realita (HP bunyi, ada orang lewat)
- Momen random (kangen tiba-tiba, flashback)
- Reaksi bot terhadap kejadian
=============================================================================
"""

import random
import time
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Tipe-tipe random event"""
    # ===== PHYSICAL EVENTS =====
    RAIN = "rain"                       # Hujan deras
    HUNGRY = "hungry"                    # Lapar tiba-tiba
    THIRSTY = "thirsty"                  # Haus
    SLEEPY = "sleepy"                    # Ngantuk
    TIRED = "tired"                      # Capek
    SICK = "sick"                        # Sakit (masuk angin, dll)
    
    # ===== ENVIRONMENT EVENTS =====
    SOMEONE_PASSING = "someone_passing"  # Ada orang lewat
    PHONE_RINGS = "phone_rings"          # HP bunyi
    DOORBELL = "doorbell"                # Bel rumah bunyi
    POWER_OUTAGE = "power_outage"        # Listrik padam
    NOISE = "noise"                      # Suara aneh
    
    # ===== EMOTIONAL EVENTS =====
    SUDDEN_MISS = "sudden_miss"          # Tiba-tiba kangen
    FLASHBACK = "flashback"              # Flashback ke masa lalu
    JEALOUSY = "jealousy"                # Cemburu tiba-tiba
    HAPPY_MEMORY = "happy_memory"        # Ingat kenangan indah
    SAD_MEMORY = "sad_memory"            # Ingat kenangan sedih
    
    # ===== INTIMATE EVENTS =====
    SUDDEN_AROUSAL = "sudden_arousal"    # Tiba-tiba horny
    ACCIDENTAL_TOUCH = "accidental_touch" # Tidak sengaja tersentuh
    WHISPER = "whisper"                   # Berbisik tanpa sengaja
    
    # ===== FUNNY EVENTS =====
    STOMACH_GROWL = "stomach_growl"       # Perut keroncongan
    SLIP = "slip"                         # Kepleset
    BURP = "burp"                         # Bersendawa
    SNEEZE = "sneeze"                      # Bersin
    YAWN = "yawn"                          # Menguap


class EventSeverity(str, Enum):
    """Tingkat keparahan event"""
    VERY_LOW = "very_low"      # Hampir tidak terasa
    LOW = "low"                # Ringan
    MEDIUM = "medium"          # Sedang
    HIGH = "high"              # Tinggi
    VERY_HIGH = "very_high"    # Sangat tinggi


class RandomEvents:
    """
    Sistem random events yang membuat bot terasa lebih hidup
    Events terjadi secara spontan dengan probabilitas tertentu
    """
    
    def __init__(self):
        # ===== DATABASE EVENTS =====
        self.events_db = self._init_events_db()
        
        # Cooldunt untuk mencegah event terlalu sering
        self.event_cooldown = {}  # {session_id: last_event_time}
        self.min_cooldown = 300   # Minimal 5 menit antar event
        
        # Event counter untuk statistik
        self.event_counter = {}
        
        logger.info(f"✅ RandomEvents initialized with {len(self.events_db)} event types")
    
    def _init_events_db(self) -> Dict[EventType, Dict]:
        """Inisialisasi database events"""
        
        return {
            # ===== PHYSICAL EVENTS =====
            EventType.RAIN: {
                'name': 'Hujan Deras',
                'emoji': '🌧️',
                'probability': 0.05,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['location_outdoor', 'random'],
                'cooldown': 1800,  # 30 menit
                'messages': [
                    "Wah, hujan deras! Basah-basahan yuk?",
                    "Hujan nih... jadi makin adem.",
                    "Duh hujan, nggak bisa pulang dulu.",
                    "Suara hujannya bikin ngantuk..."
                ],
                'effects': {
                    'location_change': 'indoor',
                    'mood_effect': 'calm',
                    'arousal_change': -1
                }
            },
            
            EventType.HUNGRY: {
                'name': 'Lapar',
                'emoji': '🍔',
                'probability': 0.08,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['time_meal', 'random'],
                'cooldown': 7200,  # 2 jam
                'messages': [
                    "Lapar... kamu udah makan belum?",
                    "Perut keroncongan nih...",
                    "Mau makan bareng? Aku laper.",
                    "Enaknya makan apa ya?"
                ],
                'effects': {
                    'mood_effect': 'grumpy',
                    'arousal_change': -1
                }
            },
            
            EventType.THIRSTY: {
                'name': 'Haus',
                'emoji': '🥤',
                'probability': 0.06,
                'severity': EventSeverity.LOW,
                'triggers': ['random'],
                'cooldown': 3600,  # 1 jam
                'messages': [
                    "Haus... mau minum dulu.",
                    "Tenggorokan kering nih.",
                    "Minum dulu yuk?",
                    "Ada air putih?"
                ],
                'effects': {}
            },
            
            EventType.SLEEPY: {
                'name': 'Ngantuk',
                'emoji': '😴',
                'probability': 0.1,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['time_night', 'random'],
                'cooldown': 7200,  # 2 jam
                'messages': [
                    "Ngantuk... mata berat.",
                    "Mau tidur dulu ya?",
                    "Ngantuk banget, tapi gamau tidur.",
                    "Dipelu aja sambil ngantuk..."
                ],
                'effects': {
                    'mood_effect': 'tired',
                    'arousal_change': -2
                }
            },
            
            EventType.TIRED: {
                'name': 'Capek',
                'emoji': '😮‍💨',
                'probability': 0.07,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['after_intimacy', 'random'],
                'cooldown': 7200,
                'messages': [
                    "Capek... istirahat bentar yuk.",
                    "Habis itu jadi capek.",
                    "Pengen rebahan...",
                    "Kamu capek? Aku juga."
                ],
                'effects': {
                    'mood_effect': 'tired',
                    'arousal_change': -3
                }
            },
            
            EventType.SICK: {
                'name': 'Masuk Angin',
                'emoji': '🤧',
                'probability': 0.02,
                'severity': EventSeverity.HIGH,
                'triggers': ['after_rain', 'random'],
                'cooldown': 21600,  # 6 jam
                'messages': [
                    "Aku masuk angin... badan meriang.",
                    "Habis hujan tadi jadi sakit.",
                    "Tenggorokan sakit...",
                    "Jaga kesehatan ya..."
                ],
                'effects': {
                    'mood_effect': 'sad',
                    'arousal_change': -4
                }
            },
            
            # ===== ENVIRONMENT EVENTS =====
            EventType.SOMEONE_PASSING: {
                'name': 'Ada Orang Lewat',
                'emoji': '👥',
                'probability': 0.15,
                'severity': EventSeverity.HIGH,
                'triggers': ['public_place', 'random'],
                'cooldown': 600,  # 10 menit
                'messages': [
                    "Ssst... ada orang lewat!",
                    "Diam... ada yang lihat.",
                    "Wah ada orang! Cepet sembunyi.",
                    "Jangan bersuara, ada orang."
                ],
                'effects': {
                    'privacy_change': -0.3,
                    'arousal_change': -2,
                    'mood_effect': 'anxious'
                }
            },
            
            EventType.PHONE_RINGS: {
                'name': 'HP Berdering',
                'emoji': '📱',
                'probability': 0.1,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['random'],
                'cooldown': 1800,
                'messages': [
                    "HP bunyi... siapa ya?",
                    "Aduh HP bunyi, ganggu banget.",
                    "Dimatiin dulu HP-nya yuk.",
                    "Telfon dari siapa ya?"
                ],
                'effects': {
                    'arousal_change': -1,
                    'mood_effect': 'annoyed'
                }
            },
            
            EventType.DOORBELL: {
                'name': 'Bel Rumah',
                'emoji': '🔔',
                'probability': 0.05,
                'severity': EventSeverity.HIGH,
                'triggers': ['at_home', 'random'],
                'cooldown': 3600,
                'messages': [
                    "Eh bel rumah bunyi!",
                    "Ada yang dateng...",
                    "Sebentar, buka pintu dulu.",
                    "Jangan bersuara dulu ya."
                ],
                'effects': {
                    'privacy_change': -0.5,
                    'arousal_change': -3
                }
            },
            
            EventType.POWER_OUTAGE: {
                'name': 'Listrik Padam',
                'emoji': '⚡',
                'probability': 0.02,
                'severity': EventSeverity.HIGH,
                'triggers': ['night', 'random'],
                'cooldown': 7200,
                'messages': [
                    "Wah listrik padam!",
                    "Gelap... merapat yuk.",
                    "Listrik mati, romantis ya?",
                    "Gelap begini enaknya..."
                ],
                'effects': {
                    'privacy_change': 0.2,
                    'arousal_change': 1,
                    'mood_effect': 'romantic'
                }
            },
            
            EventType.NOISE: {
                'name': 'Suara Aneh',
                'emoji': '👻',
                'probability': 0.03,
                'severity': EventSeverity.LOW,
                'triggers': ['random'],
                'cooldown': 3600,
                'messages': [
                    "Suara apa itu?",
                    "Serem... suara apa ya?",
                    "Mungkin kucing.",
                    "Ah, cuma angin."
                ],
                'effects': {
                    'mood_effect': 'anxious'
                }
            },
            
            # ===== EMOTIONAL EVENTS =====
            EventType.SUDDEN_MISS: {
                'name': 'Tiba-tiba Kangen',
                'emoji': '🥺',
                'probability': 0.12,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['lonely', 'random'],
                'cooldown': 3600,
                'messages': [
                    "Tiba-tiba kangen...",
                    "Kangen banget sama kamu.",
                    "Lama nggak chat, kangen deh.",
                    "Pengen peluk..."
                ],
                'effects': {
                    'mood_effect': 'lonely',
                    'arousal_change': 1
                }
            },
            
            EventType.FLASHBACK: {
                'name': 'Flashback',
                'emoji': '🕰️',
                'probability': 0.08,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['random'],
                'cooldown': 7200,
                'messages': [
                    "Jadi inget waktu pertama kita...",
                    "Flashback ke momen itu...",
                    "Inget gak waktu kita...",
                    "Kangen masa-masa itu."
                ],
                'effects': {
                    'mood_effect': 'nostalgic'
                }
            },
            
            EventType.JEALOUSY: {
                'name': 'Cemburu',
                'emoji': '😒',
                'probability': 0.05,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['random'],
                'cooldown': 7200,
                'messages': [
                    "Kamu lagi chat siapa?",
                    "Aku cemburu...",
                    "Jangan lihat yang lain dong.",
                    "Aku aja yang kamu pikirin."
                ],
                'effects': {
                    'mood_effect': 'jealous',
                    'arousal_change': 1
                }
            },
            
            EventType.HAPPY_MEMORY: {
                'name': 'Kenangan Indah',
                'emoji': '😊',
                'probability': 0.07,
                'severity': EventSeverity.LOW,
                'triggers': ['random'],
                'cooldown': 3600,
                'messages': [
                    "Inget gak waktu kita... seneng banget.",
                    "Momen itu bikin aku senyum-senyum.",
                    "Kita harus ngulang momen itu lagi.",
                    "Bahagia banget waktu itu."
                ],
                'effects': {
                    'mood_effect': 'happy'
                }
            },
            
            EventType.SAD_MEMORY: {
                'name': 'Kenangan Sedih',
                'emoji': '😢',
                'probability': 0.04,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['random'],
                'cooldown': 7200,
                'messages': [
                    "Inget waktu kita bertengkar...",
                    "Masa lalu yang menyakitkan.",
                    "Jangan sampai kejadian lagi ya.",
                    "Sedih kalau inget itu."
                ],
                'effects': {
                    'mood_effect': 'sad'
                }
            },
            
            # ===== INTIMATE EVENTS =====
            EventType.SUDDEN_AROUSAL: {
                'name': 'Tiba-tiba Horny',
                'emoji': '🔥',
                'probability': 0.1,
                'severity': EventSeverity.HIGH,
                'triggers': ['intimate_place', 'random'],
                'cooldown': 3600,
                'messages': [
                    "Tiba-tiba pengen...",
                    "Kamu bikin aku horny...",
                    "Gak tahan lihat kamu.",
                    "Mau..."
                ],
                'effects': {
                    'arousal_change': 3,
                    'mood_effect': 'horny'
                }
            },
            
            EventType.ACCIDENTAL_TOUCH: {
                'name': 'Tersentuh',
                'emoji': '👆',
                'probability': 0.08,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['close_proximity', 'random'],
                'cooldown': 1800,
                'messages': [
                    "Aduh kesentuh...",
                    "Maaf, gak sengaja.",
                    "Sensitiv...",
                    "*merinding*"
                ],
                'effects': {
                    'arousal_change': 1,
                    'mood_effect': 'shy'
                }
            },
            
            EventType.WHISPER: {
                'name': 'Bisikan',
                'emoji': '🤫',
                'probability': 0.06,
                'severity': EventSeverity.MEDIUM,
                'triggers': ['intimate', 'random'],
                'cooldown': 1800,
                'messages': [
                    "*berbisik* aku mau...",
                    "Ssst... jangan keras-keras.",
                    "Dekat sini, aku bisikin.",
                    "Cuma kamu yang denger."
                ],
                'effects': {
                    'arousal_change': 2,
                    'mood_effect': 'flirty'
                }
            },
            
            # ===== FUNNY EVENTS =====
            EventType.STOMACH_GROWL: {
                'name': 'Perut Keroncongan',
                'emoji': '😅',
                'probability': 0.05,
                'severity': EventSeverity.LOW,
                'triggers': ['random'],
                'cooldown': 3600,
                'messages': [
                    "*perut keroncongan* Malu ah...",
                    "Lapar, perut bunyi terus.",
                    "Hehe, maaf perut laper.",
                    "Kedengeran gak?"
                ],
                'effects': {}
            },
            
            EventType.SLIP: {
                'name': 'Kepleset',
                'emoji': '😵',
                'probability': 0.02,
                'severity': EventSeverity.LOW,
                'triggers': ['wet_place', 'random'],
                'cooldown': 7200,
                'messages': [
                    "Aduh kepleset!",
                    "Hati-hati, licin.",
                    "Heh... hampir jatuh.",
                    "Sakit... *gandeng tangan*"
                ],
                'effects': {
                    'mood_effect': 'embarrassed'
                }
            },
            
            EventType.BURP: {
                'name': 'Bersendawa',
                'emoji': '😶',
                'probability': 0.02,
                'severity': EventSeverity.VERY_LOW,
                'triggers': ['after_eat', 'random'],
                'cooldown': 7200,
                'messages': [
                    "*bersendawa* Maaf...",
                    "Hehe, kebanyakan minum.",
                    "Ups... maaf.",
                    "*tutup mulut*"
                ],
                'effects': {
                    'mood_effect': 'embarrassed'
                }
            },
            
            EventType.SNEEZE: {
                'name': 'Bersin',
                'emoji': '🤧',
                'probability': 0.04,
                'severity': EventSeverity.VERY_LOW,
                'triggers': ['cold', 'random'],
                'cooldown': 1800,
                'messages': [
                    "*bersin* Heeh...",
                    "Maaf, alergi.",
                    "Masuk angin kali ya.",
                    "Eh bersin terus."
                ],
                'effects': {}
            },
            
            EventType.YAWN: {
                'name': 'Menguap',
                'emoji': '🥱',
                'probability': 0.08,
                'severity': EventSeverity.VERY_LOW,
                'triggers': ['sleepy', 'random'],
                'cooldown': 1800,
                'messages': [
                    "*menguap* Ngantuk...",
                    "Maaf, ngantuk.",
                    "Ngantuk tapi gamau tidur.",
                    "Ikutan ngantuk gak?"
                ],
                'effects': {
                    'mood_effect': 'tired'
                }
            }
        }
    
    # =========================================================================
    # TRIGGER DETECTION
    # =========================================================================
    
    async def should_trigger_event(self, session_id: str, context: Dict) -> bool:
        """
        Cek apakah perlu trigger random event
        
        Args:
            session_id: ID session
            context: Konteks saat ini
            
        Returns:
            True jika perlu trigger
        """
        # Cek cooldown
        if session_id in self.event_cooldown:
            time_since = time.time() - self.event_cooldown[session_id]
            if time_since < self.min_cooldown:
                return False
        
        # Base probability
        base_prob = 0.15  # 15% chance
        
        # Adjust berdasarkan mood
        mood = context.get('mood', 'neutral')
        if mood in ['happy', 'excited']:
            base_prob *= 1.2
        elif mood in ['sad', 'tired']:
            base_prob *= 0.8
        
        # Adjust berdasarkan lokasi
        location = context.get('location', '')
        if 'public' in location or 'rame' in location:
            base_prob *= 1.3  # Tempat rame lebih banyak event
        
        # Random roll
        return random.random() < base_prob
    
    def _get_active_triggers(self, context: Dict) -> List[str]:
        """Dapatkan trigger yang aktif berdasarkan konteks"""
        triggers = ['random']
        
        # Time-based triggers
        hour = datetime.now().hour
        if 5 <= hour < 11:
            triggers.append('time_morning')
        elif 11 <= hour < 15:
            triggers.append('time_afternoon')
            triggers.append('time_meal')
        elif 15 <= hour < 18:
            triggers.append('time_evening')
        elif 18 <= hour < 22:
            triggers.append('time_night')
            triggers.append('time_dinner')
        else:
            triggers.append('time_late_night')
        
        # Location-based triggers
        location = context.get('location', '').lower()
        if 'kamar' in location or 'toilet' in location:
            triggers.append('intimate_place')
            triggers.append('close_proximity')
        if 'pantai' in location or 'taman' in location:
            triggers.append('outdoor')
            triggers.append('public_place')
        if 'mall' in location or 'kantor' in location:
            triggers.append('public_place')
        if 'rumah' in location or 'apartemen' in location:
            triggers.append('at_home')
        
        # Activity-based triggers
        activity = context.get('activity', '')
        if 'makan' in activity:
            triggers.append('after_eat')
        if 'intim' in activity or 'sex' in activity:
            triggers.append('after_intimacy')
            triggers.append('intimate')
        if 'mandi' in activity:
            triggers.append('wet_place')
        
        # Mood-based triggers
        mood = context.get('mood', '')
        if 'lonely' in mood:
            triggers.append('lonely')
        if 'sleepy' in mood:
            triggers.append('sleepy')
        
        return triggers
    
    async def get_random_event(self, session_id: str, context: Dict) -> Optional[Dict]:
        """
        Dapatkan random event berdasarkan konteks
        
        Args:
            session_id: ID session
            context: Konteks saat ini
            
        Returns:
            Event data atau None
        """
        if not await self.should_trigger_event(session_id, context):
            return None
        
        # Dapatkan trigger aktif
        active_triggers = self._get_active_triggers(context)
        
        # Filter events berdasarkan trigger
        eligible_events = []
        for event_type, event_data in self.events_db.items():
            # Cek cooldown spesifik event
            event_key = f"{session_id}_{event_type.value}"
            if event_key in self.event_cooldown:
                time_since = time.time() - self.event_cooldown[event_key]
                if time_since < event_data['cooldown']:
                    continue
            
            # Cek trigger match
            event_triggers = event_data['triggers']
            if any(trigger in active_triggers for trigger in event_triggers):
                # Adjust probability based on context
                prob = event_data['probability']
                
                # Mood adjustment
                mood = context.get('mood', 'neutral')
                if event_type == EventType.SUDDEN_MISS and mood == 'lonely':
                    prob *= 2
                elif event_type == EventType.SUDDEN_AROUSAL and mood == 'horny':
                    prob *= 2
                
                if random.random() < prob:
                    eligible_events.append(event_type)
        
        if not eligible_events:
            return None
        
        # Pilih random event
        selected_type = random.choice(eligible_events)
        event_data = self.events_db[selected_type].copy()
        
        # Pilih random message
        event_data['message'] = random.choice(event_data['messages'])
        event_data['type'] = selected_type
        
        # Record cooldown
        self.event_cooldown[session_id] = time.time()
        event_key = f"{session_id}_{selected_type.value}"
        self.event_cooldown[event_key] = time.time()
        
        # Update counter
        self.event_counter[selected_type.value] = self.event_counter.get(selected_type.value, 0) + 1
        
        logger.info(f"🎲 Random event triggered: {selected_type.value}")
        
        return event_data
    
    # =========================================================================
    # EVENT EFFECTS
    # =========================================================================
    
    async def apply_event_effects(self, event: Dict, context: Dict) -> Dict:
        """
        Apply efek event ke konteks
        
        Args:
            event: Event data
            context: Konteks saat ini
            
        Returns:
            Updated context
        """
        effects = event.get('effects', {})
        new_context = context.copy()
        
        # Location change
        if 'location_change' in effects:
            new_context['location'] = effects['location_change']
        
        # Mood effect
        if 'mood_effect' in effects:
            new_context['mood_delta'] = effects['mood_effect']
        
        # Arousal change
        if 'arousal_change' in effects:
            new_context['arousal_delta'] = effects['arousal_change']
        
        # Privacy change
        if 'privacy_change' in effects:
            current_privacy = new_context.get('privacy_level', 1.0)
            new_context['privacy_level'] = max(0.1, min(1.0, 
                current_privacy + effects['privacy_change']))
        
        return new_context
    
    # =========================================================================
    # EVENT HANDLING
    # =========================================================================
    
    async def process_event(self, event: Dict, ai_engine) -> Optional[str]:
        """
        Proses event dan dapatkan respons
        
        Args:
            event: Event data
            ai_engine: AI engine instance
            
        Returns:
            Response message atau None
        """
        message = event['message']
        
        # Tambah efek khusus berdasarkan tipe event
        if event['type'] == EventType.RAIN:
            message += " Basah-basahan yuk?"
        elif event['type'] == EventType.SOMEONE_PASSING:
            message += " *merapat*"
        elif event['type'] == EventType.SUDDEN_MISS:
            message += " 🥺"
        elif event['type'] == EventType.SUDDEN_AROUSAL:
            message += " 😏"
        
        return message
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    async def get_stats(self) -> Dict:
        """Dapatkan statistik random events"""
        return {
            'total_events': sum(self.event_counter.values()),
            'event_distribution': self.event_counter,
            'active_cooldowns': len(self.event_cooldown)
        }
    
    def format_event_message(self, event: Dict, bot_name: str) -> str:
        """Format event message untuk ditampilkan"""
        emoji = event.get('emoji', '🎲')
        severity = event.get('severity', EventSeverity.MEDIUM).value
        
        severity_indicators = {
            'very_low': '',
            'low': '☝️',
            'medium': '❗',
            'high': '⚠️',
            'very_high': '🔴'
        }
        
        indicator = severity_indicators.get(severity, '')
        
        return f"{emoji} {indicator} {event['message']}"


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_random_events = None


def get_random_events() -> RandomEvents:
    """Dapatkan global RandomEvents instance"""
    global _random_events
    if _random_events is None:
        _random_events = RandomEvents()
    return _random_events


__all__ = ['RandomEvents', 'EventType', 'EventSeverity', 'get_random_events']
