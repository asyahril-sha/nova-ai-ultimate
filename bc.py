# ===================== BAB 12: MAIN FUNCTION & ENTRY POINT =====================
# Bagian 12.1: Setup & Handlers
# Bagian 12.2: Error Handler
# Bagian 12.3: Webhook Setup
# Bagian 12.4: Startup & Graceful Shutdown

# ===== WEBHOOK SETUP UNTUK RAILWAY =====
from flask import Flask, request, jsonify
import threading
import requests
import logging

# Matikan log Flask yang berlebihan
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Global variables untuk Flask
flask_app = Flask(__name__)
bot_instance = None

# ===== ENDPOINTS FLASK =====

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates from Telegram"""
    global bot_instance
    if bot_instance and hasattr(bot_instance, 'application'):
        try:
            update = Update.de_json(request.get_json(force=True), bot_instance.application.bot)
            bot_instance.application.process_update(update)
            return 'OK', 200
        except Exception as e:
            print(f"❌ Error processing webhook: {e}")
            return 'Error', 500
    return 'Bot not ready', 503

@flask_app.route('/')
@flask_app.route('/health')
def home():
    """Healthcheck endpoint untuk Railway"""
    return jsonify({
        'status': 'healthy',
        'message': 'NOVA GIRL Bot is running!',
        'timestamp': datetime.now().isoformat()
    }), 200

@flask_app.route('/null')
def null_endpoint():
    """Handle /null requests from Railway"""
    return jsonify({
        'status': 'healthy',
        'message': 'NOVA GIRL Bot is running!'
    }), 200

@flask_app.route('/favicon.ico')
def favicon():
    """Handle favicon requests"""
    return '', 204

def run_flask():
    """Run Flask app for webhook"""
    port = int(os.getenv('PORT', 8080))
    flask_app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

def get_railway_url():
    """Dapatkan URL Railway dari berbagai sumber"""
    railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')
    if railway_url:
        return railway_url
    
    railway_url = os.getenv('RAILWAY_STATIC_URL', '')
    if railway_url:
        return railway_url
    
    railway_url = os.getenv('RAILWAY_SERVICE_NAME', '')
    if railway_url:
        return f"{railway_url}.railway.app"
    
    return None

def setup_webhook():
    """Set webhook Telegram"""
    global bot_instance
    
    railway_url = get_railway_url()
    
    if railway_url and bot_instance:
        webhook_url = f"https://{railway_url}/webhook"
        try:
            token = Config.TELEGRAM_TOKEN
            response = requests.get(
                f"https://api.telegram.org/bot{token}/setWebhook",
                params={"url": webhook_url}
            )
            if response.status_code == 200 and response.json().get('ok'):
                print(f"✅ Webhook set to: {webhook_url}")
                return True
            else:
                print(f"❌ Failed to set webhook: {response.text}")
        except Exception as e:
            print(f"❌ Error setting webhook: {e}")
    else:
        print("⚠️ Railway URL not found, using polling mode")
    
    return False

async def start_polling():
    """Start polling mode as fallback"""
    global bot_instance
    if bot_instance and hasattr(bot_instance, 'application'):
        print("🚀 Starting polling mode...")
        await bot_instance.application.run_polling()

# ===== MAIN ASYNC FUNCTION =====

async def main():
    """
    Main async function to run the bot
    Setup all handlers and start webhook/polling
    """
    # Print startup banner
    print("\n" + "="*70)
    print("    GADIS ULTIMATE V60.0 - THE PERFECT HUMAN")
    print("    Premium Edition dengan Arsitektur Modular")
    print("="*70)
    print("\n🚀 Initializing bot...")
    
    # Initialize bot instance
    bot = GadisUltimateV60()
    global bot_instance
    bot_instance = bot
    
    # ===== SETUP REQUEST DENGAN TIMEOUT BESAR =====
    request = HTTPXRequest(
        connection_pool_size=20,
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60,
    )
    
    # Build application dengan custom request
    app = Application.builder().token(Config.TELEGRAM_TOKEN).request(request).build()
    bot.application = app
    
    # ===== CONVERSATION HANDLERS (tanpa per_message) =====
    
    start_conv = ConversationHandler(
        entry_points=[CommandHandler('start', bot.start_command)],
        states={
            Constants.SELECTING_ROLE: [
                CallbackQueryHandler(bot.agree_18_callback, pattern='^agree_18$'),
                CallbackQueryHandler(bot.start_pause_callback, pattern='^(unpause|new)$'),
                CallbackQueryHandler(bot.role_ipar_callback, pattern='^role_ipar$'),
                CallbackQueryHandler(bot.role_teman_kantor_callback, pattern='^role_teman_kantor$'),
                CallbackQueryHandler(bot.role_janda_callback, pattern='^role_janda$'),
                CallbackQueryHandler(bot.role_pelakor_callback, pattern='^role_pelakor$'),
                CallbackQueryHandler(bot.role_istri_orang_callback, pattern='^role_istri_orang$'),
                CallbackQueryHandler(bot.role_pdkt_callback, pattern='^role_pdkt$'),
            ],
        },
        fallbacks=[CommandHandler('cancel', bot.cancel_command)],
        name="start_conversation",
        persistent=False
    )
    
    end_conv = ConversationHandler(
        entry_points=[CommandHandler('end', bot.end_command)],
        states={
            Constants.CONFIRM_END: [CallbackQueryHandler(bot.end_callback, pattern='^end_')],
        },
        fallbacks=[CommandHandler('cancel', bot.cancel_command)],
        name="end_conversation",
        persistent=False
    )
    
    close_conv = ConversationHandler(
        entry_points=[CommandHandler('close', bot.close_command)],
        states={
            Constants.CONFIRM_CLOSE: [CallbackQueryHandler(bot.close_callback, pattern='^close_')],
        },
        fallbacks=[CommandHandler('cancel', bot.cancel_command)],
        name="close_conversation",
        persistent=False
    )
    
    print("  • Conversation handlers created")
    
    # ===== ADD ALL HANDLERS =====
    app.add_handler(start_conv)
    app.add_handler(end_conv)
    app.add_handler(close_conv)
    
    app.add_handler(CommandHandler("status", bot.status_command))
    app.add_handler(CommandHandler("dominant", bot.dominant_command))
    app.add_handler(CommandHandler("pause", bot.pause_command))
    app.add_handler(CommandHandler("unpause", bot.unpause_command))
    app.add_handler(CommandHandler("help", bot.help_command))
    
    app.add_handler(CommandHandler("admin", bot.admin_command))
    app.add_handler(CommandHandler("stats", bot.stats_command))
    app.add_handler(CommandHandler("db_stats", bot.db_stats_command))
    app.add_handler(CommandHandler("reload", bot.reload_command))
    app.add_handler(CommandHandler("list_users", bot.list_users_command))
    app.add_handler(CommandHandler("get_user", bot.get_user_command))
    app.add_handler(CommandHandler("force_reset", bot.force_reset_command))
    app.add_handler(CommandHandler("backup_db", bot.backup_db_command))
    app.add_handler(CommandHandler("vacuum", bot.vacuum_command))
    app.add_handler(CommandHandler("memory_stats", bot.memory_stats_command))
    app.add_handler(CommandHandler("reset", bot.force_reset_command))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    print("  • All handlers registered")
    
    # ===== ERROR HANDLER =====
    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Exception while handling an update: {context.error}", exc_info=True)
        
        if update and update.effective_message:
            error_msg = (
                "😔 *maaf* ada error kecil.\n"
                "Jangan khawatir, bot masih berjalan normal.\n\n"
                "Coba lagi ya, atau ketik /help untuk bantuan."
            )
            try:
                await update.effective_message.reply_text(error_msg, parse_mode='Markdown')
            except:
                pass
        
        if bot.admin_id != 0:
            try:
                error_text = f"⚠️ *Error Report*\n\n`{str(context.error)[:500]}`"
                await context.bot.send_message(
                    chat_id=bot.admin_id,
                    text=error_text,
                    parse_mode='Markdown'
                )
            except:
                pass
    
    app.add_error_handler(error_handler)
    print("  • Error handler configured")
    
    # ===== START BACKGROUND TASKS =====
    asyncio.create_task(bot.start_background_tasks(app))
    print("  • Background tasks started")
    
    # ===== START FLASK SERVER =====
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    print(f"✅ Flask server started on port {os.getenv('PORT', '8080')}")
    
    # ===== SETUP WEBHOOK =====
    if setup_webhook():
        print("🚀 Bot is running with WEBHOOK...")
    else:
        print("🚀 Bot is running with POLLING (fallback)...")
        asyncio.create_task(start_polling())
    
    # ===== STARTUP COMPLETE =====
    print("\n" + "="*70)
    print("✅ **BOT READY!**")
    print("="*70)
    print("\n📊 **STATISTICS:**")
    print(f"• Database: {Config.DB_PATH}")
    print(f"• Admin ID: {Config.ADMIN_ID if Config.ADMIN_ID != 0 else 'Tidak diset'}")
    print(f"• Target level: {Config.TARGET_LEVEL} in {Config.LEVEL_UP_TIME} menit")
    print(f"• Rate limit: {Config.MAX_MESSAGES_PER_MINUTE} pesan/menit")
    print(f"• Server: Flask (threaded)")
    print(f"• Port: {os.getenv('PORT', '8080')}")
    
    print("\n📝 **USER COMMANDS:**")
    print("• /start     - Mulai hubungan baru")
    print("• /status    - Lihat status lengkap")
    print("• /dominant  - Set mode dominan")
    print("• /pause     - Jeda sesi")
    print("• /unpause   - Lanjutkan sesi")
    print("• /close     - Tutup sesi (simpan memori)")
    print("• /end       - Akhiri hubungan & hapus data")
    print("• /help      - Tampilkan bantuan")
    
    if Config.ADMIN_ID != 0:
        print("\n🔐 **ADMIN COMMANDS:**")
        print("• /admin     - Menu admin")
        print("• /stats     - Statistik bot")
        print("• /db_stats  - Statistik database")
        print("• /reload    - Reload konfigurasi")
        print("• /list_users - Daftar user")
        print("• /get_user  - Detail user")
        print("• /force_reset - Reset user")
        print("• /backup_db - Backup database")
        print("• /vacuum    - Optimasi database")
        print("• /memory_stats - Statistik memori")
    
    print("\n" + "="*70 + "\n")
    
    # Keep the main thread alive
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("👋 Bot stopped by user (Ctrl+C)")
        print("="*70)
        
        print("\n📝 Saving sessions to database...")
        for uid in list(bot.sessions.keys()):
            bot.save_session_to_db(uid)
        
        bot.db.close_all()
        print("✅ Cleanup completed")
        print("\nSelamat tinggal! Sampai jumpa lagi... 💕")
        print("="*70 + "\n")
        
    except Exception as e:
        print("\n\n" + "="*70)
        print("❌ **FATAL ERROR**")
        print("="*70)
        print(f"\nError: {e}")
        print("\nBot crashed. Check gadis.log for details.")
        print("="*70 + "\n")
        
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


# ===================== ENTRY POINT =====================

if __name__ == "__main__":
    """
    Entry point for the bot application
    """
    asyncio.run(main())


# ===================== END OF FILE =====================
# GADIS ULTIMATE V60.0 - THE PERFECT HUMAN
# Premium Edition dengan Arsitektur Modular
# ========================================================

print("✅ BAB 12 Selesai: Main Function & Entry Point")
print("="*70)
print("🎉🎉🎉 SELURUH BAB TELAH SELESAI! 🎉🎉🎉")
print("="*70)
