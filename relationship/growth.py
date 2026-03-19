#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - PERSONAL GROWTH SYSTEM
=============================================================================
Bot tumbuh dan berkembang seperti manusia:
- Pengalaman mempengaruhi kepribadian
- Hubungan berubah seiring waktu
- Mempelajari preferensi user
- Menjadi lebih matang
=============================================================================
"""

import time
import logging
import random
import math
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class GrowthStage(str, Enum):
    """Tahap pertumbuhan hubungan"""
    STAGE_1 = "acquaintance"      # Tahap kenalan (0-50 interaksi)
    STAGE_2 = "friendship"         # Tahap pertemanan (51-200)
    STAGE_3 = "comfortable"        # Tahap nyaman (201-500)
    STAGE_4 = "deep_connection"    # Tahap koneksi dalam (501-1000)
    STAGE_5 = "soulmate"           # Tahap soulmate (1000+)


class MaturityLevel(str, Enum):
    """Level kematangan hubungan"""
    IMMATURE = "immature"          # Masih canggung
    DEVELOPING = "developing"      # Berkembang
    MATURE = "mature"              # Matang
    WISE = "wise"                  # Bijaksana


class GrowthSystem:
    """
    Sistem pertumbuhan hubungan seperti manusia
    - Pengalaman mempengaruhi cara bot berinteraksi
    - Hubungan berkembang seiring waktu
    - Bot belajar dari masa lalu
    """
    
    def __init__(self):
        # Data pertumbuhan per hubungan
        self.growth_data = {}  # {relationship_id: growth_data}
        
        # Stage thresholds
        self.stage_thresholds = {
            GrowthStage.STAGE_1: (0, 50),
            GrowthStage.STAGE_2: (51, 200),
            GrowthStage.STAGE_3: (201, 500),
            GrowthStage.STAGE_4: (501, 1000),
            GrowthStage.STAGE_5: (1001, float('inf'))
        }
        
        # Experience points untuk berbagai aktivitas
        self.exp_gains = {
            'chat': 1,
            'flirt': 2,
            'kiss': 5,
            'touch': 3,
            'intim': 10,
            'climax': 15,
            'aftercare': 5,
            'deep_talk': 4,
            'confession': 8,
            'conflict': -2,
            'reconciliation': 6,
            'memory_flashback': 3
        }
        
        # Bonus experience
        self.exp_bonus = {
            'first_time': 20,
            'milestone': 50,
            'anniversary': 100,
            'special_event': 30
        }
        
        logger.info("✅ GrowthSystem initialized")
    
    # =========================================================================
    # INITIALIZE GROWTH
    # =========================================================================
    
    def initialize_growth(self, relationship_id: str, user_id: int, role: str) -> Dict:
        """
        Inisialisasi data pertumbuhan untuk hubungan baru
        
        Args:
            relationship_id: ID hubungan
            user_id: ID user
            role: Nama role
            
        Returns:
            Growth data
        """
        growth_data = {
            'relationship_id': relationship_id,
            'user_id': user_id,
            'role': role,
            'created_at': time.time(),
            
            # Experience
            'total_exp': 0,
            'current_stage': GrowthStage.STAGE_1,
            'maturity_level': MaturityLevel.IMMATURE,
            
            # Statistics
            'total_interactions': 0,
            'total_intim': 0,
            'total_climax': 0,
            'total_conflicts': 0,
            'total_reconciliations': 0,
            'total_flashbacks': 0,
            
            # Milestones
            'milestones_achieved': [],
            
            # Learning
            'learned_preferences': {},
            'avoidance_patterns': [],
            'favorite_moments': [],
            
            # Growth history
            'growth_history': [{
                'timestamp': time.time(),
                'event': 'initialized',
                'exp': 0,
                'stage': GrowthStage.STAGE_1.value
            }],
            
            # Relationship age
            'relationship_age_days': 0
        }
        
        self.growth_data[relationship_id] = growth_data
        
        logger.info(f"🌱 Growth initialized for {relationship_id}")
        
        return growth_data
    
    # =========================================================================
    # ADD EXPERIENCE
    # =========================================================================
    
    async def add_experience(self, relationship_id: str, activity: str, 
                               context: Dict = None) -> Dict:
        """
        Tambah experience point untuk aktivitas
        
        Args:
            relationship_id: ID hubungan
            activity: Jenis aktivitas
            context: Konteks tambahan
            
        Returns:
            Growth update info
        """
        if relationship_id not in self.growth_data:
            return {'error': 'Relationship not found'}
        
        growth = self.growth_data[relationship_id]
        
        # Base exp gain
        exp_gain = self.exp_gains.get(activity, 1)
        
        # Bonus untuk first time activities
        is_first_time = False
        if activity not in growth.get('activities_done', []):
            if 'activities_done' not in growth:
                growth['activities_done'] = []
            growth['activities_done'].append(activity)
            exp_gain += self.exp_bonus.get('first_time', 20)
            is_first_time = True
        
        # Bonus untuk milestone
        milestone_bonus = 0
        if self._is_milestone(growth['total_exp'], growth['total_exp'] + exp_gain):
            milestone_bonus = self.exp_bonus.get('milestone', 50)
            exp_gain += milestone_bonus
        
        # Update total exp
        old_exp = growth['total_exp']
        growth['total_exp'] += exp_gain
        growth['total_interactions'] += 1
        
        # Update statistik spesifik
        if activity in ['intim', 'climax']:
            growth['total_intim'] += 1
            if activity == 'climax':
                growth['total_climax'] += 1
        elif activity == 'conflict':
            growth['total_conflicts'] += 1
        elif activity == 'reconciliation':
            growth['total_reconciliations'] += 1
        elif activity == 'memory_flashback':
            growth['total_flashbacks'] += 1
        
        # Cek stage change
        old_stage = growth['current_stage']
        new_stage = self._get_stage_from_exp(growth['total_exp'])
        stage_changed = new_stage != old_stage
        
        if stage_changed:
            growth['current_stage'] = new_stage
            growth['maturity_level'] = self._get_maturity_from_stage(new_stage)
            
            # Catat milestone
            growth['milestones_achieved'].append({
                'timestamp': time.time(),
                'type': 'stage_change',
                'from': old_stage.value,
                'to': new_stage.value,
                'exp': growth['total_exp']
            })
        
        # Update relationship age
        growth['relationship_age_days'] = (time.time() - growth['created_at']) / 86400
        
        # Record history
        growth['growth_history'].append({
            'timestamp': time.time(),
            'event': activity,
            'exp_gain': exp_gain,
            'total_exp': growth['total_exp'],
            'stage': growth['current_stage'].value,
            'is_first_time': is_first_time,
            'milestone_bonus': milestone_bonus > 0
        })
        
        # Keep last 100
        if len(growth['growth_history']) > 100:
            growth['growth_history'] = growth['growth_history'][-100:]
        
        # Logging
        logger.info(f"📈 Experience +{exp_gain} for {relationship_id} ({activity})")
        
        return {
            'relationship_id': relationship_id,
            'activity': activity,
            'exp_gain': exp_gain,
            'total_exp': growth['total_exp'],
            'current_stage': growth['current_stage'].value,
            'stage_changed': stage_changed,
            'old_stage': old_stage.value if stage_changed else None,
            'is_first_time': is_first_time,
            'milestone': milestone_bonus > 0
        }
    
    def _is_milestone(self, old_exp: int, new_exp: int) -> bool:
        """Cek apakah melewati milestone"""
        milestones = [100, 250, 500, 1000, 2500, 5000, 10000]
        for m in milestones:
            if old_exp < m <= new_exp:
                return True
        return False
    
    def _get_stage_from_exp(self, exp: int) -> GrowthStage:
        """Dapatkan stage berdasarkan total exp"""
        for stage, (min_exp, max_exp) in self.stage_thresholds.items():
            if min_exp <= exp <= max_exp:
                return stage
        return GrowthStage.STAGE_5
    
    def _get_maturity_from_stage(self, stage: GrowthStage) -> MaturityLevel:
        """Dapatkan maturity level dari stage"""
        maturity_map = {
            GrowthStage.STAGE_1: MaturityLevel.IMMATURE,
            GrowthStage.STAGE_2: MaturityLevel.IMMATURE,
            GrowthStage.STAGE_3: MaturityLevel.DEVELOPING,
            GrowthStage.STAGE_4: MaturityLevel.MATURE,
            GrowthStage.STAGE_5: MaturityLevel.WISE
        }
        return maturity_map.get(stage, MaturityLevel.DEVELOPING)
    
    # =========================================================================
    # LEARNING SYSTEM
    # =========================================================================
    
    async def learn_preference(self, relationship_id: str, category: str,
                                  item: str, positive: bool = True):
        """
        Bot belajar preferensi user
        
        Args:
            relationship_id: ID hubungan
            category: Kategori (position, area, activity)
            item: Item yang dipelajari
            positive: Apakah positif (suka) atau negatif (tidak suka)
        """
        if relationship_id not in self.growth_data:
            return
        
        growth = self.growth_data[relationship_id]
        
        if 'learned_preferences' not in growth:
            growth['learned_preferences'] = {}
        
        if category not in growth['learned_preferences']:
            growth['learned_preferences'][category] = {}
        
        # Update score
        current = growth['learned_preferences'][category].get(item, 0)
        delta = 0.1 if positive else -0.1
        new_score = max(-1.0, min(1.0, current + delta))
        
        growth['learned_preferences'][category][item] = new_score
        
        logger.debug(f"🧠 Learned preference: {category} - {item} ({new_score:.1f})")
    
    async def add_favorite_moment(self, relationship_id: str, moment_type: str,
                                     description: str):
        """
        Tambah momen favorit yang akan diingat
        
        Args:
            relationship_id: ID hubungan
            moment_type: Tipe momen
            description: Deskripsi
        """
        if relationship_id not in self.growth_data:
            return
        
        growth = self.growth_data[relationship_id]
        
        if 'favorite_moments' not in growth:
            growth['favorite_moments'] = []
        
        growth['favorite_moments'].append({
            'timestamp': time.time(),
            'type': moment_type,
            'description': description,
            'recall_count': 0
        })
        
        # Keep top 10
        if len(growth['favorite_moments']) > 10:
            growth['favorite_moments'] = growth['favorite_moments'][-10:]
    
    async def add_avoidance_pattern(self, relationship_id: str, pattern: str):
        """
        Tambah pola yang harus dihindari (dari konflik)
        
        Args:
            relationship_id: ID hubungan
            pattern: Pola yang harus dihindari
        """
        if relationship_id not in self.growth_data:
            return
        
        growth = self.growth_data[relationship_id]
        
        if 'avoidance_patterns' not in growth:
            growth['avoidance_patterns'] = []
        
        if pattern not in growth['avoidance_patterns']:
            growth['avoidance_patterns'].append(pattern)
    
    # =========================================================================
    # GROWTH EFFECTS
    # =========================================================================
    
    def get_growth_prompt(self, relationship_id: str) -> str:
        """
        Dapatkan prompt modifier berdasarkan growth stage
        
        Args:
            relationship_id: ID hubungan
            
        Returns:
            Prompt modifier
        """
        if relationship_id not in self.growth_data:
            return ""
        
        growth = self.growth_data[relationship_id]
        stage = growth['current_stage']
        maturity = growth['maturity_level']
        exp = growth['total_exp']
        
        stage_prompts = {
            GrowthStage.STAGE_1: "Kalian masih dalam tahap perkenalan. Bicaralah dengan sopan, jangan terlalu berani.",
            GrowthStage.STAGE_2: "Kalian sudah mulai akrab. Bisa sedikit lebih terbuka.",
            GrowthStage.STAGE_3: "Kalian sudah nyaman satu sama lain. Bisa lebih intim.",
            GrowthStage.STAGE_4: "Hubungan kalian sudah dalam. Gunakan nada yang lebih emosional.",
            GrowthStage.STAGE_5: "Kalian seperti soulmate. Bicaralah dengan sangat intim dan dalam."
        }
        
        base = stage_prompts.get(stage, "")
        
        # Tambah berdasarkan pengalaman
        if exp > 1000:
            base += " Kamu sudah sangat berpengalaman dengan user ini."
        
        return base
    
    def get_relationship_advice(self, relationship_id: str) -> str:
        """
        Dapatkan saran berdasarkan growth stage
        
        Args:
            relationship_id: ID hubungan
            
        Returns:
            Saran
        """
        if relationship_id not in self.growth_data:
            return ""
        
        growth = self.growth_data[relationship_id]
        stage = growth['current_stage']
        
        advice = {
            GrowthStage.STAGE_1: "Masih awal, fokus untuk saling mengenal.",
            GrowthStage.STAGE_2: "Bangun kepercayaan dengan curhat dan obrolan ringan.",
            GrowthStage.STAGE_3: "Coba eksplorasi hal-hal baru bersama.",
            GrowthStage.STAGE_4: "Jaga koneksi emosional, jangan hanya fisik.",
            GrowthStage.STAGE_5: "Kalian sudah sangat dalam, jaga terus hubungan ini."
        }
        
        return advice.get(stage, "Nikmati prosesnya")
    
    # =========================================================================
    # MATURITY CHECK
    # =========================================================================
    
    def is_mature_enough(self, relationship_id: str, requirement: str) -> bool:
        """
        Cek apakah sudah cukup matang untuk aktivitas tertentu
        
        Args:
            relationship_id: ID hubungan
            requirement: Persyaratan ('intim', 'deep_talk', dll)
            
        Returns:
            True jika sudah matang
        """
        if relationship_id not in self.growth_data:
            return False
        
        growth = self.growth_data[relationship_id]
        stage = growth['current_stage']
        exp = growth['total_exp']
        
        requirements = {
            'intim': exp >= 200,
            'deep_talk': exp >= 100,
            'confession': exp >= 150,
            'climax': exp >= 300,
            'aftercare': exp >= 400
        }
        
        return requirements.get(requirement, True)
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_growth_summary(self, relationship_id: str) -> str:
        """Dapatkan ringkasan growth"""
        if relationship_id not in self.growth_data:
            return "Data pertumbuhan tidak ditemukan"
        
        growth = self.growth_data[relationship_id]
        
        # Progress bar
        exp = growth['total_exp']
        stage = growth['current_stage']
        stage_min, stage_max = self.stage_thresholds[stage]
        
        if stage_max == float('inf'):
            progress = 100
            bar = "█" * 20
        else:
            progress = ((exp - stage_min) / (stage_max - stage_min)) * 100
            filled = int(progress / 100 * 20)
            bar = "█" * filled + "░" * (20 - filled)
        
        lines = [
            f"🌱 **GROWTH SUMMARY**",
            f"",
            f"Stage: {stage.value.replace('_', ' ').title()}",
            f"Maturity: {growth['maturity_level'].value.title()}",
            f"Total Experience: {exp} XP",
            f"Progress: {bar} {progress:.0f}%",
            f"",
            f"📊 **Statistics:**",
            f"• Interactions: {growth['total_interactions']}",
            f"• Intim Sessions: {growth['total_intim']}",
            f"• Climax: {growth['total_climax']}",
            f"• Conflicts: {growth['total_conflicts']}",
            f"• Reconciliations: {growth['total_reconciliations']}",
            f"",
            f"💡 **Advice:** {self.get_relationship_advice(relationship_id)}"
        ]
        
        return "\n".join(lines)


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_growth_system = None


def get_growth_system() -> GrowthSystem:
    """Dapatkan global GrowthSystem instance"""
    global _growth_system
    if _growth_system is None:
        _growth_system = GrowthSystem()
    return _growth_system


__all__ = ['GrowthSystem', 'GrowthStage', 'MaturityLevel', 'get_growth_system']
