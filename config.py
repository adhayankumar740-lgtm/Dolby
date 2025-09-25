import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = ("BQE1hZwAgJCqhVVjJ6fiEgeZtu_TD7kqwI0mR3D2wRhy3e17P5eVqV_aG7enGYx_vEOwrrcUAn8Tm2o_w3ciXNghc-tMJNgNgsZSt8fGyo02kgkRLVVxPcMYnDc40it2yfTnUcNC9XWOK6DHY0VWiNkKsoPU0vvpjOvI9Y4J814Hv48gPA5kQNcSEKWpZ5ovDaa7ovv-M5jb29XI8Yz-honbQKElb-ooUSX3CMT0JdumN5AtdOGsLj_-H94EJzd7ac_NF8yuh_eNhcD3BUKNuGIEbVhc65_SLCxvAqKwGp23GNKrdZ1G-x_SH1bnxFQboczUIVGiD11UknlhdZiqIA-K3NQKqQAAAAHo78rIAA")  # Userbot session string

# alias so that old code using config.SESSION works
SESSION = SESSION_NAME
