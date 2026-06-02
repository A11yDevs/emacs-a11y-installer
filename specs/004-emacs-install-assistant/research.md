# Research: Emacs Install Assistant

## Decision 1: Tratar a feature ativa como `004-emacs-install-assistant`
- Decision: Planejar todos os artefatos tecnicos em `specs/004-emacs-install-assistant/`.
- Rationale: O setup oficial do Spec Kit resolveu a branch `004-emacs-install-assistant` e copiou o template de plano para esse diretorio.
- Alternatives considered: reutilizar artefatos da feature 003 (rejeitado por misturar escopos de instalacao do Emacs e de perfil `minimal`).

## Decision 2: Reusar deteccao do `doctor` por adaptacao, nao por duplicacao
- Decision: O assistente vai consumir a infraestrutura diagnostica existente sempre que util para detectar plataforma, Emacs, PATH e versao, encapsulando a traducao em adaptadores locais.
- Rationale: Isso evita drift de comportamento entre `doctor`, `install emacs` e `install --profile minimal`.
- Alternatives considered: reimplementar toda a deteccao no subdominio `install` (rejeitado por duplicacao e maior risco de inconsistencias).

## Decision 3: Guidance-only como comportamento padrao
- Decision: O comportamento padrao do comando sera guidance-only, sem execucao automatica.
- Rationale: A especificacao prioriza seguranca, clareza e consentimento explicito; guidance-only entrega valor imediato mesmo em ambientes nao suportados para automacao.
- Alternatives considered: tentar execucao assistida automaticamente quando um metodo fosse detectado (rejeitado por violar a politica de consentimento explicito).

## Decision 4: Expor `--execute`, `--dry-run` e `--method`, mas nao `--manual`
- Decision: A superficie inicial da CLI vai usar `--execute` para solicitar execucao assistida, `--dry-run` para obter saida previsivel sem execucao e `--method` para escolha explicita entre metodos validos; `--manual` nao sera necessario porque o modo padrao ja e manual/orientativo.
- Rationale: Reduz redundancia na UX e mantem a CLI curta, explicita e acessivel.
- Alternatives considered: expor `--manual` alem do comportamento padrao (rejeitado por acrescentar alias sem ganho funcional real).

## Decision 5: Nao expor `--yes` na v1 desta feature
- Decision: O plano adia qualquer forma de confirmacao nao interativa para feature futura.
- Rationale: O risco operacional e alto em comandos externos de instalacao; guidance-only ja cobre o uso nao interativo seguro e `--execute` sem TTY deve falhar com seguranca.
- Alternatives considered: aceitar `--yes` apenas para winget ou brew (rejeitado porque ainda abriria um atalho perigoso antes da maturacao do fluxo de consentimento).

## Decision 6: Windows usa `winget install -e --id GNU.Emacs`
- Decision: O comando canonico de recomendacao/execucao assistida para Windows sera `winget install -e --id GNU.Emacs`.
- Rationale: A pesquisa confirmou o identificador oficial `GNU.Emacs` e a forma exata com `-e --id` torna a resolucao mais deterministica do que a forma abreviada.
- Alternatives considered: forma simplificada sem flags (rejeitada como forma interna canonica por ser menos explicita, embora possa aparecer em documentacao resumida).

## Decision 7: macOS usa `brew install emacs` na v1
- Decision: O metodo Homebrew planejado para macOS sera `brew install emacs`.
- Rationale: A pesquisa encontrou formula oficial ativa para `emacs`, enquanto o caminho pesquisado para `--cask` nao trouxe uma base equivalente para justificar a mesma confianca no plano.
- Alternatives considered: `brew install --cask emacs` (rejeitado nesta fase por base de evidencia mais fraca para adotar como caminho oficial do contrato).

## Decision 8: Debian/Ubuntu fica guidance-only na v1
- Decision: O assistente vai recomendar `sudo apt update` seguido de `sudo apt install emacs`, mas nao executara esse fluxo automaticamente na primeira versao.
- Rationale: O uso de `sudo`, prompts de privilegio e possiveis variacoes de ambiente tornam a execucao assistida mais arriscada e menos previsivel para leitores de tela na v1.
- Alternatives considered: suportar execucao assistida de `apt` com confirmacao (rejeitado por aumentar complexidade e risco sem necessidade para a primeira entrega).

## Decision 9: Plataformas desconhecidas nao devem ter comando adivinhado
- Decision: Em ambientes fora de Windows, macOS e Debian/Ubuntu formalmente suportados, o sistema entra em guidance-only seguro com orientacao manual e proximos passos.
- Rationale: Tentar inferir automaticamente comandos de instalacao em plataformas desconhecidas pode produzir instrucoes inseguras ou incorretas.
- Alternatives considered: mapear heuristicas para Fedora, Arch e outras distros na mesma feature (rejeitado por ampliar escopo e superficie de risco).

## Decision 10: Politica de versao configuravel com tres estados testaveis
- Decision: O sistema avaliara a versao detectada do Emacs em `supported`, `unknown` ou `too_old`, usando uma politica minima configuravel pelos mantenedores.
- Rationale: A especificacao exige comportamento testavel mesmo sem versao minima definitiva fechada.
- Alternatives considered: bloquear a feature ate a definicao final da politica de versao (rejeitado por impedir planejamento e testes de comportamento agora).

## Decision 11: Execucao externa com `subprocess.run` e `shell=False`
- Decision: A execucao assistida sera planejada com biblioteca padrao, usando `subprocess.run` com lista de argumentos, captura controlada de saida e sem shell implicito.
- Rationale: Isso reduz risco de injecao, melhora previsibilidade entre plataformas e facilita mocks em teste.
- Alternatives considered: usar shell string unica ou delegar para scripts externos (rejeitado por seguranca e por contrariar a constituicao).

## Decision 12: Pos-deteccao obrigatoria apos sucesso do comando assistido
- Decision: Apos um comando assistido bem-sucedido, o sistema fara nova deteccao do Emacs antes de declarar `SUCCESS` completo.
- Rationale: Algumas instalacoes concluem no gerenciador de pacotes, mas o executavel ainda nao fica visivel para a sessao atual; a UX precisa tratar isso explicitamente.
- Alternatives considered: assumir sucesso definitivo com base apenas no retorno do comando externo (rejeitado por gerar falso positivo de prontidao).