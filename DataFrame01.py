
url = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2022/uf=BA/lote=1/part-00000-ecd4fc79-1113-4c73-9917-0f83aa9e0235.c000.csv'
dtypes = {
    "sintomas":"str",
    "profissionalSaude": "str",
    "racaCor": "str",
    "outrosSintomas": "str",
    "idade": "float",
    "sexo": "str",  #tipo de dados apropriado
}
arquivo = "/Users/Eduarda/OneDrive/Área de Trabalho/PIBITI-IFBA-CNPq-2023-2024/part-00000-7794e106-1591-454b-abb8-7840c03edf5e.c000.csv"

# df = pd.read_csv(url, dtype=dtypes, sep=';', on_bad_lines='skip')
# #print(df)
# #df = requests.get(url)

import tkinter as tk
from tkinter import ttk
import pandas as pd

# Carregue seu DataFrame aqui
#url = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2022/uf=BA/lote=1/part-00000-ecd4fc79-1113-4c73-9917-0f83aa9e0235.c000.csv'
df = pd.read_csv(arquivo, sep=';', dtype=dtypes, on_bad_lines='skip')

# Função para atualizar a tabela com base nos filtros
def atualizar_tabela():
    sintomas_selecionados = combo_sintomas.get()
    profissional_saude_selecionado = combo_profissional_saude.get()
    racaCor_selecionado = combo_racaCor.get()
    idade_selecionado = combo_idade.get()

    # Converter idade_selecionado para float (ou int, dependendo dos seus dados)
    idade_selecionado = float(idade_selecionado)

    # Aplicar os filtros ao DataFrame
    filtro_sintomas = df['sintomas'] == sintomas_selecionados
    filtro_profissional_saude = df['profissionalSaude'] == profissional_saude_selecionado
    filtro_racaCor = df['racaCor'] == racaCor_selecionado
    filtro_idade = df['idade'] == idade_selecionado

    resultados_filtrados = df[filtro_sintomas & filtro_profissional_saude & filtro_racaCor & filtro_idade]

    #print("Número de resultados encontrados:", len(resultados_filtrados))
    

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

# Função para limpar filtros e mostrar a tabela completa
def limpar_filtros():
    # Resetar valores dos ComboBoxes
    combo_sintomas.set("Selecione um sintoma")
    combo_profissional_saude.set("Selecione um profissional de saúde")
    combo_racaCor.set("Selecione uma Raça/Cor")
    combo_idade.set("Selecione uma Idade")
    
    # Limpar a tabela existente
    for i in tree.get_children():
        tree.delete(i)

    # Preencher a tabela com todos os dados
    for index, row in df.iterrows():
        tree.insert("", "end", values=(row['sintomas'], row['profissionalSaude'], row['racaCor'], row['idade']))

# Crie uma janela principal
root = tk.Tk()
root.title("Filtragem de Tabela")

# Divida os valores na coluna 'sintomas' com base nas vírgulas
df['sintomas'] = df['sintomas'].str.split(',')
df['profissionalSaude'] = df['profissionalSaude'].str.split(',')
df['racaCor'] = df['racaCor'].str.split(',')

# Use a função explode para criar várias linhas a partir de uma única linha
df = df.explode('sintomas')
df = df.explode('profissionalSaude')
df = df.explode('racaCor')

# Crie as ComboBox para seleção de filtros
#sintomas = df['sintomas'].values.tolist()
#combo_sintomas = ttk.Combobox(root, values=sintomas, state="readonly")
sintomas_unicos = set(df['sintomas'].values.tolist())
combo_sintomas = ttk.Combobox(root, values=list(sintomas_unicos), state="readonly")
combo_sintomas.set("Selecione um sintoma")
combo_sintomas.grid(row=0, column=0, sticky="e")

#profissionais_saude = df['profissionalSaude'].unique()
#combo_profissional_saude = ttk.Combobox(root, values=profissionais_saude, state="readonly")
profissional_saude_unicos = set(df['profissionalSaude'].values.tolist())
combo_profissional_saude = ttk.Combobox(root, values=list(profissional_saude_unicos), state="readonly")
combo_profissional_saude.set("Selecione um profissional de saúde")
combo_profissional_saude.grid(row=0, column=1, sticky="e")

# racaCor = df['racaCor'].unique()
# combo_racaCor = ttk.Combobox(root, values=racaCor, state="readonly")
racaCor_unicos = set(df['racaCor'].values.tolist())
combo_racaCor = ttk.Combobox(root, values=list(racaCor_unicos), state="readonly")
combo_racaCor.set("Selecione uma Raça/Cor")
combo_racaCor.grid(row=0, column=3, sticky="w")

# idade = df['idade'].unique()
# combo_idade = ttk.Combobox(root, values=idade, state="readonly")
idade_unicos = set(df['idade'].values.tolist())
combo_idade = ttk.Combobox(root, values=list(idade_unicos), state="readonly")
combo_idade.set("Selecione uma Idade")
combo_idade.grid(row=0, column=4, sticky="w")

# Botão para aplicar filtros
botao_filtrar = ttk.Button(root, text="Filtrar", command=atualizar_tabela)
botao_filtrar.grid(row=0, column=5, sticky="e")

# Botão para limpar filtros
botao_limpar = ttk.Button(root, text="Limpar Filtros", command=limpar_filtros)
botao_limpar.grid(row=0, column=6, sticky="e")

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

