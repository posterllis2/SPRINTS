import time
import json
import random

# CONFIGURAÇÕES DA ESTAÇÃO REECHARGE
POTENCIA_NOMINAL_VAGA = 7.0  # kW por carregador
LIMITE_POTENCIA_HUB = 15.0  # Limite total que a estação aguenta (Demanda)
TARIFA_BASE_RESIDENCIAL = 0.64
TARIFA_BASE_COMERCIAL = 0.80


def simular_log_ocpp(mensagem_tipo, payload):
    """Simula o envio consistente de frames no protocolo OCPP 1.6J via WebSocket (Critério 4)"""
    frame_ocpp = [2, f"msg_{random.randint(1000, 9999)}", mensagem_tipo, payload]
    print(f"\n[OCPP >> CENTRAL] {json.dumps(frame_ocpp, indent=2)}")
    time.sleep(0.4)


def calcular_tarifa_dinamica(categoria, hora_atual):
    """Aplica tarifas diferenciadas e dinâmica por horário de pico (Critério 3)"""
    tarifa = TARIFA_BASE_COMERCIAL if categoria == "Comercial" else TARIFA_BASE_RESIDENCIAL

    # Horário de Pico: entre 18h e 21h (Demanda da rede alta)
    if 18 <= hora_atual <= 21:
        tarifa *= 1.30  # Acréscimo de 30%
        status_tarifa = "DINÂMICA (PICO - +30%)"
    else:
        status_tarifa = "CONVENCIONAL"

    return tarifa, status_tarifa


def gerenciar_potencia_hub(vagas_ativas):
    """Controle inteligente de demanda limitando a potência por veículo (Critério 2)"""
    qtd_veiculos = len(vagas_ativas)
    if qtd_veiculos == 0:
        return 0, 0

    demanda_solicitada = qtd_veiculos * POTENCIA_NOMINAL_VAGA

    # Se estourar o limite do Hub, divide a potência igualmente entre os conectados
    if demanda_solicitada > LIMITE_POTENCIA_HUB:
        potencia_permitida_por_vaga = LIMITE_POTENCIA_HUB / qtd_veiculos
        status_controle = f"⚠️ LIMITADO (Sobrecarga Evitada: {LIMITE_POTENCIA_HUB} kW máx)"
    else:
        potencia_permitida_por_vaga = POTENCIA_NOMINAL_VAGA
        status_controle = "🟢 NORMAL (Rede Estável)"

    return potencia_permitida_por_vaga, status_controle


