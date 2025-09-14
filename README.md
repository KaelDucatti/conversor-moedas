# Currency Bot - AWS Lambda

Este projeto implementa uma função **AWS Lambda** em Python que obtém a cotação do **Bitcoin em USD** e envia notificações via [CallMeBot](https://www.callmebot.com/).

---

## 📌 Pré-requisitos

* Conta AWS configurada ([tutorial oficial](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)).
* Python 3.9 ou superior instalado localmente.
* Biblioteca `requests`.
* Usuário registrado no **CallMeBot** (Telegram).
* Chave de API da [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas).

---

## 🚀 Estrutura do Projeto

```
lambda-deploy/
│── lambda_function.py   # Código principal
│── requirements.txt     # Dependências (requests)
```

Exemplo do `requirements.txt`:

```txt
requests==2.32.5
```

---

## 📝 Configuração do Código

No arquivo `lambda_function.py` você encontrará a linha:

```python
notification = converter.send_to_user(
    user=os.environ.get("CALLMEBOT_USER"), message=message
)
```

➡️ **Importante:** antes de fazer o deploy, configure seu usuário do CallMeBot em uma **variável de ambiente** no Lambda chamada `CALLMEBOT_USER`.
Assim, cada pessoa que utilizar este repositório poderá definir o próprio usuário, sem precisar alterar o código.

Exemplo no **AWS Console**:

* Nome: `CALLMEBOT_USER`
* Valor: `@seu_usuario_telegram`

⚠️ Removemos o usuário fixo do código para evitar exposição.

---

## 📦 Passo a Passo para Deploy

### 1. Preparar arquivos localmente

Crie uma pasta nova (ex: `lambda-deploy`) e coloque:

```
📁 lambda-deploy/
│── lambda_function.py
│── requirements.txt
```

### 2. Criar o pacote ZIP

No terminal/cmd dentro da pasta `lambda-deploy`:

**Linux/Mac:**

```bash
pip install -r requirements.txt -t .
zip -r currency-bot.zip .
```

**Windows (PowerShell):**

```powershell
pip install -r requirements.txt -t .
Compress-Archive -Path * -DestinationPath currency-bot.zip
```

Isso gera o arquivo `currency-bot.zip` pronto para subir no Lambda.

---

## ☁️ Criando a Lambda pelo Console AWS

1. Acesse o serviço **AWS Lambda**.
2. Clique em **Criar função**.

   * Nome: `currency-bot-btc`
   * Runtime: `Python 3.9`
   * Permissão: escolha uma role nova com permissão básica de execução Lambda.
3. Em **Código**, faça upload do arquivo `currency-bot.zip`.
4. Em **Configurações → Variáveis de ambiente**, adicione:

   * `API_KEY` → sua chave da AwesomeAPI.
   * `CALLMEBOT_USER` → seu usuário do CallMeBot (exemplo: `@seunome`).
5. Salve e teste clicando em **Testar**.

---

## ⏰ Agendamento com EventBridge (Console AWS)

1. Acesse o serviço **Amazon EventBridge → Schedules**.
2. Clique em **Criar Schedule**.

   * Nome: `currency-bot-hourly`
   * Frequência: `cron(0 8-23 * * ? *)` → Executa todo dia das 08h até 23h (inclusive).
   * Alvo: selecione sua Lambda (`currency-bot-btc`).
3. Salve. Agora sua função roda automaticamente nos horários definidos.

---

## 🧪 Teste Local

Você pode rodar o código localmente antes de empacotar:

```bash
python lambda_function.py
```

Certifique-se de exportar as variáveis de ambiente:

```bash
export API_KEY=sua_chave_api
export CALLMEBOT_USER=@seu_usuario
```

---

## 🧹 Limpeza de Recursos

Para evitar custos desnecessários:

1. Delete o **Schedule** no EventBridge.
2. Delete a função **Lambda** no console.
3. (Opcional) Delete o **IAM Role** criado automaticamente.
4. (Opcional) Delete os **logs do CloudWatch**.

---

## 📖 Observações

* Esse projeto serve como exemplo educacional.
* Se quiser melhorar, considere usar **AWS Lambda Layers** ou **Docker Images** para facilitar o deploy de dependências.
