import asyncio

from loguru import logger
from .http import HTTPclient

class Client:

    def __init__(self) -> None:
        self.token: str = None
        self.http: HTTPclient = HTTPclient()

    # run() fonksiyonu içinde async runner() fonksiyonunu tanımlıyoruz.
    # runner() fonksiyonunda, async with self ifadesiyle, self nesnesinin asenkron bağlam yöneticisi metodları (__aenter__ ve __aexit__) çalıştırılır.
    # Bu bağlamda, self.start(token) metodunu await ile bekleyerek çalıştırıyoruz.
    # Bu yapı, kaynakların (bağlantı, oturum vb.) doğru bir şekilde açılmasını ve iş bittikten sonra düzgünce kapanmasını sağlar.
    def run(self, token: str):

        async def runner():
            logger.debug("runner() started")
            async with self:
                await self.start(token)

        # asyncio.run(runner()) komutu ile runner() adlı asenkron fonksiyon çalıştırılıyor.
        # try-except bloğu sayesinde kullanıcı Ctrl+C ile programı durdurduğunda
        # KeyboardInterrupt hatası yakalanıyor ve program sessizce kapanıyor.
        # Bu, programın ani kesintilerde düzgün şekilde kapanmasını sağlar.
        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass

    # start() fonksiyonu async bir fonksiyondur.
    # Bu fonksiyon içinde self.http.static_login await ile çağrılarak,
    # uygulamanın çalışma süresi boyunca geçerli olacak statik bir aiohttp ClientSession nesnesi oluşturulur.
    async def start(self, token: str):
        await self.http.static_login(token)

    # close() fonksiyonu async bir fonksiyondur.
    # Fonksiyon içinde self.http.close() metodu await ile çağrılarak,
    # daha önce açılmış olan aiohttp ClientSession bağlantısı düzgün bir şekilde kapatılır.
    async def close(self):
        logger.debug("closing ClientSession...")
        await self.http.close()


    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
