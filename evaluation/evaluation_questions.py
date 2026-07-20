EVALUATION_DATA: list[dict[str, str]] = [
    {
        "question": "Qual é o objetivo principal da RDC 09/2015?",
        "ground_truth": (
            "O objetivo da RDC 09/2015 é definir os procedimentos e requisitos "
            "para a realização de ensaios clínicos com medicamentos no Brasil, "
            "incluindo a submissão do Dossiê de Desenvolvimento Clínico de "
            "Medicamento (DDCM). "
            "(Fonte: Art. 1º da RDC 09/2015)"
        )
    },
    {
        "question": "Quais etapas de desenvolvimento clínico exigem submissão de DDCM segundo a RDC 09/2015?",
        "ground_truth": (
            "Todos os ensaios clínicos que tenham parte do desenvolvimento no "
            "Brasil para fins de registro devem submeter um DDCM. Ensaios fase IV "
            "não exigem DDCM, exceto quando fornecem dados para registro ou "
            "renovação. (Fonte: Art. 2º e Art. 3º da RDC 09/2015)"
        )
    },

    # -------------------------------------------------------
    # Uncomment these AFTER your MVP runs correctly.
    # -------------------------------------------------------

    # {
    #     "question": "Quais documentos compõem uma Notificação de Ensaio Clínico segundo a RDC 09/2015?",
    #     "ground_truth": (
    #         "A Notificação deve conter: formulário preenchido, comprovante de GRU, "
    #         "protocolo do ensaio conforme BPC, registro na plataforma ICTRP/WHO "
    #         "ou equivalente, e parecer do CEP do primeiro centro. "
    #         "(Fonte: Art. 3º, inciso IV, alíneas a–e, RDC 09/2015)"
    #     )
    # },

    # {
    #     "question": "O que caracteriza uma Modificação Substancial no DDCM segundo a RDC 09/2015?",
    #     "ground_truth": (
    #         "Uma Modificação Substancial é qualquer mudança que possa impactar a "
    #         "segurança dos participantes, a integridade dos dados ou a condução do estudo. "
    #         "(Fonte: Art. 42 da RDC 09/2015)"
    #     )
    # },

    # {
    #     "question": "Onde a RDC 406/2020 define as condições climáticas para estudos de estabilidade?",
    #     "ground_truth": (
    #         "As condições climáticas fazem parte da zona climática IVb, "
    #         "definidas pela RDC 406/2020 como o ambiente padrão brasileiro para "
    #         "estudos de estabilidade. (Referência: RDC 406/2020)"
    #     )
    # },

    # {
    #     "question": "Quais são os requisitos básicos de registro de produtos biológicos na RDC 55/2010?",
    #     "ground_truth": (
    #         "A RDC 55/2010 exige dados de qualidade, segurança e eficácia, incluindo "
    #         "caracterização, estudos não clínicos, estudos clínicos, comparabilidade e "
    #         "informações de fabricação. "
    #         "(Fonte: RDC 55/2010, Seções de Registro e Pós-Registro)"
    #     )
    # },

    # {
    #     "question": "Quais produtos se enquadram na Classificação de Risco II segundo a RDC 751/2022?",
    #     "ground_truth": (
    #         "A Classificação de Risco II inclui dispositivos médicos de risco moderado, "
    #         "conforme regras específicas definidas na RDC 751/2022. "
    #     )
    # },

    # {
    #     "question": "A IN 338/2024 altera procedimentos de ensaios clínicos no Brasil?",
    #     "ground_truth": (
    #         "Sim, a IN 338/2024 atualiza procedimentos relacionados à condução e "
    #         "supervisão de pesquisas clínicas no país. (Fonte: IN 338/2024)"
    #     )
    # },
]
