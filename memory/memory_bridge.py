#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - MEMORY BRIDGE (ENHANCED)
=============================================================================
Menghubungkan semua sistem memory menjadi satu kesatuan
- Mengintegrasikan working, episodic, semantic, relationship
- Menyediakan interface seragam untuk mengambil/menyimpan memory
- Enhanced dengan growth system dan environment awareness
=============================================================================
"""

import time
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .working_memory import WorkingMemory
from .episodic_memory import EpisodicMemory, EpisodeType
from .semantic_memory import SemanticMemory
from .relationship_memory import RelationshipMemory
from ..dynamics.time_awareness import get_time_awareness
from ..dynamics.environment import get_environment_awareness
from ..relationship.growth import get_growth_system

logger = logging.getLogger(__name__)


class MemoryBridge:
    """
    Jembatan yang menghubungkan semua sistem memory
    Enhanced dengan growth, time, dan environment awareness
    """
    
    def __init__(self, user_id: int):
        """
        Args:
            user_id: ID user
        """
        self.user_id = user_id
        
        # Inisialisasi semua sistem memory
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.relationship = RelationshipMemory()
        
        # Sistem pendukung
        self.time = get_time_awareness()
        self.environment = get_environment_awareness()
        self.growth = get_growth_system()
        
        # Session aktif
        self.current_session_id = None
        self.current_role = None
        self.current_instance = None
        self.current_relationship_id = None
        
        # Buffer untuk konteks percakapan real-time
        self.context_buffer = {
            'location': None,
            'clothing': None,
            'position': None,
            'mood': None,
            'activity': None,
            'last_message': None,
            'last_response': None,
            'privacy_level': 1.0,
            'crowd_level': 'empty',
            'time_of_day': None
        }
        
        logger.info(f"✅ MemoryBridge Enhanced initialized for user {user_id}")
    
    # =========================================================================
    # SESSION MANAGEMENT
    # =========================================================================
    
    async def start_session(self, session_id: str, role: str, 
                              bot_name: str, instance_id: str = "default",
                              rel_type: str = "non_pdkt"):
        """
        Memulai sesi baru
        
        Args:
            session_id: ID sesi
            role: Role yang aktif
            bot_name: Nama bot
            instance_id: Instance ID (untuk multiple)
            rel_type: Tipe hubungan
        """
        self.current_session_id = session_id
        self.current_role = role
        self.current_instance = instance_id
        
        # Buat relationship ID
        self.current_relationship_id = f"{role}_{instance_id}_{self.user_id}"
        
        # Inisialisasi growth untuk hubungan ini
        self.growth.initialize_growth(
            relationship_id=self.current_relationship_id,
            user_id=self.user_id,
            role=role
        )
        
        # Reset context buffer
        self.context_buffer = {
            'location': None,
            'clothing': None,
            'position': None,
            'mood': None,
            'activity': None,
            'last_message': None,
            'last_response': None,
            'privacy_level': 1.0,
            'crowd_level': 'empty',
            'time_of_day': self.time.get_current_time()['time_of_day'].value
        }
        
        # Update time info
        time_info = self.time.get_current_time()
        self.context_buffer['time_of_day'] = time_info['time_of_day'].value
        self.context_buffer['greeting'] = time_info['greeting']
        
        logger.info(f"Session started: {session_id} ({role})")
    
    async def end_session(self):
        """Mengakhiri sesi"""
        if self.current_session_id:
            # Simpan ringkasan akhir sesi
            summaries = await self.working.get_recent_summaries(
                self.user_id, 
                self.current_session_id, 
                limit=1
            )
            
            if summaries:
                await self.episodic.add_episode(
                    session_id=self.current_session_id,
                    episode_type=EpisodeType.SESSION_END,
                    data={'summary': summaries[0].get('topics', ['umum'])},
                    importance=0.5
                )
        
        self.current_session_id = None
        self.current_role = None
        self.current_instance = None
        
        logger.info("Session ended")
    
    # =========================================================================
    # PROCESS MESSAGE (MAIN FUNCTION)
    # =========================================================================
    
    async def process_message(self, 
                             user_message: str, 
                             bot_response: str,
                             context: Dict) -> Dict:
        """
        Memproses pesan baru: menyimpan ke semua sistem memory
        
        Args:
            user_message: Pesan user
            bot_response: Respon bot
            context: Konteks percakapan (lokasi, mood, dll)
            
        Returns:
            Dict dengan hasil processing
        """
        if not self.current_session_id:
            raise ValueError("No active session. Call start_session first.")
        
        # Update context buffer
        self._update_context(context)
        
        # Update time and environment
        time_info = self.time.get_current_time()
        env_info = self.environment.get_current_env()
        
        # ===== 1. SIMPAN KE WORKING MEMORY =====
        await self.working.add_message(
            user_id=self.user_id,
            session_id=self.current_session_id,
            role=self.current_role,
            user_message=user_message,
            bot_message=bot_response,
            context={**self.context_buffer, **time_info, **env_info}
        )
        
        # ===== 2. EKSTRAK FAKTA DARI PESAN USER =====
        await self.semantic.extract_facts_from_message(
            user_id=self.user_id,
            message=user_message,
            role=self.current_role
        )
        
        # ===== 3. DETEKSI MOMEN PENTING =====
        episode = await self._detect_important_moment(
            user_message, 
            bot_response, 
            context
        )
        
        if episode:
            await self.episodic.add_episode(
                session_id=self.current_session_id,
                episode_type=episode['type'],
                data=episode['data'],
                importance=episode['importance'],
                emotional_tag=episode.get('emotion')
            )
            
            # Tambah experience untuk momen penting
            if self.current_relationship_id:
                await self.growth.add_experience(
                    relationship_id=self.current_relationship_id,
                    activity=episode['type'].value if hasattr(episode['type'], 'value') else str(episode['type']),
                    context=episode
                )
        
        # ===== 4. UPDATE RELATIONSHIP =====
        if self.current_relationship_id:
            # Record interaction
            await self.relationship.record_interaction(
                user_id=self.user_id,
                role=self.current_role,
                instance_id=self.current_instance,
                interaction_type='chat',
                data={'duration': 1, 'boost': 1.0}
            )
            
            # Add experience
            await self.growth.add_experience(
                relationship_id=self.current_relationship_id,
                activity='chat',
                context=context
            )
        
        # ===== 5. UPDATE GROWTH =====
        if self.current_relationship_id:
            # Belajar preferensi dari pesan
            if 'suka' in user_message.lower() or 'favorit' in user_message.lower():
                # Simple extraction, bisa ditingkatkan
                await self.growth.learn_preference(
                    relationship_id=self.current_relationship_id,
                    category='general',
                    item=user_message[:50],
                    positive=True
                )
        
        return {
            'session_id': self.current_session_id,
            'episode_detected': episode is not None,
            'facts_extracted': True,
            'context': self.context_buffer,
            'time': time_info,
            'environment': env_info
        }
    
    def _update_context(self, context: Dict):
        """Update context buffer dengan data terbaru"""
        for key in ['location', 'clothing', 'position', 'mood', 'activity']:
            if key in context:
                self.context_buffer[key] = context[key]
        
        if 'message' in context:
            self.context_buffer['last_message'] = context['message']
        
        if 'response' in context:
            self.context_buffer['last_response'] = context['response']
        
        # Update environment
        if 'location' in context and context['location']:
            self.environment.update_location(context['location'])
            env = self.environment.get_current_env()
            self.context_buffer['privacy_level'] = env.get('privacy_level', 1.0)
            self.context_buffer['crowd_level'] = env.get('crowd_level', 'empty').value if env.get('crowd_level') else 'empty'
    
    async def _detect_important_moment(self, 
                                      user_message: str, 
                                      bot_response: str,
                                      context: Dict) -> Optional[Dict]:
        """
        Deteksi apakah pesan ini包含 momen penting
        """
        combined = (user_message + " " + bot_response).lower()
        
        # Keywords untuk berbagai tipe episode
        moment_patterns = [
            # First kiss
            (['cium', 'kiss', 'first kiss'], EpisodeType.FIRST_KISS, 0.9, 'romantic'),
            # First intim
            (['intim', 'ml', 'first time', 'pertama kali intim'], EpisodeType.FIRST_INTIM, 1.0, 'passionate'),
            # First climax
            (['climax', 'come', 'keluar', 'first climax'], EpisodeType.CLIMAX, 1.0, 'intense'),
            # Confession
            (['sayang', 'cinta', 'love you', 'jatuh cinta'], EpisodeType.CONFESSION, 0.8, 'romantic'),
            # Jadi pacar
            (['jadi pacar', 'jadipacar', 'pacar'], EpisodeType.FIRST_DATE, 0.9, 'happy'),
            # Fight
            (['marah', 'kesel', 'kecewa'], EpisodeType.FIGHT, 0.7, 'angry'),
            # Reconciliation
            (['maaf', 'sorry', 'baikan'], EpisodeType.RECONCILIATION, 0.8, 'happy')
        ]
        
        for keywords, ep_type, importance, emotion in moment_patterns:
            if any(k in combined for k in keywords):
                # Cek apakah sudah pernah terjadi
                existing = await self.episodic.get_episodes(
                    session_id=self.current_session_id,
                    episode_type=ep_type,
                    limit=1
                )
                
                if not existing:
                    return {
                        'type': ep_type,
                        'data': {
                            'description': user_message[:100],
                            'context': context
                        },
                        'importance': importance,
                        'emotion': emotion
                    }
        
        return None
    
    # =========================================================================
    # RECALL MEMORY
    # =========================================================================
    
    async def recall(self, 
                    query: str, 
                    memory_type: Optional[str] = None,
                    limit: int = 5) -> List[Dict]:
        """
        Mengingat memori berdasarkan query
        
        Args:
            query: Kata kunci pencarian
            memory_type: Tipe memori (optional)
            limit: Jumlah maksimal
            
        Returns:
            List of memories
        """
        results = []
        
        # 1. Recall dari working memory
        summaries = await self.working.search_summaries(
            user_id=self.user_id,
            session_id=self.current_session_id,
            keyword=query
        )
        for s in summaries:
            s['source'] = 'working'
            s['relevance'] = 0.6
        results.extend(summaries[:limit])
        
        # 2. Recall dari episodic (momen spesial)
        episodes = await self.episodic.search_episodes(
            session_id=self.current_session_id,
            query=query
        )
        for ep in episodes[:limit]:
            ep['source'] = 'episodic'
            ep['relevance'] = 0.8
            results.append(ep)
        
        # 3. Recall dari semantic (fakta)
        facts = await self.semantic.get_all_facts(self.user_id)
        for category, cat_facts in facts.items():
            for fact_type, value in cat_facts.items():
                if query.lower() in str(value).lower():
                    results.append({
                        'source': 'semantic',
                        'category': category,
                        'type': fact_type,
                        'value': value,
                        'relevance': 0.7
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x.get('relevance', 0.5), reverse=True)
        
        return results[:limit]
    
    async def get_context_for_prompt(self) -> Dict:
        """
        Dapatkan semua konteks untuk prompt AI
        
        Returns:
            Dict dengan semua memory yang relevan
        """
        context = {}
        
        # 1. Recent working memory
        if self.current_session_id:
            summaries = await self.working.get_recent_summaries(
                self.user_id,
                self.current_session_id,
                limit=3
            )
            if summaries:
                context['recent_summaries'] = summaries
        
        # 2. Recent episodes
        episodes = await self.episodic.get_episodes(
            self.current_session_id,
            limit=3
        )
        if episodes:
            context['recent_episodes'] = [
                {
                    'type': e['type'].value if hasattr(e['type'], 'value') else str(e['type']),
                    'description': e.get('data', {}).get('description', ''),
                    'time_ago': self._format_time_ago(e['timestamp'])
                }
                for e in episodes
            ]
        
        # 3. Fakta user
        facts = await self.semantic.get_all_facts(self.user_id, min_confidence=0.6)
        if facts:
            context['user_facts'] = facts
        
        # 4. Preferensi
        if self.current_role:
            prefs = {}
            for cat in ['position', 'area', 'activity', 'location']:
                top = await self.semantic.get_top_preferences(
                    self.user_id,
                    cat,
                    self.current_role,
                    limit=3
                )
                if top:
                    prefs[cat] = top
            if prefs:
                context['preferences'] = prefs
        
        # 5. Growth info
        if self.current_relationship_id:
            growth = self.growth.growth_data.get(self.current_relationship_id)
            if growth:
                context['growth'] = {
                    'stage': growth['current_stage'].value,
                    'maturity': growth['maturity_level'].value,
                    'total_exp': growth['total_exp']
                }
                context['advice'] = self.growth.get_relationship_advice(self.current_relationship_id)
        
        # 6. Time awareness
        time_info = self.time.get_current_time()
        context['time'] = {
            'time_of_day': time_info['time_of_day'].value,
            'greeting': time_info['greeting'],
            'is_weekend': time_info['is_weekend'],
            'description': time_info['description']
        }
        
        # 7. Environment awareness
        env = self.environment.get_current_env()
        context['environment'] = {
            'location': env.get('location'),
            'crowd': env.get('crowd_level').value if env.get('crowd_level') else 'unknown',
            'risk': env.get('risk_level').value if env.get('risk_level') else 'unknown',
            'privacy': env.get('privacy_level', 1.0),
            'people': env.get('people_nearby', 0)
        }
        context['safety_tip'] = self.environment.get_safety_tip()
        
        # 8. Context buffer (real-time)
        context['current_context'] = {
            k: v for k, v in self.context_buffer.items() if v is not None
        }
        
        return context
    
    def _format_time_ago(self, timestamp: float) -> str:
        """Format waktu yang lalu"""
        diff = time.time() - timestamp
        
        if diff < 60:
            return "baru saja"
        elif diff < 3600:
            return f"{int(diff / 60)} menit lalu"
        elif diff < 86400:
            return f"{int(diff / 3600)} jam lalu"
        else:
            return f"{int(diff / 86400)} hari lalu"
    
    # =========================================================================
    # FLASHBACK GENERATION
    # =========================================================================
    
    async def generate_flashback(self, trigger: Optional[str] = None) -> Optional[str]:
        """
        Generate flashback dari memory
        
        Args:
            trigger: Kata kunci pemicu
            
        Returns:
            Teks flashback atau None
        """
        # Coba dari episodic dulu
        flashback = await self.episodic.generate_flashback_text(
            session_id=self.current_session_id,
            trigger=trigger
        )
        
        if flashback:
            # Update growth
            if self.current_relationship_id:
                await self.growth.add_experience(
                    relationship_id=self.current_relationship_id,
                    activity='memory_flashback',
                    context={'trigger': trigger}
                )
            return flashback
        
        # Jika tidak ada, coba dari working memory
        if trigger:
            memories = await self.recall(trigger, limit=1)
            if memories:
                mem = memories[0]
                content = mem.get('content') or mem.get('description', '')
                return f"Jadi inget... {content} {self._format_time_ago(mem.get('timestamp', time.time()))}."
        
        return None
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    async def get_memory_summary(self) -> str:
        """
        Format ringkasan memory untuk ditampilkan ke user
        
        Returns:
            String ringkasan
        """
        lines = ["🧠 **MEMORY SUMMARY**\n"]
        
        # Time info
        time_info = self.time.get_current_time()
        lines.append(f"🕐 {time_info['greeting']}! Sekarang {time_info['time_name']}.")
        lines.append(f"📅 {time_info['day_name']}, {time_info['date']}")
        lines.append("")
        
        # Environment
        env = self.environment.get_current_env()
        if env.get('location'):
            lines.append(f"📍 **Lokasi:** {env['location']}")
            lines.append(f"👥 {self.environment.get_crowd_description()}")
            lines.append(f"⚠️ {self.environment.get_safety_tip()}")
            lines.append("")
        
        # Episodic (momen spesial)
        episodes = await self.episodic.get_episodes(self.current_session_id, limit=5)
        if episodes:
            lines.append("📖 **Momen Spesial Terakhir:**")
            for ep in episodes[:3]:
                time_str = datetime.fromtimestamp(ep['timestamp']).strftime("%H:%M")
                desc = ep.get('data', {}).get('description', '')[:50]
                lines.append(f"• [{time_str}] {desc}...")
            lines.append("")
        
        # Fakta user
        facts = await self.semantic.get_user_summary(self.user_id)
        lines.append(facts)
        lines.append("")
        
        # Growth
        if self.current_relationship_id:
            growth_summary = self.growth.get_growth_summary(self.current_relationship_id)
            lines.append(growth_summary)
        
        return "\n".join(lines)


__all__ = ['MemoryBridge']
