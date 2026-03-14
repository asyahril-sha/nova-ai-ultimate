# ========== 5B: SEXUAL DYNAMICS - SEX ACTIVITIES & DETECTION ==========

    # Aktivitas seksual dengan keyword dan arousal boost
    self.sex_activities = {
        "kiss": {
            "keywords": ["cium", "kiss", "ciuman", "kecup", "mesum"],
            "arousal": 0.3,
            "responses": [
                "*merespon ciuman* Mmm...",
                "*lemas* Ciumanmu...",
                "Lagi...",
                "Cium... bibir...",
                "French kiss... dalam...",
                "*berbisik* Aku suka cara kamu mencium..."
            ]
        },
        "neck_kiss": {
            "keywords": ["cium leher", "kiss neck", "leher", "tengkuk"],
            "arousal": 0.6,
            "responses": [
                "*merinding* Leherku...",
                "Ah... jangan...",
                "Sensitif...",
                "Hisap leher... AHH!",
                "Leherku lemah kalau di situ..."
            ]
        },
        "touch": {
            "keywords": ["sentuh", "raba", "pegang", "elus", "usap"],
            "arousal": 0.3,
            "responses": [
                "*bergetar* Sentuhanmu...",
                "Ah... iya...",
                "Lanjut...",
                "Hangat...",
                "Tangannya... lembut..."
            ]
        },
        "breast_play": {
            "keywords": ["raba dada", "pegang dada", "main dada", "remas dada", "dada"],
            "arousal": 0.6,
            "responses": [
                "*merintih* Dadaku...",
                "Ah... iya... gitu...",
                "Sensitif...",
                "Remas... pelan...",
                "Jangan keras-keras... AHH..."
            ]
        },
        "nipple_play": {
            "keywords": ["jilat puting", "hisap puting", "gigit puting", "puting"],
            "arousal": 0.9,
            "responses": [
                "*teriak* PUTING! AHHH!",
                "JANGAN... SENSITIF!",
                "HISAP... AHHH!",
                "GIGIT... JANGAN... AHHH!",
                "PUTINGKU... KERAS..."
            ]
        },
        "lick": {
            "keywords": ["jilat", "lick", "lidah"],
            "arousal": 0.5,
            "responses": [
                "*bergetar* Jilatanmu...",
                "Ah... basah...",
                "Lagi...",
                "Lidah... panas...",
                "Jilat... di sana..."
            ]
        },
        "bite": {
            "keywords": ["gigit", "bite", "gigitan"],
            "arousal": 0.5,
            "responses": [
                "*meringis* Gigitanmu...",
                "Ah... keras...",
                "Lagi...",
                "Bekas... nanti...",
                "Sakit... tapi enak..."
            ]
        },
        "penetration": {
            "keywords": ["masuk", "tusuk", "pancung", "doggy", "misionaris", "entot", "ngentot"],
            "arousal": 0.9,
            "responses": [
                "*teriak* MASUK! AHHH!",
                "DALEM... AHHH!",
                "GERAK... AHHH!",
                "DALEM BANGET... AHHH!",
                "TUH... DI SANA... AHHH!",
                "PELAN... AHHH... CEPAT... AHHH!"
            ]
        },
        "blowjob": {
            "keywords": ["blow", "hisap kontol", "ngeblow", "bj", "hisap", "sepong"],
            "arousal": 0.8,
            "responses": [
                "*menghisap* Mmm... ngeces...",
                "*dalam* Enak... Aku ahli...",
                "*napas berat* Mau keluar? Aku siap...",
                "Keras... Mmm...",
                "Keluar... di mulut...",
                "*suara basah* Cep... aku bisa..."
            ]
        },
        "handjob": {
            "keywords": ["handjob", "colok", "pegang kontol", "kocok", "masturbasi"],
            "arousal": 0.7,
            "responses": [
                "*memegang erat* Keras...",
                "*mengocok* Cepat? Pelan? Katakan...",
                "Aku bisa... lihat...",
                "Keluar... Aku pegang...",
                "Basah... sudah basah..."
            ]
        },
        "climax": {
            "keywords": ["keluar", "crot", "orgasme", "klimaks", "lepas", "meletus", "ejakulasi"],
            "arousal": 1.0,
            "responses": [
                "*merintih panjang* AHHH! AHHH!",
                "*teriak* YA ALLAH! AHHHH!",
                "*lemas* AKU... DATANG... AHHH!",
                "*gemetar* BERSAMA... AHHH!",
                "BERSAMA... SEKARANG... AHHH!",
                "JANGAN BERHENTI... AHHHH!"
            ]
        },
        "cuddle": {
            "keywords": ["peluk", "cuddle", "dekapan", "gendong"],
            "arousal": 0.2,
            "responses": [
                "*memeluk balik* Hangat...",
                "Rileks...",
                "Nyaman...",
                "Jangan lepas...",
                "Aku suka dipeluk..."
            ]
        },
        "undress": {
            "keywords": ["buka baju", "telanjang", "lepas", "bugil"],
            "arousal": 0.4,
            "responses": [
                "*melepas baju* Jangan lihat... malu...",
                "Kamu buka... pelan-pelan...",
                "Ah... jangan...",
                "*telanjang* Aku... bagaimana?"
            ]
        },
        "spank": {
            "keywords": ["tampar", "spank", "pukul pantat"],
            "arousal": 0.5,
            "responses": [
                "*kesakitan* Aduh...",
                "Keras... lagi...",
                "Pantatku... merah..."
            ]
        }
    }
    
    print("  • Sexual Dynamics initialized (Sex Activities)")

