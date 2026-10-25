# Prova de Seleção – Analista de Desenvolvimento I (Timpel)
Autora: Fabiana Gomes Diniz

Este projeto lê as titulações de PEEP de um arquivo JSON, identifica a PEEP mais adequada de cada paciente (a PEEP imediatamente anterior ao cruzamento entre as curvas de hiperdistensão e colapso) e gera um gráfico PNG por paciente.

## Ambiente utilizado
Windows;
Visual Studio Code 1.100.3;
Python 3.10.16.

## Respostas

**a)	O que a sua função deve retornar se as curvas de hiperdistensão e colapso nunca se cruzarem? Por quê?**

A função de identificação da PEEP ideal retorna um array vazio. A função gera o gráfico, no entanto, não traça a linha correspondente a PEEP ótima e gera um alerta visual quanto ao não cruzamento das curvas.

**b)	E se as curvas se cruzarem mais de uma vez**

A função de identificação da PEEP ideal retorna um array com mais de um valor. A função gera o gráfico, no entanto, não traça a linha correspondente a PEEP ótima e gera um alerta visual quanto ao cruzamento múltiplo das curvas.

**c) Que outros problemas nos dados poderiam afetar o resultado (por exemplo, valores ausentes, passos fora de ordem ou valores fora do intervalo de 0 a 100%)? Como o seu código lida com eles?**

Além dos problemas citados, poderia haver curvas idênticas; que se tocam, mas não se cruzam; com intersecção no primeiro ou no último passo; com valores iguais a 0% ou a 100% em todos os passos; entre outros. Quando possível, o gráfico é gerado com um aviso visual e sem a identificação da PEEP ótima; quando a inconsistência no dado impossibilita a criação do gráfico, é gerado um erro e o código é interrompido. 
