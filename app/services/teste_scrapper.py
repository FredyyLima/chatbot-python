import asyncio
from app.services.nota_scrapper import consultar_nota_via_sefaz

async def main():
    link = "https://www.fazenda.pr.gov.br/nfce/qrcode?p=41250436340041000174650050000157521035263724%7C2%7C1%7C1%7CAF08CA85D32950FA633E42C2E1D5DDC542A05DAD"
    dados = await consultar_nota_via_sefaz(link)

    if dados:
        print("Dados extraídos com sucesso:")
        print(dados)
    else:
        print("Erro ao extrair os dados.")

asyncio.run(main())

