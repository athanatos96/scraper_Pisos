

#######################################################################################
#
#
# https://seleniumbase.io/help_docs/uc_mode/
#
#
#######################################################################################


# Here's an example with the Driver manager:
'''
from seleniumbase import Driver
driver = Driver(uc=True)
try:
    url = "https://gitlab.com/users/sign_in"
    driver.uc_open_with_reconnect(url, 3)
    driver.sleep(5)
finally:
    driver.quit()
'''

# Here's an example with the SB manager (which has more methods and functionality than the Driver format):
'''
from seleniumbase import SB
with SB(uc=True) as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.driver.uc_open_with_reconnect(url, 3)
    sb.sleep(5)
'''

# Here's a longer example, which includes a retry if the CAPTCHA isn't bypassed on the first attempt:
'''
from seleniumbase import SB
with SB(uc=True, test=True) as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.driver.uc_open_with_reconnect(url, 3)
    sb.sleep(5)
    if not sb.is_text_visible("Username", '[for="user_login"]'):
        sb.driver.uc_open_with_reconnect(url, 4)
    sb.sleep(5)
    sb.assert_text("Username", '[for="user_login"]', timeout=3)
    sb.sleep(5)
    sb.highlight('label[for="user_login"]', loops=3)
    sb.sleep(5)
    sb.post_message("SeleniumBase wasn't detected", duration=4)
    sb.sleep(5)
'''

# Here's an example where clicking the checkbox is required, even for humans:
# (Commonly seen on forms that are CAPTCHA-protected.)
'''
from seleniumbase import SB
def open_the_turnstile_page(sb):
    url = "seleniumbase.io/apps/turnstile"
    sb.driver.uc_open_with_reconnect(url, reconnect_time=2)

def click_turnstile_and_verify(sb):
    sb.switch_to_frame("iframe")
    sb.driver.uc_click("span.mark")
    sb.assert_element("img#captcha-success", timeout=3)

with SB(uc=True, test=True) as sb:
    open_the_turnstile_page(sb)
    try:
        click_turnstile_and_verify(sb)
    except Exception:
        open_the_turnstile_page(sb)
        click_turnstile_and_verify(sb)
    sb.set_messenger_theme(location="top_left")
    sb.post_message("SeleniumBase wasn't detected", duration=3)
'''

# Here's an example where the CAPTCHA appears after submitting a form:
'''
from seleniumbase import SB
with SB(uc=True, test=True, locale_code="en") as sb:
    url = "https://ahrefs.com/website-authority-checker"
    input_field = 'input[placeholder="Enter domain"]'
    submit_button = 'span:contains("Check Authority")'
    sb.driver.uc_open_with_reconnect(url, 1)  # The bot-check is later
    sb.type(input_field, "github.com/seleniumbase/SeleniumBase")
    sb.driver.reconnect(0.1)
    sb.driver.uc_click(submit_button, reconnect_time=4)
    sb.wait_for_text_not_visible("Checking", timeout=10)
    sb.highlight('p:contains("github.com/seleniumbase/SeleniumBase")')
    sb.highlight('a:contains("Top 100 backlinks")')
    sb.set_messenger_theme(location="bottom_center")
    sb.post_message("SeleniumBase wasn't detected!")
'''

# Here, the CAPTCHA appears after clicking to go to the sign-in screen:

from seleniumbase import SB
with SB(uc=True, test=True, ad_block_on=True) as sb:
    url = "https://www.thaiticketmajor.com/concert/"
    sb.driver.uc_open_with_reconnect(url, 5.5)
    sb.driver.uc_click("button.btn-signin", 4)
    sb.switch_to_frame('iframe[title*="Cloudflare"]')
    sb.assert_element("div#success svg#success-icon")
    sb.switch_to_default_content()
    sb.set_messenger_theme(location="top_center")
    sb.post_message("SeleniumBase wasn't detected!")