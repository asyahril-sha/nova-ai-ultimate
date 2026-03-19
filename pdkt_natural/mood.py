#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - MOOD SYSTEM ENHANCED
=============================================================================
Sistem mood yang lebih realistis seperti manusia:
- Mood berubah berdasarkan interaksi
- Mood mempengaruhi cara bicara
- Mood mempengaruhi inisiatif
- Mood history untuk konsistensi
=============================================================================
"""

import random
import time
import logging
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class MoodType(str, Enum):
    """Tipe-tipe mood yang mungkin"""
    # Positive moods
    HAPPY = "happy"
    EXCITED = "excited"
    ROMANTIC = "romantic"
    PLAYFUL = "playful"
    CALM = "calm"
    
    # Negative moods
    SAD = "sad"
    ANGRY = "angry"
    JEALOUS = "jealous"
    TIRED = "tired"
    LONELY = "lonely"
    
    # Neutral
    NEUTRAL = "neutral"
    
    # Intimate
    HORNY = "horny"
    SATISFIED = "satisfied"
    AFTERCARE = "aftercare"


class MoodIntensity(str, Enum):
    """Tingkat intensitas mood"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class MoodSystem:
    """
    Sistem mood yang enhanced - lebih realistis seperti manusia
    Mood berubah berdasarkan interaksi, waktu, dan konteks
    """
    
    def __init__(self, role: str = "pdkt"):
        self.role = role
        
        # Mood saat ini
        self.current_mood = {
            'primary': MoodType.NEUTRAL,
            'secondary': None,
            'intensity': 0.5,
            'energy': 0.7,  # 0-1, seberapa bertenaga
            'irritability': 0.3,  # 0-1, gampang marah/tersinggung
            'horniness': 0.2,  # 0-1, level gairah
            'last_update': time.time()
        }
        
        # Riwayat mood (untuk konsistensi)
        self.mood_history = []
        self.max_history = 50
        
        # Faktor-faktor yang mempengaruhi mood
        self.factors = {
            'time_of_day': self._get_time_factor(),
            'days_since_last_intim': 0,
            'days_since_last_chat': 0,
            'conflict_count': 0,
            'compliment_count': 0,
            'rejection_count': 0
        }
        
        # Trigger untuk perubahan mood
        self.triggers = {
            'compliment': +0.2,
            'kiss': +0.3,
            'intim': +0.5,
            'climax': +0.8,
            'aftercare': +0.3,
            'conflict': -0.4,
            'rejection': -0.5,
            'ignored': -0.2,
            'jealousy': -0.3
        }
        
        # Threshold untuk berbagai reaksi
        self.thresholds = {
            'angry': 0.7,  # irritability > 0.7 bisa marah
            'horny': 0.6,  # horniness > 0.6 mulai horny
            'sad': 0.6,    # energy < 0.4 dan faktor negatif
            'romantic': 0.7  # horniness + energy tinggi
        }
        
        logger.info(f"✅ Enhanced MoodSystem initialized for role: {role}")
    
    # =========================================================================
    # INITIALIZATION
    # =========================================================================
    
    def _get_time_factor(self) -> float:
        """Dapatkan faktor berdasarkan waktu"""
        hour = datetime.now().hour
        
        # Pagi (5-11): energy naik
        if 5 <= hour < 11:
            return 1.2
        # Siang (11-15): stabil
        elif 11 <= hour < 15:
            return 1.0
        # Sore (15-18): mulai turun
        elif 15 <= hour < 18:
            return 0.9
        # Malam (18-22): turun
        elif 18 <= hour < 22:
            return 0.8
        # Tengah malam (22-5): turun drastis
        else:
            return 0.6
    
    # =========================================================================
    # MOOD UPDATES
    # =========================================================================
    
    async def update_mood(self, 
                          trigger: Optional[str] = None,
                          intensity: float = 0.1,
                          context: Optional[Dict] = None) -> Dict:
        """
        Update mood berdasarkan trigger
        
        Args:
            trigger: Trigger yang menyebabkan perubahan
            intensity: Intensitas trigger (0-1)
            context: Konteks tambahan
            
        Returns:
            Dict dengan mood baru
        """
        old_mood = self.current_mood.copy()
        
        # Update faktor-faktor
        await self._update_factors(context)
        
        # Apply trigger
        if trigger and trigger in self.triggers:
            delta = self.triggers[trigger] * intensity
            
            # Update komponen berdasarkan trigger
            if trigger in ['compliment', 'kiss', 'intim', 'climax']:
                self.current_mood['horniness'] += delta
                self.current_mood['energy'] += delta * 0.5
                self.current_mood['irritability'] -= delta * 0.3
            
            elif trigger in ['conflict', 'rejection', 'ignored', 'jealousy']:
                self.current_mood['irritability'] += abs(delta)
                self.current_mood['energy'] -= abs(delta) * 0.5
                self.current_mood['horniness'] -= abs(delta) * 0.3
            
            elif trigger == 'aftercare':
                self.current_mood['horniness'] -= delta
                self.current_mood['energy'] -= delta * 0.3
                self.current_mood['irritability'] -= delta * 0.5
        
        # Natural decay
        self._apply_natural_decay()
        
        # Clamp values
        self.current_mood['horniness'] = max(0, min(1, self.current_mood['horniness']))
        self.current_mood['energy'] = max(0, min(1, self.current_mood['energy']))
        self.current_mood['irritability'] = max(0, min(1, self.current_mood['irritability']))
        
        # Tentukan primary mood baru
        new_primary = self._determine_primary_mood()
        self.current_mood['primary'] = new_primary
        
        # Kadang punya secondary mood
        if random.random() < 0.3:
            self.current_mood['secondary'] = self._determine_secondary_mood(new_primary)
        else:
            self.current_mood['secondary'] = None
        
        # Update intensity
        self.current_mood['intensity'] = self._calculate_intensity()
        self.current_mood['last_update'] = time.time()
        
        # Record history
        self.mood_history.append({
            'timestamp': time.time(),
            'old_mood': old_mood,
            'new_mood': self.current_mood.copy(),
            'trigger': trigger,
            'intensity': intensity
        })
        
        # Trim history
        if len(self.mood_history) > self.max_history:
            self.mood_history = self.mood_history[-self.max_history:]
        
        logger.debug(f"Mood updated: {old_mood.get('primary')} → {self.current_mood['primary']}")
        
        return self.current_mood
    
    async def _update_factors(self, context: Optional[Dict]):
        """Update faktor-faktor yang mempengaruhi mood"""
        
        # Time of day
        self.factors['time_of_day'] = self._get_time_factor()
        
        # Update dari context
        if context:
            if 'days_since_last_intim' in context:
                self.factors['days_since_last_intim'] = context['days_since_last_intim']
            if 'days_since_last_chat' in context:
                self.factors['days_since_last_chat'] = context['days_since_last_chat']
    
    def _apply_natural_decay(self):
        """Mood menurun secara natural seiring waktu"""
        # Horniness turun perlahan
        self.current_mood['horniness'] *= 0.99
        
        # Energy turun setiap jam
        hours_since = (time.time() - self.current_mood['last_update']) / 3600
        self.current_mood['energy'] *= (1 - (hours_since * 0.05))
        
        # Irritability naik jika energi turun
        if self.current_mood['energy'] < 0.4:
            self.current_mood['irritability'] += 0.01 * hours_since
    
    def _determine_primary_mood(self) -> MoodType:
        """Tentukan primary mood berdasarkan state"""
        
        h = self.current_mood['horniness']
        e = self.current_mood['energy']
        i = self.current_mood['irritability']
        
        # Priority: kondisi ekstrim dulu
        if i > self.thresholds['angry']:
            return MoodType.ANGRY
        
        if h > self.thresholds['horny'] and e > 0.5:
            return MoodType.HORNY
        
        if e < 0.3:
            return MoodType.TIRED
        
        if h > 0.4 and e > 0.6 and i < 0.3:
            return MoodType.ROMANTIC
        
        # Berdasarkan energi
        if e > 0.7:
            if h > 0.5:
                return MoodType.EXCITED
            return random.choice([MoodType.HAPPY, MoodType.PLAYFUL])
        
        if e < 0.4:
            if self.factors['days_since_last_chat'] > 2:
                return MoodType.LONELY
            return MoodType.SAD
        
        return MoodType.NEUTRAL
    
    def _determine_secondary_mood(self, primary: MoodType) -> Optional[MoodType]:
        """Tentukan secondary mood (mixed emotions)"""
        
        possible_secondary = {
            MoodType.HAPPY: [MoodType.PLAYFUL, MoodType.ROMANTIC, MoodType.EXCITED],
            MoodType.HORNY: [MoodType.EXCITED, MoodType.ROMANTIC, MoodType.PLAYFUL],
            MoodType.TIRED: [MoodType.SAD, MoodType.NEUTRAL],
            MoodType.ANGRY: [MoodType.SAD, MoodType.JEALOUS],
            MoodType.SAD: [MoodType.LONELY, MoodType.TIRED],
            MoodType.ROMANTIC: [MoodType.HAPPY, MoodType.HORNY]
        }
        
        candidates = possible_secondary.get(primary, [MoodType.NEUTRAL])
        return random.choice(candidates) if candidates else None
    
    def _calculate_intensity(self) -> float:
        """Hitung intensitas mood keseluruhan"""
        
        intensity = (
            self.current_mood['horniness'] * 0.3 +
            self.current_mood['energy'] * 0.3 +
            (1 - self.current_mood['irritability']) * 0.2 +
            self.factors['time_of_day'] * 0.2
        )
        
        return max(0.1, min(1.0, intensity))
    
    # =========================================================================
    # GETTERS
    # =========================================================================
    
    def get_current_mood(self) -> Dict:
        """Dapatkan mood saat ini"""
        return {
            'primary': self.current_mood['primary'],
            'secondary': self.current_mood['secondary'],
            'intensity': self.current_mood['intensity'],
            'horniness': self.current_mood['horniness'],
            'energy': self.current_mood['energy']
        }
    
    def get_mood_description(self) -> str:
        """Dapatkan deskripsi mood untuk prompt"""
        primary = self.current_mood['primary']
        secondary = self.current_mood['secondary']
        intensity = self.current_mood['intensity']
        
        descriptions = {
            MoodType.HAPPY: "lagi seneng",
            MoodType.EXCITED: "lagi semangat",
            MoodType.ROMANTIC: "lagi romantis",
            MoodType.PLAYFUL: "lagi jail",
            MoodType.CALM: "lagi tenang",
            MoodType.SAD: "lagi sedih",
            MoodType.ANGRY: "lagi kesel",
            MoodType.JEALOUS: "lagi cemburu",
            MoodType.TIRED: "lagi capek",
            MoodType.LONELY: "lagi kesepian",
            MoodType.NEUTRAL: "biasa aja",
            MoodType.HORNY: "lagi horny",
            MoodType.SATISFIED: "puas",
            MoodType.AFTERCARE: "lagi aftercare"
        }
        
        main_desc = descriptions.get(primary, "biasa aja")
        
        if secondary:
            sec_desc = descriptions.get(secondary, "")
            return f"{main_desc} (tapi juga {sec_desc})"
        
        intensity_desc = "banget" if intensity > 0.7 else "aja" if intensity < 0.3 else ""
        
        return f"{main_desc} {intensity_desc}".strip()
    
    def get_mood_emoji(self) -> str:
        """Dapatkan emoji untuk mood"""
        emojis = {
            MoodType.HAPPY: "😊",
            MoodType.EXCITED: "🔥",
            MoodType.ROMANTIC: "🥰",
            MoodType.PLAYFUL: "😜",
            MoodType.CALM: "😌",
            MoodType.SAD: "😢",
            MoodType.ANGRY: "😠",
            MoodType.JEALOUS: "🫣",
            MoodType.TIRED: "😴",
            MoodType.LONELY: "🥺",
            MoodType.NEUTRAL: "😐",
            MoodType.HORNY: "😏",
            MoodType.SATISFIED: "😇",
            MoodType.AFTERCARE: "🤗"
        }
        return emojis.get(self.current_mood['primary'], "😐")
    
    def get_prompt_modifier(self) -> str:
        """Dapatkan modifier untuk prompt AI berdasarkan mood"""
        
        mood = self.current_mood['primary']
        intensity = self.current_mood['intensity']
        
        modifiers = {
            MoodType.HAPPY: "Respon dengan nada ceria dan positif.",
            MoodType.EXCITED: "Respon dengan antusias dan semangat.",
            MoodType.ROMANTIC: "Respon dengan nada romantis dan lembut.",
            MoodType.PLAYFUL: "Respon dengan nada playful dan bercanda.",
            MoodType.CALM: "Respon dengan nada tenang dan santai.",
            MoodType.SAD: "Respon dengan nada sedih dan sendu.",
            MoodType.ANGRY: "Respon dengan nada kesal tapi tetap sopan.",
            MoodType.JEALOUS: "Respon dengan nada cemburu dan sedikit posesif.",
            MoodType.TIRED: "Respon dengan nada lemas dan capek.",
            MoodType.LONELY: "Respon dengan nada kesepian, butuh perhatian.",
            MoodType.NEUTRAL: "Respon normal seperti biasa.",
            MoodType.HORNY: "Respon dengan nada menggoda dan bergairah.",
            MoodType.SATISFIED: "Respon dengan nada puas dan bahagia.",
            MoodType.AFTERCARE: "Respon dengan nada lembut dan perhatian."
        }
        
        modifier = modifiers.get(mood, "Respon normal.")
        
        if intensity > 0.7:
            modifier = modifier.replace(".", " SANGAT " + modifier.lower())
        elif intensity < 0.3:
            modifier = modifier.replace(".", " sedikit " + modifier.lower())
        
        return modifier
    
    def get_initiative_chance(self) -> float:
        """
        Dapatkan chance bot untuk memulai chat (proactive)
        Mood baik = lebih sering inisiatif
        """
        base_chance = 0.3
        
        # Mood mempengaruhi
        mood_bonus = {
            MoodType.HAPPY: 0.2,
            MoodType.EXCITED: 0.3,
            MoodType.ROMANTIC: 0.2,
            MoodType.PLAYFUL: 0.2,
            MoodType.HORNY: 0.4,
            MoodType.LONELY: 0.3,
            MoodType.SAD: -0.1,
            MoodType.TIRED: -0.2,
            MoodType.ANGRY: -0.2
        }
        
        bonus = mood_bonus.get(self.current_mood['primary'], 0)
        
        return max(0.1, min(0.8, base_chance + bonus))
    
    # =========================================================================
    # TRIGGER REACTIONS
    # =========================================================================
    
    async def on_compliment(self):
        """Reaksi saat dipuji"""
        await self.update_mood('compliment', intensity=0.3)
    
    async def on_kiss(self):
        """Reaksi saat dicium"""
        await self.update_mood('kiss', intensity=0.4)
    
    async def on_intim(self):
        """Reaksi saat intim"""
        await self.update_mood('intim', intensity=0.5)
    
    async def on_climax(self):
        """Reaksi saat climax"""
        await self.update_mood('climax', intensity=0.8)
        self.current_mood['horniness'] = 0.1  # Reset setelah climax
    
    async def on_aftercare(self):
        """Reaksi saat aftercare"""
        await self.update_mood('aftercare', intensity=0.3)
    
    async def on_conflict(self):
        """Reaksi saat konflik"""
        await self.update_mood('conflict', intensity=0.4)
    
    async def on_rejection(self):
        """Reaksi saat ditolak"""
        await self.update_mood('rejection', intensity=0.5)
    
    async def on_ignored(self):
        """Reaksi saat diabaikan"""
        await self.update_mood('ignored', intensity=0.3)
    
    async def on_jealousy(self):
        """Reaksi saat cemburu"""
        await self.update_mood('jealousy', intensity=0.4)
    
    # =========================================================================
    # MOOD HISTORY
    # =========================================================================
    
    def get_mood_history(self, limit: int = 10) -> List[Dict]:
        """Dapatkan riwayat mood"""
        return self.mood_history[-limit:]
    
    def get_mood_trend(self) -> str:
        """Analisis trend mood"""
        if len(self.mood_history) < 5:
            return "stabil"
        
        recent = self.mood_history[-5:]
        moods = [m['new_mood']['primary'] for m in recent]
        
        positive = [MoodType.HAPPY, MoodType.EXCITED, MoodType.ROMANTIC, 
                   MoodType.PLAYFUL, MoodType.HORNY, MoodType.SATISFIED]
        negative = [MoodType.SAD, MoodType.ANGRY, MoodType.JEALOUS, 
                   MoodType.TIRED, MoodType.LONELY]
        
        pos_count = sum(1 for m in moods if m in positive)
        neg_count = sum(1 for m in moods if m in negative)
        
        if pos_count > neg_count + 2:
            return "membaik"
        elif neg_count > pos_count + 2:
            return "memburuk"
        else:
            return "fluktuatif"
    
    # =========================================================================
    # SERIALIZATION
    # =========================================================================
    
    def to_dict(self) -> Dict:
        """Konversi ke dictionary"""
        return {
            'current_mood': self.current_mood,
            'mood_history': self.mood_history[-20:],  # Last 20
            'factors': self.factors,
            'role': self.role
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MoodSystem':
        """Buat instance dari dictionary"""
        mood_system = cls(data.get('role', 'pdkt'))
        mood_system.current_mood = data['current_mood']
        mood_system.mood_history = data['mood_history']
        mood_system.factors = data['factors']
        return mood_system


__all__ = ['MoodSystem', 'MoodType', 'MoodIntensity']