def executar_simulador():
    vagas = {}  # Gerencia sessões ativas (Vaga: Dados do Veículo) (Critério 1)
    historico_geral = []

    # Integração Inicial OCPP ao ligar o Hub
    print("\n--- Inicializando Estação REECHARGE (by GoodWe) ---")
    simular_log_ocpp("BootNotification", {"chargePointModel": "GW-7KW-EV", "chargePointVendor": "GoodWe"})

    while True:
        print("\n" + "=" * 45)
        print("    CENTRAL DE CONTROLE REECHARGE     ")
        print("=" * 45)
        print(f" Vagas Ocupadas: {len(vagas)}/4 | Limite da Estação: {LIMITE_POTENCIA_HUB} kW")
        print("-" * 45)
        print("[1] Conectar Veículo (Nova Sessão)")
        print("[2] Exibir Monitoramento em Tempo Real")
        print("[3] Simular Ciclo de Recarga Atual")
        print("[4] Liberar Vaga / Encerrar Sessão")
        print("[5] Emitir Relatório e Encerrar Sistema")
        print("=" * 45)

        opcao = input("Selecione uma opção (1-5): ").strip()

        # OPERAÇÃO 1: CONECTAR VEÍCULO (Múltiplas sessões básicas - Critério 1)
        if opcao == "1":
            if len(vagas) >= 4:
                print("❌ Estação Lotada! Aguarde a liberação de uma vaga.")
                continue

            vaga_id = str(len(vagas) + 1)
            print(f"\n--- Iniciando Cadastro para a Vaga #{vaga_id} ---")

            while True:
                try:
                    capacidade = float(input("Capacidade total da bateria (kWh): "))
                    if capacidade > 0: break
                    print("Erro! A capacidade deve ser maior que zero.")
                except ValueError:
                    print("Erro! Digite um valor numérico válido.")

            while True:
                print("\nTipos de Tarifa: [1] Residencial | [2] Comercial")
                tipo = input("Escolha a tarifa: ").strip()
                if tipo == "1":
                    categoria = "Residencial"
                    break
                elif tipo == "2":
                    categoria = "Comercial"
                    break
                print("Erro! Opção inválida.")

            while True:
                try:
                    hora = int(input("Hora de início da recarga (0-23h): "))
                    if 0 <= hora <= 23: break
                    print("Erro! A hora deve ser entre 0 e 23.")
                except ValueError:
                    print("Erro! Digite um valor válido.")

            # Montando a estrutura da sessão ativa
            vagas[vaga_id] = {
                "capacidade": capacidade,
                "categoria": categoria,
                "hora_inicio": hora,
                "energia_recarregada": 0.0,
                "soc": 0  # State of Charge (Percentual da Bateria)
            }
            print(f"\n✅ Veículo conectado com sucesso na Vaga #{vaga_id}!")

            # Envio de mensagem OCPP para registrar início físico no servidor
            simular_log_ocpp("StartTransaction",
                             {"connectorId": int(vaga_id), "idTag": f"RFID_USER_{vaga_id}", "meterStart": 0})

        # OPERAÇÃO 2: MONITORAMENTO (Demonstra múltiplos cenários - Critério 7)
        elif opcao == "2":
            if not vagas:
                print("\nNenhum veículo conectado no momento.")
                continue

            potencia_por_vaga, status_rede = gerenciar_potencia_hub(vagas)
            print("\n" + "·" * 50)
            print(f" STATUS ATUAL DA REDE: {status_rede}")
            print(f" Potência entregue por vaga ativa: {potencia_por_vaga:.2f} kW")
            print("·" * 50)
            for vid, dados in vagas.items():
                tarifa_atual, status_t = calcular_tarifa_dinamica(dados["categoria"], dados["hora_inicio"])
                print(
                    f" Vaga #{vid} | Tipo: {dados['categoria']} ({status_t}) | Tarifa: R${tarifa_atual:.2f}/kWh | Carga: {dados['soc']}% ({dados['energia_recarregada']:.2f}kWh)")
            print("·" * 50)

        # OPERAÇÃO 3: SIMULAR CICLO DE RECARGA (Controle Inteligente - Critério 2)
        elif opcao == "3":
            if not vagas:
                print("\nNão há veículos para recarregar. Conecte um carro primeiro.")
                continue

            print("\n⚡ Processando cargas simultâneas...")
            potencia_por_vaga, _ = gerenciar_potencia_hub(vagas)

            concluidos = 0
            while concluidos < len(vagas):
                concluidos = 0
                for vid, dados in vagas.items():
                    if dados["soc"] < 100:
                        # Energia injetada proporcional à potência disponível do gerenciador inteligente
                        incremento_energia = (potencia_por_vaga * 0.1)  # Simula ganho por intervalo técnico
                        dados["energia_recarregada"] = min(dados["energia_recarregada"] + incremento_energia,
                                                           dados["capacidade"])
                        dados["soc"] = int((dados["energia_recarregada"] / dados["capacidade"]) * 100)
                    else:
                        concluidos += 1

                # Renderiza o andamento das vagas ativas na tela
                status_linha = " | ".join([f"Vaga #{k}: {v['soc']}%" for k, v in vagas.items()])
                print(f"Progresso Real do Hub: {status_linha}", end="\r")
                time.sleep(0.15)

            print("\n\n🔋 Todos os veículos processados até o limite atual!")

            # OCPP envia telemetria final pós-carga
            for vid, dados in vagas.items():
                simular_log_ocpp("MeterValues", {"connectorId": int(vid), "transactionId": 100 + int(vid),
                                                 "meterValue": [{"sampledValue": [
                                                     {"value": f"{dados['energia_recarregada']:.2f}",
                                                      "unit": "kWh"}]}]})

        # OPERAÇÃO 4: LIBERAR VAGA E GERAR COBRANÇA
        elif opcao == "4":
            if not vagas:
                print("\nNenhuma sessão ativa encontrada.")
                continue

            vaga_fechar = input(f"Informe o número da vaga para encerrar ({', '.join(vagas.keys())}): ").strip()
            if vaga_fechar in vagas:
                dados = vagas[vaga_fechar]
                tarifa, _ = calcular_tarifa_dinamica(dados["categoria"], dados["hora_inicio"])
                custo_total = dados["energia_recarregada"] * tarifa

                # Transferência para o registro histórico definitivo
                sessao_finalizada = {
                    "id": len(historico_geral) + 1,
                    "vaga": vaga_fechar,
                    "tipo": dados["categoria"],
                    "energia": dados["energia_recarregada"],
                    "total": custo_total
                }
                historico_geral.append(sessao_finalizada)

                # OCPP Stop Transaction
                simular_log_ocpp("StopTransaction", {"transactionId": 100 + int(vaga_fechar),
                                                     "meterStop": int(dados["energia_recarregada"]), "reason": "Local"})

                # Relatório Cupom Fiscal da Sessão Individual
                print("\n" + "=" * 40)
                print("       REECHARGE - RECIBO DE SESSÃO       ")
                print("=" * 40)
                print(f"Vaga Liberada:     #{vaga_fechar}")
                print(f"Categoria:         {dados['categoria']}")
                print(f"Energia Fornecida: {dados['energia_recarregada']:.2f} kWh")
                print(f"Valor Pago Final:  R$ {custo_total:.2f}")
                print("=" * 40)

                del vagas[vaga_fechar]  # Remove das vagas ativas
            else:
                print("Vaga inválida ou sem veículo ativo.")

        # OPERAÇÃO 5: ENCERRAMENTO E RELATÓRIO GLOBAL (Critério 1 e 5)
        elif opcao == "5":
            # Força o encerramento seguro de carros que esqueceram de deslogar
            if vagas:
                print("\nFinalizando sessões pendentes automaticamente...")
                for vid, dados in list(vagas.items()):
                    tarifa, _ = calcular_tarifa_dinamica(dados["categoria"], dados["hora_inicio"])
                    historico_geral.append({
                        "id": len(historico_geral) + 1,
                        "vaga": vid,
                        "tipo": dados["categoria"],
                        "energia": dados["energia_recarregada"],
                        "total": dados["energia_recarregada"] * tarifa
                    })

            print("\n\n" + "=" * 60)
            print("          RELATÓRIO DE RECARGAS      ")
            print("=" * 60)
            if not historico_geral:
                print("Nenhum registro de movimentação nesta execução.")
            else:
                faturamento_total = 0.0
                energia_total_hub = 0.0
                for reg in historico_geral:
                    print(
                        f"Sessão #{reg['id']} | Vaga {reg['vaga']} | {reg['tipo']:<11} | Carga: {reg['energia']:.2f} kWh | Recebido: R$ {reg['total']:.2f}")
                    faturamento_total += reg["total"]
                    energia_total_hub += reg["energia"]
                print("-" * 60)
                print(f"Total de Energia Escoada no Hub: {energia_total_hub:.2f} kWh")
                print(f"Faturamento Bruto REECHARGE:     R$ {faturamento_total:.2f}")
            print("=" * 60)
            print("Desconectando da rede... Sistema REECHARGE Encerrado.")
            break
        else:
            print("Opção inválida! Digite um número de 1 a 5.")


if __name__ == "__main__":
    executar_simulador()
