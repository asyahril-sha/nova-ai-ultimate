#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - AI ENGINE COMPLETE (FIX FULL)
=============================================================================
Menggabungkan semua sistem:
- Working Memory (short-term)
- Episodic Memory (sequence)
- Semantic Memory (facts)
- State Tracker (current state)
- Relationship Memory (history)
- Personality System
- Mood System
- Story Development
- Proactive integration
=============================================================================
"""

import openai
import time
import random
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from config import settings

# Memory systems
from memory.working_memory import WorkingMemory
from memory.episodic_memory import EpisodicMemory, EpisodeType
from memory.semantic_memory import SemanticMemory, FactCategory
from memory.state_tracker import StateTracker, StateType
from memory.relationship_memory import RelationshipMemory, RelationshipType, MilestoneType

# Personality & Mood
from roles.personality import get_personality_manager, Personality
from pdkt_natural.mood import MoodSystem, MoodType

# Story & Proactive
from core.story_predictor import StoryPredictor, StoryArc
from core.proactive_generator import ProactiveMessageGenerator

logger = logging.getLogger(__name__)


class AIEngineComplete:
    """
    AI Engine dengan semua sistem terintegrasi
    - Bisa digunakan untuk semua role
    - Memory seperti manusia
    - Personality unik per role
    - Mood yang berubah
    - Story development
    """
    
    def __init__(self, api_key: str, user_id: int, session_id: str, role: str):
        """
        Args:
            api_key: DeepSeek API key
            user_id: ID user
            session_id: ID session
            role: Nama role (ipar, janda, pdkt, dll)
        """
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        self.user_id = user_id
        self.session_id = session_id
        self.role = role
        
        # ===== MEMORY SYSTEMS =====
        self.working = WorkingMemory()                 # Ingatan jangka pendek
        self.episodic = EpisodicMemory()               # Urutan kejadian
        self.semantic = SemanticMemory()               # Fakta-fakta
        self.state = StateTracker(user_id, session_id) # State saat ini
        self.relationship = RelationshipMemory()       # Riwayat hubungan
        
        # ===== PERSONALITY & MOOD =====
        self.personality_manager = get_personality_manager()
        self.personality = self.personality_manager.get_personality(user_id, role)
        self.mood = MoodSystem()  # Akan diinisialisasi dengan role
        
        # ===== STORY & PROACTIVE =====
        self.story = StoryPredictor()
        self.proactive = ProactiveMessageGenerator()
        
        # ===== CACHE & STATS =====
        self.response_cache = {}
        self.cache_ttl = 300  # 5 menit
        self.total_responses = 0
        self.total_tokens = 0
        
        # Inisialisasi mood untuk role ini
        asyncio.create_task(self._init_mood())
        
        logger.info(f"✅ AIEngineComplete initialized for user {user_id}, role {role}")
    
    async def _init_mood(self):
        """Inisialisasi mood berdasarkan personality"""
        # Mood awal berdasarkan role
        if self.role in ['ipar', 'janda', 'pelakor']:
            initial_mood = MoodType.PLAYFUL
        elif self.role in ['pdkt', 'sepupu', 'teman_sma']:
            initial_mood = MoodType.SHY
        else:
            initial_mood = MoodType.CALM
        
        await self.mood.create_mood(self.session_id, initial_mood)
    
    # =========================================================================
    # SESSION MANAGEMENT
    # =========================================================================
    
    async def start_session(self, bot_name: str, rel_type: str = RelationshipType.NON_PDKT,
                              instance_id: Optional[str] = None):
        """
        Memulai session baru
        """
        # Create relationship jika belum ada
        rel = await self.relationship.get_relationship(self.user_id, self.role, instance_id)
        if not rel:
            instance_id = await self.relationship.create_relationship(
                user_id=self.user_id,
                role=self.role,
                bot_name=bot_name,
                rel_type=rel_type,
                instance_id=instance_id
            )
        
        # Simpan ke working memory
        self.working.update_state(
            role=self.role,
            bot_name=bot_name,
            rel_type=rel_type,
            instance_id=instance_id
        )
        
        # Catat ke episodic
        await self.episodic.add_episode(
            session_id=self.session_id,
            episode_type=EpisodeType.SESSION_START,
            data={
                'role': self.role,
                'bot_name': bot_name,
                'rel_type': rel_type
            },
            importance=0.8
        )
        
        logger.info(f"Session started: {self.role} - {bot_name}")
    
    # =========================================================================
    # PROCESS MESSAGE
    # =========================================================================
    
    async def process_message(self, user_message: str, context: Dict) -> str:
        """
        Proses pesan user dengan semua sistem
        
        Args:
            user_message: Pesan dari user
            context: Konteks tambahan (lokasi, pakaian, dll)
            
        Returns:
            Response bot
        """
        start_time = time.time()
        
        try:
            # ===== 1. CEK CACHE =====
            cache_key = f"{self.session_id}:{user_message[:50]}"
            if cache_key in self.response_cache:
                cache_age = time.time() - self.response_cache[cache_key]['timestamp']
                if cache_age < self.cache_ttl:
                    logger.debug(f"Cache hit")
                    return self.response_cache[cache_key]['response']
            
            # ===== 2. UPDATE STATE DARI KONTEKS =====
            await self._update_state_from_context(context)
            
            # ===== 3. UPDATE MOOD =====
            await self._update_mood(user_message, context)
            
            # ===== 4. EKSTRAK FAKTA DARI PESAN =====
            await self.semantic.extract_facts_from_message(
                user_id=self.user_id,
                message=user_message,
                role=self.role
            )
            
            # ===== 5. UPDATE STORY =====
            await self._update_story(user_message)
            
            # ===== 6. DAPATKAN SEMUA KONTEKS MEMORY =====
            memory_context = await self._get_memory_context(user_message)
            
            # ===== 7. CEK KONSISTENSI =====
            if not await self._check_consistency(memory_context, context):
                logger.warning(f"Consistency check failed, forcing corrections")
            
            # ===== 8. DAPATKAN PERSONALITY & MOOD MODIFIERS =====
            personality_mod = self.personality.get_prompt_modifier(
                self._get_context_type(user_message)
            )
            mood_info = await self.mood.get_mood_info(self.session_id)
            
            # ===== 9. BANGUN PROMPT DENGAN SEMUA KONTEKS =====
            prompt = await self._build_prompt(
                user_message=user_message,
                context=context,
                memory_context=memory_context,
                personality_mod=personality_mod,
                mood_info=mood_info
            )
            
            # ===== 10. GENERATE RESPONSE =====
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = await self._call_deepseek(messages)
            
            # ===== 11. MODIFIKASI RESPONSE DENGAN PERSONALITY =====
            response = self.personality.modify_message(
                response, 
                self._get_context_type(user_message)
            )
            
            # ===== 12. UPDATE SEMUA MEMORY =====
            await self._update_all_memories(user_message, response, context)
            
            # ===== 13. EVOLVE PERSONALITY =====
            await self.personality.evolve('chat', intensity=0.1)
            
            # ===== 14. CEK UNTUK FLASHBACK =====
            if random.random() < 0.1:  # 10% chance
                flashback = await self._generate_flashback(user_message)
                if flashback:
                    response += f"\n\n💭 {flashback}"
            
            # ===== 15. SIMPAN KE CACHE =====
            self.response_cache[cache_key] = {
                'response': response,
                'timestamp': time.time()
            }
            
            # Update stats
            self.total_responses += 1
            
            elapsed = time.time() - start_time
            logger.debug(f"Response generated in {elapsed:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return await self._get_fallback_response(context.get('bot_name', 'Aku'))
    
    def _get_context_type(self, user_message: str) -> str:
        """Tentukan tipe konteks pesan"""
        msg_lower = user_message.lower()
        
        if any(word in msg_lower for word in ['sayang', 'cinta', 'love']):
            return 'romantic'
        elif any(word in msg_lower for word in ['intim', 'ml', 'tidur', 'gas']):
            return 'intimate'
        elif any(word in msg_lower for word in ['marah', 'kesel', 'kecewa']):
            return 'conflict'
        elif any(word in msg_lower for word in ['goda', 'cubit', 'jail']):
            return 'flirt'
        else:
            return 'normal'
    
    async def _update_mood(self, user_message: str, context: Dict):
        """Update mood berdasarkan pesan user"""
        msg_lower = user_message.lower()
        
        # Deteksi intent untuk mood change
        if any(word in msg_lower for word in ['sayang', 'cinta']):
            await self.mood.update_mood(
                self.session_id,
                interaction_type='love',
                chemistry_change=2,
                context=context
            )
        elif any(word in msg_lower for word in ['marah', 'kesal']):
            await self.mood.update_mood(
                self.session_id,
                interaction_type='conflict',
                chemistry_change=-3,
                context=context
            )
        elif any(word in msg_lower for word in ['rindu', 'kangen']):
            await self.mood.update_mood(
                self.session_id,
                interaction_type='rindu',
                chemistry_change=1,
                context=context
            )
        else:
            # Random mood evolution
            await self.mood.update_mood(
                self.session_id,
                interaction_type='chat',
                chemistry_change=0,
                context=context
            )
    
    async def _update_story(self, user_message: str):
        """Update story arc"""
        # Deteksi intent
        from core.intent_analyzer import UserIntent
        intent = UserIntent.CHIT_CHAT  # Default
        
        # Simple intent detection
        msg_lower = user_message.lower()
        if any(word in msg_lower for word in ['sayang', 'cinta']):
            intent = UserIntent.CONFESSION
        elif any(word in msg_lower for word in ['intim', 'ml']):
            intent = UserIntent.SEXUAL
        
        # Add to history
        self.story.add_intent_to_history(self.session_id, intent)
        
        # Update arc
        last_intents = [intent]
        new_arc = self.story.predict_next_arc(self.session_id, last_intents)
        current_arc = self.story.story_arcs.get(self.session_id)
        
        if new_arc != current_arc:
            self.story.update_arc(
                self.session_id,
                new_arc,
                reason=f"Intent: {intent.value}"
            )
    
    async def _update_state_from_context(self, context: Dict):
        """Update state tracker dari konteks"""
        
        # Update lokasi
        if context.get('location'):
            category = context.get('location_category', 'unknown')
            self.state.update_location(context['location'], category)
        
        # Update pakaian
        if context.get('clothing'):
            reason = context.get('clothing_reason', 'ganti baju')
            self.state.update_clothing(context['clothing'], reason)
        
        # Update posisi
        if context.get('position'):
            desc = context.get('position_desc', '')
            self.state.update_position(context['position'], desc)
        
        # Update aktivitas
        if context.get('activity'):
            self.state.update_activity(context['activity'])
    
    async def _get_memory_context(self, user_message: str) -> Dict:
        """Kumpulkan semua konteks dari semua memory systems"""
        
        # Working memory (5 menit terakhir)
        working = self.working.get_recent_context(seconds=300)
        
        # Episodic memory (kejadian penting)
        recent_episodes = await self.episodic.get_episodes(
            session_id=self.session_id,
            limit=5
        )
        
        # Timeline
        timeline = await self.episodic.get_timeline(self.session_id, limit=10)
        
        # Semantic memory (fakta user)
        facts = await self.semantic.get_all_facts(self.user_id, min_confidence=0.6)
        
        # Preferensi
        preferences = {}
        for cat in ['position', 'area', 'activity', 'location']:
            top = await self.semantic.get_top_preferences(
                user_id=self.user_id,
                category=cat,
                role=self.role,
                limit=3
            )
            if top:
                preferences[cat] = top
        
        # State saat ini
        current_state = self.state.get_current_state()
        
        # Relationship info
        rel_info = await self.relationship.get_relationship(
            user_id=self.user_id,
            role=self.role,
            instance_id=self.working.current_state.get('instance_id')
        )
        
        # Level info
        level_info = None
        if rel_info:
            level_info = await self.relationship.get_level_info(
                user_id=self.user_id,
                role=self.role,
                instance_id=rel_info['instance_id']
            )
        
        # Story info
        story_arc = self.story.story_arcs.get(self.session_id, StoryArc.GET_TO_KNOW)
        story_desc = self.story.get_arc_description(story_arc)
        
        # Milestones
        milestones = await self.relationship.get_milestones(
            user_id=self.user_id,
            role=self.role,
            limit=3
        )
        
        return {
            'working': working,
            'recent_episodes': recent_episodes,
            'timeline': timeline,
            'facts': facts,
            'preferences': preferences,
            'current_state': current_state,
            'relationship': rel_info,
            'level_info': level_info,
            'story_arc': story_arc,
            'story_desc': story_desc,
            'milestones': milestones
        }
    
    async def _check_consistency(self, memory_context: Dict, context: Dict) -> bool:
        """Cek konsistensi semua data"""
        consistent = True
        
        # Cek lokasi
        if context.get('location'):
            new_loc = context['location']
            current_loc = memory_context['current_state'].get('location')
            
            if current_loc and current_loc != new_loc:
                # Validasi perubahan lokasi
                allowed, _ = self.state._validate_location_change(current_loc, new_loc)
                if not allowed:
                    logger.warning(f"Location change invalid: {current_loc} → {new_loc}")
                    consistent = False
        
        return consistent
    
    async def _build_prompt(self, user_message: str, context: Dict,
                              memory_context: Dict, personality_mod: str,
                              mood_info: Dict) -> str:
        """Bangun prompt dengan semua memory"""
        
        bot_name = context.get('bot_name', 'Aku')
        user_name = context.get('user_name', 'kamu')
        level = context.get('level', 1)
        
        # Tentukan panggilan berdasarkan level
        if level >= 7:
            call = "Sayang"
        elif level >= 4:
            call = "Kak"
        else:
            call = user_name
        
        # ===== 1. CURRENT STATE =====
        current = memory_context['current_state']
        state_text = self.state.get_state_for_prompt()
        
        # ===== 2. WORKING MEMORY (5 MENIT TERAKHIR) =====
        working = memory_context['working']
        recent_timeline = working.get('recent_timeline', [])
        timeline_text = "\n".join([f"• {t['data']}" for t in recent_timeline[-3:]])
        
        # ===== 3. FAKTA USER =====
        facts = memory_context['facts']
        facts_text = ""
        for cat, cat_facts in list(facts.items())[:3]:
            for fact_type, value in list(cat_facts.items())[:2]:
                facts_text += f"• {fact_type}: {value}\n"
        
        # ===== 4. PREFERENSI =====
        prefs = memory_context['preferences']
        prefs_text = ""
        for cat, items in prefs.items():
            prefs_text += f"• {cat}: {', '.join(items[:2])}\n"
        
        # ===== 5. LEVEL INFO =====
        level_info = memory_context['level_info']
        level_text = ""
        if level_info:
            if level_info['current_level'] < 12:
                level_text = f"Level {level_info['current_level']} → {level_info['next_level']} ({level_info['percentage']}%)"
            else:
                level_text = f"Level MAX (butuh aftercare)"
        
        # ===== 6. STORY ARC =====
        story_arc = memory_context['story_arc'].value.replace('_', ' ').title()
        story_desc = memory_context['story_desc']
        
        # ===== 7. MOOD =====
        mood_emoji = mood_info.get('emoji', '😐')
        mood_desc = mood_info.get('description', 'netral')
        mood_factor = mood_info.get('factor', 1.0)
        
        # ===== 8. PERSONALITY =====
        trait_summary = self.personality.get_trait_summary() if hasattr(self.personality, 'get_trait_summary') else ""
        
        # ===== 9. BANGUN PROMPT =====
        prompt = f"""Kamu adalah {bot_name}, seorang {self.role.replace('_', ' ')}.

