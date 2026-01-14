import telebot
from google_sheet_connect import connect
import os


def run_bot():
    # Get Telegram bot token from environment variable
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=['start'])
    def welcome(message):
        # Send welcome message when user starts the bot
        bot.send_message(message.chat.id, "Welcome to Lashesforgirlies management system 🤖")

    @bot.message_handler(commands=['info'])
    def info(message):
        # Send business info and total customer count
        workbook = connect.connecting()
        total_customer = str(connect.calc_total_customer(workbook))
        info_text = (
            "<b>Lashesforgirlies</b> 💖\n\n"
            "<b>Owner:</b> My San Do\n"
            "<b>Based in:</b> Vaughan, Canada\n"
            "<b>Established:</b> September 2024\n\n"
            "<b>Services:</b>\n"
            "• Classic Lashes\n"
            "• Hybrid Lashes\n"
            "• Volume Lashes\n"
            "• Mega Volume\n"
            "• Lash Lift\n\n"
            "<i>Professional lash services with care & quality ✨</i>\n"
            "@lashesforgirlies\n\n"
            f"<b>Total customer: {total_customer}</b>"
        )
        bot.send_message(message.chat.id, info_text, parse_mode="HTML")

    @bot.message_handler(commands=["schedule"])
    def print_coming_schedule(message):
        # Show upcoming schedule with icons
        workbook = connect.connecting()
        upcoming_schedule = connect.find_schedule(workbook)
        bot.send_message(message.chat.id, upcoming_schedule, parse_mode="HTML")

    @bot.message_handler(commands=["history"])
    def ask_history_month(message):
        # Ask user for month to see history
        sent_msg = bot.send_message(
            message.chat.id,
            "Enter a month you would like to see the history of (1, 2, 3, etc.)"
        )
        bot.register_next_step_handler(sent_msg, print_history_schedule)

    def print_history_schedule(message):
        # Print history for given month
        month = message.text
        workbook = connect.connecting()
        history_schedule = connect.history_schedule(workbook, month)
        bot.send_message(message.chat.id, history_schedule, parse_mode="HTML")

    @bot.message_handler(commands=["search_customers"])
    def ask_customer_name_input(message):
        # Ask user to input customer name
        sent_msg = bot.send_message(message.chat.id, "Enter a customer name")
        bot.register_next_step_handler(sent_msg, print_customer_info)

    def print_customer_info(message):
        # Show customer info based on input
        customer = message.text
        workbook = connect.connecting()
        customer_search = connect.search_customer(workbook, customer)
        bot.send_message(message.chat.id, customer_search, parse_mode="HTML")

    @bot.message_handler(commands=["calc_income"])
    def ask_income_month(message):
        # Ask user for month to calculate income
        sent_msg = bot.send_message(
            message.chat.id,
            "Enter a month you would like to calculate the income of (1, 2, etc.). Enter 0 for all time"
        )
        bot.register_next_step_handler(sent_msg, print_income)

    def print_income(message):
        # Print income calculation for the selected month
        month = message.text
        workbook = connect.connecting()
        income = connect.calc_income(workbook, month)
        bot.send_message(message.chat.id, income, parse_mode="HTML")

    # Return the configured bot instance
    return bot