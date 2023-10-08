
url = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2022/uf=BA/lote=1/part-00000-ecd4fc79-1113-4c73-9917-0f83aa9e0235.c000.csv'

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

df = pd.read_csv(url, dtype=dtypes, sep=';', on_bad_lines='skip')
#print(df)

#Função para atualizar a tabela com base nos filtros
def atualizar_tabela():
    sintomas_selecionados = combo_sintomas.get()
    profissional_saude_selecionado = combo_profissional_saude.get()
    racaCor_selecionado = combo_racaCor.get()
    idade_selecionado = combo_idade.get()

    # Aplicar os filtros ao DataFrame
    filtro_sintomas = df['sintomas'] == sintomas_selecionados
    filtro_profissional_saude = df['profissionalSaude'] == profissional_saude_selecionado
    filtro_racaCor = df['racaCor'] == racaCor_selecionado
    filtro_idade = df['idade'] == idade_selecionado
    resultados_filtrados = df[filtro_sintomas & filtro_profissional_saude & filtro_racaCor & filtro_idade]

    # Limpar a tabela existente
    for i in tree.get_children():
        tree.delete(i)

    # Verificar se há resultados
    if resultados_filtrados.empty:
        tree.insert("", "end", values=("Nenhum resultado encontrado", "", "", ""))  # Inserir mensagem de nenhum resultado
    else:
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
combo_sintomas.grid(row=0, column=0, sticky="e")

profissionais_saude = df['profissionalSaude'].unique()
combo_profissional_saude = ttk.Combobox(root, values=profissionais_saude, state="readonly")
combo_profissional_saude.set("Selecione um profissional de saúde")
combo_profissional_saude.grid(row=0, column=1, sticky="e")

racaCor = df['racaCor'].unique()
combo_racaCor = ttk.Combobox(root, values=racaCor, state="readonly")
combo_racaCor.set("Selecione uma Raça/Cor")
combo_racaCor.grid(row=0, column=3, sticky="w")

idade = df['idade'].unique()
combo_idade = ttk.Combobox(root, values=idade, state="readonly")
combo_idade.set("Selecione uma Idade")
combo_idade.grid(row=0, column=4, sticky="w")

# Botão para aplicar filtros
botao_filtrar = ttk.Button(root, text="Filtrar", command=atualizar_tabela)
botao_filtrar.grid(row=0, column=4)

# Crie uma tabela para exibir os resultados
columns = ("Sintomas", "Profissional de Saúde", "Raça/Cor", "Idade")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=1, column=0, columnspan=5)

# Inicialize a tabela com todos os dados
for index, row in df.iterrows():
    tree.insert("", "end", values=(row['sintomas'], row['profissionalSaude'], row['racaCor'], row['idade']))

root.mainloop()