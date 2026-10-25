# Prova de Seleção – Analista de Desenvolvimento I (Timpel)
Autora: Fabiana Gomes Diniz

Este projeto lê as titulações de PEEP de um arquivo JSON, identifica a PEEP mais adequada de cada paciente (a PEEP imediatamente anterior ao cruzamento entre as curvas de hiperdistensão e colapso) e gera um gráfico PNG por paciente.

## Ambiente utilizado
Windows;

Visual Studio Code 1.100.3;

Python 3.10.16.

## Funções
- data_validation_and_opt_PEEP_identification

  Validates data and identifies the ideal PEEP value given the collapse and hyperdistension values of the respiratory system.

    Args:
  
        hyperdistension (pandas Series): Hyperdistension values.
        PEEP (pandas Series): PEEP values.
        collapse (pandas Series): Collapse values.

    Returns:
  
        opt_PEEP (array): Array with the possible optimal points found; if the number of points is different from 1, they will not be displayed on the graph.

- saves_opt_PEEP_graphs

  Plots collapse values, hyperdistension values and optimal PEEP as a function of PEEP. Saves the graphs in the 'opt_PEEP_plots' file.

    Args:
  
        patient_ID (str): Patient identification
        hyperdistension (pandas Series): Hyperdistension values.
        PEEP (pandas Series): PEEP values.
        collapse (pandas Series): Collapse values.
        opt_PEEP (array): Array with the possible optimal points found; 
        if the number of points is different from 1, they will not be displayed on the graph.
        
    Returns:
  
        None.

- peep_identification_and_plot

  Loads data from the.json file containing the collapse and hyperdistension values of the respiratory system;
  validates data;
  identifies the ideal PEEP value;
  plots collapse values, hyperdistension values and optimal PEEP as a function of PEEP; and
  saves the graphs in the 'opt_PEEP_plots' file.

    Args:
  
        json_path (str): Path to the .json file containing the data.

    Returns:
  
        None.

## Respostas

### Parte 2 – Verificação

**A PEEP indicada em cada gráfico será utilizada no relatório final do protocolo de pesquisa clínica. Por isso, os pesquisadores precisam ter confiança de que ela está correta.**
**a)	Implemente a identificação da PEEP mais adequada como uma função separada da geração dos gráficos.**

O código foi organizado em três funções, com responsabilidades distintas: a primeira realiza a validação dos dados e a identificação da PEEP ótima; a segunda gera os gráficos individuais, incluindo os alertas pertinentes; e a terceira é responsável pelo carregamento dos dados e pela chamada das duas funções anteriores.

A função de validação verifica a dimensão dos dados, a presença de valores ausentes ou infinitos, a ordem decrescente das medidas de PEEP e a existência de uma única titulação. Já a função de geração dos gráficos verifica condições que podem comprometer a interpretação dos resultados, como valores de hiperdistensão ou colapso persistentemente iguais a 0% ou 100%, valores fora do intervalo de 0% a 100% e a ausência ou multiplicidade de intersecções entre as curvas.

Optei por apresentar essas últimas inconsistências como alertas nos gráficos, em vez de interromper a execução do código, para permitir a confirmação da inconsistência visualmente. Apesar de todos os gráficos serem gerados, por meio deles é facilmente identificável algum erro, pois a PEEP ótima só é identificada nos gráficos após validação e são escritos alertas no gráfico quando pertinente.

**b)	Escreva testes automatizados que demonstrem que essa função está correta, incluindo casos limite. Para cada teste, explique brevemente o que ele verifica e por quê.**

Para validar o funcionamento correto do código, utilizei o Claude como ferramenta de apoio para elaborar um arquivo JSON com conjuntos de dados que representam diferentes situações esperadas e casos limite. As verificações foram feitas considerando os seguintes casos:

1)	Dados válidos;
   
Verifica o perfeito funcionamento do código quando os dados fornecidos não estão com nenhuma inconsistência.

2)	Hiperdistensão igual a 0% em todos os casos e não cruzamento das curvas;
   
Verifica a emissão de aviso no gráfico quando um dos dados permanece em 0% (possível erro de medição) e quando não há cruzamento das curvas e, portanto, não é possível identificar a PEEP ótima.

3)	Colapso igual a 0% em todos os casos e não cruzamento das curvas;
   
Verifica a emissão de aviso no gráfico quando um dos dados permanece em 0% (possível erro de medição) e quando não há cruzamento das curvas e, portanto, não é possível identificar a PEEP ótima.

4)	Hiperdistensão igual a 100% em todos os casos e não cruzamento das curvas;

Verifica a emissão de aviso no gráfico quando um dos dados permanece em 100% (possível erro de medição) e quando não há cruzamento das curvas e, portanto, não é possível identificar a PEEP ótima.

