import subprocess
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging to capture errors
logging.basicConfig(level=logging.DEBUG)

# Replace with your bot token
TELEGRAM_BOT_TOKEN = "7751143833:AAF3PNPRjzC2D4mFtnea_-khMhfIkjhSamU"

# Command to generate password
async def generate_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Run the Ansible playbook to generate a password
        result = subprocess.run(["ansible-playbook", "generate_password.yml"], capture_output=True, text=True)

        # Check if the playbook executed successfully
        if result.returncode == 0:
            # Find the generated password in the output
            for line in result.stdout.splitlines():
                if "Generated password:" in line:
                    password = line.split(": ")[1]
                    formatted_password = f"<u><span style='color:blue;'>{password}</span></u>"

                    # Send the formatted password to the Telegram group
                    await update.message.reply_text(
                        f"Generated password: {formatted_password}",
                        parse_mode=ParseMode.HTML
                    )
                    return
            await update.message.reply_text("Password generated, but couldn't parse output.")
        else:
            await update.message.reply_text("Failed to generate password. Check Ansible playbook for errors.")
    
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

# Main function to set up the bot
def main():
    try:
        # Create the application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Add command handler for /generate_password
        application.add_handler(CommandHandler("generate_password", generate_password))

        # Start polling for messages
        application.run_polling(timeout=10, allowed_updates=["message", "edited_message", "callback_query", "inline_query"])

    except Exception as e:
        logging.error(f"Failed to start bot: {e}")

if __name__ == "__main__":
    main()