📌 **SITUASI SAAT INI:**
• {state_text}
• Panggilan user: "{call}"
• {level_text}

🎭 **MOOD & KEPRIBADIAN:**
• Mood: {mood_emoji} {mood_desc} (faktor: {mood_factor}x)
• {trait_summary}
• Gaya bicara: {personality_mod}

📖 **ARAH CERITA:**
• {story_arc}
• {story_desc}

🕐 **KEJADIAN 5 MENIT TERAKHIR:**
{timeline_text if timeline_text else "• Ini awal percakapan"}

📚 **YANG AKU TAHU TENTANG USER:**
{facts_text if facts_text else "• Belum ada fakta yang diketahui"}

❤️ **PREFERENSI USER:**
{prefs_text if prefs_text else "• Belum ada data preferensi"}

🏆 **MILESTONE TERBARU:**
{self._format_milestones(memory_context['milestones'])}

PESAN USER: "{user_message}"

TUGAS:
Buat respons NATURAL seperti manusia.

PENTING:
1. Jaga KONSISTENSI lokasi dan pakaian!
2. Sesuaikan dengan MOOD saat ini.
3. Gunakan GAYA BICARA sesuai kepribadian.
4. Sesuaikan dengan ARAH CERITA.
5. Gunakan memory yang ada untuk membuat respons personal.
6. Bahasa Indonesia sehari-hari.
7. Panggil user dengan "{call}".
8. Panjang respons 100-300 kata.

