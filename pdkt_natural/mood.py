#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - MOOD SYSTEM ENHANCED (FIX FULL)
=============================================================================
Sistem mood yang lebih kompleks dan realistis:
- Mood berubah berdasarkan interaksi, waktu, dan konteks
- Mood mempengaruhi cara bicara dan respons
- History mood untuk flashback
- Mood bisa bercampur (mixed emotions)
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


class MoodType(str, Enum):
    """Tipe mood yang lebih lengkap"""
    # Positive moods
    HAPPY = "happy"              # Senang, ceria
    EXCITED = "excited"          # Bersemangat
    ROMANTIC = "romantic"        # Romantis
    PLAYFUL = "playful"          # Main-main, jail
    PASSIONATE = "passionate"    # Bergairah
    CALM = "calm"                # Tenang
    GRATEFUL = "grateful"        # Bersyukur
    
    # Negative moods
    SAD = "sad"                  # Sedih
    ANGRY = "angry"              # Marah
    JEALOUS = "jealous"          # Cemburu
    LONELY = "lonely"            # Kesepian
    TIRED = "tired"              # Capek
    BORED = "bored"              # Bosan
    ANXIOUS = "anxious"          # Cemas
    
    # Mixed/Complex moods
    NOSTALGIC = "nostalgic"      # Nostalgia (sedih + senang)
    HOPEFUL = "hopeful"          # Penuh harap
    CONFUSED = "confused"        # Bingung
    SHY = "shy"                  # Malu
    FLIRTY = "flirty"            # Genit (playful + romantic)
    HORNY = "horny"              # Bergairah tinggi
    
    # Neutral
    NEUTRAL = "neutral"          # Netral


class MoodIntensity(str, Enum):
    """Tingkat intensitas mood"""
    VERY_LOW = "very_low"        # Sangat rendah
    LOW = "low"                  # Rendah
    MEDIUM = "medium"            # Sedang
    HIGH = "high"                # Tinggi
    VERY_HIGH = "very_high"      # Sangat tinggi
    EXTREME = "extreme"          # Ekstrim