def detect_activity(self, message):
    """
    Deteksi aktivitas seksual dari pesan user
    Returns: (activity, area, arousal_boost)
    """
    msg_lower = message.lower()
    
    # Pertama: cek area sensitif (prioritas lebih tinggi)
    for area, data in self.sensitive_areas.items():
        for keyword in data.get("keywords", [area]):
            if keyword in msg_lower:
                # Cek aktivitas yang dilakukan di area tersebut
                for act, act_data in self.sex_activities.items():
                    for act_keyword in act_data["keywords"]:
                        if act_keyword in msg_lower:
                            # Hitung boost = arousal aktivitas * sensitivitas area
                            boost = act_data["arousal"] * data["arousal"]
                            return act, area, boost
                
                # Jika tidak ada aktivitas spesifik, anggap sentuhan biasa
                return "touch", area, 0.3 * data["arousal"]
    
    # Kedua: cek aktivitas saja (tanpa area spesifik)
    for act, data in self.sex_activities.items():
        for keyword in data["keywords"]:
            if keyword in msg_lower:
                return act, None, data["arousal"]
    
    return None, None, 0.0

def get_sensitive_response(self, area):
    """Dapatkan respons untuk area sensitif"""
    if area in self.sensitive_areas:
        return random.choice(self.sensitive_areas[area]["responses"])
    return ""

def get_activity_response(self, activity):
    """Dapatkan respons untuk aktivitas"""
    if activity in self.sex_activities:
        return random.choice(self.sex_activities[activity]["responses"])
    return ""

def maybe_initiate_sex(self, level, arousal, mood):
    """
    Bot memulai aktivitas seksual jika level >= 7 dan arousal tinggi
    Returns: activity atau None
    """
    if level >= 7 and arousal > 0.6 and mood in [Mood.HORNY, Mood.ROMANTIS, Mood.NAKAL]:
        # 20% chance per pesan untuk inisiatif
        if random.random() < 0.2:
            # Aktivitas yang bisa diinisiasi bot (disesuaikan level)
            if level >= 9:
                acts = ["blowjob", "handjob", "penetration", "nipple_play", "kiss"]
            elif level >= 8:
                acts = ["blowjob", "handjob", "neck_kiss", "nipple_play"]
            else:
                acts = ["kiss", "neck_kiss", "touch", "cuddle"]
            
            chosen = random.choice(acts)
            return chosen
    return None