5)	Colapso igual a 100% em todos os casos e não cruzamento das curvas;
   
Verifica a emissão de aviso no gráfico quando um dos dados permanece em 100% (possível erro de medição) e quando não há cruzamento das curvas e, portanto, não é possível identificar a PEEP ótima.

6)	Hiperdistensão com valor maior que 100%;
   
Verifica a emissão de aviso no gráfico quando um dos dados ultrapassa 100% (dado inválido).

7)	Colapso com valor menor que 0%;
   
Verifica a emissão de aviso no gráfico quando um dos dados é menor que 0% (dado inválido).

8)	Curvas sem intersecção;

Verifica a emissão de aviso no gráfico quando não há intersecção das curvas e, portanto, não é possível identificar a PEEP ótima.

9)	Curvas com mais de uma intersecção;
    
Verifica a emissão de aviso no gráfico quando há mais de uma intersecção das curvas e, portanto, não é possível identificar a PEEP ótima.

10)	Hiperdistensão igual a 0% em todos os casos, colapso maior que 100% e sem intersecção;
    
Verifica a emissão de mais de um aviso no gráfico.

11)	Intersecção exatamente no valor de PEEP;
    
Verifica se a melhor PEEP identificada é a anterior à intersecção.

12)	Intersecção no primeiro passo;
    
Verifica a emissão de aviso no gráfico quando a intersecção ocorre no primeiro passo (não é possível identificar a PEEP ótima, dado a ausência de PEEP anterior à intersecção).

13)	Intersecção no último passo;
    
Verifica se a melhor PEEP identificada é a anterior à intersecção.

14)	Curvas se tocam, mas não se cruzam;
    
Verifica se a melhor PEEP identificada é a anterior ao igualamento das curvas.

15)	Curvas idênticas;
    
Verifica a emissão de aviso no gráfico quando as curvas são idênticas (mais de uma intersecção);

16)	PEEP em ordem crescente;
    
Verifica o interrompimento do código quando as medidas de PEEP são crescentes;

17)	PEEP com valor repetido;
    
Verifica o interrompimento do código quando as medidas de PEEP estão repetidas;

18)	Valor nulo/NaN;
    
Verifica o interrompimento do código quando há um valor nulo ou NaN entre os dados;

19)	Valor infinito;
    
Verifica o interrompimento do código quando há um valor infinito entre os dados;

20)	Valor ausente;
    
Verifica o interrompimento do código quando há um valor ausente entre os dados;

21)	Apenas um passo.
    
Verifica o interrompimento do código quando há apenas uma titulação nos dados.

**c)	Descreva como você verificaria que os gráficos gerados estão corretos antes de serem inseridos no relatório.**

Com a implementação de testes de validação no código, é possível filtrar os erros mais comuns nos dados. Entretanto, a validação humana posterior à geração dos gráficos também é válida. Portanto, antes de incluir os gráficos no relatório, eu verificaria a consistência entre os resultados numéricos e sua representação gráfica, conferindo se os valores de PEEP estão na ordem correta, se as curvas correspondem aos dados originais e se a PEEP indicada no gráfico coincide com o resultado calculado pelo algoritmo. Também inspecionaria os gráficos em busca de problemas de apresentação que pudessem comprometer sua interpretação. Caso a quantidade de dados fosse muito grande para validação humana, escolheria uma fração deles aleatoriamente para fazer uma checagem.

### Parte 3 – Comportamento do algoritmo

**Responda de forma breve, no README:**

**a)	O que a sua função deve retornar se as curvas de hiperdistensão e colapso nunca se cruzarem? Por quê?**

A função de identificação da PEEP ótima retorna um array vazio, indicando que não foi encontrada uma intersecção entre as curvas. A função gera o gráfico, no entanto, não traça a linha correspondente a PEEP ótima e gera um alerta visual quanto ao não cruzamento das curvas.

**b)	E se as curvas se cruzarem mais de uma vez**

A função retorna um array com os valores de PEEP correspondentes às múltiplas intersecções. Como não é possível determinar uma PEEP ótima única, a função gera o gráfico, no entanto, não traça a linha correspondente a PEEP ótima e gera um alerta visual quanto ao cruzamento múltiplo das curvas.

**c) Que outros problemas nos dados poderiam afetar o resultado (por exemplo, valores ausentes, passos fora de ordem ou valores fora do intervalo de 0 a 100%)? Como o seu código lida com eles?**

Além dos problemas citados, poderia haver curvas idênticas; que se tocam, mas não se cruzam; com intersecção no primeiro ou no último passo; com valores iguais a 0% ou a 100% em todos os passos; entre outros. Quando possível, o gráfico é gerado com um aviso visual e sem a identificação da PEEP ótima; quando a inconsistência no dado impossibilita a criação do gráfico, é gerado um erro e o código é interrompido. 
