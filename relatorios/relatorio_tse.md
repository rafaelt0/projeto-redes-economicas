# Prefeitos eleitos (TSE) e trocas de partido


## Casamento com o IBGE


| eleicao | ue_tse | municipio_tse |
|---|---|---|

| eleicao | municipios_com_eleito_ordinario | suplementares | municipios |
|---|---|---|---|
| 2.008 | 640 | 3 | 640 |
| 2.012 | 645 | 21 | 645 |
| 2.016 | 628 | 21 | 640 |
| 2.020 | 622 | 23 | 645 |


## Mais de um eleito na mesma eleição ordinária

Deve ficar vazia.

| eleicao | codigo_ibge | municipio | eleitos |
|---|---|---|---|


## Municípios sem eleito na eleição ordinária

Votos anulados (candidato com registro indeferido). O mandato fica com o vencedor da suplementar. Sem suplementar, o vencedor estava sub judice e o arquivo do TSE não registra quem assumiu: o mandato fica sem partido e as transições dele saem da comparação.

| codigo_ibge | municipio | eleicao | suplementares |
|---|---|---|---|
| 3502507 | Aparecida | 2.008 | None |
| 3505609 | Barrinha | 2.008 | None |
| 3537602 | Peruíbe | 2.008 | None |
| 3540754 | Potim | 2.008 | None |
| 3544301 | Roseira | 2.008 | None |
| 3505203 | Bariri | 2.016 | 03/06/2018 PSDB |
| 3509205 | Cajamar | 2.016 | None |
| 3515905 | Floreal | 2.016 | 04/08/2019 PTB |
| 3516903 | General Salgado | 2.016 | 06/10/2019 PSDB |
| 3517208 | Guaiçara | 2.016 | 27/10/2019 DEM |
| 3519105 | Iacanga | 2.016 | None |
| 3524006 | Itupeva | 2.016 | None |
| 3526308 | Lagoinha | 2.016 | 17/03/2019 PR |
| 3527108 | Lins | 2.016 | None |
| 3529609 | Meridiano | 2.016 | 04/08/2019 PODE |
| 3530102 | Mirandópolis | 2.016 | 01/09/2019 PSL |
| 3530508 | Mococa | 2.016 | 02/04/2017 PMDB |
| 3539103 | Pirapora do Bom Jesus | 2.016 | 03/06/2018 MDB |
| 3545506 | Sandovalina | 2.016 | None |
| 3546306 | Santa Cruz das Palmeiras | 2.016 | 24/06/2018 PATRIOTA |
| 3551306 | Sebastianópolis do Sul | 2.016 | 19/11/2017 PTB |
| 3555307 | Turmalina | 2.016 | 03/06/2018 MDB |
| 3502002 | Analândia | 2.020 | 07/04/2024 SOLIDARIEDADE |
| 3502200 | Angatuba | 2.020 | 03/10/2021 REPUBLICANOS |
| 3502309 | Anhembi | 2.020 | 03/10/2021 PP |
| 3502705 | Apiaí | 2.020 | 03/10/2021 PSD |
| 3509254 | Cajati | 2.020 | 03/10/2021 PSDB |
| 3509452 | Campina do Monte Alegre | 2.020 | 03/10/2021 PSDB |
| 3517406 | Guaíra | 2.020 | 03/10/2021 MDB |
| 3522158 | Itaoca | 2.020 | 03/10/2021 DEM |
| 3524006 | Itupeva | 2.020 | 03/12/2023 MDB |
| 3526704 | Leme | 2.020 | 11/12/2022 PSD |
| 3529500 | Mendonça | 2.020 | 03/10/2021 PSDB |
| 3529807 | Mineiros do Tietê | 2.020 | 03/10/2021 PSL |
| 3537701 | Piacatu | 2.020 | 03/10/2021 PSDB |
| 3538204 | Pinhalzinho | 2.020 | 30/10/2022 PSDB |
| 3542503 | Reginópolis | 2.020 | 05/12/2021 PODE |
| 3543303 | Ribeirão Pires | 2.020 | 11/12/2022 PL |
| 3545100 | Salmourão | 2.020 | 05/12/2021 PSDB |
| 3548104 | Santo Antônio do Jardim | 2.020 | 03/10/2021 PODE |
| 3549953 | São Lourenço da Serra | 2.020 | 03/10/2021 PSDB |
| 3553401 | Tanabi | 2.020 | 27/11/2022 PSB |
| 3554755 | Trabiju | 2.020 | 03/10/2021 DEM |
| 3555356 | Ubarana | 2.020 | 03/12/2023 SOLIDARIEDADE |
| 3556354 | Vargem | 2.020 | 05/12/2021 PDT |


