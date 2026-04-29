# SKILL.md - Heartbeat (Verificação Periódica)

## Quando usar
Esta skill é executada automaticamente a cada 1 hora via cron job para processar emails e enviar resumo proativo.

## Steps (Execução Determinística)

### 1. Configuração
```bash
export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"
export GOG_KEYRING_PASSWORD="x"

BOT_TOKEN="8345047089:AAFmn7WGtckjsUwucYLfEn9YacGb6wuoVg4"
CHAT_ID="8352338864"
EMAIL_ACCOUNT="ariahamamura@gmail.com"
```

### 2. Buscar emails não lidos
```bash
gog gmail messages list --account "$EMAIL_ACCOUNT" "is:unread" -j --max 10
```

### 3. Extrair IDs dos emails
Parse o JSON e extraia os campos `id` de cada mensagem.

### 4. Para cada email:
- Verificar se é reunião/urgente (prioridade #1)
- Se reunião → criar card Trello + enviar msg imediata
- **Arquivar** (lido + remover do inbox):
```bash
gog gmail messages modify --account "$EMAIL_ACCOUNT" <ID> --remove UNREAD,INBOX
```

### 5. Contar total processado
Se COUNT > 0, enviar resumo proativo:

### 6. Enviar resumo via Telegram
```bash
TEXT="📊 *Heartbeat* - $(date '+%d/%m %H:%M')

✅ *$COUNT email(s) processado(s)*
📧 Processados e arquivados"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"${TEXT}\", \"parse_mode\": \"Markdown\"}"
```

### 7. Se COUNT == 0
Responder apenas `HEARTBEAT_OK` (não precisa enviar Telegram).

---

## Prioridades de Ação

| Tipo | Ação |
|------|------|
| Reunião | Msg imediata + card Trello + arquivar |
| Urgente (prazo, IMPORTANTE) | Msg imediata + card Trello + arquivar |
| Informativo | Arquivar silenciosamente |
| Automático (GitHub, receipts) | Arquivar silenciosamente |

## Referências
- Script: `/home/openclaw/.openclaw/workspace/heartbeat.sh`
- HEARTBEAT.md para regras completas