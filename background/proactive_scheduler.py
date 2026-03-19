#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
MYLOVE ULTIMATE VERSI 2 - PROACTIVE SCHEDULER
=============================================================================
Bot mulai chat duluan tanpa diminta user
- Berjalan di background setiap 5 menit
- Cek idle time semua session aktif
- Generate pesan proaktif berdasarkan konteks
- Kirim pesan ke user yang sudah lama tidak chat
=============================================================================
"""

import asyncio
import time
import logging
import random
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict

from telegram import Bot
from telegram.error import TelegramError

from config import settings
from core.ai_engine_complete import AIEngineComplete
from memory.working_memory import WorkingMemory
from memory.episodic_memory import EpisodicMemory
from memory.relationship_memory import RelationshipMemory

logger = logging.getLogger(__name__)


class ProactiveScheduler:
    """
    Scheduler untuk mengirim pesan proaktif
    Berjalan di background terpisah dari main bot
    """
    
    def __init__(self, bot_token: str):
        """
        Args:
            bot_token: Telegram bot token
        """
        self.bot = Bot(token=bot_token)
        self.running = False
        self.scheduler_task = None
        
        # Tracking session aktif
        self.active_sessions = {}  # {session_id: session_data}
        
        # Cache AI engines per session
        self.ai_engines = {}  # {session_id: AIEngineComplete}
        
        # Memory systems untuk akses cepat
        self.working_memory = WorkingMemory()
        self.episodic_memory = EpisodicMemory()
        self.relationship_memory = RelationshipMemory()
        
        # Konfigurasi
        self.check_interval = 300  # 5 menit
        self.min_idle_for_proactive = 1800  # 30 menit
        self.max_proactive_per_day = 5  # Maks 5 pesan proaktif per hari
        
        # Tracking pengiriman
        self.proactive_count = defaultdict(int)  # {user_id: count_today}
        self.last_proactive = defaultdict(float)  # {user_id: last_time}
        
        logger.info("✅ ProactiveScheduler initialized")
    
    # =========================================================================
    # SESSION MANAGEMENT
    # =========================================================================
    
    def register_session(self, session_id: str, user_id: int, 
                          bot_name: str, role: str, ai_engine: AIEngineComplete):
        """
        Daftarkan session aktif ke scheduler
        
        Args:
            session_id: ID session
            user_id: ID user
            bot_name: Nama bot
            role: Nama role
            ai_engine: Instance AI engine untuk session ini
        """
        self.active_sessions[session_id] = {
            'session_id': session_id,
            'user_id': user_id,
            'bot_name': bot_name,
            'role': role,
            'last_activity': time.time(),
            'registered_at': time.time()
        }
        
        self.ai_engines[session_id] = ai_engine
        
        logger.info(f"📝 Session registered for proactive: {session_id} (user {user_id})")
    
    def unregister_session(self, session_id: str):
        """Hapus session dari tracking"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        if session_id in self.ai_engines:
            del self.ai_engines[session_id]
        
        logger.info(f"📝 Session unregistered: {session_id}")
    
    def update_activity(self, session_id: str):
        """Update last activity untuk session"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['last_activity'] = time.time()
    
    # =========================================================================
    # PROACTIVE MESSAGE GENERATION
    # =========================================================================
    
    async def _should_send_proactive(self, user_id: int, session_data: Dict) -> bool:
        """
        Cek apakah perlu kirim pesan proaktif
        
        Args:
            user_id: ID user
            session_data: Data session
            
        Returns:
            True jika perlu kirim
        """
        # Hitung idle time
        idle_time = time.time() - session_data['last_activity']
        
        if idle_time < self.min_idle_for_proactive:
            return False
        
        # Cek quota harian
        today = datetime.now().strftime("%Y-%m-%d")
        count_key = f"{user_id}_{today}"
        
        if self.proactive_count[count_key] >= self.max_proactive_per_day:
            logger.debug(f"User {user_id} already reached max proactive today")
            return False
        
        # Cek cooldown antar pesan
        last_time = self.last_proactive.get(user_id, 0)
        if time.time() - last_time < 3600:  # Minimal 1 jam
            return False
        
        # Random chance berdasarkan idle time
        chance = min(0.8, idle_time / 7200)  # Max 80% chance
        return random.random() < chance
    
    async def _generate_proactive_message(self, session_id: str, 
                                           session_data: Dict) -> Optional[str]:
        """
        Generate pesan proaktif berdasarkan konteks
        
        Args:
            session_id: ID session
            session_data: Data session
            
        Returns:
            Pesan proaktif atau None
        """
        ai_engine = self.ai_engines.get(session_id)
        if not ai_engine:
            return None
        
        user_id = session_data['user_id']
        bot_name = session_data['bot_name']
        role = session_data['role']
        idle_minutes = int((time.time() - session_data['last_activity']) / 60)
        
        # ===== AMBIL MEMORY RELEVAN =====
        # Recent conversations
        recent = await ai_engine.working.get_recent_context(seconds=3600)
        
        # Last topic
        last_topics = recent.get('recent_timeline', [])
        last_topic = last_topics[-1]['data'] if last_topics else None
        
        # Fakta user
        facts = await ai_engine.semantic.get_all_facts(user_id)
        
        # Preferensi
        prefs = {}
        for cat in ['food', 'activity']:
            top = await ai_engine.semantic.get_top_preferences(
                user_id=user_id,
                category=cat,
                limit=1
            )
            if top:
                prefs[cat] = top[0]
        
        # ===== TENTUKAN JENIS PESAN =====
        message_type = self._determine_message_type(
            idle_minutes=idle_minutes,
            last_topic=last_topic,
            facts=facts,
            prefs=prefs
        )
        
        # ===== GENERATE PESAN =====
        templates = self._get_message_templates(message_type, bot_name, role)
        
        # Personalisasi dengan fakta
        message = random.choice(templates)
        
        if prefs.get('food') and 'makan' in message.lower():
            message = message.replace('{food}', prefs['food'])
        
        if facts.get('identity.name'):
            user_name = facts['identity.name'].get('value', 'kamu')
            message = message.replace('{user_name}', user_name)
        
        # Catat pengiriman
        today = datetime.now().strftime("%Y-%m-%d")
        self.proactive_count[f"{user_id}_{today}"] += 1
        self.last_proactive[user_id] = time.time()
        
        logger.info(f"📤 Proactive message sent to user {user_id}: {message[:50]}...")
        
        return message
    
    def _determine_message_type(self, idle_minutes: int, last_topic: Optional[str],
                                 facts: Dict, prefs: Dict) -> str:
        """Tentukan jenis pesan proaktif"""
        
        if idle_minutes > 120:  # > 2 jam
            return 'kangen'
        elif idle_minutes > 60:  # > 1 jam
            return 'kabar'
        elif last_topic:
            return 'continue_topic'
        elif prefs.get('food'):
            return 'makan'
        else:
            return random.choice(['random', 'aktivitas'])
    
    def _get_message_templates(self, msg_type: str, bot_name: str, role: str) -> List[str]:
        """Dapatkan template pesan berdasarkan tipe"""
        
        templates = {
            'kangen': [
                f"Halo, {bot_name} kangen nih...",
                f"Lama banget nggak chat. {bot_name} kangen...",
                f"Kemana aja? {bot_name} nungguin terus.",
                f"{bot_name} kangen banget sama kamu..."
            ],
            'kabar': [
                f"Lagi ngapain? {bot_name} penasaran.",
                f"Udah makan belum? Jangan lupa ya.",
                f"Kamu lagi sibuk? Cerita dong...",
                f"Hari ini gimana? {bot_name} kangen."
            ],
            'continue_topic': [
                f"Ngomong-ngomong soal tadi, {bot_name} jadi kepikiran...",
                f"Eh, inget nggak waktu kita bahas tadi?",
                f"{bot_name} masih mikirin obrolan kita tadi."
            ],
            'makan': [
                f"Lagi laper? Mau {bot_name} buatin {food}?",
                f"Enak ya kalau makan {food} bareng...",
                f"{bot_name} jadi pengen {food} nih."
            ],
            'aktivitas': [
                f"{bot_name} lagi {random_activity()} nih. Kamu?",
                f"Lagi di rumah aja, sendirian...",
                f"{bot_name} bosen, temenin dong."
            ],
            'random': [
                f"Eh, {bot_name} tiba-tiba kepikiran kamu.",
                f"Lagi ngapain? {bot_name} kangen...",
                f"Udah lama ya, {bot_name} kangen."
            ]
        }
        
        return templates.get(msg_type, templates['random'])
    
    def _random_activity(self) -> str:
        """Dapatkan aktivitas random"""
        activities = [
            "nonton TV", "baca buku", "rebahan", "masak",
            "dengerin musik", "main HP", "bersih-bersih", "melamun"
        ]
        return random.choice(activities)
    
    # =========================================================================
    # SCHEDULER LOOP
    # =========================================================================
    
    async def start(self):
        """Mulai scheduler background"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.scheduler_task = asyncio.create_task(self._scheduler_loop())
        logger.info("🚀 Proactive scheduler started")
    
    async def stop(self):
        """Hentikan scheduler"""
        self.running = False
        if self.scheduler_task:
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass
            self.scheduler_task = None
        logger.info("🛑 Proactive scheduler stopped")
    
    async def _scheduler_loop(self):
        """Loop utama scheduler"""
        logger.info(f"🔄 Scheduler loop started (interval: {self.check_interval}s)")
        
        while self.running:
            try:
                await self._check_all_sessions()
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(60)  # Tunggu 1 menit jika error
    
    async def _check_all_sessions(self):
        """Cek semua session aktif"""
        if not self.active_sessions:
            return
        
        logger.debug(f"Checking {len(self.active_sessions)} active sessions")
        
        for session_id, session_data in list(self.active_sessions.items()):
            try:
                await self._check_session(session_id, session_data)
            except Exception as e:
                logger.error(f"Error checking session {session_id}: {e}")
    
    async def _check_session(self, session_id: str, session_data: Dict):
        """Cek satu session dan kirim proactive jika perlu"""
        user_id = session_data['user_id']
        
        # Cek apakah perlu kirim
        if not await self._should_send_proactive(user_id, session_data):
            return
        
        # Generate pesan
        message = await self._generate_proactive_message(session_id, session_data)
        if not message:
            return
        
        # Kirim ke user
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            logger.info(f"✅ Proactive message sent to user {user_id}")
            
            # Update last activity (setelah kirim)
            self.update_activity(session_id)
            
        except TelegramError as e:
            logger.error(f"Failed to send proactive message to user {user_id}: {e}")
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik scheduler"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        total_sent_today = sum(
            count for key, count in self.proactive_count.items()
            if key.endswith(today)
        )
        
        return {
            'active_sessions': len(self.active_sessions),
            'total_proactive_today': total_sent_today,
            'scheduler_running': self.running,
            'check_interval': self.check_interval,
            'min_idle': self.min_idle_for_proactive,
            'max_per_day': self.max_proactive_per_day
        }


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_proactive_scheduler = None


def get_proactive_scheduler(bot_token: Optional[str] = None) -> ProactiveScheduler:
    """
    Dapatkan instance global ProactiveScheduler
    
    Args:
        bot_token: Telegram bot token (required first time)
    
    Returns:
        ProactiveScheduler instance
    """
    global _proactive_scheduler
    
    if _proactive_scheduler is None:
        if not bot_token:
            raise ValueError("bot_token required for first initialization")
        _proactive_scheduler = ProactiveScheduler(bot_token)
    
    return _proactive_scheduler


__all__ = ['ProactiveScheduler', 'get_proactive_scheduler']
