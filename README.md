# 💸 Currency Converter Bot (AWS Lambda + EventBridge)

Este repositório contém uma função AWS Lambda em Python que consulta cotações (ex.: BTC → USD) pela **AwesomeAPI** e envia notificações via **CallMeBot**. O README abaixo explica passo a passo como empacotar (com dependências) e fazer o deploy **pelo Console da AWS** — além de opções avançadas (Lambda Layers e container image).

> 🎯 Objetivo: permitir que outra pessoa clone o repo, prepare o pacote com dependências e faça upload rápido pelo Console da AWS.

---

## 📁 Estrutura sugerida do projeto

```
currency-bot/
├── lambda_function.py   # Seu código (a função lambda_handler)
├── requirements.txt     # Ex: requests
├── README.md            # (este arquivo)
```

No `requirements.txt` coloque as dependências que sua função precisa. Exemplo mínimo:

```
requests
```

> Observação: não é obrigatório fixar versões, mas fixar (`requests==2.31.0`) ajuda a garantir reprodutibilidade.

---

## ⚙️ Preparar o pacote localmente (com dependências)

Vou mostrar 2 formas comuns — **método recomendado** (criar uma pasta `package/`, instalar dependências nela e gerar zip limpo) e uma alternativa direta.

### Método A — Recomendado (criar `package/` e gerar zip)

Esse método evita incluir arquivos do ambiente virtual (.venv) no zip.

1. Crie uma pasta de trabalho e coloque `lambda_function.py` e `requirements.txt` lá.

```bash
mkdir lambda-deploy
cd lambda-deploy
# coloque aqui lambda_function.py e requirements.txt
```

2. Crie uma pasta `package/` e instale as dependências dentro dela:

```bash
# Mac/Linux
python3 -m venv .venv              # opcional: isolar ambiente local
source .venv/bin/activate
pip install -r requirements.txt -t package/

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -t package\
```

3. Copie seu arquivo principal para dentro de `package/` e gere o ZIP final:

```bash
cp lambda_function.py package/
cd package
zip -r ../currency-bot.zip .
cd ..
```

No Windows PowerShell:

```powershell
Copy-Item lambda_function.py -Destination package\
Set-Location package
Compress-Archive -Path * -DestinationPath ..\currency-bot.zip
Set-Location ..
```

Resultado: `currency-bot.zip` pronto para upload. Esse zip contém seu código + todas as dependências necessárias no mesmo nível que o arquivo `lambda_function.py`.

---

### Método B — Instalar direto na pasta atual (rápido, mas cuidado com .venv)

Dentro da pasta do projeto:

```bash
# Instalar dependências no diretório atual
pip install -r requirements.txt -t .

# Criar ZIP (Mac/Linux)
zip -r currency-bot.zip .

# Windows PowerShell
Compress-Archive -Path * -DestinationPath currency-bot.zip
```

> ⚠️ Atenção: se você usar um virtualenv na mesma pasta (ex: `.venv`), remova/ignore essa pasta antes de criar o ZIP para não incluir arquivos desnecessários.

---

## 📤 Upload do ZIP pelo Console da AWS (passo a passo)

1. Acesse o Console AWS → **Lambda**.
2. Clique em **Create function** → **Author from scratch**:

   * Function name: `CurrencyBot`
   * Runtime: `Python 3.11` (ou a versão que preferir)
   * Permissions: escolha ou crie uma role com `AWSLambdaBasicExecutionRole`.
3. Depois de criada, abra a função e vá na aba **Code**.
4. Clique em **Upload from** → **.zip file** → selecione `currency-bot.zip` e faça o upload.
5. Clique em **Deploy** (ou **Save**) para aplicar o código.

---

## 🔧 Configurar variáveis de ambiente (pelo Console)

1. Na página da sua função Lambda, vá em **Configuration** → **Environment variables** → **Edit**.
2. Adicione a variável `API_KEY` com a sua chave da AwesomeAPI.
3. Salve.

