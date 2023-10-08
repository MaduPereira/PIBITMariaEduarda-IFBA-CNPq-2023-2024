
#url = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2022/uf=BA/lote=1/part-00000-7794e106-1591-454b-abb8-7840c03edf5e.c000.csv'

#df = requests.get(url)

import tkinter as tk
from tkinter import ttk
import pandas as pd

# Carregue seu DataFrame aqui
# ...
dtypes = {
    "sintomas":"str",
    "profissionalSaude": "str",
    "racaCor": "str",
    "outrosSintomas": "str",
    "idade": "float",
    "sexo": "str",  # Ou o tipo de dados apropriado
    # Adicione outras colunas aqui se necessário
}
arquivo = "/Users/Eduarda/OneDrive/Área de Trabalho/PIBITI-IFBA-CNPq-2023-2024/part-00000-7794e106-1591-454b-abb8-7840c03edf5e.c000.csv"

df = pd.read_csv(arquivo, dtype=dtypes, sep=';', on_bad_lines='skip')

# Função para atualizar a tabela com base nos filtros
def atualizar_tabela():
    sintomas_selecionados = combo_sintomas.get()
    profissional_saude_selecionado = combo_profissional_saude.get()

    # Aplicar os filtros ao DataFrame
    filtro_sintomas = df['sintomas'] == sintomas_selecionados
    filtro_profissional_saude = df['profissionalSaude'] == profissional_saude_selecionado
    resultados_filtrados = df[filtro_sintomas & filtro_profissional_saude]

    # Limpar a tabela existente
    for i in tree.get_children():
        tree.delete(i)

    # Preencher a tabela com os resultados filtrados
    for index, row in resultados_filtrados.iterrows():
        tree.insert("", "end", values=(row['sintomas'], row['profissionalSaude'], row['racaCor'], row['idade']))

# Crie uma janela principal
root = tk.Tk()
root.title("Filtragem de Tabela")

# Crie as ComboBox para seleção de filtros
sintomas = df['sintomas'].unique()
combo_sintomas = ttk.Combobox(root, values=sintomas, state="readonly")
combo_sintomas.set("Selecione um sintoma")
combo_sintomas.pack()

profissionais_saude = df['profissionalSaude'].unique()
combo_profissional_saude = ttk.Combobox(root, values=profissionais_saude, state="readonly")
combo_profissional_saude.set("Selecione um profissional de saúde")
combo_profissional_saude.pack()

# Botão para aplicar filtros
botao_filtrar = ttk.Button(root, text="Filtrar", command=atualizar_tabela)
botao_filtrar.pack()

# Crie uma tabela para exibir os resultados
columns = ("Sintomas", "Profissional de Saúde", "Raça/Cor", "Idade")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack()

# Inicialize a tabela com todos os dados
for index, row in df.iterrows():
    tree.insert("", "end", values=(row['sintomas'], row['profissionalSaude'], row['racaCor'], row['idade']))

root.mainloop()