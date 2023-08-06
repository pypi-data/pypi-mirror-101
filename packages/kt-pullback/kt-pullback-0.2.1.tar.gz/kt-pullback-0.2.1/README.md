# kt-pullback
Calcula os preços de retração de uma pernada no gráfico

## Pré-requisitos
Python instalado e disponível no terminal de comandos.  
  
## Instalação
```cmd
pip install kt-pullback
```
  
## Uso
```cmd
pb <PRECO_FINAL> <PRECO_INICIAL>
```
Onde:  
PRECO_FINAL é o preço final da pernada.  
PRECO_INICIAL é o preço inicial da pernada.  
Retorna, de cima para baixo, as retrações de 1/3, 1/2 e 2/3 da pernada.  
  
Exemplo:  
```cmd
pb 100.09 93.40
97.86
96.85
95.63
```
