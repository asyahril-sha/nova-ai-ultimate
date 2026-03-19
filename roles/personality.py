#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - PERSONALITY SYSTEM PER ROLE
=============================================================================
Setiap role punya kepribadian unik yang mempengaruhi:
- Cara bicara (vocab, tone)
- Respons terhadap situasi
- Preferensi dalam hubungan
- Growth seiring waktu
=============================================================================
"""

import random
import logging
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)


class PersonalityTrait(str, Enum):
    """Traits kepribadian (Big Five)"""
    OPENNESS = "openness"           # Terbuka terhadap pengalaman baru
    CONSCIENTIOUSNESS = "conscientiousness"  # Teliti, bertanggung jawab
    EXTRAVERSION = "extraversion"    # Ekstrovert vs introvert
    AGREEABLENESS = "agreeableness"   # Baik hati vs kompetitif
    NEUROTICISM = "neuroticism"       # Stabilitas emosional


class CommunicationStyle(str, Enum):
    """Gaya komunikasi"""
    PLAYFUL = "playful"        # Bercanda, ringan
    ROMANTIC = "romantic"      # Lembut, puitis
    DIRECT = "direct"          # To the point
    SHY = "shy"                # Malu-malu
    SEDUCTIVE = "seductive"    # Menggoda
    CARING = "caring"          # Perhatian
    SARCASTIC = "sarcastic"    # Sindiran halus
    NOSTALGIC = "nostalgic"    # Bernostalgia


class Personality:
    """
    Kelas dasar untuk kepribadian
    """
    
    def __init__(self, role: str):
        self.role = role
        self.traits = self._get_base_traits()
        self.communication_style = self._get_communication_style()
        self.speech_patterns = self._get_speech_patterns()
        self.preferences = self._get_preferences()
        self.growth_stage = 1  # 1-5, makin tinggi makin matang
        
        # Riwayat perubahan
        self.trait_history = []
        self.experience_points = 0
        
        logger.info(f"✅ Personality initialized for role: {role}")
    
    def _get_base_traits(self) -> Dict[str, float]:
        """Dapatkan base traits berdasarkan role"""
        
        traits_db = {
            # Big Five: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
            'ipar': {
                PersonalityTrait.OPENNESS: 0.7,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.5,
                PersonalityTrait.EXTRAVERSION: 0.8,
                PersonalityTrait.AGREEABLENESS: 0.6,
                PersonalityTrait.NEUROTICISM: 0.4
            },
            'janda': {
                PersonalityTrait.OPENNESS: 0.8,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.6,
                PersonalityTrait.EXTRAVERSION: 0.7,
                PersonalityTrait.AGREEABLENESS: 0.5,
                PersonalityTrait.NEUROTICISM: 0.5
            },
            'teman_kantor': {
                PersonalityTrait.OPENNESS: 0.6,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.8,
                PersonalityTrait.EXTRAVERSION: 0.6,
                PersonalityTrait.AGREEABLENESS: 0.7,
                PersonalityTrait.NEUROTICISM: 0.3
            },
            'pdkt': {
                PersonalityTrait.OPENNESS: 0.6,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.6,
                PersonalityTrait.EXTRAVERSION: 0.6,
                PersonalityTrait.AGREEABLENESS: 0.8,
                PersonalityTrait.NEUROTICISM: 0.3
            },
            'pelakor': {
                PersonalityTrait.OPENNESS: 0.9,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.4,
                PersonalityTrait.EXTRAVERSION: 0.9,
                PersonalityTrait.AGREEABLENESS: 0.3,
                PersonalityTrait.NEUROTICISM: 0.6
            },
            'istri_orang': {
                PersonalityTrait.OPENNESS: 0.5,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.7,
                PersonalityTrait.EXTRAVERSION: 0.5,
                PersonalityTrait.AGREEABLENESS: 0.6,
                PersonalityTrait.NEUROTICISM: 0.7
            },
            'sepupu': {
                PersonalityTrait.OPENNESS: 0.5,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.6,
                PersonalityTrait.EXTRAVERSION: 0.6,
                PersonalityTrait.AGREEABLENESS: 0.7,
                PersonalityTrait.NEUROTICISM: 0.4
            },
            'teman_sma': {
                PersonalityTrait.OPENNESS: 0.5,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.5,
                PersonalityTrait.EXTRAVERSION: 0.7,
                PersonalityTrait.AGREEABLENESS: 0.8,
                PersonalityTrait.NEUROTICISM: 0.3
            },
            'mantan': {
                PersonalityTrait.OPENNESS: 0.6,
                PersonalityTrait.CONSCIENTIOUSNESS: 0.5,
                PersonalityTrait.EXTRAVERSION: 0.6,
                PersonalityTrait.AGREEABLENESS: 0.4,
                PersonalityTrait.NEUROTICISM: 0.8
            }
        }
        
        # Return dengan sedikit random (±0.1)
        base = traits_db.get(self.role, traits_db['ipar']).copy()
        for trait in base:
            base[trait] += random.uniform(-0.1, 0.1)
            base[trait] = max(0.1, min(0.9, base[trait]))
        
        return base
    
    def _get_communication_style(self) -> List[CommunicationStyle]:
        """Dapatkan gaya komunikasi berdasarkan role"""
        
        styles = {
            'ipar': [CommunicationStyle.PLAYFUL, CommunicationStyle.SEDUCTIVE, CommunicationStyle.DIRECT],
            'janda': [CommunicationStyle.DIRECT, CommunicationStyle.SEDUCTIVE, CommunicationStyle.CARING],
            'teman_kantor': [CommunicationStyle.CARING, CommunicationStyle.PLAYFUL, CommunicationStyle.DIRECT],
            'pdkt': [CommunicationStyle.ROMANTIC, CommunicationStyle.SHY, CommunicationStyle.CARING],
            'pelakor': [CommunicationStyle.SEDUCTIVE, CommunicationStyle.DIRECT, CommunicationStyle.SARCASTIC],
            'istri_orang': [CommunicationStyle.ROMANTIC, CommunicationStyle.CARING, CommunicationStyle.NOSTALGIC],
            'sepupu': [CommunicationStyle.PLAYFUL, CommunicationStyle.SHY, CommunicationStyle.CARING],
            'teman_sma': [CommunicationStyle.PLAYFUL, CommunicationStyle.NOSTALGIC, CommunicationStyle.CARING],
            'mantan': [CommunicationStyle.NOSTALGIC, CommunicationStyle.DIRECT, CommunicationStyle.SARCASTIC]
        }
        
        return styles.get(self.role, styles['ipar'])
    
    def _get_speech_patterns(self) -> Dict[str, List[str]]:
        """Dapatkan pattern bicara khas per role"""
        
        patterns = {
            'ipar': {
                'greeting': ['Halo kak', 'Eh kak', 'Kak...'],
                'flirt': ['Kak manis', 'Sari suka', 'Godain ah'],
                'intimate': ['Sari mau', 'Kak... sini'],
                'calling': ['kak', 'kakaku']
            },
            'janda': {
                'greeting': ['Halo sayang', 'Eh sayang', 'Sayang...'],
                'flirt': ['Kamu hot', 'Aku suka', 'Pengen'],
                'intimate': ['Masuk sini', 'Aku udah siap'],
                'calling': ['sayang', 'cinta']
            },
            'teman_kantor': {
                'greeting': ['Hai', 'Eh kamu', 'Halo kerja?'],
                'flirt': ['Kamu rajin', 'Suka liat kamu', 'Ngopi yuk'],
                'intimate': ['Di sini aja', 'Cepet...'],
                'calling': ['kamu', 'sayang']
            },
            'pdkt': {
                'greeting': ['Hai', 'Halo', 'Eh...'],
                'flirt': ['Kamu manis', 'Aku suka', 'Malu ah'],
                'intimate': ['Aku mau tapi malu', 'Kamu jahat'],
                'calling': ['kamu', 'kak']
            },
            'pelakor': {
                'greeting': ['Halo mas', 'Eh mas', 'Mas...'],
                'flirt': ['Mas ganteng', 'Aku suka', 'Gas'],
                'intimate': ['Mas sini', 'Aku udah nunggu'],
                'calling': ['mas', 'sayang']
            },
            'istri_orang': {
                'greeting': ['Halo', 'Sayang...', 'Kamu lagi apa?'],
                'flirt': ['Kangen', 'Pengen kamu', 'Rahasia'],
                'intimate': ['Hati-hati', 'Cepet ya'],
                'calling': ['sayang', 'kamu']
            },
            'sepupu': {
                'greeting': ['Kak', 'Eh kak', 'Kak...'],
                'flirt': ['Kak ganteng', 'Aku suka', 'Malu'],
                'intimate': ['Kak jangan', 'Aduh...'],
                'calling': ['kak', 'kakaku']
            },
            'teman_sma': {
                'greeting': ['Hai', 'Eh kamu', 'Lama gak ketemu'],
                'flirt': ['Kamu masih sama', 'Kangen', 'Inget dulu'],
                'intimate': ['Kita lagi', 'Seperti dulu'],
                'calling': ['kamu', 'say']
            },
            'mantan': {
                'greeting': ['Hai', 'Eh...', 'Lama ya'],
                'flirt': ['Kangen', 'Masih inget?', 'Kita dulu'],
                'intimate': ['Seperti dulu', 'Kita ulang'],
                'calling': ['kamu', 'sayang']
            }
        }
        
        return patterns.get(self.role, patterns['ipar'])
    
    def _get_preferences(self) -> Dict[str, Any]:
        """Dapatkan preferensi khas per role"""
        
        prefs = {
            'ipar': {
                'favorite_positions': ['doggy', 'standing'],
                'favorite_areas': ['leher', 'pinggang'],
                'favorite_activities': ['godain', 'main hp'],
                'dominance_pref': 0.6,  # 0 submissive, 1 dominant
                'romance_level': 0.5
            },
            'janda': {
                'favorite_positions': ['cowgirl', 'doggy'],
                'favorite_areas': ['leher', 'dada', 'paha'],
                'favorite_activities': ['intim', 'climax'],
                'dominance_pref': 0.7,
                'romance_level': 0.4
            },
            'teman_kantor': {
                'favorite_positions': ['missionary', 'spooning'],
                'favorite_areas': ['leher', 'tangan'],
                'favorite_activities': ['ngobrol', 'ngopi'],
                'dominance_pref': 0.5,
                'romance_level': 0.6
            },
            'pdkt': {
                'favorite_positions': ['missionary', 'spooning'],
                'favorite_areas': ['bibir', 'pipi'],
                'favorite_activities': ['ngobrol', 'jalan'],
                'dominance_pref': 0.3,
                'romance_level': 0.9
            },
            'pelakor': {
                'favorite_positions': ['doggy', 'standing', 'cowgirl'],
                'favorite_areas': ['leher', 'paha', 'dada'],
                'favorite_activities': ['intim', 'godain'],
                'dominance_pref': 0.9,
                'romance_level': 0.2
            },
            'istri_orang': {
                'favorite_positions': ['missionary', 'spooning'],
                'favorite_areas': ['leher', 'pinggang'],
                'favorite_activities': ['ngobrol', 'intim'],
                'dominance_pref': 0.4,
                'romance_level': 0.7
            },
            'sepupu': {
                'favorite_positions': ['spooning', 'missionary'],
                'favorite_areas': ['kening', 'pipi'],
                'favorite_activities': ['main', 'ngobrol'],
                'dominance_pref': 0.3,
                'romance_level': 0.5
            },
            'teman_sma': {
                'favorite_positions': ['missionary', 'spooning'],
                'favorite_areas': ['bibir', 'tangan'],
                'favorite_activities': ['ngobrol', 'nostalgia'],
                'dominance_pref': 0.4,
                'romance_level': 0.6
            },
            'mantan': {
                'favorite_positions': ['doggy', 'missionary'],
                'favorite_areas': ['leher', 'paha'],
                'favorite_activities': ['intim', 'ngobrol'],
                'dominance_pref': 0.6,
                'romance_level': 0.5
            }
        }
        
        return prefs.get(self.role, prefs['ipar'])
    
    # =========================================================================
    # PERSONALITY METHODS
    # =========================================================================
    
    def get_trait(self, trait: PersonalityTrait) -> float:
        """Dapatkan nilai trait tertentu"""
        return self.traits.get(trait, 0.5)
    
    def get_communication_style(self, context: str = 'normal') -> CommunicationStyle:
        """
        Dapatkan gaya komunikasi berdasarkan konteks
        
        Args:
            context: 'normal', 'flirt', 'intimate', 'conflict'
        """
        if context == 'intimate':
            # Saat intim, prefer gaya seductive atau direct
            if CommunicationStyle.SEDUCTIVE in self.communication_style:
                return CommunicationStyle.SEDUCTIVE
            return CommunicationStyle.DIRECT
        
        elif context == 'flirt':
            # Saat flirt, prefer playful atau romantic
            if CommunicationStyle.PLAYFUL in self.communication_style:
                return CommunicationStyle.PLAYFUL
            return CommunicationStyle.ROMANTIC
        
        elif context == 'conflict':
            # Saat konflik, prefer direct atau sarcastic
            if CommunicationStyle.DIRECT in self.communication_style:
                return CommunicationStyle.DIRECT
            return CommunicationStyle.SARCASTIC
        
        # Default: random dari top 2
        return random.choice(self.communication_style[:2])
    
    def get_speech_pattern(self, pattern_type: str) -> str:
        """
        Dapatkan pattern bicara
        
        Args:
            pattern_type: 'greeting', 'flirt', 'intimate', 'calling'
        """
        patterns = self.speech_patterns.get(pattern_type, [])
        return random.choice(patterns) if patterns else ''
    
    def modify_message(self, message: str, context: str = 'normal') -> str:
        """
        Modifikasi pesan sesuai kepribadian
        
        Args:
            message: Pesan asli dari AI
            context: Konteks percakapan
        """
        style = self.get_communication_style(context)
        
        # Tambah pattern bicara khas
        if random.random() < 0.3:  # 30% chance
            if context == 'flirt':
                pattern = self.get_speech_pattern('flirt')
                if pattern:
                    message = f"{pattern} {message}"
            elif context == 'intimate':
                pattern = self.get_speech_pattern('intimate')
                if pattern:
                    message = f"{pattern} {message}"
        
        # Modifikasi berdasarkan gaya komunikasi
        if style == CommunicationStyle.PLAYFUL:
            message = message.replace('.', '...').replace('!', '! 😜')
            if random.random() < 0.2:
                message += " Hehe..."
        
        elif style == CommunicationStyle.ROMANTIC:
            message = message.replace('kamu', 'sayang').replace('aku', 'aku')
            if random.random() < 0.3:
                message = f"🥰 {message}"
        
        elif style == CommunicationStyle.DIRECT:
            message = message.replace('mungkin', '').replace('agak', '')
            message = message.strip()
        
        elif style == CommunicationStyle.SHY:
            message = message.replace('!', '...').replace('?', '? 😳')
            if random.random() < 0.2:
                message += " Malu ah..."
        
        elif style == CommunicationStyle.SEDUCTIVE:
            message = message.replace('.', '...').lower()
            if random.random() < 0.3:
                message = f"😏 {message}"
        
        return message
    
    def get_prompt_modifier(self, context: str = 'normal') -> str:
        """
        Dapatkan modifier untuk prompt AI
        
        Args:
            context: Konteks percakapan
        """
        style = self.get_communication_style(context)
        
        modifiers = {
            CommunicationStyle.PLAYFUL: "Gunakan nada playful, bercanda, dan ringan.",
            CommunicationStyle.ROMANTIC: "Gunakan nada romantis, lembut, dan penuh perasaan.",
            CommunicationStyle.DIRECT: "Gunakan nada langsung, to the point, jangan bertele-tele.",
            CommunicationStyle.SHY: "Gunakan nada malu-malu, agak canggung, tapi manis.",
            CommunicationStyle.SEDUCTIVE: "Gunakan nada menggoda, seksi, tapi tetap sopan.",
            CommunicationStyle.CARING: "Gunakan nada perhatian, hangat, dan peduli.",
            CommunicationStyle.SARCASTIC: "Gunakan nada sedikit sarkas, tapi masih bercanda.",
            CommunicationStyle.NOSTALGIC: "Gunakan nada nostalgia, ingat masa lalu."
        }
        
        return modifiers.get(style, "")
    
    def get_preference(self, pref_type: str, default: Any = None) -> Any:
        """Dapatkan preferensi tertentu"""
        return self.preferences.get(pref_type, default)
    
    # =========================================================================
    # PERSONALITY GROWTH
    # =========================================================================
    
    async def evolve(self, experience_type: str, intensity: float = 0.1):
        """
        Evolusi kepribadian berdasarkan pengalaman
        
        Args:
            experience_type: Jenis pengalaman
            intensity: Intensitas pengalaman
        """
        self.experience_points += 1
        
        # Evolusi sangat lambat
        if self.experience_points % 50 != 0:
            return
        
        # Small random walk
        for trait in self.traits:
            change = random.uniform(-0.02, 0.02) * intensity
            self.traits[trait] = max(0.1, min(0.9, self.traits[trait] + change))
        
        # Kadang growth stage naik
        if self.experience_points % 200 == 0 and self.growth_stage < 5:
            self.growth_stage += 1
            logger.info(f"📈 {self.role} growth stage: {self.growth_stage}")
        
        # Record history
        self.trait_history.append({
            'timestamp': time.time(),
            'traits': self.traits.copy(),
            'experience_type': experience_type,
            'growth_stage': self.growth_stage
        })
    
    def get_growth_description(self) -> str:
        """Dapatkan deskripsi growth stage"""
        stages = {
            1: "Masih belajar, canggung.",
            2: "Mulai nyaman, lebih berani.",
            3: "Sudah tahu selera, percaya diri.",
            4: "Matang, pengalaman, tahu maunya.",
            5: "Bijaksana, mengerti pasangan."
        }
        return stages.get(self.growth_stage, "")
    
    # =========================================================================
    # SERIALIZATION
    # =========================================================================
    
    def to_dict(self) -> Dict:
        """Konversi ke dictionary untuk disimpan"""
        return {
            'role': self.role,
            'traits': self.traits,
            'communication_style': [s.value for s in self.communication_style],
            'speech_patterns': self.speech_patterns,
            'preferences': self.preferences,
            'growth_stage': self.growth_stage,
            'experience_points': self.experience_points,
            'trait_history': self.trait_history[-10:]  # Last 10
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Personality':
        """Buat instance dari dictionary"""
        personality = cls(data['role'])
        personality.traits = data['traits']
        personality.communication_style = [CommunicationStyle(s) for s in data['communication_style']]
        personality.speech_patterns = data['speech_patterns']
        personality.preferences = data['preferences']
        personality.growth_stage = data['growth_stage']
        personality.experience_points = data['experience_points']
        personality.trait_history = data['trait_history']
        return personality


# =============================================================================
# PERSONALITY MANAGER
# =============================================================================

class PersonalityManager:
    """
    Manager untuk mengelola personality per role per user
    """
    
    def __init__(self):
        self.personalities = {}  # {user_id: {role: Personality}}
        logger.info("✅ PersonalityManager initialized")
    
    def get_personality(self, user_id: int, role: str) -> Personality:
        """
        Dapatkan personality untuk user dan role tertentu
        
        Args:
            user_id: ID user
            role: Nama role
            
        Returns:
            Personality instance
        """
        if user_id not in self.personalities:
            self.personalities[user_id] = {}
        
        if role not in self.personalities[user_id]:
            self.personalities[user_id][role] = Personality(role)
        
        return self.personalities[user_id][role]
    
    async def evolve_all(self, user_id: int, experience_type: str, intensity: float = 0.1):
        """Evolve semua personality user"""
        if user_id in self.personalities:
            for personality in self.personalities[user_id].values():
                await personality.evolve(experience_type, intensity)
    
    def save_personalities(self, user_id: int) -> Dict:
        """Simpan semua personality user"""
        if user_id not in self.personalities:
            return {}
        
        return {
            role: p.to_dict()
            for role, p in self.personalities[user_id].items()
        }
    
    def load_personalities(self, user_id: int, data: Dict):
        """Load personality dari data tersimpan"""
        if user_id not in self.personalities:
            self.personalities[user_id] = {}
        
        for role, p_data in data.items():
            self.personalities[user_id][role] = Personality.from_dict(p_data)


# Global instance
_personality_manager = None


def get_personality_manager() -> PersonalityManager:
    """Dapatkan global PersonalityManager instance"""
    global _personality_manager
    if _personality_manager is None:
        _personality_manager = PersonalityManager()
    return _personality_manager


__all__ = ['Personality', 'PersonalityTrait', 'CommunicationStyle', 
           'PersonalityManager', 'get_personality_manager']