> Dica: para maior segurança em produção, use **AWS Secrets Manager** ou **Parameter Store** e recupere o segredo em tempo de execução.

---

## 🧪 Testar a função (Console)

1. Na página da função Lambda, clique em **Test**.
2. Configure um evento de teste (um JSON vazio `{}` funciona).
3. Clique em **Test** novamente.
4. Confira a resposta e os logs: **Monitor** → **View logs in CloudWatch**.

---

## ⏰ Agendamento com EventBridge (Console)

1. Console AWS → **Amazon EventBridge** → **Rules** (ou **Scheduler / Cronograms**, conforme sua região/versão do console) → **Create rule**.
2. Preencha:

   * Name: `CurrencyBotSchedule`
   * Type: **Schedule**
   * Expression: escolha uma expressão apropriada. Exemplo para rodar **apenas das 08:00 às 23:00, no minuto 00** (horário `America/Sao_Paulo`):

```
cron(0 8-23 * * ? *)
```

* Caso queira também meia-noite (00:00), use:

```
cron(0 0,8-23 * * ? *)
```

3. Em **Target**, selecione **Lambda function** e escolha `CurrencyBot`.
4. Crie a regra.

> Lembre-se de ajustar o fuso horário do agendamento no console, se disponível, para `America/Sao_Paulo`.

---

## 🧩 Alternativa: usar Lambda Layer para dependências

Se seu pacote com dependências ficar grande, use um **Layer** e mantenha apenas o seu código na função.

**Criar um Lambda Layer (pelo Console + empacotamento local):**

1. Na pasta local, crie a estrutura para o layer (ex.: targeting Python 3.11):

```bash
mkdir -p python/lib/python3.11/site-packages
pip install -r requirements.txt -t python/lib/python3.11/site-packages
zip -r layer-requests.zip python
```

2. Console AWS → **Lambda** → **Layers** → **Create layer**.

   * Name: `requests-layer`
   * Upload: `layer-requests.zip`
   * Runtime compatibility: selecione `Python 3.11` (ou a sua runtime)
3. Após criar, abra sua função Lambda → **Configuration** → **Layers** → **Add a layer** → selecione o layer criado.

Agora as dependências estarão disponíveis para sua função sem precisar empacotar tudo no ZIP principal.

---

## 🐳 Alternativa: Deploy como Container Image (opcional)

Se preferir, crie uma imagem Docker com todas as dependências e publique no **ECR**. Na criação da função Lambda escolha **Container image** em vez de ZIP. Essa abordagem é útil se o pacote for muito grande ou você já usa containers.

---

## 📉 Remover recursos pelo Console (evitar custos)

1. EventBridge → Rules → selecione `CurrencyBotSchedule` → Delete rule.
2. Lambda → Functions → selecione `CurrencyBot` → Delete.
3. IAM → Roles → remova a role criada (se aplicável).
4. CloudWatch → Logs → delete o log group da função (opcional).

---

## 🐛 Troubleshooting rápido

* **Erro: API\_KEY não encontrada** → verifique em *Configuration → Environment variables* se `API_KEY` foi adicionada corretamente.
* **Timeout ou erro na requisição** → aumente o timeout da requisição (`requests.get(..., timeout=10)`) e o timeout da função Lambda (Configuration → General configuration → Timeout).
* **Pacote muito grande** → use Lambda Layer ou Container Image.

---

## 🔐 Segurança / Boas práticas

* Não coloque a API\_KEY no código. Use variáveis de ambiente ou Secrets Manager.
* Dê à role da Lambda apenas as permissões necessárias (princípio do menor privilégio).
* Monitore custos e logs com CloudWatch e crie alertas se necessário.

---

## 📦 Exemplo rápido de `requirements.txt`

```
requests
```

---

## 📜 Licença

MIT — sinta-se à vontade para usar, adaptar e melhorar.
