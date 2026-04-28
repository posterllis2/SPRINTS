import time

def executar_simulador():
    historico_geral = []

    while True:
        print("--- Boas-Vindas ao REECHARGE (by GoodWe) ---")

        # ENTRADA DE DADOS E VALIDAÇÃO
        while True:
            try:
                capacidade_bateria = float(input("\nCapacidade total da bateria (kWh): "))
                if capacidade_bateria <= 0:
                    print("Erro! A capacidade deve ser maior que zero.")
                    continue
                break
            except ValueError:
                print("Erro! Digite um valor numérico válido.")

        # TIPO DE TARIFAÇÃO
        while True:
            print("\nTipos de Tarifa:")
            print("[1] Residencial")
            print("[2] Comercial")

            tipo_tarifa = input("Escolha o tipo de tarifa: ").strip()

            if tipo_tarifa == "1":
                valor_kwh = 0.64
                categoria = "Residencial"
                break
            elif tipo_tarifa == "2":
                valor_kwh = 0.80
                categoria = "Comercial"
                break
            else:
                print("Erro! A tarifa selecionada não é válida.")

        # SESSÃO DE RECARGA
        energia_recarregada = 0.0
        percentual_atual = 0
        print(f"\nIniciando sessão de recarga {categoria}...")
        time.sleep(0.05)

        # PROGRESSO DE RECARGA
        while percentual_atual <= 100:
            energia_recarregada = (percentual_atual / 100) * capacidade_bateria
            print(f"Progresso: {percentual_atual}% | Energia: {energia_recarregada:.2f} kWh", end="\r")
            time.sleep(0.05)
            percentual_atual += 10

        # CALCULO DA TARIFA
        custo_total = energia_recarregada * valor_kwh

        # REGISTRO DA SESSÃO ATUAL
        sessao_registro = {
            "id": len(historico_geral) + 1,
            "tipo": categoria,
            "energia": energia_recarregada,
            "total": custo_total
        }
        historico_geral.append(sessao_registro)

        # RELATÓRIO INDIVIDUAL
        print("\n\n" + "=" * 40)
        print("      RELATÓRIO FINAL DA SESSÃO        ")
        print("=" * 40)
        print(f"Status:            CONCLUÍDO")
        print(f"Categoria:         {categoria}")
        print(f"Energia Consumida: {energia_recarregada:.2f} kWh")
        print(f"Valor por kWh:     R$ {valor_kwh:.2f}")
        print(f"Custo Total:       R$ {custo_total:.2f}")
        print("=" * 40)

        # CONTINUAR OU VER REGISTRO FINAL
        while True:
            continuar = input("\nDeseja realizar uma nova recarga? (s/n): ").lower().strip()

            if continuar in ['s', 'n']:
                break
            else:
                print("Erro! Por favor, responda apenas com 's' para SIM ou 'n' para NÃO.")

        if continuar == 'n':
            print("\nFinalizando sessões e gerando histórico...")
            time.sleep(0.05)
            break


    # EXIBIÇÃO DO REGISTRO DE DADOS
    if historico_geral:
        print("\n\n" + "=" * 60)
        print("              HISTÓRICO DE RECARGAS    ")
        print("=" * 60)
        for registro in historico_geral:
            print(f"Sessão #{registro['id']} | {registro['tipo']} | {registro['energia']:.2f} kWh | Total: R$ {registro['total']:.2f}")
        print("=" * 60)
        print("--- Sistema encerrado. Agradecemos por usar o REECHARGE (by GoodWe)! ---")

if __name__ == "__main__":
    executar_simulador()