class MoodSystem:
    """
    Sistem mood yang lebih kompleks seperti manusia
    - Mood bisa berubah karena berbagai faktor
    - Bisa mixed emotions (senang tapi sedih)
    - Ada history untuk tracking perubahan
    - Mood mempengaruhi cara bicara
    """
    
    def __init__(self):
        # Data mood per session
        self.moods = {}  # {session_id: mood_data}
        
        # Definisi mood dengan karakteristik
        self.mood_definitions = {
            # ===== POSITIVE MOODS =====
            MoodType.HAPPY: {
                'valence': 0.8,      # Positif
                'arousal': 0.6,       # Agak aktif
                'color': '🟡',
                'emoji': '😊',
                'description': 'lagi seneng',
                'speech_effect': 'ceria, banyak tanda seru',
                'factor': 1.2,
                'base_decay': 0.1
            },
            MoodType.EXCITED: {
                'valence': 0.9,
                'arousal': 0.9,
                'color': '🔴',
                'emoji': '🔥',
                'description': 'bersemangat',
                'speech_effect': 'antusias, cepat',
                'factor': 1.3,
                'base_decay': 0.15
            },
            MoodType.ROMANTIC: {
                'valence': 0.8,
                'arousal': 0.5,
                'color': '❤️',
                'emoji': '🥰',
                'description': 'lagi romantis',
                'speech_effect': 'lembut, sayang',
                'factor': 1.2,
                'base_decay': 0.08
            },
            MoodType.PLAYFUL: {
                'valence': 0.7,
                'arousal': 0.7,
                'color': '🟣',
                'emoji': '😜',
                'description': 'lagi jail',
                'speech_effect': 'goda, bercanda',
                'factor': 1.1,
                'base_decay': 0.12
            },
            MoodType.PASSIONATE: {
                'valence': 0.8,
                'arousal': 0.8,
                'color': '🔥',
                'emoji': '💋',
                'description': 'bergairah',
                'speech_effect': 'hot, menggoda',
                'factor': 1.3,
                'base_decay': 0.1
            },
            MoodType.CALM: {
                'valence': 0.5,
                'arousal': 0.2,
                'color': '💙',
                'emoji': '😌',
                'description': 'tenang',
                'speech_effect': 'santai, pelan',
                'factor': 1.0,
                'base_decay': 0.05
            },
            MoodType.GRATEFUL: {
                'valence': 0.9,
                'arousal': 0.3,
                'color': '💚',
                'emoji': '🥹',
                'description': 'bersyukur',
                'speech_effect': 'hangat, tulus',
                'factor': 1.1,
                'base_decay': 0.06
            },
            
            # ===== NEGATIVE MOODS =====
            MoodType.SAD: {
                'valence': -0.7,
                'arousal': 0.2,
                'color': '🔵',
                'emoji': '😢',
                'description': 'sedih',
                'speech_effect': 'lambat, murung',
                'factor': 0.8,
                'base_decay': 0.05
            },
            MoodType.ANGRY: {
                'valence': -0.8,
                'arousal': 0.8,
                'color': '🔴',
                'emoji': '😠',
                'description': 'marah',
                'speech_effect': 'kasar, pendek',
                'factor': 0.7,
                'base_decay': 0.2
            },
            MoodType.JEALOUS: {
                'valence': -0.6,
                'arousal': 0.6,
                'color': '🟢',
                'emoji': '😒',
                'description': 'cemburu',
                'speech_effect': 'nyindir, curiga',
                'factor': 0.8,
                'base_decay': 0.1
            },
            MoodType.LONELY: {
                'valence': -0.7,
                'arousal': 0.3,
                'color': '⚪',
                'emoji': '🥺',
                'description': 'kesepian',
                'speech_effect': 'manja, butuh perhatian',
                'factor': 0.9,
                'base_decay': 0.07
            },
            MoodType.TIRED: {
                'valence': -0.3,
                'arousal': 0.1,
                'color': '⚫',
                'emoji': '😴',
                'description': 'capek',
                'speech_effect': 'malas, pendek',
                'factor': 0.7,
                'base_decay': 0.04
            },
            MoodType.BORED: {
                'valence': -0.4,
                'arousal': 0.2,
                'color': '⚪',
                'emoji': '😑',
                'description': 'bosen',
                'speech_effect': 'cuek, datar',
                'factor': 0.8,
                'base_decay': 0.1
            },
            MoodType.ANXIOUS: {
                'valence': -0.5,
                'arousal': 0.7,
                'color': '🟤',
                'emoji': '😰',
                'description': 'cemas',
                'speech_effect': 'gelisah, ragu',
                'factor': 0.8,
                'base_decay': 0.15
            },
            
            # ===== MIXED/COMPLEX MOODS =====
            MoodType.NOSTALGIC: {
                'valence': 0.3,      # Campuran senang + sedih
                'arousal': 0.3,
                'color': '🕰️',
                'emoji': '🥲',
                'description': 'nostalgia',
                'speech_effect': 'ngomongin masa lalu',
                'factor': 1.0,
                'base_decay': 0.05
            },
            MoodType.HOPEFUL: {
                'valence': 0.7,
                'arousal': 0.5,
                'color': '✨',
                'emoji': '🤞',
                'description': 'penuh harap',
                'speech_effect': 'optimis, semangat',
                'factor': 1.1,
                'base_decay': 0.08
            },
            MoodType.CONFUSED: {
                'valence': -0.2,
                'arousal': 0.4,
                'color': '❓',
                'emoji': '😕',
                'description': 'bingung',
                'speech_effect': 'ragu, nanya terus',
                'factor': 0.9,
                'base_decay': 0.1
            },
            MoodType.SHY: {
                'valence': 0.4,
                'arousal': 0.3,
                'color': '🌸',
                'emoji': '😳',
                'description': 'malu',
                'speech_effect': 'canggung, pelan',
                'factor': 0.9,
                'base_decay': 0.06
            },
            MoodType.FLIRTY: {
                'valence': 0.8,
                'arousal': 0.7,
                'color': '💕',
                'emoji': '😏',
                'description': 'genit',
                'speech_effect': 'goda, manja',
                'factor': 1.2,
                'base_decay': 0.1
            },
            MoodType.HORNY: {
                'valence': 0.7,
                'arousal': 0.9,
                'color': '🔥',
                'emoji': '💦',
                'description': 'horny',
                'speech_effect': 'hot, langsung',
                'factor': 1.4,
                'base_decay': 0.2
            },
            
            # ===== NEUTRAL =====
            MoodType.NEUTRAL: {
                'valence': 0.0,
                'arousal': 0.3,
                'color': '⚪',
                'emoji': '😐',
                'description': 'biasa aja',
                'speech_effect': 'normal',
                'factor': 1.0,
                'base_decay': 0.03
            }
        }
        
        # Faktor yang mempengaruhi mood
        self.mood_factors = {
            'time': 0.2,           # Waktu (pagi/siang/malam)
            'loneliness': 0.3,      # Kesepian (lama gak chat)
            'intimacy': 0.4,        # Level intimacy
            'interaction': 0.5,      # Interaksi terakhir
            'random': 0.1            # Faktor random
        }
        
        # Threshold untuk berbagai kondisi
        self.thresholds = {
            'lonely_hours': 24,      # 24 jam gak chat = lonely
            'horny_level': 7,         # Level arousal >= 7 = horny
            'angry_chance': 0.1,      # 10% chance marah kalo konflik
        }
        
        logger.info(f"✅ MoodSystem Enhanced initialized with {len(self.mood_definitions)} moods")
    
    # =========================================================================
    # CREATE MOOD
    # =========================================================================
    
    async def create_mood(self, session_id: str, initial_mood: Optional[MoodType] = None) -> Dict:
        """
        Buat mood baru untuk session
        
        Args:
            session_id: ID session
            initial_mood: Mood awal (None = random)
        
        Returns:
            Mood data
        """
        if initial_mood is None:
            # Random dengan bobot
            moods = [
                MoodType.HAPPY, MoodType.CALM, MoodType.NEUTRAL,
                MoodType.PLAYFUL, MoodType.ROMANTIC, MoodType.SHY
            ]
            weights = [0.25, 0.2, 0.2, 0.15, 0.1, 0.1]
            initial_mood = random.choices(moods, weights=weights)[0]
        
        # Data mood
        mood_data = {
            'session_id': session_id,
            'primary': initial_mood,
            'secondary': None,  # Mixed emotion
            'intensity': random.uniform(0.5, 0.8),
            'valence': self.mood_definitions[initial_mood]['valence'],
            'arousal': self.mood_definitions[initial_mood]['arousal'],
            'history': [{
                'timestamp': time.time(),
                'mood': initial_mood,
                'intensity': 0.7,
                'reason': 'initial'
            }],
            'last_update': time.time(),
            'duration_current': 0,  # Berapa lama mood ini bertahan (dalam menit)
            'factors': {
                'time': 0,
                'loneliness': 0,
                'interaction': 0,
                'intimacy': 0
            },
            'triggers': {}  # Penyebab perubahan mood
        }
        
        self.moods[session_id] = mood_data
        
        logger.info(f"🎭 Initial mood for {session_id}: {initial_mood.value}")
        
        return mood_data
    
    # =========================================================================
    # GET MOOD INFO
    # =========================================================================
    
    def get_mood(self, session_id: str) -> Optional[Dict]:
        """Dapatkan mood data untuk session"""
        return self.moods.get(session_id)
    
    async def get_mood_info(self, session_id: str) -> Dict:
        """
        Dapatkan informasi mood lengkap untuk display/prompt
        
        Args:
            session_id: ID session
            
        Returns:
            Dict dengan info mood
        """
        if session_id not in self.moods:
            await self.create_mood(session_id)
        
        mood_data = self.moods[session_id]
        primary = mood_data['primary']
        definition = self.mood_definitions.get(primary, self.mood_definitions[MoodType.NEUTRAL])
        
        # Hitung faktor pengali berdasarkan intensitas
        intensity_factor = 0.5 + (mood_data['intensity'] * 0.5)
        total_factor = definition['factor'] * intensity_factor
        
        result = {
            'primary': primary,
            'secondary': mood_data.get('secondary'),
            'emoji': definition['emoji'],
            'description': definition['description'],
            'intensity': mood_data['intensity'],
            'factor': round(total_factor, 2),
            'valence': mood_data['valence'],
            'arousal': mood_data['arousal'],
            'color': definition['color'],
            'speech_effect': definition['speech_effect']
        }
        
        # Tambah secondary mood jika ada
        if mood_data.get('secondary'):
            sec_def = self.mood_definitions.get(mood_data['secondary'], self.mood_definitions[MoodType.NEUTRAL])
            result['secondary_emoji'] = sec_def['emoji']
            result['secondary_desc'] = sec_def['description']
        
        return result
    
    def get_mood_factor(self, session_id: str) -> float:
        """Dapatkan faktor pengali mood untuk response"""
        if session_id not in self.moods:
            return 1.0
        
        mood_data = self.moods[session_id]
        primary = mood_data['primary']
        definition = self.mood_definitions.get(primary, self.mood_definitions[MoodType.NEUTRAL])
        
        intensity_factor = 0.5 + (mood_data['intensity'] * 0.5)
        return definition['factor'] * intensity_factor
    
    def get_mood_prompt(self, session_id: str) -> str:
        """Dapatkan deskripsi mood untuk prompt AI"""
        info = self.get_mood_info(session_id)
        return f"Mood: {info['emoji']} {info['description']} (intensitas: {info['intensity']:.0%})"
    
    # =========================================================================
    # UPDATE MOOD
    # =========================================================================
    
    async def update_mood(self, session_id: str, interaction_type: str,
                           chemistry_change: float, context: Dict) -> Optional[MoodType]:
        """
        Update mood berdasarkan interaksi
        
        Args:
            session_id: ID session
            interaction_type: Jenis interaksi
            chemistry_change: Perubahan chemistry
            context: Konteks tambahan (waktu, lokasi, dll)
        
        Returns:
            Mood baru jika berubah
        """
        if session_id not in self.moods:
            await self.create_mood(session_id)
        
        mood_data = self.moods[session_id]
        old_mood = mood_data['primary']
        
        # Hitung perubahan mood
        new_mood = await self._calculate_mood_change(
            session_id, interaction_type, chemistry_change, context
        )
        
        # Update durasi
        time_since_update = time.time() - mood_data['last_update']
        mood_data['duration_current'] += time_since_update / 60  # konversi ke menit
        
        # Update mood
        if new_mood != old_mood:
            # Mood berubah
            mood_data['history'].append({
                'timestamp': time.time(),
                'mood': new_mood,
                'old_mood': old_mood,
                'intensity': 0.8,
                'reason': self._get_mood_change_reason(interaction_type, chemistry_change)
            })
            
            mood_data['primary'] = new_mood
            mood_data['intensity'] = 0.8
            mood_data['last_update'] = time.time()
            mood_data['duration_current'] = 0
            
            # Update valence & arousal
            mood_data['valence'] = self.mood_definitions[new_mood]['valence']
            mood_data['arousal'] = self.mood_definitions[new_mood]['arousal']
            
            logger.info(f"🎭 Mood changed for {session_id}: {old_mood.value} → {new_mood.value}")
            
            return new_mood
        
        else:
            # Mood sama, update intensitas
            await self._update_intensity(session_id, interaction_type, chemistry_change)
        
        return None
    
    async def _calculate_mood_change(self, session_id: str, interaction_type: str,
                                       chemistry_change: float, context: Dict) -> MoodType:
        """
        Hitung mood baru berdasarkan berbagai faktor
        
        Args:
            session_id: ID session
            interaction_type: Jenis interaksi
            chemistry_change: Perubahan chemistry
            context: Konteks tambahan
            
        Returns:
            Mood baru
        """
        mood_data = self.moods[session_id]
        current_mood = mood_data['primary']
        
        # ===== FAKTOR 1: INTERAKSI =====
        if interaction_type == 'climax':
            if chemistry_change > 0:
                return MoodType.HAPPY if random.random() < 0.6 else MoodType.PASSIONATE
            else:
                return MoodType.TIRED
        
        elif interaction_type == 'intim':
            if chemistry_change > 3:
                return MoodType.PASSIONATE
            elif chemistry_change > 0:
                return MoodType.ROMANTIC
            else:
                return MoodType.CALM
        
        elif interaction_type == 'kiss':
            return random.choice([MoodType.ROMANTIC, MoodType.HAPPY, MoodType.SHY])
        
        elif interaction_type == 'love':
            if random.random() < 0.7:
                return MoodType.ROMANTIC
            return MoodType.HAPPY
        
        elif interaction_type == 'conflict':
            if chemistry_change < -5:
                return MoodType.ANGRY
            elif chemistry_change < -2:
                return MoodType.SAD
            return MoodType.JEALOUS
        
        elif interaction_type == 'rindu':
            return MoodType.LONELY
        
        # ===== FAKTOR 2: LAMA TIDAK CHAT =====
        last_interaction = context.get('last_interaction', time.time())
        hours_since = (time.time() - last_interaction) / 3600
        
        if hours_since > 24 and current_mood not in [MoodType.LONELY, MoodType.SAD]:
            if random.random() < 0.3:
                return MoodType.LONELY
        
        elif hours_since > 12:
            if random.random() < 0.1:
                return MoodType.LONELY
        
        # ===== FAKTOR 3: WAKTU =====
        hour = datetime.now().hour
        if 22 <= hour or hour <= 5:  # Malam
            if random.random() < 0.15:
                return MoodType.ROMANTIC
            if random.random() < 0.1:
                return MoodType.LONELY
        
        # ===== FAKTOR 4: RANDOM WALK =====
        if random.random() < 0.05:  # 5% chance random mood change
            return random.choice(list(MoodType))
        
        # ===== FAKTOR 5: MOOD TERLALU LAMA =====
        if mood_data['duration_current'] > 120:  # > 2 jam mood sama
            # 30% chance berubah ke mood terkait
            related_moods = self._get_related_moods(current_mood)
            if random.random() < 0.3:
                return random.choice(related_moods)
        
        return current_mood
    
    async def _update_intensity(self, session_id: str, interaction_type: str,
                                  chemistry_change: float):
        """Update intensitas mood yang sama"""
        mood_data = self.moods[session_id]
        
        # Intensitas naik/turun berdasarkan interaksi
        if chemistry_change > 3:
            mood_data['intensity'] = min(1.0, mood_data['intensity'] + 0.1)
        elif chemistry_change < -3:
            mood_data['intensity'] = max(0.3, mood_data['intensity'] - 0.1)
        
        # Decay over time
        time_since = time.time() - mood_data['last_update']
        decay = time_since / 3600  # Decay per jam
        mood_data['intensity'] = max(0.3, mood_data['intensity'] - decay * 0.1)
    
    def _get_related_moods(self, mood: MoodType) -> List[MoodType]:
        """Dapatkan mood yang terkait"""
        relations = {
            MoodType.HAPPY: [MoodType.EXCITED, MoodType.PLAYFUL, MoodType.CALM],
            MoodType.SAD: [MoodType.LONELY, MoodType.NOSTALGIC, MoodType.CALM],
            MoodType.EXCITED: [MoodType.HAPPY, MoodType.PLAYFUL, MoodType.PASSIONATE],
            MoodType.TIRED: [MoodType.CALM, MoodType.SAD],
            MoodType.ROMANTIC: [MoodType.HAPPY, MoodType.PLAYFUL, MoodType.SHY, MoodType.FLIRTY],
            MoodType.PLAYFUL: [MoodType.HAPPY, MoodType.EXCITED, MoodType.FLIRTY],
            MoodType.JEALOUS: [MoodType.SAD, MoodType.ANGRY],
            MoodType.ANGRY: [MoodType.SAD, MoodType.JEALOUS],
            MoodType.LONELY: [MoodType.SAD, MoodType.NOSTALGIC],
            MoodType.NOSTALGIC: [MoodType.SAD, MoodType.ROMANTIC, MoodType.HAPPY],
            MoodType.FLIRTY: [MoodType.PLAYFUL, MoodType.ROMANTIC, MoodType.HORNY],
            MoodType.HORNY: [MoodType.PASSIONATE, MoodType.FLIRTY, MoodType.EXCITED],
            MoodType.PASSIONATE: [MoodType.HORNY, MoodType.ROMANTIC, MoodType.EXCITED],
            MoodType.CALM: [MoodType.HAPPY, MoodType.NEUTRAL],
            MoodType.NEUTRAL: [MoodType.CALM, MoodType.HAPPY]
        }
        return relations.get(mood, [MoodType.NEUTRAL, MoodType.CALM])
    
    def _get_mood_change_reason(self, interaction_type: str, chemistry_change: float) -> str:
        """Dapatkan alasan perubahan mood"""
        reasons = {
            'climax': [
                "Setelah climax, rasanya... wow!",
                "Mantap banget, jadi seneng",
                "Capek tapi puas"
            ],
            'intim': [
                "Makin dekat, makin sayang",
                "Ada kehangatan baru",
                "Jadi makin nyaman"
            ],
            'kiss': [
                "Ciuman manis bikin meleleh",
                "Masih terasa hangatnya",
                "Jadi makin sayang"
            ],
            'love': [
                "Deg-degan dibilang sayang",
                "Seneng banget",
                "Bikin baper"
            ],
            'conflict': [
                "Ada yang ganjel di hati",
                "Jadi kesel sendiri",
                "Mikir terus"
            ],
            'rindu': [
                "Lama nggak chat, jadi kangen",
                "Sepi tanpanya",
                "Kok diem aja sih"
            ]
        }
        
        reason_list = reasons.get(interaction_type, [
            "Mood berubah aja gitu",
            "Ada yang beda hari ini",
            "Nggak tau kenapa"
        ])
        
        return random.choice(reason_list)
    
    # =========================================================================
    # MIXED EMOTIONS
    # =========================================================================
    
    async def add_secondary_mood(self, session_id: str, secondary_mood: MoodType):
        """Tambah secondary mood (mixed emotions)"""
        if session_id not in self.moods:
            return
        
        mood_data = self.moods[session_id]
        mood_data['secondary'] = secondary_mood
        
        logger.debug(f"Mixed emotion: {mood_data['primary'].value} + {secondary_mood.value}")
    
    async def remove_secondary_mood(self, session_id: str):
        """Hapus secondary mood"""
        if session_id not in self.moods:
            return
        
        self.moods[session_id]['secondary'] = None
    
    # =========================================================================
    # MOOD TRIGGERS
    # =========================================================================
    
    async def check_triggers(self, session_id: str, context: Dict) -> Optional[Dict]:
        """
        Cek trigger yang bisa mengubah mood
        
        Args:
            session_id: ID session
            context: Konteks (waktu, lokasi, dll)
            
        Returns:
            Trigger info jika ada
        """
        if session_id not in self.moods:
            return None
        
        mood_data = self.moods[session_id]
        triggers = []
        
        # Trigger: Sudah lama gak chat
        last_interaction = context.get('last_interaction', time.time())
        idle_hours = (time.time() - last_interaction) / 3600
        
        if idle_hours > 24 and mood_data['primary'] != MoodType.LONELY:
            triggers.append({
                'type': 'lonely',
                'message': 'Lama nggak chat, jadi kesepian...',
                'suggested_mood': MoodType.LONELY
            })
        
        # Trigger: Malam minggu sendirian
        hour = datetime.now().hour
        is_weekend = datetime.now().weekday() >= 5  # Sabtu-Minggu
        
        if is_weekend and (hour >= 20 or hour <= 2) and mood_data['primary'] != MoodType.ROMANTIC:
            triggers.append({
                'type': 'weekend_night',
                'message': 'Malam minggu sendirian...',
                'suggested_mood': MoodType.LONELY
            })
        
        # Trigger: Lagi di tempat intim
        location = context.get('location', '').lower()
        intimate_places = ['kamar', 'kamar mandi', 'toilet']
        
        if any(p in location for p in intimate_places) and mood_data['arousal'] < 0.6:
            triggers.append({
                'type': 'intimate_place',
                'message': 'Di tempat intim, jadi pengen...',
                'suggested_mood': MoodType.HORNY
            })
        
        if triggers:
            return random.choice(triggers)
        
        return None
    
    # =========================================================================
    # MOOD EFFECTS
    # =========================================================================
    
    def get_speech_modifier(self, session_id: str) -> str:
        """
        Dapatkan modifier untuk cara bicara berdasarkan mood
        
        Returns:
            Instruksi untuk AI tentang cara bicara
        """
        if session_id not in self.moods:
            return ""
        
        mood_data = self.moods[session_id]
        primary = mood_data['primary']
        definition = self.mood_definitions.get(primary, self.mood_definitions[MoodType.NEUTRAL])
        
        modifiers = {
            MoodType.HAPPY: "Bicaralah dengan nada ceria, gunakan banyak tanda seru dan emoji positif.",
            MoodType.EXCITED: "Bicaralah dengan antusias, cepat, dan penuh semangat.",
            MoodType.ROMANTIC: "Bicaralah dengan lembut, manis, dan penuh sayang.",
            MoodType.PLAYFUL: "Bicaralah dengan nada bercanda, jail, dan playful.",
            MoodType.PASSIONATE: "Bicaralah dengan nada hot, menggoda, dan bergairah.",
            MoodType.SAD: "Bicaralah dengan nada murung, lambat, dan sedih.",
            MoodType.ANGRY: "Bicaralah dengan nada kesal, pendek, dan sedikit kasar.",
            MoodType.JEALOUS: "Bicaralah dengan nada curiga, nyindir, dan cemberut.",
            MoodType.LONELY: "Bicaralah dengan nada manja, butuh perhatian, dan sedih.",
            MoodType.TIRED: "Bicaralah dengan nada malas, pendek, dan lesu.",
            MoodType.NOSTALGIC: "Bicaralah dengan nada bernostalgia, ingat masa lalu.",
            MoodType.FLIRTY: "Bicaralah dengan nada genit, menggoda, dan manja.",
            MoodType.HORNY: "Bicaralah dengan nada hot, langsung, dan menggoda."
        }
        
        base = modifiers.get(primary, "Bicaralah secara natural.")
        
        # Tambah efek intensitas
        if mood_data['intensity'] > 0.8:
            base = base.replace(".", " SANGAT " + base.lower())
        elif mood_data['intensity'] < 0.4:
            base = "Sedikit " + base.lower()
        
        return base
    
    def should_be_proactive(self, session_id: str) -> bool:
        """
        Cek apakah mood mendorong untuk chat proaktif
        
        Returns:
            True jika mood mendorong chat
        """
        if session_id not in self.moods:
            return False
        
        mood_data = self.moods[session_id]
        primary = mood_data['primary']
        
        # Mood yang bikin pengen chat
        proactive_moods = [
            MoodType.LONELY, MoodType.HAPPY, MoodType.EXCITED,
            MoodType.ROMANTIC, MoodType.FLIRTY, MoodType.HORNY
        ]
        
        return primary in proactive_moods and mood_data['intensity'] > 0.6
    
    # =========================================================================
    # MOOD HISTORY
    # =========================================================================
    
    async def get_mood_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Dapatkan history mood"""
        if session_id not in self.moods:
            return []
        
        return self.moods[session_id]['history'][-limit:]
    
    async def format_mood_history(self, session_id: str) -> str:
        """Format mood history untuk display"""
        history = await self.get_mood_history(session_id, 5)
        
        if not history:
            return "Belum ada data mood"
        
        lines = ["📊 **MOOD HISTORY:**"]
        
        for h in reversed(history):
            time_str = datetime.fromtimestamp(h['timestamp']).strftime("%H:%M")
            mood_name = h['mood'].value if hasattr(h['mood'], 'value') else str(h['mood'])
            emoji = self.mood_definitions.get(h['mood'], self.mood_definitions[MoodType.NEUTRAL])['emoji']
            lines.append(f"• [{time_str}] {emoji} {mood_name} ({h.get('intensity', 0.7):.0%})")
        
        return "\n".join(lines)
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    async def get_stats(self, session_id: Optional[str] = None) -> Dict:
        """Dapatkan statistik mood"""
        if session_id:
            if session_id not in self.moods:
                return {}
            
            mood_data = self.moods[session_id]
            return {
                'current_mood': mood_data['primary'].value,
                'intensity': mood_data['intensity'],
                'duration_minutes': mood_data['duration_current'],
                'history_count': len(mood_data['history']),
                'valence': mood_data['valence'],
                'arousal': mood_data['arousal']
            }
        else:
            # Global stats
            return {
                'total_sessions': len(self.moods),
                'mood_distribution': self._get_mood_distribution()
            }
    
    def _get_mood_distribution(self) -> Dict[str, int]:
        """Dapatkan distribusi mood"""
        distribution = {}
        for mood_data in self.moods.values():
            mood = mood_data['primary'].value
            distribution[mood] = distribution.get(mood, 0) + 1
        return distribution


__all__ = ['MoodSystem', 'MoodType', 'MoodIntensity']