## Transições

Uma linha por município e eleição. `mandatos_inteiros`: sem suplementar antes nem depois.

| eleicao | municipios | sem_prefeito_conhecido | alternancia | reeleito_ou_mesmo_prefeito | mesmo_partido_outro_prefeito | mandatos_inteiros | inteiros_com_alternancia |
|---|---|---|---|---|---|---|---|
| 2.012 | 644 | 5 | 420 | 163 | 56 | 615 | 403 |
| 2.016 | 644 | 5 | 461 | 137 | 41 | 598 | 433 |
| 2.020 | 644 | 5 | 374 | 223 | 42 | 596 | 342 |


## Mesmo prefeito com partido diferente

Prefeito que trocou de legenda: não conta como alternância.

| eleicao | municipios |
|---|---|
| 2.012 | 16 |
| 2.016 | 30 |
| 2.020 | 61 |


## Partidos dos prefeitos (eleição ordinária e suplementar sem eleito ordinário)


| partido | 2008 | 2012 | 2016 | 2020 |
|---|---|---|---|---|
| 45 PSDB | 203 | 171 | 168 | 179 |
| 25 DEM | 74 | 45 | 50 | 70 |
| 55 PSD | 0 | 35 | 60 | 66 |
| 15 MDB | 0 | 0 | 2 | 58 |
| 14 PTB | 61 | 54 | 61 | 51 |
| 22 PL | 0 | 0 | 0 | 41 |
| 11 PP | 25 | 28 | 12 | 32 |
| 23 CIDADANIA | 0 | 0 | 0 | 25 |
| 10 REPUBLICANOS | 0 | 0 | 0 | 23 |
| 19 PODE | 0 | 0 | 1 | 22 |
| 43 PV | 23 | 30 | 32 | 16 |
| 40 PSB | 25 | 29 | 41 | 15 |
| 17 PSL | 1 | 4 | 1 | 10 |
| 51 PATRIOTA | 0 | 0 | 3 | 9 |
| 12 PDT | 28 | 18 | 13 | 6 |
| 20 PSC | 6 | 5 | 0 | 6 |
| 77 SOLIDARIEDADE | 0 | 0 | 0 | 6 |
| 13 PT | 63 | 73 | 8 | 4 |
| 70 AVANTE | 0 | 0 | 0 | 2 |
| 50 PSOL | 0 | 0 | 0 | 1 |
| 65 PC do B | 0 | 4 | 1 | 1 |
| 90 PROS | 0 | 0 | 2 | 1 |
| 10 PRB | 2 | 5 | 13 | 0 |
| 15 PMDB | 70 | 84 | 83 | 0 |
| 18 REDE | 0 | 0 | 1 | 0 |
| 19 PTN | 0 | 1 | 3 | 0 |
| 22 PR | 25 | 28 | 31 | 0 |
| 23 PPS | 28 | 26 | 33 | 0 |
| 27 PSDC | 0 | 1 | 0 | 0 |
| 31 PHS | 2 | 1 | 5 | 0 |
| 33 PMN | 2 | 1 | 0 | 0 |
| 36 PTC | 0 | 0 | 1 | 0 |
| 44 PRP | 1 | 1 | 3 | 0 |
| 77 SD | 0 | 0 | 11 | 0 |


## Siglas diferentes com o mesmo número

Renomeações, que o número trata como o mesmo partido.

| nr_partido | siglas |
|---|---|
| 10 | PRB, REPUBLICANOS |
| 15 | MDB, PMDB |
| 19 | PODE, PTN |
| 22 | PL, PR |
| 23 | CIDADANIA, PPS |
| 77 | SD, SOLIDARIEDADE |
