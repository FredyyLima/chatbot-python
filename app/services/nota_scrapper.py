import asyncio
from playwright.async_api import async_playwright

async def consultar_nota_via_sefaz(url: str):
    try:
        async with async_playwright() as p:
            # Cria o navegador
            browser = await p.chromium.launch(headless=False)
            
            # Cria um contexto com o User-Agent
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            
            # Cria a página no contexto configurado
            page = await context.new_page()

            try:
                await page.goto(url, timeout=30000)
                print("🌐 URL final:", page.url)

                # Aguarda o carregamento do conteúdo
                await page.wait_for_selector('#conteudo', timeout=30000)

                # Extração dos dados
                dados = await page.evaluate('''() => {
                    const razaoSocial = document.querySelector('#u20')?.innerText?.trim() || null;

                    const linhas = Array.from(document.querySelectorAll('*'))
                        .map(e => e.innerText)
                        .filter(t => t?.trim())
                        .join('\\n')
                        .split('\\n')
                        .map(l => l.trim())
                        .filter(Boolean);

                    let cnpj = null;
                    let dataHora = null;
                    let valorTotal = null;

                    for (let i = 0; i < linhas.length; i++) {
                        const linha = linhas[i];

                        if (!cnpj && linha.includes('CNPJ:')) {
                            const match = linha.match(/CNPJ:\\s*([\\d\\.\\/\\-]+)/);
                            if (match) cnpj = match[1];
                        }

                        if (!dataHora && linha.includes('Emissão:')) {
                            const match = linha.match(/Emissão:\\s*([\\d\\/\\: ]+)/);
                            if (match) dataHora = match[1];
                        }

                        if (!valorTotal && linha.includes('Valor a pagar R$:')) {
                            const proximaLinha = linhas[i + 1];
                            if (proximaLinha) valorTotal = proximaLinha.replace(',', '.').trim();
                        }
                    }

                    return {
                        razaoSocial,
                        cnpj,
                        dataHora,
                        valorTotal
                    };
                }''')

                await browser.close()
                return dados

            except Exception as e:
                await browser.close()
                print(f"Erro ao consultar nota na SEFAZ: {e}")
                return None

    except Exception as e:
        print(f"Erro geral no Playwright: {e}")
        return None
