# bot/echo_bot.py

from botbuilder.core import ActivityHandler, TurnContext
from db.sql_conector import get_admin_by_id

class EchoBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text.strip()
        
        if user_input.isdigit():
            data = get_admin_by_id(int(user_input))
            if data:
                response = (
                    f"🧾 Data for ID {user_input}:\n"
                    f"- Username: {data['username']}\n"
                    f"- Password: {data['password']}\n"
                    f"- Current Status: {data['current_status']}\n"
                    f"- New Status: {data['new_status']}"
                )
            else:
                response = f"No data found for ID {user_input}."
        else:
            response = "❗ Please enter a valid numeric ID."

        await turn_context.send_activity(response)
