from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8842564826:AAHr81N5vwGQjXYTtMk4RE3_bLFbTP6KinU" # Tera Token
ADMIN_ID = 7732391940 # Teri ID

BOT_ACTIVE = True

DOCTORS = {
    "gupta": {
        "name": "Dr. R K Gupta",
        "dept": "Medicine",
        "time": "9 AM - 2 PM",
        "room": "Room No. 12",
        "desc": "Senior Physician - Diabetes, BP Specialist"
    },
    "gopal": {
        "name": "Dr. Gopal",
        "dept": "Surgery",
        "time": "10 AM - 1 PM",
        "room": "Room No. 15",
        "desc": "General Surgeon"
    },
    "tahir": {
        "name": "Dr. Tahir",
        "dept": "Orthopedics",
        "time": "11 AM - 3 PM",
        "room": "Room No. 8",
        "desc": "Bone & Joint Specialist"
    },
    "faisal": {
        "name": "Dr. Faisal",
        "dept": "Eye",
        "time": "9 AM - 12 PM",
        "room": "Room No. 20",
        "desc": "Eye Specialist"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not BOT_ACTIVE and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🔧 Bot abhi maintenance pe hai.")
        return
    keyboard = [
        [InlineKeyboardButton("👨‍⚕️ Dr. R K Gupta", callback_data="gupta")],
        [InlineKeyboardButton("👨‍⚕️ Dr. Gopal", callback_data="gopal")],
        [InlineKeyboardButton("👨‍⚕️ Dr. Tahir", callback_data="tahir")],
        [InlineKeyboardButton("👨‍⚕️ Dr. Faisal", callback_data="faisal")],
    ]
    await update.message.reply_text("🙏 Welcome to SRSMH DOCTORS\nSelect kare:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    doc = DOCTORS[query.data]
    text = f"👨‍⚕️ *{doc['name']}*\n\n🏥 {doc['dept']}\n🕒 {doc['time']}\n📍 {doc['room']}\n\n📝 {doc['desc']}"
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

async def toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    if update.effective_user.id != ADMIN_ID: return
    if "/off" in update.message.text:
        BOT_ACTIVE = False
        await update.message.reply_text("🔴 Bot OFF")
    else:
        BOT_ACTIVE = True
        await update.message.reply_text("🟢 Bot ON")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("on", toggle))
app.add_handler(CommandHandler("off", toggle))
app.add_handler(CallbackQueryHandler(back, pattern="back"))
app.add_handler(CallbackQueryHandler(show_detail))

app.run_polling()
