import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import firebase_admin
from firebase_admin import credentials, db
import json

# تهيئة التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# معلومات البوت
TOKEN = "8467235480:AAGYqj1rQRpIG2fJMhahrZIbOFS0TbItido"
ADMIN_ID = 5582333658

# بيانات Firebase من المعلومات التي قدمتها
firebase_credentials = {
  "type": "service_account",
  "project_id": "koko-caffe",
  "private_key_id": "83d08e255028321afcc7d99cfa8fbf815a586287",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC8gFY0lC5yHnw8\nj3NBMz2RZyX320y4SnL/O6Tu1Czd0bTjr8+tMXnxtgCJd/beQw2Jo88MXW3VQRy/\nlapLsi3Jy5UtTwFs1EA5amLmuQrFisFzqqSoIvloasb4zsv35C+QQwGG+HBgiQaD\nR5Kt5hj7bWJjdw8fZtajU1K6oZgCZeEhAvxAksc9H8/m1a3qsgubCSHxVO3asm6K\n5gWAx4mweanZKYp3gaOisjcY0ZkqZDMQtijWKNn6jz4bBzlvq/MtKe3Xg5TVwhOE\nV9ZCIAQbj9OuxyvMmBumMDj8pGLgZ09H+FDmd/yp2NHpJKKOxyboEr43ErErsd6e\nmpN/cLX7AgMBAAECggEAAyGXerZBbmYBGQcB2njEpLF4TaIRJ9P4xKAvOfr3lUG0\nmCvuigAueCxWb4Rv2Lrlab6Lf0mVvB/GREOXi85+r8qqBH+WHdTAe4FkZ1RRtPzF\nbgcWImdwnCt/C1koDqZRWxbnkYTAitjU/4GyyWoBb4RVSLVDhUKD/YVEdHef/3B0\n3li3e+paEwmyov0Z8mqKVaoYaa4+X8IOxd+ewrmXgUk15LtIdKbq/FncL09Or+PP\n0P5uo9LGhjXUkaRaNqRlx4lv6Znhw+zAhVimm7gjdBBEz/zmGeJ7575ivASf9+FO\n9MTisWKDiAj3+i5yJ5DAlL3Gd2gbYDo+1fByHMPvbQKBgQD7QEdrVB6vCZ850Hz7\nx/IsM+spopk6dL4yczr9Jdub8mVoUNK+cgUO2OKf1C3DGJ3eFanJtsU92yQg6ASf\nNwkgrBJVpxtfrKoj0dR78Nhp5z7wwqXHU++XwLH9e4Vo//GegZlMiICexuM8NCkD\n4T7Diov3wzEfYMA6fvNl1ZuNVwKBgQDAEG6tNkN8rAXCuRF5y49wXISY1jrSqB2q\nR2EcqlI3rVlmWRTtIFuPVVPoW1FH2t3D74SFbSlPdypdKv/y7SigkOW8mHYQFcXp\n3Mz3kOpFuCb1CUG9LPxHpKf+kklsv7mSQPDn++zWixQVuv9WP1WGzt8YJKIlQdYy\ncyrv5v7R/QKBgHSr/74+XNVJcZAmWbONwM53+Y7m+6KijaPd0Jm3V8iOAjsztPlM\n9z5SxsIThIChUMXNZ3/NCMDVn2xMccEBjJKIdScjJ1oBUyy5BqPbTpO3F4ozyUnL\nl2nvyHd+QZBlsey6H9bjWF7i2qidTCKKGVwyXRbbpFb+1aUUSLCURdyXAoGAdDm9\ncA41Wr2Sotpxi922SI2EJCUH5bCcew3E457iMBUz02627iQ1pBBDvYl9L1lv+AD6\nle+QHymCtmyuBGilvDzS+YTddTBn2vSmCG5mhphA4umeIYeWhxhKHRCTZD7FYo7v\n+cKG+PGizt+hYqTi8bhAYxDQGnGz2EW/RvvnWlUCgYB1chpFNWz32BU6pcTRKwpo\ndR6C1B0PnrnzMh/PRxihM4b+fXvBfCG6t82i5+EvM0J8Pib/LvApSx1Bj2wcT5f1\nzdTZFdNgTAuxeUHfWZ5yXiLEscZxFoE3AahFNtc86oaX24Z2eF2XUMq6iWAg0YLy\nS19HH/1e3glOTRmZuvJ33w==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@koko-caffe.iam.gserviceaccount.com",
  "client_id": "110585030663354370686",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40koko-caffe.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# حفظ بيانات الاعتماد في ملف مؤقت
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://koko-caffe-default-rtdb.europe-west1.firebasedatabase.app'
})