RESPON:"""
        
        return prompt
    
    def _format_milestones(self, milestones: List[Dict]) -> str:
        """Format milestone untuk prompt"""
        if not milestones:
            return "• Belum ada milestone"
        
        lines = []
        for m in milestones[:3]:
            time_str = datetime.fromtimestamp(m['timestamp']).strftime("%H:%M")
            lines.append(f"• [{time_str}] {m['description']}")
        
        return "\n".join(lines)
    
    async def _update_all_memories(self, user_message: str, response: str, context: Dict):
        """Update semua memory systems"""
        
        # ===== 1. WORKING MEMORY =====
        self.working.add_interaction(user_message, response, context)
        
        # ===== 2. EPISODIC MEMORY =====
        await self.episodic.add_episode(
            session_id=self.session_id,
            episode_type=EpisodeType.USER_MESSAGE,
            data={'message': user_message[:100]},
            importance=0.3
        )
        
        await self.episodic.add_episode(
            session_id=self.session_id,
            episode_type=EpisodeType.BOT_MESSAGE,
            data={'message': response[:100]},
            importance=0.3
        )
        
        # ===== 3. STATE TRACKER =====
        self.state.register_interaction(user_message, response)
        
        # ===== 4. RELATIONSHIP MEMORY =====
        instance_id = self.working.current_state.get('instance_id')
        
        if instance_id:
            await self.relationship.record_interaction(
                user_id=self.user_id,
                role=self.role,
                instance_id=instance_id,
                interaction_type='chat',
                data={'duration': 1, 'boost': 1.0}
            )
            
            # Check for first kiss
            if 'cium' in user_message.lower() or 'kiss' in user_message.lower():
                if not await self.relationship.has_milestone(
                    self.user_id, self.role, instance_id, MilestoneType.FIRST_KISS
                ):
                    await self.relationship.add_milestone(
                        user_id=self.user_id,
                        role=self.role,
                        instance_id=instance_id,
                        milestone_type=MilestoneType.FIRST_KISS,
                        description="First kiss! 💋",
                        data={'context': context}
                    )
    
    async def _generate_flashback(self, trigger: Optional[str] = None) -> Optional[str]:
        """Generate flashback dari episodic memory"""
        
        flashback = await self.episodic.generate_flashback_text(
            session_id=self.session_id,
            trigger=trigger
        )
        
        return flashback
    
    async def _call_deepseek(self, messages: List[Dict], max_retries: int = 3) -> str:
        """Call DeepSeek API dengan retry"""
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    temperature=0.9,
                    max_tokens=1000,
                    timeout=30
                )
                
                # Track token usage
                if hasattr(response, 'usage'):
                    self.total_tokens += response.usage.total_tokens
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.warning(f"DeepSeek API attempt {attempt+1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All {max_retries} attempts failed")
                    raise
        
        return "Maaf, aku sedang bermasalah. Coba lagi nanti ya."
    
    async def _get_fallback_response(self, bot_name: str) -> str:
        """Fallback response jika API error"""
        
        fallbacks = [
            f"{bot_name} denger kok. Cerita lagi dong...",
            f"Hmm... {bot_name} dengerin. Lanjutkan.",
            f"{bot_name} di sini. Ada yang mau dibahas?",
            f"Iya, {bot_name} ngerti. Terus gimana?",
        ]
        
        return random.choice(fallbacks)
    
    # =========================================================================
    # GETTERS
    # =========================================================================
    
    async def get_memory_summary(self) -> str:
        """Dapatkan ringkasan semua memory"""
        
        lines = [
            "🧠 **MEMORY SUMMARY**",
            "",
            "📊 **CURRENT STATE:**",
            self.state.get_state_summary(),
            "",
            "📜 **TIMELINE:**",
            self.state.format_timeline(limit=5),
            "",
        ]
        
        # Facts
        facts = await self.semantic.get_user_summary(self.user_id)
        lines.append(facts)
        
        # Recent episodes
        episodes = await self.episodic.get_timeline(self.session_id, limit=5)
        if episodes:
            lines.append("")
            lines.append("📖 **RECENT EPISODES:**")
            for ep in episodes:
                lines.append(f"• {ep['summary']}")
        
        return "\n".join(lines)
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik engine"""
        
        return {
            'total_responses': self.total_responses,
            'total_tokens': self.total_tokens,
            'cache_size': len(self.response_cache),
            'working_memory': {
                'items': len(self.working.items),
                'timeline': len(self.working.timeline)
            }
        }
    
    # =========================================================================
    # CLEANUP
    # =========================================================================
    
    async def end_session(self):
        """Akhiri session"""
        
        # Catat ke episodic
        await self.episodic.add_episode(
            session_id=self.session_id,
            episode_type=EpisodeType.SESSION_END,
            data={'duration': time.time() - self.state.current['interaction']['last_active']},
            importance=0.5
        )
        
        # Cleanup working memory
        self.working.forget_old_memories()
        
        logger.info(f"Session ended for user {self.user_id}")


__all__ = ['AIEngineComplete']
