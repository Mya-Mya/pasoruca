from app import App

app = App()
while True:
    try:
        result = app.switch_status_by_cardid(input("CARD ID:"))
        print(result)
    except Exception as e:
        print(e)
