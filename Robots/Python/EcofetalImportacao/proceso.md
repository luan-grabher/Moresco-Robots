Pastas
=======
**Empresa:** Ecofetal  Serviço de Auxílio Diagnóstico e Terapia Ltda

**Mensal:** Movimentos

**Receitas:** Receitas

**Taxa Cartão:** Baixa Cartões

Arquivos
=======
**Receitas:** RECEITA MAPA.xlsx -> Aba 'Listagem Completa'

**Taxa Cartão:** TAXA CARTÃO.xlsx

Necessidade:
============
Converter os dois arquivos em arquivos csv com as seguintes colunas:
- Data
- Conta de Debito
- Conta de Credito
- Codigo Historico Padrão
- Historico
- Valor

Contas Receitas:
======
- 7 = banco brasil movimento
- 154 = cliente convenios
- 410 = receitas vista
- 411 = receitas cart es
- 882 = cliente cart es
- 929 = receitas convenios
- 2153 = cliente depositos
- 2154 = cliente cheque pr
- 2215 = caixa rec vista
- 2220 = grava
- 2222 = receitas cheque prazo

Contas Taxa Cartão':
======
- Debito = 715
- Credito = 882
- Historico Padrao = 80

Extração de dados Receita:
========
- Data - Coluna E (Emissão)
- Conta Debito - Coluna T (Conta débito)
- Conta Credito - Coluna S (Conta crédito)
- Historico - Colunas A (Nº nota/NFSe), D (Tipo receita), F (Nome), B (Nº RPS), C (Tipo pagamento)
- Valor - Coluna U (Valor)

* Para linhas com somente 'Tipo pagamento' e o resto vazio, copia a linha acima da linha analisada: A,B,C,D,F,U,T,S
* Salvar data como dd/mm/aaaa

Extração de dados Taxa Cartão:
========
Data - Coluna A (Realização)
Conta Debito - 715
Conta Credito - 882
Historico - Colunas L (Descrição), N (Nº Nota), P (Nº Duplicata)
Valor - Coluna R (Valor)