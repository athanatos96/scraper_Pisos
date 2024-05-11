import time
from tqdm import tqdm

from playsound import playsound # pip install playsound


def play_noise():
        file_path = "./data/sound/Alert-beep-sound-effect.mp3"  # Update this with your file path
        try:
            # Attempt to play the specified audio file
            playsound(file_path)
        except Exception as e:
            # If an error occurs (e.g., file not found or unsupported format), print the error
            print(f"Error playing noise: {e}")

def wait_for_captcha(sb, captcha_id, max_attempts=10):
    # wait for iframe
    time.sleep(2)
    # Select iframe
    css_selector = f'iframe[src*="captcha"]'
    tqdm.write(css_selector)
    
    
    if not sb.is_element_visible(css_selector):
        tqdm.write(' - NO CAPTCHA - ')
        return True
    
    
    
    tqdm.write(' - CAPTCHA - ')
    try:
        # Switch to the frame
        sb.switch_to_frame(css_selector)
        
        css_selector = f"#{captcha_id}"  
        sb.wait_for_element(css_selector)
        
        attempt = 1
        while attempt <= max_attempts:
            if sb.is_element_visible(css_selector):
                # There is a captcha
                tqdm.write(" - WARNING - Captcha Present, Please fix")
                
                # Emit a NOISE sound to alert a human
                play_noise()
                
                # Wait for 30 seconds before checking again
                #time.sleep(30)
                for _ in tqdm(range(int(30 * 10)), desc=f"Sleeping HANDLE CAPTCHA", unit="milliseconds"):
                    time.sleep(0.1)
                tqdm.write("After sleep")
                attempt += 1
            else:
                tqdm.write(" Captcha Handled")
                return True    
    except Exception as e:
        print(f"ERROR {e}")
        sb.switch_to_default_content()
        raise e
    
    raise Exception(f"Reached maximum attempts ({max_attempts}) to handle CAPTCHA")     
    