# أقسام القائمة
SECTIONS = {
    'MAIN_DISHES': 'الوجبات الرئيسية',
    'ADD_ONS': 'الإضافات',
    'COFFEE_HOT_DRINKS': 'القهوة والمشروبات الساخنة',
    'SOFT_DRINKS': 'المشروبات الغازية',
    'COLD_DRINKS': 'المشروبات الباردة',
    'DESSERTS': 'الحلويات',
    'CLASSIC_SHISHA': 'الشيشة التقليدية',
    'SHISHA_ADD_ONS': 'إضافات الشيشة',
    'PREMIUM_SHISHA': 'الشيشة المميزة'
}

# حالة المستخدمين
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("عفوا، هذا البوت مخصص للإدارة فقط.")
        return
    
    keyboard = [
        [InlineKeyboardButton("➕ إضافة صنف", callback_data="add_item")],
        [InlineKeyboardButton("✏️ تعديل صنف", callback_data="edit_item")],
        [InlineKeyboardButton("🗑️ حذف صنف", callback_data="delete_item")],
        [InlineKeyboardButton("💲 تعديل السعر", callback_data="edit_price")],
        [InlineKeyboardButton("📂 اختيار القسم", callback_data="select_section")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("مرحبا بك في لوحة تحكم كافيه نوفا. اختر الإجراء المطلوب:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id != ADMIN_ID:
        await query.edit_message_text("عفوا، هذا البوت مخصص للإدارة فقط.")
        return
    
    data = query.data
    
    if data == "add_item":
        # عرض قائمة الأقسام للاختيار
        keyboard = []
        for section_id, section_name in SECTIONS.items():
            keyboard.append([InlineKeyboardButton(section_name, callback_data=f"add_to_{section_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("اختر القسم لإضافة صنف جديد:", reply_markup=reply_markup)
    
    elif data == "edit_item":
        # عرض قائمة الأقسام للاختيار
        keyboard = []
        for section_id, section_name in SECTIONS.items():
            keyboard.append([InlineKeyboardButton(section_name, callback_data=f"edit_in_{section_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("اختر القسم لتعديل صنف:", reply_markup=reply_markup)
    
    elif data == "delete_item":
        # عرض قائمة الأقسام للاختيار
        keyboard = []
        for section_id, section_name in SECTIONS.items():
            keyboard.append([InlineKeyboardButton(section_name, callback_data=f"delete_from_{section_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("اختر القسم لحذف صنف:", reply_markup=reply_markup)
    
    elif data == "edit_price":
        # عرض قائمة الأقسام للاختيار
        keyboard = []
        for section_id, section_name in SECTIONS.items():
            keyboard.append([InlineKeyboardButton(section_name, callback_data=f"price_in_{section_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("اختر القسم لتعديل سعر صنف:", reply_markup=reply_markup)
    
    elif data == "select_section":
        # عرض قائمة الأقسام للاختيار
        keyboard = []
        for section_id, section_name in SECTIONS.items():
            keyboard.append([InlineKeyboardButton(section_name, callback_data=f"view_{section_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("اختر القسم لعرض محتوياته:", reply_markup=reply_markup)
    
    elif data == "back_to_main":
        # العودة إلى القائمة الرئيسية
        keyboard = [
            [InlineKeyboardButton("➕ إضافة صنف", callback_data="add_item")],
            [InlineKeyboardButton("✏️ تعديل صنف", callback_data="edit_item")],
            [InlineKeyboardButton("🗑️ حذف صنف", callback_data="delete_item")],
            [InlineKeyboardButton("💲 تعديل السعر", callback_data="edit_price")],
            [InlineKeyboardButton("📂 اختيار القسم", callback_data="select_section")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("مرحبا بك في لوحة تحكم كافيه نوفا. اختر الإجراء المطلوب:", reply_markup=reply_markup)
    
    elif data.startswith("add_to_"):
        section_id = data[7:]
        user_states[user_id] = {"action": "add_item", "section": section_id}
        
        await query.edit_message_text(f"أرسل اسم الصنف بالعربية والإنجليزية والسعر بالصيغة:\nالاسم العربي|الاسم الانجليزي|السعر\n\nمثال:\nإسبريسو|Espresso|25")
    
    elif data.startswith("edit_in_"):
        section_id = data[8:]
        # جلب العناصر من القسم وعرضها للاختيار
        ref = db.reference(section_id)
        items = ref.get()
        
        if not items:
            await query.edit_message_text("هذا القسم فارغ حاليا.")
            return
        
        keyboard = []
        for item_id, item_data in items.items():
            keyboard.append([InlineKeyboardButton(f"{item_data.get('nameAr', 'بدون اسم')} - {item_data.get('price', '0')} ج.م", callback_data=f"edit_item_{section_id}_{item_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("اختر الصنف لتعديله:", reply_markup=reply_markup)
    
    elif data.startswith("edit_item_"):
        # استخراج معلومات الصنف
        parts = data.split('_')
        section_id = parts[2]
        item_id = parts[3]
        
        user_states[user_id] = {"action": "edit_item", "section": section_id, "item_id": item_id}
        
        await query.edit_message_text("أرسل البيانات الجديدة بالصيغة:\nالاسم العربي|الاسم الانجليزي|السعر\n\nمثال:\nإسبريسو|Espresso|30")
    
    elif data.startswith("delete_from_"):
        section_id = data[12:]
        # جلب العناصر من القسم وعرضها للاختيار
        ref = db.reference(section_id)
        items = ref.get()
        
        if not items:
            await query.edit_message_text("هذا القسم فارغ حاليا.")
            return
        
        keyboard = []
        for item_id, item_data in items.items():
            keyboard.append([InlineKeyboardButton(f"{item_data.get('nameAr', 'بدون اسم')} - {item_data.get('price', '0')} ج.م", callback_data=f"delete_item_{section_id}_{item_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("اختر الصنف لحذفه:", reply_markup=reply_markup)
    
    elif data.startswith("delete_item_"):
        # استخراج معلومات الصنف
        parts = data.split('_')
        section_id = parts[2]
        item_id = parts[3]
        
        # حذف الصنف من Firebase
        ref = db.reference(f"{section_id}/{item_id}")
        ref.delete()
        
        await query.edit_message_text("تم حذف الصنف بنجاح.")
    
    elif data.startswith("price_in_"):
        section_id = data[9:]
        # جلب العناصر من القسم وعرضها للاختيار
        ref = db.reference(section_id)
        items = ref.get()
        
        if not items:
            await query.edit_message_text("هذا القسم فارغ حاليا.")
            return
        
        keyboard = []
        for item_id, item_data in items.items():
            keyboard.append([InlineKeyboardButton(f"{item_data.get('nameAr', 'بدون اسم')} - {item_data.get('price', '0')} ج.م", callback_data=f"price_item_{section_id}_{item_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("اختر الصنف لتعديل سعره:", reply_markup=reply_markup)
    
    elif data.startswith("price_item_"):
        # استخراج معلومات الصنف
        parts = data.split('_')
        section_id = parts[2]
        item_id = parts[3]
        
        user_states[user_id] = {"action": "edit_price", "section": section_id, "item_id": item_id}
        
        await query.edit_message_text("أرسل السعر الجديد:")
    
    elif data.startswith("view_"):
        section_id = data[5:]
        # جلب العناصر من القسم وعرضها
        ref = db.reference(section_id)
        items = ref.get()
        
        if not items:
            await query.edit_message_text("هذا القسم فارغ حاليا.")
            return
        
        message = f"محتويات قسم {SECTIONS.get(section_id, section_id)}:\n\n"
        for item_id, item_data in items.items():
            message += f"• {item_data.get('nameAr', 'بدون اسم')} - {item_data.get('nameEn', 'No name')} - {item_data.get('price', '0')} ج.م\n"
        
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("عفوا، هذا البوت مخصص للإدارة فقط.")
        return
    
    if user_id not in user_states:
        await update.message.reply_text("يرجى اختيار إجراء من القائمة أولاً.")
        return
    
    state = user_states[user_id]
    action = state.get("action")
    text = update.message.text
    
    if action == "add_item":
        # معالجة إضافة صنف جديد
        section = state.get("section")
        parts = text.split('|')
        
        if len(parts) != 3:
            await update.message.reply_text("الصيغة غير صحيحة. يرجى استخدام الصيغة: الاسم العربي|الاسم الانجليزي|السعر")
            return
        
        name_ar, name_en, price = parts
        
        # إضافة إلى Firebase
        ref = db.reference(section)
        new_item_ref = ref.push()
        new_item_ref.set({
            'nameAr': name_ar.strip(),
            'nameEn': name_en.strip(),
            'price': price.strip()
        })
        
        await update.message.reply_text("تم إضافة الصنف بنجاح!")
        del user_states[user_id]
    
    elif action == "edit_item":
        # معالجة تعديل صنف
        section = state.get("section")
        item_id = state.get("item_id")
        parts = text.split('|')
        
        if len(parts) != 3:
            await update.message.reply_text("الصيغة غير صحيحة. يرجى استخدام الصيغة: الاسم العربي|الاسم الانجليزي|السعر")
            return
        
        name_ar, name_en, price = parts
        
        # التعديل في Firebase
        ref = db.reference(f"{section}/{item_id}")
        ref.update({
            'nameAr': name_ar.strip(),
            'nameEn': name_en.strip(),
            'price': price.strip()
        })
        
        await update.message.reply_text("تم تعديل الصنف بنجاح!")
        del user_states[user_id]
    
    elif action == "edit_price":
        # معالجة تعديل السعر فقط
        section = state.get("section")
        item_id = state.get("item_id")
        
        # التعديل في Firebase
        ref = db.reference(f"{section}/{item_id}")
        ref.update({
            'price': text.strip()
        })
        
        await update.message.reply_text("تم تعديل السعر بنجاح!")
        del user_states[user_id]

def main():
    # إنشاء التطبيق وإضافة المعالجات
    application = Application.builder().token(TOKEN).build()
    
    # معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    
    # معالجات الأزرار
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # معالجات الرسائل
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
