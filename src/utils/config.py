
MENU_PRINCIPAL = """\n========== SISTEMA DE LOCAÇÃO DE VEÍCULOS ==========\n1 - Relatórios\n2 - Inserir registros\n3 - Atualizar registros\n4 - Remover registros\n5 - Sair\n"""

MENU_RELATORIOS = """\n==================== RELATÓRIOS ====================\n1 - Clientes\n2 - Locadoras\n3 - Categorias\n4 - Veículos\n5 - Funcionários\n6 - Aluguéis\n7 - Pagamentos\n8 - Faturamento por categoria\n0 - Voltar ao menu principal\n"""

MENU_ENTIDADES = """\n==================== ENTIDADES =====================\n1 - Clientes\n2 - Locadoras\n3 - Categorias\n4 - Veículos\n5 - Funcionários\n6 - Aluguéis (cadastro/status/devolução)\n7 - Pagamentos\n0 - Voltar ao menu principal\n"""

QUERY_COUNT = "SELECT COUNT(*) AS total FROM {tabela}"


def clear_console(wait_time: float = 0.0) -> None:
    """Limpa o terminal, funcionando tanto no Windows quanto no Linux/macOS.

    Args:
        wait_time: segundos opcionais de espera antes de limpar a tela.
    """
    import os
    from time import sleep

    if wait_time > 0:
        sleep(wait_time)
    os.system("cls" if os.name == "nt" else "clear")
