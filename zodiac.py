import gradio as gr
from datetime import datetime
from lunar_python import Lunar, Solar
import csv
import os

class ZodiacInfo:
    def __init__(self):
        self.zodiac_data = {}
        self.load_zodiac_data()

    def load_zodiac_data(self):
        """Load zodiac information from CSV file"""
        with open('data/zodiac_info.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.zodiac_data[row['German']] = row

    def get_zodiac_info(self, date_str):
        try:
            birth_date = datetime.strptime(date_str, "%d.%m.%Y")
            solar_date = Solar.fromYmd(birth_date.year, birth_date.month, birth_date.day)
            lunar_date = solar_date.getLunar()
            lunar_year = lunar_date.getYear()

            zodiac_animals_en = [
                "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
                "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
            ]
            zodiac_german = [
                "Ratte", "Büffel", "Tiger", "Hase", "Drache", "Schlange",
                "Pferd", "Ziege", "Affe", "Hahn", "Hund", "Schwein"
            ]
            
            zodiac_emojis = {
                "Rat": "🐀",
                "Ox": "🐂",
                "Tiger": "🐅",
                "Rabbit": "🐇",
                "Dragon": "🐲",
                "Snake": "🐍",
                "Horse": "🐎",
                "Goat": "🐐",
                "Monkey": "🐒",
                "Rooster": "🐓",
                "Dog": "🐕",
                "Pig": "🐷"
            }
            
            zodiac_index = (lunar_year - 1900) % 12
            zodiac = zodiac_german[zodiac_index]
            zodiac_en = zodiac_animals_en[zodiac_index]
            info = self.zodiac_data[zodiac]
            
            return f"""
            <div style='text-align:center; padding: 20px; max-width: 800px; margin: 0 auto;'>
                <div style='background-color: #4a90e2; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                    <h1 style='color: white; margin: 0;'>Your Chinese Zodiac Sign: {zodiac_emojis[zodiac_en]} {zodiac_en}</h1>
                    <h2 style='color: white; margin: 10px 0;'>Birth Date: {date_str}</h2>
                    <h2 style='color: white; margin: 0;'>Lunar Year: {lunar_year}</h2>
                </div>
                
                <div style='text-align:left; background-color: #f5f5f5; padding: 20px; border-radius: 10px; color: black;'>
                    <h3 style='color: #333;'>📖 Legend:</h3>
                    <p style='color: black;'>{info['Legend']}</p>
                    
                    <h3 style='color: #333;'>🎭 Personality:</h3>
                    <p style='color: black;'>{info['Personality']}</p>
                    
                    <h3 style='color: #333;'>❤️ Best Match:</h3>
                    <p style='color: black;'>{info['Best Match']}</p>
                    
                    <h3 style='color: #333;'>💼 Career:</h3>
                    <p style='color: black;'>{info['Career']}</p>
                    
                    <h3 style='color: #333;'>🏥 Health:</h3>
                    <p style='color: black;'>{info['Health']}</p>
                    
                    <h3 style='color: #333;'>🎨 Lucky Colors:</h3>
                    <p style='color: black;'>{info['Lucky Colors']}</p>
                    
                    <h3 style='color: #333;'>🔢 Lucky Numbers:</h3>
                    <p style='color: black;'>{info['Lucky Numbers']}</p>
                    
                    <h3 style='color: #333;'>📅 Lucky Months:</h3>
                    <p style='color: black;'>{info['Lucky Months']}</p>
                </div>
            </div>
            """
        except ValueError:
            return "<h1 style='text-align:center;color:red;'>Invalid date format. Please use DD.MM.YYYY format</h1>"
        except Exception as e:
            return f"<h1 style='text-align:center;color:red;'>An error occurred: {str(e)}</h1>"

# Initialize zodiac information
zodiac_info = ZodiacInfo()

# Create Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            <div style='background-color: #f0f0f0; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h1 style='color: #333; margin: 0;'>Welcome to Chinese Zodiac Finder!</h1>
                <h2 style='color: #333; margin: 10px 0;'>2024 is the Year of the Dragon. Discover Your Chinese Zodiac Sign!</h2>
                <p style='color: #333; margin: 0;'>Please enter your birth date in Gregorian calendar (Format: DD.MM.YYYY):</p>
            </div>
            """)
            date_input = gr.Textbox(
                label="Enter your birth date (Format: DD.MM.YYYY)", 
                placeholder="e.g., 17.06.1994"
            )
            submit_button = gr.Button("Find My Zodiac Sign")
    
    result_output = gr.HTML()

    def get_styled_zodiac_info(date_str):
        try:
            result = zodiac_info.get_zodiac_info(date_str)
            if result.startswith("<h1 style='text-align:center;color:red;'>"):
                return result
            
            birth_date = datetime.strptime(date_str, "%d.%m.%Y")
            solar_date = Solar.fromYmd(birth_date.year, birth_date.month, birth_date.day)
            lunar_date = solar_date.getLunar()
            lunar_year = lunar_date.getYear()

            zodiac_animals_en = [
                "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
                "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
            ]
            zodiac_german = [
                "Ratte", "Büffel", "Tiger", "Hase", "Drache", "Schlange",
                "Pferd", "Ziege", "Affe", "Hahn", "Hund", "Schwein"
            ]
            
            zodiac_emojis = {
                "Rat": "🐀",
                "Ox": "🐂",
                "Tiger": "🐅",
                "Rabbit": "🐇",
                "Dragon": "🐲",
                "Snake": "🐍",
                "Horse": "🐎",
                "Goat": "🐐",
                "Monkey": "🐒",
                "Rooster": "🐓",
                "Dog": "🐕",
                "Pig": "🐷"
            }
            
            zodiac_index = (lunar_year - 1900) % 12
            zodiac = zodiac_german[zodiac_index]
            zodiac_en = zodiac_animals_en[zodiac_index]
            info = zodiac_info.zodiac_data[zodiac]
            
            return f"""
            <div style='text-align:center; padding: 20px; max-width: 800px; margin: 0 auto;'>
                <div style='background-color: #4a90e2; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                    <h1 style='color: white; margin: 0;'>Your Chinese Zodiac Sign: {zodiac_emojis[zodiac_en]} {zodiac_en}</h1>
                    <h2 style='color: white; margin: 10px 0;'>Birth Date: {date_str}</h2>
                    <h2 style='color: white; margin: 0;'>Lunar Year: {lunar_year}</h2>
                </div>
                
                <div style='text-align:left; background-color: #f5f5f5; padding: 20px; border-radius: 10px; color: black;'>
                    <h3 style='color: #333;'>📖 Legend:</h3>
                    <p style='color: black;'>{info['Legend']}</p>
                    
                    <h3 style='color: #333;'>🎭 Personality:</h3>
                    <p style='color: black;'>{info['Personality']}</p>
                    
                    <h3 style='color: #333;'>❤️ Best Match:</h3>
                    <p style='color: black;'>{info['Best Match']}</p>
                    
                    <h3 style='color: #333;'>💼 Career:</h3>
                    <p style='color: black;'>{info['Career']}</p>
                    
                    <h3 style='color: #333;'>🏥 Health:</h3>
                    <p style='color: black;'>{info['Health']}</p>
                    
                    <h3 style='color: #333;'>🎨 Lucky Colors:</h3>
                    <p style='color: black;'>{info['Lucky Colors']}</p>
                    
                    <h3 style='color: #333;'>🔢 Lucky Numbers:</h3>
                    <p style='color: black;'>{info['Lucky Numbers']}</p>
                    
                    <h3 style='color: #333;'>📅 Lucky Months:</h3>
                    <p style='color: black;'>{info['Lucky Months']}</p>
                </div>
            </div>
            """
        except ValueError:
            return "<h1 style='text-align:center;color:red;'>Invalid date format. Please use DD.MM.YYYY format</h1>"
        except Exception as e:
            return f"<h1 style='text-align:center;color:red;'>An error occurred: {str(e)}</h1>"

    date_input.submit(get_styled_zodiac_info, inputs=date_input, outputs=result_output)
    submit_button.click(get_styled_zodiac_info, inputs=date_input, outputs=result_output)

if __name__ == "__main__":
    demo.launch(share=True)