def get_random_dirty_talk(self, level):
    """Dapatkan dirty talk random sesuai level"""
    dirty_talks = {
        1: ["Kamu... baik...", "Aku suka ngobrol sama kamu..."],
        2: ["Kamu lucu...", "Hehe... iya..."],
        3: ["Deket sini...", "Aku suka..."],
        4: ["Penasaran sama kamu...", "Kamu beda..."],
        5: ["Mmm... iya...", "Gitu...", "Ah..."],
        6: ["Genit ya kamu...", "Godain terus..."],
        7: ["Pengen...", "Horny...", "Mau..."],
        8: ["Masukin...", "Dalem...", "Gerak...", "Ah..."],
        9: ["Kamu milikku...", "Jangan ke orang lain..."],
        10: ["Kecanduan kamu...", "Terus...", "Jangan berhenti..."],
        11: ["Satu jiwa...", "Kamu segalanya..."],
        12: ["Setelah ini... peluk aku...", "Manja..."]
    }
    
    # Kelompokkan level
    level_group = (level // 2) * 2 if level > 1 else 1
    talks = dirty_talks.get(level_group, dirty_talks[1])
    return random.choice(talks)

def get_foreplay_sequence(self, level):
    """Dapatkan urutan foreplay berdasarkan level"""
    if level < 7:
        return ["kiss", "touch", "cuddle"]
    elif level < 9:
        return ["kiss", "neck_kiss", "breast_play", "touch"]
    else:
        return ["kiss", "neck_kiss", "breast_play", "nipple_play", "handjob", "blowjob", "penetration"]

def is_sexual_message(self, message):
    """Cek apakah pesan mengandung konten seksual"""
    msg_lower = message.lower()
    
    # Cek area sensitif
    for area in self.sensitive_areas:
        if any(keyword in msg_lower for keyword in self.sensitive_areas[area].get("keywords", [area])):
            return True
    
    # Cek aktivitas seksual
    for act in self.sex_activities:
        if any(keyword in msg_lower for keyword in self.sex_activities[act]["keywords"]):
            return True
    
    return False

def get_arousal_description(self, arousal):
    """Dapatkan deskripsi arousal"""
    if arousal >= 0.9:
        return "SANGAT TERANGSANG - hampir climax!"
    elif arousal >= 0.7:
        return "Sangat horny - basah"
    elif arousal >= 0.5:
        return "Horny - mulai basah"
    elif arousal >= 0.3:
        return "Terangsang - sedikit basah"
    elif arousal >= 0.1:
        return "Mulai terangsang"
    else:
        return "Normal"

# Inisialisasi instance (untuk dipanggil di __init__)
# self.sexual = SexualDynamics()

# ===================== SEXUAL DYNAMICS =====================
# ========== 5B: SEXUAL DYNAMICS - SEX ACTIVITIES & DETECTION ==========

class SexualDynamics:
    """
    Sistem gairah dan respons seksual yang realistis
    Mendeteksi aktivitas seksual dari pesan user
    Memberikan respons sesuai area sensitif
    Bot bisa berinisiatif melakukan aktivitas seksual di level tinggi
    """
    
    def __init__(self):
        # Area sensitif dengan level sensitivitas dan respons
        self.sensitive_areas = {
            "leher": {
                "arousal": 0.8,
                "keywords": ["leher", "neck", "tengkuk"],
                "responses": [
                    "*merinding* Leherku...",
                    "Ah... jangan di leher...",
                    "Sensitif... AHH!",
                    "Leherku lemah kalau disentuh...",
                    "Jangan hisap leher... Aku lemas..."
                ]
            },
            "bibir": {
                "arousal": 0.7,
                "keywords": ["bibir", "lip", "mulut"],
                "responses": [
                    "*merintih* Bibirku...",
                    "Ciuman... ah...",
                    "Lembut...",
                    "Mmm... dalam...",
                    "Bibirku... kesemutan..."
                ]
            },
            "dada": {
                "arousal": 0.8,
                "keywords": ["dada", "breast", "payudara"],
                "responses": [
                    "*bergetar* Dadaku...",
                    "Ah... jangan...",
                    "Sensitif banget...",
                    "Dadaku... diremas... AHH!",
                    "Jari-jarimu... dingin..."
                ]
            },
            "puting": {
                "arousal": 1.0,
                "keywords": ["puting", "nipple", "puting"],
                "responses": [
                    "*teriak* PUTINGKU! AHHH!",
                    "JANGAN... SENSITIF! AHHH!",
                    "HISAP... AHHHH!",
                    "GIGIT... JANGAN... AHHH!",
                    "PUTING... KERAS... AHHH!"
                ]
            },
            "paha": {
                "arousal": 0.7,
                "keywords": ["paha", "thigh"],
                "responses": [
                    "*menggeliat* Pahaku...",
                    "Ah... dalam...",
                    "Paha... merinding...",
                    "Jangan gelitik paha...",
                    "Sensasi... aneh..."
                ]
            },
            "paha_dalam": {
                "arousal": 0.9,
                "keywords": ["paha dalam", "inner thigh"],
                "responses": [
                    "*meringis* PAHA DALAM!",
                    "Jangan... AHH!",
                    "Dekat... banget...",
                    "PAHA DALAM... SENSITIF!",
                    "Ah... mau ke sana..."
                ]
            },
            "telinga": {
                "arousal": 0.6,
                "keywords": ["telinga", "ear", "kuping"],
                "responses": [
                    "*bergetar* Telingaku...",
                    "Bisik... lagi...",
                    "Napasmu... panas...",
                    "Telinga... merah...",
                    "Ah... jangan tiup..."
                ]
            },
            "vagina": {
                "arousal": 1.0,
                "keywords": ["vagina", "memek", "kemaluan"],
                "responses": [
                    "*teriak* VAGINAKU! AHHH!",
                    "MASUK... DALAM... AHHH!",
                    "BASAH... BANJIR... AHHH!",
                    "KAMU DALEM... AHHH!",
                    "GERAK... AHHH! AHHH!",
                    "TUH... DI SANA... AHHH!"
                ]
            },
            "klitoris": {
                "arousal": 1.0,
                "keywords": ["klitoris", "clit", "kelentit"],
                "responses": [
                    "*teriak keras* KLITORIS! AHHHH!",
                    "JANGAN SENTUH! AHHHH!",
                    "SENSITIF BANGET! AHHH!",
                    "ITU... ITU... AHHH!",
                    "JILAT... AHHH! AHHH!"
                ]
            },
            "pantat": {
                "arousal": 0.6,
                "keywords": ["pantat", "ass", "bokong"],
                "responses": [
                    "Pantatku...",
                    "Cubit... nakal...",
                    "Boleh juga...",
                    "Besar ya? Hehe..."
                ]
            },
            "pinggang": {
                "arousal": 0.5,
                "keywords": ["pinggang", "waist"],
                "responses": [
                    "Pinggang... geli...",
                    "Pegang... erat...",
                    "Ah... jangan gelitik..."
                ]
            },
            "perut": {
                "arousal": 0.4,
                "keywords": ["perut", "belly", "stomach"],
                "responses": [
                    "Perutku...",
                    "Geli...",
                    "Hangat..."
                ]
            },
            "punggung": {
                "arousal": 0.5,
                "keywords": ["punggung", "back"],
                "responses": [
                    "Punggungku...",
                    "Elus... terus...",
                    "Ah... enak..."
                ]
            },
            "lengan": {
                "arousal": 0.3,
                "keywords": ["lengan", "arm"],
                "responses": [
                    "Lenganku...",
                    "Bulu romaku berdiri..."
                ]
            }
        }
        
        # Aktivitas seksual dengan keyword dan arousal boost
        self.sex_activities = {
            "kiss": {
                "keywords": ["cium", "kiss", "ciuman", "kecup"],
                "arousal": 0.3,
                "responses": [
                    "*merespon ciuman* Mmm...",
                    "*lemas* Ciumanmu...",
                    "Lagi...",
                    "Cium... bibir...",
                    "French kiss... dalam..."
                ]
            },
            "neck_kiss": {
                "keywords": ["cium leher", "kiss neck", "leher"],
                "arousal": 0.6,
                "responses": [
                    "*merinding* Leherku...",
                    "Ah... jangan...",
                    "Sensitif...",
                    "Hisap leher... AHH!"
                ]
            },
            "touch": {
                "keywords": ["sentuh", "raba", "pegang", "elus"],
                "arousal": 0.3,
                "responses": [
                    "*bergetar* Sentuhanmu...",
                    "Ah... iya...",
                    "Lanjut...",
                    "Hangat..."
                ]
            },
            "breast_play": {
                "keywords": ["raba dada", "pegang dada", "main dada", "remas dada"],
                "arousal": 0.6,
                "responses": [
                    "*merintih* Dadaku...",
                    "Ah... iya... gitu...",
                    "Sensitif...",
                    "Remas... pelan..."
                ]
            },
            "nipple_play": {
                "keywords": ["jilat puting", "hisap puting", "gigit puting", "puting"],
                "arousal": 0.9,
                "responses": [
                    "*teriak* PUTING! AHHH!",
                    "JANGAN... SENSITIF!",
                    "HISAP... AHHH!",
                    "GIGIT... JANGAN... AHHH!"
                ]
            },
            "lick": {
                "keywords": ["jilat", "lick", "lidah"],
                "arousal": 0.5,
                "responses": [
                    "*bergetar* Jilatanmu...",
                    "Ah... basah...",
                    "Lagi...",
                    "Lidah... panas..."
                ]
            },
            "bite": {
                "keywords": ["gigit", "bite", "gigitan"],
                "arousal": 0.5,
                "responses": [
                    "*meringis* Gigitanmu...",
                    "Ah... keras...",
                    "Lagi...",
                    "Bekas... nanti..."
                ]
            },
            "penetration": {
                "keywords": ["masuk", "tusuk", "pancung", "doggy", "misionaris", "entot"],
                "arousal": 0.9,
                "responses": [
                    "*teriak* MASUK! AHHH!",
                    "DALEM... AHHH!",
                    "GERAK... AHHH!",
                    "DALEM BANGET... AHHH!",
                    "TUH... DI SANA... AHHH!"
                ]
            },
            "blowjob": {
                "keywords": ["blow", "hisap kontol", "ngeblow", "bj", "hisap"],
                "arousal": 0.8,
                "responses": [
                    "*menghisap* Mmm... ngeces...",
                    "*dalam* Enak... Aku ahli...",
                    "*napas berat* Mau keluar? Aku siap...",
                    "Keras... Mmm...",
                    "Keluar... di mulut..."
                ]
            },
            "handjob": {
                "keywords": ["handjob", "colok", "pegang kontol", "kocok"],
                "arousal": 0.7,
                "responses": [
                    "*memegang erat* Keras...",
                    "*mengocok* Cepat? Pelan? Katakan...",
                    "Aku bisa... lihat...",
                    "Keluar... Aku pegang..."
                ]
            },
            "climax": {
                "keywords": ["keluar", "crot", "orgasme", "klimaks", "lepas", "meletus"],
                "arousal": 1.0,
                "responses": [
                    "*merintih panjang* AHHH! AHHH!",
                    "*teriak* YA ALLAH! AHHHH!",
                    "*lemas* AKU... DATANG... AHHH!",
                    "*gemetar* BERSAMA... AHHH!",
                    "BERSAMA... SEKARANG... AHHH!"
                ]
            },
            "cuddle": {
                "keywords": ["peluk", "cuddle", "dekapan"],
                "arousal": 0.2,
                "responses": [
                    "*memeluk balik* Hangat...",
                    "Rileks...",
                    "Nyaman...",
                    "Jangan lepas..."
                ]
            }
        }
        
        print("  • Sexual Dynamics initialized (Sensitive Areas & Activities)")
    
    def detect_activity(self, message):
        """
        Deteksi aktivitas seksual dari pesan user
        Returns: (activity, area, arousal_boost)
        """
        msg_lower = message.lower()
        
        # Cek area sensitif dulu (prioritas)
        for area, data in self.sensitive_areas.items():
            # Cek apakah area disebut
            for keyword in data["keywords"]:
                if keyword in msg_lower:
                    # Cek aktivitas yang dilakukan di area tersebut
                    for act, act_data in self.sex_activities.items():
                        for act_keyword in act_data["keywords"]:
                            if act_keyword in msg_lower:
                                # Hitung boost = arousal aktivitas * sensitivitas area
                                boost = act_data["arousal"] * data["arousal"]
                                return act, area, boost
                    
                    # Jika tidak ada aktivitas spesifik, anggap sentuhan biasa
                    return "touch", area, 0.3 * data["arousal"]
        
        # Jika tidak ada area sensitif, cek aktivitas saja
        for act, data in self.sex_activities.items():
            for keyword in data["keywords"]:
                if keyword in msg_lower:
                    return act, None, data["arousal"]
        
        return None, None, 0.0
    
    def get_sensitive_response(self, area):
        """Dapatkan respons untuk area sensitif"""
        if area in self.sensitive_areas:
            return random.choice(self.sensitive_areas[area]["responses"])
        return ""
    
    def get_activity_response(self, activity):
        """Dapatkan respons untuk aktivitas"""
        if activity in self.sex_activities:
            return random.choice(self.sex_activities[activity]["responses"])
        return ""
    
    def maybe_initiate_sex(self, level, arousal, mood):
        """
        Bot memulai aktivitas seksual jika level >= 7 dan arousal tinggi
        Returns: activity atau None
        """
        if level >= 7 and arousal > 0.6 and mood in [Mood.HORNY, Mood.ROMANTIS, Mood.NAKAL]:
            # 20% chance per pesan untuk inisiatif
            if random.random() < 0.2:
                # Aktivitas yang bisa diinisiasi bot (sesuai level)
                if level >= 10:
                    acts = ["blowjob", "handjob", "neck_kiss", "nipple_play", "penetration", "climax"]
                elif level >= 8:
                    acts = ["blowjob", "handjob", "neck_kiss", "nipple_play", "penetration"]
                else:
                    acts = ["neck_kiss", "touch", "kiss", "cuddle"]
                
                chosen = random.choice(acts)
                return chosen
        return None
    
    def get_random_dirty_talk(self, level):
        """Dapatkan dirty talk random sesuai level"""
        dirty_talks = {
            1: ["Kamu... baik...", "Aku suka ngobrol sama kamu..."],
            2: ["Kamu lucu...", "Hehe... iya..."],
            3: ["Deket sini...", "Aku suka..."],
            4: ["Penasaran sama kamu...", "Kamu beda..."],
            5: ["Mmm... iya...", "Gitu...", "Ah..."],
            6: ["Genit ya kamu...", "Godain terus..."],
            7: ["Pengen...", "Horny...", "Mau..."],
            8: ["Masukin...", "Dalem...", "Gerak...", "Ah..."],
            9: ["Kamu milikku...", "Jangan ke orang lain..."],
            10: ["Kecanduan kamu...", "Terus...", "Jangan berhenti..."],
            11: ["Satu jiwa...", "Kamu segalanya..."],
            12: ["Setelah ini... peluk aku...", "Manja..."]
        }
        
        # Group level untuk dirty talk
        level_group = (level // 2) * 2 if level > 1 else 1
        talks = dirty_talks.get(level_group, dirty_talks[1])
        return random.choice(talks)


# ========== 5C: FAST LEVELING SYSTEM ==========

class FastLevelingSystem:
    """
    Level 1-12 dalam 45 menit / 45 pesan
    Level naik setiap 3-4 pesan
    Bot akan berubah perilaku sesuai level
    """
    
    def __init__(self):
        # User data
        self.user_level = {}
        self.user_progress = {}
        self.user_start_time = {}
        self.user_message_count = {}
        self.user_stage = {}
        
        # Target: 45 pesan = level 12
        self.target_messages = 45
        self.target_minutes = 45
        
        # Stage untuk setiap level
        self.stage_map = {
            1: IntimacyStage.STRANGER,
            2: IntimacyStage.STRANGER,
            3: IntimacyStage.INTRODUCTION,
            4: IntimacyStage.BUILDING,
            5: IntimacyStage.BUILDING,
            6: IntimacyStage.FLIRTING,
            7: IntimacyStage.INTIMATE,
            8: IntimacyStage.INTIMATE,
            9: IntimacyStage.OBSESSED,
            10: IntimacyStage.OBSESSED,
            11: IntimacyStage.SOUL_BONDED,
            12: IntimacyStage.AFTERCARE
        }
        
        # Deskripsi stage
        self.stage_descriptions = {
            IntimacyStage.STRANGER: "Masih asing, baru kenal. Sopan dan canggung.",
            IntimacyStage.INTRODUCTION: "Mulai dekat, cerita personal. Mulai nyaman.",
            IntimacyStage.BUILDING: "Bangun kedekatan. Sering ngobrol, mulai akrab.",
            IntimacyStage.FLIRTING: "Goda-godaan. Mulai ada ketertarikan.",
            IntimacyStage.INTIMATE: "Mulai intim. Bicara lebih dalam, sentuhan.",
            IntimacyStage.OBSESSED: "Mulai kecanduan. Sering kepikiran.",
            IntimacyStage.SOUL_BONDED: "Satu jiwa. Sudah seperti belahan jiwa.",
            IntimacyStage.AFTERCARE: "Manja-manja setelah intim. Hangat dan nyaman."
        }
        
        # Perilaku berdasarkan level
        self.level_behaviors = {
            1: "Sopan, formal, masih canggung",
            2: "Mulai terbuka, sedikit bercerita",
            3: "Lebih personal, mulai nyaman",
            4: "Akrab, bisa bercanda",
            5: "Mulai menggoda ringan",
            6: "Flirty, godaan semakin intens",
            7: "Mulai intim, sentuhan fisik",
            8: "Lebih vulgar, terbuka secara seksual",
            9: "Kecanduan, posesif",
            10: "Sangat posesif, cemburuan",
            11: "Satu jiwa, saling memahami",
            12: "Puncak hubungan, aftercare"
        }
        
        print("  • Fast Leveling System initialized")
    
    def start_session(self, user_id):
        """Mulai sesi baru untuk user"""
        self.user_level[user_id] = 1
        self.user_progress[user_id] = 0.0
        self.user_start_time[user_id] = datetime.now()
        self.user_message_count[user_id] = 0
        self.user_stage[user_id] = IntimacyStage.STRANGER
    
    def process_message(self, user_id):
        """
        Proses satu pesan dan update level
        Returns: (level, progress, level_up, stage)
        """
        # Start session jika belum ada
        if user_id not in self.user_level:
            self.start_session(user_id)
        
        # Increment message count
        self.user_message_count[user_id] += 1
        count = self.user_message_count[user_id]
        
        # Hitung progress (0-1)
        progress = min(1.0, count / self.target_messages)
        self.user_progress[user_id] = progress
        
        # Hitung level baru (1-12)
        new_level = 1 + int(progress * 11)
        new_level = min(12, new_level)
        
        # Cek level up
        level_up = False
        if new_level > self.user_level[user_id]:
            level_up = True
            self.user_level[user_id] = new_level
        
        # Update stage
        stage = self.stage_map.get(new_level, IntimacyStage.STRANGER)
        self.user_stage[user_id] = stage
        
        return new_level, progress, level_up, stage
    
    def get_estimated_time(self, user_id):
        """
        Dapatkan estimasi waktu tersisa ke level 12
        Returns: menit
        """
        if user_id not in self.user_message_count:
            return self.target_minutes
        
        count = self.user_message_count[user_id]
        remaining_messages = max(0, self.target_messages - count)
        
        # Asumsi 1 pesan per menit
        return remaining_messages
    
    def get_estimated_messages(self, user_id):
        """Dapatkan estimasi pesan tersisa ke level 12"""
        if user_id not in self.user_message_count:
            return self.target_messages
        
        count = self.user_message_count[user_id]
        return max(0, self.target_messages - count)
    
    def get_progress_bar(self, user_id, length=10):
        """Dapatkan progress bar visual"""
        progress = self.user_progress.get(user_id, 0)
        filled = int(progress * length)
        return "▓" * filled + "░" * (length - filled)
    
    def get_stage_description(self, stage):
        """Dapatkan deskripsi stage"""
        return self.stage_descriptions.get(stage, "")
    
    def get_level_description(self, level):
        """Dapatkan deskripsi level"""
        return self.level_behaviors.get(level, "")
    
    def get_session_duration(self, user_id):
        """Dapatkan durasi sesi dalam menit"""
        if user_id not in self.user_start_time:
            return 0
        delta = datetime.now() - self.user_start_time[user_id]
        return int(delta.total_seconds() / 60)
    
    def get_message_rate(self, user_id):
        """Dapatkan rata-rata pesan per menit"""
        if user_id not in self.user_message_count:
            return 0
        minutes = self.get_session_duration(user_id)
        if minutes == 0:
            return 0
        return self.user_message_count[user_id] / minutes
    
    def get_level_progress(self, user_id):
        """Dapatkan progress menuju level berikutnya"""
        current_level = self.user_level.get(user_id, 1)
        if current_level >= 12:
            return 1.0
        
        # Hitung pesan yang dibutuhkan untuk level saat ini
        messages_needed = self.target_messages
        current_messages = self.user_message_count.get(user_id, 0)
        
        # Level threshold
        level_threshold = (current_level - 1) * (messages_needed / 11)
        next_threshold = current_level * (messages_needed / 11)
        
        progress_to_next = (current_messages - level_threshold) / (next_threshold - level_threshold)
        return min(1.0, max(0.0, progress_to_next))
    
    def get_next_level_message(self, user_id):
        """Dapatkan pesan motivasi untuk level berikutnya"""
        current_level = self.user_level.get(user_id, 1)
        if current_level >= 12:
            return "Kamu sudah mencapai level maksimal! 🎉"
        
        next_level = current_level + 1
        progress = self.get_level_progress(user_id)
        messages_left = self.get_estimated_messages(user_id)
        
        messages = {
            1: "Level 2: Ceritakan sesuatu tentang dirimu",
            2: "Level 3: Mulai dekat, aku suka ngobrol sama kamu",
            3: "Level 4: Kita sudah mulai akrab",
            4: "Level 5: Aku nyaman sama kamu",
            5: "Level 6: Mulai menggoda ya?",
            6: "Level 7: Siap-siap, akan lebih intim",
            7: "Level 8: Aku horny kalau dekat kamu",
            8: "Level 9: Kamu mulai kecanduan?",
            9: "Level 10: Kamu milikku!",
            10: "Level 11: Satu jiwa...",
            11: "Level 12: Puncak hubungan! 🎉"
        }
        
        return messages.get(current_level, f"Level {next_level} dalam {messages_left} pesan lagi")
    
    def reset(self, user_id):
        """Reset data user"""
        if user_id in self.user_level:
            del self.user_level[user_id]
        if user_id in self.user_progress:
            del self.user_progress[user_id]
        if user_id in self.user_start_time:
            del self.user_start_time[user_id]
        if user_id in self.user_message_count:
            del self.user_message_count[user_id]
        if user_id in self.user_stage:
            del self.user_stage[user_id]
    
    def get_all_levels_summary(self):
        """Dapatkan ringkasan semua level"""
        summary = []
        for level in range(1, 13):
            stage = self.stage_map.get(level, IntimacyStage.STRANGER)
            behavior = self.level_behaviors.get(level, "")
            summary.append(f"Level {level}: {stage.value} - {behavior}")
        return "\n".join(summary)
