import flet as ft
import psycopg2

# ==========================
# FUNÇÕES DE BANCO DE DADOS
# ==========================

def inserir_funcionario(id, nome, cargo, nacionalidade, cpf, salario):
    try:
        with psycopg2.connect(
                host="127.0.0.1",
                user="seu_usuario",
                password="sua_senha",
                database="seu_banco"
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM funcionarios WHERE id = %s", (id,))
                if cursor.fetchone():
                    return False, "Código já existe! Escolha outro ID."

                cursor.execute(
                    "INSERT INTO funcionarios (id, nome, cargo, nacionalidade, cpf, salario) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, nome, cargo, nacionalidade, cpf, salario)
                )
        return True, "Funcionário inserido com sucesso."
    except Exception as e:
        return False, f"Erro ao inserir: {e}"


def excluir_funcionario(id):
    try:
        with psycopg2.connect(
                host="127.0.0.1",
                user="seu_usuario",
                password="sua_senha",
                database="seu_banco"
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("SELECT nome FROM funcionarios WHERE id = %s", (id,))
                if cursor.fetchone() is None:
                    return False, "Funcionário não encontrado."

                cursor.execute("DELETE FROM funcionarios WHERE id = %s", (id,))
        return True, "Funcionário excluído com sucesso."
    except Exception as e:
        return False, f"Erro ao excluir: {e}"


def atualizar_funcionario(id, campo, novo_valor):
    try:
        campos = {
            "nome": "nome",
            "cargo": "cargo",
            "nacionalidade": "nacionalidade",
            "cpf": "cpf",
            "salario": "salario"
        }

        if campo not in campos:
            return False, "Campo inválido."

        with psycopg2.connect(
                host="127.0.0.1",
                user="seu_usuario",
                password="sua_senha",
                database="seu_banco"
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(
                    f"UPDATE funcionarios SET {campo} = %s WHERE id = %s",
                    (novo_valor, id)
                )
                if cursor.rowcount == 0:
                    return False, "Funcionário não encontrado."

        return True, f"{campo.capitalize()} atualizado com sucesso."
    except Exception as e:
        return False, f"Erro ao atualizar: {e}"


def listar_funcionarios():
    try:
        with psycopg2.connect(
                host="127.0.0.1",
                user="seu_usuario",
                password="sua_senha",
                database="seu_banco"
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM funcionarios ORDER BY id")
                return cursor.fetchall()
    except Exception as e:
        return []


# ==========================
# INTERFACE FLET
# ==========================
def main(page: ft.Page):
    page.title = "Sistema de Funcionários"
    page.window_width = 800
    page.window_height = 600
    page.window_icon = "machine_learning.ico"
    page.scroll = "auto"

    status = ft.Text("", size=14, color="#008000")

    id_input = ft.TextField(label="ID")
    nome_input = ft.TextField(label="Nome")
    cargo_input = ft.TextField(label="Cargo")
    nacionalidade_input = ft.TextField(label="Nacionalidade")
    cpf_input = ft.TextField(label="CPF")
    salario_input = ft.TextField(label="Salário", hint_text="0,00", keyboard_type=ft.KeyboardType.NUMBER)

    excluir_id_input = ft.TextField(label="ID do Funcionário a Excluir")
    atualizar_id_input = ft.TextField(label="ID do Funcionário a Atualizar")

    campo_dropdown = ft.Dropdown(
        label="Campo",
        options=[
            ft.dropdown.Option("", "Selecione um campo"),
            ft.dropdown.Option("nome"),
            ft.dropdown.Option("cargo"),
            ft.dropdown.Option("nacionalidade"),
            ft.dropdown.Option("cpf"),
            ft.dropdown.Option("salario"),
        ],
        value=""
    )

    novo_valor_input = ft.TextField(label="Novo Valor")
    lista = ft.Column()

    def format_cpf(text: str) -> str:
        digits = ''.join(c for c in text if c.isdigit())[:11]
        res = ""
        for i, d in enumerate(digits):
            if i in [3, 6]: res += "."
            if i == 9: res += "-"
            res += d
        return res

    def format_salary(text: str) -> str:
        digits = ''.join(c for c in text if c.isdigit())
        if not digits:
            return ""
        valor_centavos = int(digits)
        reais = valor_centavos // 100
        centavos = valor_centavos % 100
        reais_formatado = f'{reais:,}'.replace(',', '.')
        centavos_formatado = f'{centavos:02d}'
        return f"{reais_formatado},{centavos_formatado}"

    def show_status(msg, success=True):
        status.value = msg
        status.color = "#008000" if success else "#FF0000"
        page.update()

    def atualizar_lista():
        funcionarios = listar_funcionarios()
        lista.controls.clear()
        for f in funcionarios:
            salario_formatado = f"{f[5]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            lista.controls.append(ft.Text(
                f"ID: {f[0]} | Nome: {f[1]} | Cargo: {f[2]} | Nacionalidade: {f[3]} | CPF: {f[4]} | Salário: R$ {salario_formatado}"
            ))
        page.update()

    def is_int(value):
        return value.strip().isdigit()

    def reset_borders(*fields):
        for f in fields:
            f.border_color = None

    def on_cpf_change(e):
        new = format_cpf(cpf_input.value)
        cpf_input.value = new
        cpf_input.selection_start = cpf_input.selection_end = len(new)
        page.update()

    def on_salario_change(e):
        new = format_salary(salario_input.value)
        salario_input.value = new
        salario_input.selection_start = salario_input.selection_end = len(new)
        page.update()

    cpf_input.on_change = on_cpf_change
    salario_input.on_change = on_salario_change

    def on_novo_valor_change(e):
        campo = campo_dropdown.value
        if campo == "cpf":
            novo_valor_input.value = format_cpf(novo_valor_input.value)
        elif campo == "salario":
            novo_valor_input.value = format_salary(novo_valor_input.value)
        novo_valor_input.selection_start = novo_valor_input.selection_end = len(novo_valor_input.value)
        page.update()

    novo_valor_input.on_change = on_novo_valor_change

    def on_inserir(e):
        reset_borders(id_input, nome_input, cargo_input, nacionalidade_input, cpf_input, salario_input)
        id_val = id_input.value.strip()
        nome = nome_input.value.strip()
        cargo = cargo_input.value.strip()
        nacionalidade = nacionalidade_input.value.strip()
        cpf = cpf_input.value.strip()
        salario_val = salario_input.value.strip()

        invalid_fields = []
        if not id_val: id_input.border_color = "#FF0000"; invalid_fields.append("ID")
        if not nome: nome_input.border_color = "#FF0000"; invalid_fields.append("Nome")
        if not cargo: cargo_input.border_color = "#FF0000"; invalid_fields.append("Cargo")
        if not nacionalidade: nacionalidade_input.border_color = "#FF0000"; invalid_fields.append("Nacionalidade")
        if not cpf: cpf_input.border_color = "#FF0000"; invalid_fields.append("CPF")
        if not salario_val: salario_input.border_color = "#FF0000"; invalid_fields.append("Salário")

        if invalid_fields:
            show_status(f"Preencha todos os campos: {', '.join(invalid_fields)}.", False)
            page.update()
            return

        if not is_int(id_val):
            id_input.border_color = "#FF0000"
            show_status("ID deve ser um número inteiro.", False)
            page.update()
            return

        try:
            salario_float = float(salario_val.replace('.', '').replace(',', '.'))
        except ValueError:
            salario_input.border_color = "#FF0000"
            show_status("Salário deve ser um número válido.", False)
            page.update()
            return

        try:
            success, msg = inserir_funcionario(int(id_val), nome, cargo, nacionalidade, cpf, salario_float)
            if success:
                atualizar_lista()
                id_input.value = nome_input.value = cargo_input.value = ""
                nacionalidade_input.value = cpf_input.value = salario_input.value = ""
                reset_borders(id_input, nome_input, cargo_input, nacionalidade_input, cpf_input, salario_input)
                page.update()
            show_status(msg, success)
        except Exception as ex:
            show_status(f"Erro: {ex}", False)

    def on_excluir(e):
        excluir_id_input.border_color = None
        id_val = excluir_id_input.value.strip()
        if not id_val:
            excluir_id_input.border_color = "#FF0000"
            show_status("Informe o ID para exclusão.", False)
            page.update()
            return
        if not is_int(id_val):
            excluir_id_input.border_color = "#FF0000"
            show_status("ID deve ser um número inteiro.", False)
            page.update()
            return

        try:
            success, msg = excluir_funcionario(int(id_val))
            if success:
                atualizar_lista()
                excluir_id_input.value = ""
                page.update()
            show_status(msg, success)
        except Exception as ex:
            show_status(f"Erro: {ex}", False)

    def on_atualizar(e):
        reset_borders(atualizar_id_input, novo_valor_input)
        campo_dropdown.border_color = None

        id_val = atualizar_id_input.value.strip()
        campo = campo_dropdown.value
        novo_valor = novo_valor_input.value.strip()

        invalid_fields = []
        if not id_val:
            atualizar_id_input.border_color = "#FF0000"
            invalid_fields.append("ID")
        if not campo:
            campo_dropdown.border_color = "#FF0000"
            invalid_fields.append("Campo")
        if not novo_valor:
            novo_valor_input.border_color = "#FF0000"
            invalid_fields.append("Novo Valor")

        if invalid_fields:
            show_status(f"Preencha todos os campos: {', '.join(invalid_fields)}.", False)
            page.update()
            return

        if not is_int(id_val):
            atualizar_id_input.border_color = "#FF0000"
            show_status("ID deve ser um número inteiro.", False)
            page.update()
            return

        if campo == "salario":
            try:
                novo_valor_float = float(novo_valor.replace('.', '').replace(',', '.'))
                novo_valor = novo_valor_float
            except ValueError:
                novo_valor_input.border_color = "#FF0000"
                show_status("Salário deve ser um número válido.", False)
                page.update()
                return

        try:
            success, msg = atualizar_funcionario(int(id_val), campo, novo_valor)
            show_status(msg, success)
            if success:
                atualizar_lista()

            atualizar_id_input.value = ""
            novo_valor_input.value = ""
            campo_dropdown.value = ""
            campo_dropdown.update()
            reset_borders(atualizar_id_input, novo_valor_input, campo_dropdown)
            page.update()
        except Exception as ex:
            show_status(f"Erro: {ex}", False)

    page.add(ft.Text("Sistema de Gestão de Funcionários", size=20, weight=ft.FontWeight.BOLD))
    page.add(ft.Divider())

    page.add(ft.Text("Inserir Funcionário", weight=ft.FontWeight.BOLD))
    page.add(ft.Row([id_input, nome_input]))
    page.add(ft.Row([cargo_input, nacionalidade_input]))
    page.add(ft.Row([cpf_input, salario_input]))
    page.add(ft.Row([ft.ElevatedButton("Inserir Funcionário", on_click=on_inserir)]))

    page.add(ft.Divider())
    page.add(ft.Text("Excluir Funcionário", weight=ft.FontWeight.BOLD))
    page.add(excluir_id_input)
    page.add(ft.Row([ft.ElevatedButton("Excluir Funcionário", on_click=on_excluir)]))

    page.add(ft.Divider())
    page.add(ft.Text("Atualizar Funcionário", weight=ft.FontWeight.BOLD))
    page.add(ft.Row([atualizar_id_input, campo_dropdown, novo_valor_input]))
    page.add(ft.Row([ft.ElevatedButton("Atualizar Funcionário", on_click=on_atualizar)]))

    page.add(ft.Divider())
    page.add(ft.Text("Funcionários Cadastrados:", weight=ft.FontWeight.BOLD))
    page.add(lista)

    page.add(ft.Divider())
    page.add(status)

    atualizar_lista()


if __name__ == "__main__":
    ft.app(target=main)
