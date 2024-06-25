from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import stripe


# This is your test secret API key.
stripe.api_key = 'sk_test_51PQwQtIf22jmWnXxgTSFMFUHxW75nkwV9kwyT6g1U62kxv65cneW5XUs0QbLbVAkB4RmBf9lh7SOB5nDC0apqWsL00DyRI6fF2'
app = FastAPI()

# Mount the static directory
app.mount("/Frontend", StaticFiles(directory="Frontend"), name="Frontend")

YOUR_DOMAIN = 'http://localhost:8003'

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/checkout.html", response_class=HTMLResponse)
async def get_checkout():
    with open('Frontend/checkout.html', 'r') as f:
        checkout_html = f.read()
    return Response(content=checkout_html, media_type="text/html")

@app.get("/success.html", response_class=HTMLResponse)
async def get_success():
    with open('Frontend/success.html', 'r') as f:
        success_html = f.read()
    return Response(content=success_html, media_type="text/html")

@app.get("/cancel.html", response_class=HTMLResponse)
async def get_cancel():
    with open('Frontend/cancel.html', 'r') as f:
        cancel_html = f.read()
    return Response(content=cancel_html, media_type="text/html")

@app.post('/create-checkout-session')
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                     'price': 'price_1PShL1If22jmWnXxW8BRw0jI',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
