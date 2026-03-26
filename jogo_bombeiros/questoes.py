# questoes.py — Banco de questões sobre normas técnicas do Corpo de Bombeiros
# Formato: (modulo, dificuldade, enunciado, op_a, op_b, op_c, op_d, correta, explicacao)

QUESTOES_SEED = [

    # ══════════════════════════════════════════════════════════════════
    #  MÓDULO 1 — Saídas de Emergência  (NBR 9077)
    # ══════════════════════════════════════════════════════════════════
    (
        "Saídas de Emergência", "basico",
        "Qual é o valor da unidade de passagem (UP) adotada pela NBR 9077 para dimensionamento das saídas de emergência?",
        "0,40 m", "0,55 m", "0,60 m", "0,80 m", "B",
        "A unidade de passagem (UP) equivale a 0,55 m, sendo a medida-base para calcular a "
        "capacidade de escoamento de corredores, portas e escadas segundo a NBR 9077."
    ),
    (
        "Saídas de Emergência", "basico",
        "A capacidade de escoamento de portas e passagens horizontais, conforme a NBR 9077, é de:",
        "40 pessoas/UP", "60 pessoas/UP", "80 pessoas/UP", "100 pessoas/UP", "D",
        "Portas e passagens horizontais possuem a maior capacidade: 100 pessoas por UP. "
        "Escadas têm valores menores pois o deslocamento vertical é mais lento."
    ),
    (
        "Saídas de Emergência", "basico",
        "As portas de saídas de emergência devem abrir em qual sentido?",
        "Para dentro do ambiente (contra o fluxo de saída)",
        "No sentido do fluxo de saída (para fora do ambiente)",
        "Em qualquer sentido, desde que com mola de fechamento",
        "Para dentro, quando localizadas em corredores estreitos",
        "B",
        "As portas de saídas de emergência devem abrir no sentido do fluxo de saída, "
        "evitando bloqueios causados pelo empurrão coletivo de pessoas em situação de pânico."
    ),
    (
        "Saídas de Emergência", "basico",
        "Qual é a largura mínima exigida para escadas de emergência em edificações de uso geral?",
        "0,80 m", "1,00 m", "1,10 m", "1,50 m", "C",
        "A largura mínima de 1,10 m corresponde a 2 UPs (2 × 0,55 m), sendo o padrão "
        "para a maioria das edificações conforme a NBR 9077."
    ),
    (
        "Saídas de Emergência", "intermediario",
        "A capacidade de escoamento para escadas utilizadas em sentido DESCENDENTE durante evacuação é de:",
        "100 pessoas/UP", "75 pessoas/UP", "60 pessoas/UP", "40 pessoas/UP", "C",
        "Escadas descendentes têm capacidade de 60 pessoas/UP. O valor é inferior ao de passagens "
        "horizontais pois a descida em emergência é mais lenta e exige atenção dos usuários."
    ),
    (
        "Saídas de Emergência", "intermediario",
        "A escada do tipo 'Enclausurada à Prova de Fumaça' (PFu) se caracteriza por possuir:",
        "Pressurização mecânica do ar interno por ventilador centralizado",
        "Antecâmara ventilada que impede a entrada de fumaça na caixa da escada",
        "Paredes de concreto armado com espessura mínima de 20 cm",
        "Sistema de chuveiros automáticos integrado ao poço da escada",
        "B",
        "A escada PFu possui antecâmara com abertura para o exterior ou duto de ventilação, "
        "criando barreira física e de pressão de ar que impede a entrada de fumaça — sem necessidade de pressurização mecânica."
    ),
    (
        "Saídas de Emergência", "intermediario",
        "Um pavimento possui 120 ocupantes que devem evacuar por uma única escada descendente. "
        "Qual é a largura mínima necessária para essa escada segundo a NBR 9077?",
        "0,55 m (1 UP)", "1,10 m (2 UPs)", "1,65 m (3 UPs)", "2,20 m (4 UPs)", "B",
        "Cálculo: 120 pessoas ÷ 60 pessoas/UP = 2 UPs. Largura = 2 × 0,55 m = 1,10 m. "
        "É a largura mínima de qualquer escada, portanto já atende ao critério normativo."
    ),
    (
        "Saídas de Emergência", "avancado",
        "Segundo a NBR 9077, qual é a distância máxima de caminhamento até uma saída em edificações de uso comercial (Grupo C) SEM chuveiros automáticos?",
        "20 m", "30 m", "40 m", "50 m", "B",
        "Para edificações comerciais (Grupo C) sem sprinklers, a NBR 9077 limita a distância "
        "de caminhamento a 30 m. Com chuveiros automáticos esse valor pode ser aumentado para até 45 m."
    ),
    (
        "Saídas de Emergência", "avancado",
        "Em edificações residenciais multifamiliares com altura de saída entre 12 m e 23 m, "
        "qual é o tipo mínimo de escada exigido pela NBR 9077?",
        "Escada Aberta (EA)",
        "Escada Enclausurada Não Protegida (NE)",
        "Escada Enclausurada Protegida (EP)",
        "Escada Enclausurada à Prova de Fumaça (PFu)",
        "C",
        "Para edificações residenciais com altura de saída entre 12 m e 23 m, a NBR 9077 exige "
        "no mínimo a escada Enclausurada Protegida (EP), com paredes corta-fogo e porta P-30."
    ),
    (
        "Saídas de Emergência", "avancado",
        "Qual é o comprimento máximo permitido para um corredor sem saída (beco) em edificações conforme a NBR 9077?",
        "5 m", "10 m", "15 m", "20 m", "B",
        "Corredores sem saída (becos) têm comprimento máximo de 10 m segundo a NBR 9077, "
        "pois representam risco em situação de evacuação — o ocupante precisa retornar ao corredor principal."
    ),

    # ══════════════════════════════════════════════════════════════════
    #  MÓDULO 2 — Extintores de Incêndio  (NBR 12693)
    # ══════════════════════════════════════════════════════════════════
    (
        "Extintores de Incêndio", "basico",
        "Qual agente extintor é indicado para combater incêndios da Classe A (materiais sólidos combustíveis)?",
        "Dióxido de carbono (CO₂)",
        "Pó químico seco BC",
        "Água",
        "Halon",
        "C",
        "A água é o agente extintor mais eficaz para incêndios Classe A (madeira, papel, tecidos), "
        "pois age por resfriamento e abafamento. CO₂ e pó BC não são adequados para essa classe."
    ),
    (
        "Extintores de Incêndio", "basico",
        "Incêndios da Classe B envolvem:",
        "Materiais sólidos que formam brasas",
        "Líquidos ou gases inflamáveis",
        "Equipamentos elétricos energizados",
        "Metais combustíveis como magnésio e titânio",
        "B",
        "A Classe B engloba incêndios em líquidos inflamáveis (gasolina, álcool, óleo) e gases combustíveis. "
        "O combate é feito por abafamento, sendo indicados extintores de CO₂, pó BC ou espuma."
    ),
    (
        "Extintores de Incêndio", "basico",
        "Qual é o agente extintor PROIBIDO para uso em incêndios Classe C (equipamentos elétricos energizados)?",
        "CO₂ (dióxido de carbono)",
        "Pó químico seco ABC",
        "Água",
        "Halon",
        "C",
        "A água conduz eletricidade e representa risco grave de eletrocussão quando usada em equipamentos "
        "energizados (Classe C). Nunca deve ser utilizada nessa situação."
    ),
    (
        "Extintores de Incêndio", "basico",
        "Segundo a NBR 12693, a distância máxima a percorrer até um extintor de incêndio em riscos médios é de:",
        "10 m", "15 m", "20 m", "25 m", "C",
        "Para riscos médios, a NBR 12693 estabelece distância máxima de 20 m ao extintor mais próximo. "
        "Para riscos leves o limite é 25 m e para riscos altos é 15 m."
    ),
    (
        "Extintores de Incêndio", "intermediario",
        "Qual extinto é adequado para incêndios Classe D (metais combustíveis como sódio, magnésio e titânio)?",
        "Água pressurizada",
        "CO₂ (dióxido de carbono)",
        "Pó químico específico para metais",
        "Espuma mecânica",
        "C",
        "Incêndios Classe D exigem pó específico desenvolvido para o tipo de metal combustível. "
        "Água e CO₂ podem reagir violentamente com metais como sódio e potássio, agravando o incêndio."
    ),
    (
        "Extintores de Incêndio", "intermediario",
        "A Classe F de incêndio, incorporada à NBR 12693, é caracterizada por incêndios em:",
        "Florestas e vegetação seca",
        "Fibras e fios elétricos de alta tensão",
        "Óleos e gorduras de cozinha em altas temperaturas",
        "Fluidos frigorígenos inflamáveis",
        "C",
        "A Classe F engloba incêndios envolvendo óleos e gorduras vegetais ou animais utilizados em "
        "frituras a altas temperaturas. Exigem extintores de pó úmido ou agentes especiais Classe K."
    ),
    (
        "Extintores de Incêndio", "intermediario",
        "Segundo a NBR 12693, a vida útil máxima de um extintor de incêndio portátil é de:",
        "5 anos", "10 anos", "15 anos", "20 anos", "B",
        "Extintores portáteis têm vida útil máxima de 10 anos. Após esse período devem ser recolhidos "
        "e descartados conforme normas ambientais, independentemente de seu estado aparente."
    ),
    (
        "Extintores de Incêndio", "avancado",
        "Para uma área de 500 m² de risco médio (Classe A), quantos extintores de água com capacidade "
        "extintora 2-A são necessários, segundo a NBR 12693?",
        "1 extintor", "2 extintores", "3 extintores", "5 extintores", "B",
        "Cada unidade extintora '1-A' protege até 250 m² em risco médio. Um extintor '2-A' equivale a "
        "2 unidades extintoras Classe A, cobrindo 500 m². Para 500 m², são necessários 2 extintores 2-A "
        "garantindo cobertura mínima de 250 m² por extintor."
    ),
    (
        "Extintores de Incêndio", "avancado",
        "Qual é a diferença entre extintores de pó químico seco BC e ABC?",
        "O pó ABC combate incêndios em equipamentos elétricos e o BC não",
        "O pó ABC contém monofosfato de amônio e combate também incêndios Classe A, diferente do BC",
        "O pó BC tem maior alcance de jato que o ABC",
        "Não há diferença prática; ambos são equivalentes para todas as classes de fogo",
        "B",
        "O pó ABC contém monofosfato de amônio, que forma uma camada sólida sobre materiais em brasa "
        "(Classe A), impedindo a reacensão. O pó BC (bicarbonato de sódio ou potássio) combate apenas "
        "as classes B e C por interrupção química da reação."
    ),
    (
        "Extintores de Incêndio", "avancado",
        "Qual requisito a NBR 12693 estabelece para a instalação de extintores em locais de grande concentração de público?",
        "Devem ser instalados exclusivamente em armários trancados para evitar vandalismo",
        "Devem ser instalados de modo que a alça esteja a no máximo 1,60 m do piso",
        "Podem ser instalados apenas no exterior das edificações para facilitar o acesso",
        "Devem ser pintados de vermelho independente do tipo de agente extintor",
        "B",
        "A NBR 12693 exige que os extintores sejam instalados de modo que a alça de transporte esteja "
        "a no máximo 1,60 m do piso, garantindo acesso ergonômico para adultos de diferentes estaturas."
    ),

    # ══════════════════════════════════════════════════════════════════
    #  MÓDULO 3 — Sinalização de Segurança  (NBR 13434)
    # ══════════════════════════════════════════════════════════════════
    (
        "Sinalização de Segurança", "basico",
        "Qual cor de segurança é associada às sinalizações de combate a incêndio e equipamentos de proteção contra incêndio?",
        "Amarelo", "Verde", "Vermelho", "Azul", "C",
        "O vermelho é a cor de segurança destinada às sinalizações de combate a incêndio, "
        "identificando extintores, hidrantes, acionadores manuais e demais equipamentos de combate."
    ),
    (
        "Sinalização de Segurança", "basico",
        "A cor verde nas sinalizações de segurança contra incêndio indica:",
        "Perigo ou advertência de risco de incêndio",
        "Equipamentos de combate a incêndio",
        "Saídas de emergência e rotas de fuga",
        "Proibição de entrada a pessoas não autorizadas",
        "C",
        "O verde identifica as rotas de saída e saídas de emergência, sendo utilizado em sinalização "
        "de portas de emergência, escadas e indicação do caminho de evacuação."
    ),
    (
        "Sinalização de Segurança", "basico",
        "Segundo a NBR 13434, a sinalização de segurança deve ser:",
        "Visível apenas com iluminação normal",
        "Fotoluminescente ou com iluminação de emergência, visível mesmo em falta de energia",
        "Instalada somente em edificações acima de 4 pavimentos",
        "Substituída a cada 2 anos independentemente do estado de conservação",
        "B",
        "A NBR 13434 exige que a sinalização seja visível mesmo em situação de falta de energia, "
        "por meio de materiais fotoluminescentes ou iluminação de emergência dedicada."
    ),
    (
        "Sinalização de Segurança", "basico",
        "Qual símbolo é utilizado pela NBR 13434 para indicar o local de um extintor de incêndio?",
        "Figura humana correndo com seta de direção",
        "Chama com barra diagonal vermelha",
        "Extintor com fundo vermelho",
        "Hidrante com caixa vermelha",
        "C",
        "O símbolo de extintor de incêndio é representado por um extintor portátil com fundo vermelho, "
        "conforme padronização da NBR 13434 e das normas ISO de sinalização de segurança."
    ),
    (
        "Sinalização de Segurança", "intermediario",
        "A distância máxima de visualização de uma sinalização de segurança com altura de símbolo de 10 cm é de:",
        "5 m", "10 m", "15 m", "20 m", "B",
        "Segundo a NBR 13434, a distância máxima de visualização é calculada multiplicando a altura "
        "do símbolo por 100. Para símbolo de 10 cm (0,10 m): 0,10 × 100 = 10 m."
    ),
    (
        "Sinalização de Segurança", "intermediario",
        "Qual é a cor de contraste utilizada obrigatoriamente com a cor vermelha nas sinalizações de combate a incêndio?",
        "Preto", "Branco", "Amarelo", "Azul", "B",
        "A cor de contraste do vermelho é o branco. A NBR 13434 define pares de cores de segurança "
        "e contraste para garantir legibilidade em diferentes condições de iluminação."
    ),
    (
        "Sinalização de Segurança", "intermediario",
        "As sinalizações de seta indicativa de rota de saída devem ser instaladas de modo que:",
        "Fiquem acima de 2,50 m do piso para não serem vandalizadas",
        "Sejam visíveis de qualquer ponto da rota de saída, com espaçamento máximo de 15 m entre sinais",
        "Sejam posicionadas exclusivamente no piso, em forma de faixa fotoluminescente",
        "Cubram apenas os dois últimos metros antes da porta de saída",
        "B",
        "As sinalizações de rota de saída devem cobrir todo o percurso de evacuação sem pontos cegos, "
        "com espaçamento máximo entre sinais de 15 m, garantindo visibilidade contínua."
    ),
    (
        "Sinalização de Segurança", "avancado",
        "Uma sinalização fotoluminescente deve emitir luminância mínima após 10 minutos no escuro de:",
        "0,3 mcd/m²", "3 mcd/m²", "30 mcd/m²", "300 mcd/m²", "B",
        "A NBR 13434 exige luminância mínima de 3 mcd/m² (milicandelas por metro quadrado) "
        "medida 10 minutos após cessar a iluminação de excitação, garantindo visibilidade na evacuação."
    ),
    (
        "Sinalização de Segurança", "avancado",
        "Para corredores de evacuação com largura superior a 2 m, a NBR 13434 recomenda que as sinaliza-ções de saída sejam instaladas:",
        "Apenas nas paredes laterais à altura de 2,20 m do piso",
        "No centro do teto ou em posição suspensa sobre o corredor",
        "No piso em faixa contínua fotoluminescente de 10 cm",
        "Em ambos os lados do corredor na altura dos olhos",
        "B",
        "Em corredores largos, a sinalização instalada no centro do teto ou suspensa garante visibilidade "
        "para pessoas de ambos os lados do corredor, mesmo em condição de fumaça baixa."
    ),
    (
        "Sinalização de Segurança", "avancado",
        "Qual afirmação sobre a manutenção da sinalização de segurança está CORRETA segundo a NBR 13434?",
        "A substituição deve ocorrer somente quando o símbolo estiver completamente apagado",
        "Sinalizações fotoluminescentes devem ser verificadas semestralmente quanto à luminância",
        "A limpeza das placas deve ser feita exclusivamente com solventes orgânicos",
        "Não há obrigatoriedade de manutenção periódica para sinalizações em locais fechados",
        "B",
        "A NBR 13434 recomenda verificação periódica (semestral) da luminância de materiais "
        "fotoluminescentes para garantir que mantêm a eficácia mínima exigida pela norma."
    ),

    # ══════════════════════════════════════════════════════════════════
    #  MÓDULO 4 — Detecção e Alarme  (NBR 17240)
    # ══════════════════════════════════════════════════════════════════
    (
        "Detecção e Alarme", "basico",
        "Qual tipo de detector de incêndio é mais indicado para ambientes com produção de fumaça visível?",
        "Detector de calor pontual",
        "Detector de chama (UV/IR)",
        "Detector de fumaça por ionização ou fotoelétrico",
        "Detector de gás combustível",
        "C",
        "Detectores de fumaça (por ionização ou fotoelétrico) são os mais indicados para detectar "
        "incêndios em fase incipiente com produção de fumaça visível, como em papéis e madeiras."
    ),
    (
        "Detecção e Alarme", "basico",
        "O acionador manual de alarme de incêndio deve ser instalado a qual altura do piso?",
        "0,80 m a 1,00 m", "1,00 m a 1,20 m", "1,20 m a 1,60 m", "1,60 m a 2,00 m", "C",
        "A NBR 17240 estabelece que os acionadores manuais devem ser instalados a uma altura de "
        "1,20 m a 1,60 m do piso, garantindo alcance acessível para a maioria dos usuários."
    ),
    (
        "Detecção e Alarme", "basico",
        "Uma Central de Detecção e Alarme de Incêndio (CDAI) deve estar localizada:",
        "No subsolo, próximo ao gerador de emergência",
        "Em local de vigilância permanente ou de fácil acesso para os bombeiros",
        "No último pavimento para facilitar a comunicação com o telhado",
        "Em qualquer local, desde que em armário com chave individual",
        "B",
        "A CDAI deve estar em local de vigilância permanente (portaria, recepção 24h) ou de acesso "
        "rápido para os bombeiros, pois é o ponto central de monitoramento e acionamento do sistema."
    ),
    (
        "Detecção e Alarme", "basico",
        "Qual é a função do detector de calor por taxa de variação (rate-of-rise)?",
        "Detectar a presença de fumaça por alteração da transmissão de luz",
        "Acionar o alarme quando a temperatura sobe acima de um limiar fixo (ex: 57°C)",
        "Acionar o alarme quando a temperatura aumenta mais de 8°C a 12°C por minuto",
        "Detectar chamas por radiação infravermelha",
        "C",
        "O detector por taxa de variação (rate-of-rise) aciona o alarme quando a taxa de elevação "
        "da temperatura excede 8°C a 12°C por minuto, detectando incêndios de crescimento rápido "
        "antes de atingir a temperatura de limiar fixo."
    ),
    (
        "Detecção e Alarme", "intermediario",
        "Qual é a área máxima de cobertura de um detector de fumaça pontual em ambientes com teto plano de até 3 m de altura?",
        "30 m²", "60 m²", "80 m²", "100 m²", "C",
        "Segundo a NBR 17240, detectores de fumaça pontuais em tetos planos de até 3 m de altura "
        "cobrem no máximo 80 m² cada, com espaçamento máximo de 9 m entre detectores."
    ),
    (
        "Detecção e Alarme", "intermediario",
        "Em sistemas de detecção e alarme, o conceito de 'zona' se refere a:",
        "Cada piso ou pavimento da edificação, obrigatoriamente",
        "Agrupamento lógico de detectores que permitem identificar a área de origem do alarme",
        "Conjunto de detectores conectados em série em um único loop",
        "Área mínima protegida por um extintor automático",
        "B",
        "Uma zona é um agrupamento de detectores ou acionadores de uma mesma área identificável, "
        "permitindo que a CDAI informe com precisão onde o alarme foi acionado."
    ),
    (
        "Detecção e Alarme", "intermediario",
        "A NBR 17240 determina que os sistemas de detecção e alarme devem ter alimentação elétrica de emergência capaz de manter o sistema em modo de supervisão por no mínimo:",
        "4 horas", "12 horas", "24 horas", "72 horas", "C",
        "A NBR 17240 exige no mínimo 24 horas de autonomia em modo de supervisão (stand-by) e "
        "30 minutos adicionais em modo de alarme, garantindo operação mesmo em falta de energia elétrica."
    ),
    (
        "Detecção e Alarme", "avancado",
        "Em qual tipo de ambiente o detector de chama (UV/IR) é mais indicado em detrimento do detector de fumaça?",
        "Dormitórios e quartos de hotel",
        "Corredores de evacuação com carpete",
        "Áreas de armazenamento de líquidos inflamáveis com combustão sem fumaça visível",
        "Cozinhas industriais com grande geração de vapores",
        "C",
        "Detectores de chama são indicados para ambientes com combustíveis que geram chama sem fumaça "
        "densa (líquidos inflamáveis como gasolina e álcool) e onde detectores de fumaça poderiam "
        "gerar alarmes falsos por vapores, poeira ou fumaça de processo industrial."
    ),
    (
        "Detecção e Alarme", "avancado",
        "O que caracteriza um sistema de detecção e alarme endereçável em comparação ao convencional?",
        "Utiliza fio de fusível no lugar de detectores pontuais",
        "Cada dispositivo possui endereço único, permitindo identificar individualmente o detector acionado",
        "É exclusivamente wireless (sem fio), dispensando cabeamento",
        "Opera apenas por temperatura, sem detecção de fumaça",
        "B",
        "Em sistemas endereçáveis, cada detector e acionador possui um código de endereço único. "
        "A CDAI identifica exatamente qual dispositivo foi acionado, diferente do convencional "
        "que informa apenas a zona, sem precisar o equipamento individual."
    ),
    (
        "Detecção e Alarme", "avancado",
        "Qual afirmativa sobre a manutenção periódica de sistemas de detecção e alarme está CORRETA segundo a NBR 17240?",
        "A manutenção pode ser realizada pelo próprio síndico do condomínio sem certificação técnica",
        "Os testes funcionais dos detectores devem ser realizados no mínimo anualmente por empresa habilitada",
        "Detectores de fumaça nunca precisam ser substituídos enquanto a central não indicar falha",
        "O sistema pode ficar desativado por até 7 dias para manutenção sem notificação ao Corpo de Bombeiros",
        "B",
        "A NBR 17240 exige manutenção periódica com testes funcionais de todos os dispositivos "
        "no mínimo anualmente, realizada por empresa habilitada e com emissão de laudo técnico."
    ),

    # ══════════════════════════════════════════════════════════════════
    #  MÓDULO 5 — Hidrantes e Mangotinhos  (NBR 13714)
    # ══════════════════════════════════════════════════════════════════
    (
        "Hidrantes e Mangotinhos", "basico",
        "Qual é a principal diferença entre hidrante e mangotinho quanto ao uso?",
        "Hidrante usa água gelada; mangotinho usa espuma",
        "Mangotinho é para uso da brigada de incêndio; hidrante é exclusivo para os bombeiros",
        "Mangotinho possui mangueira semirrígida de menor diâmetro para uso leigo; hidrante usa mangueiras de maior diâmetro operadas por equipe treinada",
        "Não há diferença operacional, apenas estética",
        "C",
        "O mangotinho tem mangueira semirrígida sempre pressurizada (tipo carretel) de fácil manuseio "
        "por pessoas sem treinamento especializado. O hidrante de coluna ou de parede usa mangueiras "
        "de maior diâmetro que exigem pelo menos dois operadores treinados."
    ),
    (
        "Hidrantes e Mangotinhos", "basico",
        "Segundo a NBR 13714, qual é a pressão mínima na saída do hidrante mais desfavorável hidraulicamente durante o uso simultâneo?",
        "0,5 mca", "5 mca", "10 mca", "20 mca", "C",
        "A NBR 13714 exige pressão mínima de 10 m.c.a (metros de coluna d'água) ≈ 1 kgf/cm² "
        "no ponto mais desfavorável (mais distante ou elevado), garantindo jato efetivo de combate."
    ),
    (
        "Hidrantes e Mangotinhos", "basico",
        "O reservatório de incêndio (reserva técnica) destinado ao sistema de hidrantes deve ser:",
        "Compartilhado com a reserva de água de consumo predial sem restrições",
        "Exclusivo para uso em emergência de incêndio, separado da reserva de consumo",
        "Localizado no subsolo para facilitar o bombeamento",
        "Dispensável quando o imóvel está conectado à rede pública de hidrantes",
        "B",
        "A reserva técnica de incêndio deve ser exclusiva (ou com válvula de separação que garanta "
        "sua disponibilidade), impedindo que o consumo predial normal comprometa o volume disponível "
        "para combate a incêndio."
    ),
    (
        "Hidrantes e Mangotinhos", "basico",
        "A distância máxima entre hidrantes de parede em um mesmo pavimento de uma edificação, segundo a NBR 13714, é determinada pela:",
        "Altura da edificação dividida pelo número de pavimentos",
        "Soma do comprimento da mangueira com o alcance do jato, garantindo cobertura de toda a área",
        "Área total do pavimento dividida por 200 m²",
        "Capacidade da bomba de incêndio instalada",
        "B",
        "O posicionamento dos hidrantes deve garantir que toda a área do pavimento seja coberta "
        "pela soma do comprimento da mangueira mais o alcance do jato d'água, sem pontos desguarnecidos."
    ),
    (
        "Hidrantes e Mangotinhos", "intermediario",
        "O que é a 'reserva de incêndio' exigida pela NBR 13714?",
        "Volume de CO₂ armazenado para uso em sprinklers",
        "Volume mínimo de água destinado exclusivamente ao combate a incêndio, calculado com base na vazão e tempo de operação",
        "Caixa de areia instalada próxima aos hidrantes",
        "Quantidade de extintores reserva em almoxarifado",
        "B",
        "A reserva técnica de incêndio é o volume de água calculado pela multiplicação da vazão total "
        "do sistema (L/min) pelo tempo mínimo de operação (min), variando conforme a classe da edificação."
    ),
    (
        "Hidrantes e Mangotinhos", "intermediario",
        "Qual é o diâmetro mínimo da mangueira utilizada em hidrantes Tipo 2 (edificações de médio e grande porte), segundo a NBR 13714?",
        "1 ½\" (38 mm)", "2\" (50 mm)", "2 ½\" (65 mm)", "3\" (80 mm)", "C",
        "Para hidrantes Tipo 2 (edificações de médio e grande porte), a NBR 13714 exige mangueiras "
        "de no mínimo 2½\" (65 mm) de diâmetro, garantindo maior vazão para combate eficaz."
    ),
    (
        "Hidrantes e Mangotinhos", "intermediario",
        "O espaço máximo de armazenamento de mangueiras no abrigo de hidrante deve garantir:",
        "Apenas o acondicionamento dobrado das mangueiras para reduzir volume",
        "Acesso rápido e desdobramento sem obstrução em situação de emergência",
        "Trancamento para evitar uso indevido por não autorizados",
        "Instalação somente em armários embutidos na parede",
        "B",
        "O abrigo de hidrante deve permitir retirada rápida e desdobramento imediato das mangueiras "
        "sem enroscar ou travar, pois qualquer obstrução em emergência pode custar vidas."
    ),
    (
        "Hidrantes e Mangotinhos", "avancado",
        "Para uma edificação de Classe 3 (alto risco), a NBR 13714 estabelece tempo mínimo de operação do sistema de hidrantes de:",
        "15 minutos", "30 minutos", "60 minutos", "120 minutos", "C",
        "Edificações de alto risco (Classe 3) requerem no mínimo 60 minutos de operação autônoma "
        "do sistema. Isso dimensiona a reserva técnica: vazão total (L/min) × 60 min."
    ),
    (
        "Hidrantes e Mangotinhos", "avancado",
        "Qual é o objetivo do registro de recalque (Siamese) instalado na fachada de edificações com sistema de hidrantes?",
        "Controlar a pressão interna da tubulação durante o uso normal",
        "Permitir que o caminhão-tanque dos bombeiros alimente o sistema hidráulico interno da edificação",
        "Realizar o teste de pressão anual da tubulação sem necessidade de entrar no edifício",
        "Conectar o sistema de hidrantes ao sistema de sprinklers",
        "B",
        "O registro de recalque (Siamese) é uma conexão externa na fachada que permite ao corpo de "
        "bombeiros bombear água de seu caminhão diretamente para a rede interna de hidrantes, "
        "essencial quando a reserva predial ou a bomba de incêndio falharem."
    ),
    (
        "Hidrantes e Mangotinhos", "avancado",
        "Qual norma regulamenta os chuveiros automáticos (sprinklers) que complementam os sistemas de hidrantes em edificações de alto risco?",
        "NBR 9077", "NBR 10897", "NBR 13714", "NBR 17240", "B",
        "A NBR 10897 regulamenta os sistemas de chuveiros automáticos (sprinklers) no Brasil. "
        "É a norma específica para projeto, instalação e manutenção desses sistemas, "
        "complementando a NBR 13714 nas edificações que exigem ambos os sistemas."
    ),
]
