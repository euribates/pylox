## Capítulo 5: Representación de código

Ya habiendo convertido el código fuente 
en una secuencia de _tokens_, este capítulo
se ocupa de como organizar esa secuencia en una
estructura de datos mejor adaptada para las siguientes fases.

Una estructura de datos muy buena para esto es un **arbol**. En
este campo se suele hablar de _Abstract Syntax Tree_ (**AST**)
o Árbol de Sintaxis Abstracto. Este árbol es una representación
más o menos directa de la gramática, ya que cada nodo
se corresponde con una regla.

### Gramáticas libres de contexto

En el capítulo anterior, usamos un lenguaje regular (_Regular_ en el
mismo sentido que en las expresiones regulares). Aunque no usamos
expresiones regulares para detectar los tokens, podríamos haberlo hecho, 
ya que la gramática de los mismos es lo suficientemente sencilla.

Pero ahora tenemos que subir un poco en la jerarquía de las gramáticas
formales, porque necesitaremos una gramática capaz de manejar la recursividad.
No en el sentido de que el lenguaje de programación que estamos diseñando
sea recursivo, sino que la propia gramática es recursiva (Unas reglas hacen
referencia, ya sea directa o internamente, a si mismas).

La herramientas que necesitas ahora se llaman **Gramáticas Libres de Contexto**
(_Context Free Grammars_).

Una definición un poco laxa de una gramática formal sería que consta de un
conjunto de elementos, llamados **alfabeto**, que es a su vez un conjunto
de **letras**. La gramática se define entonces
como el conjunto (Posiblemente infinito) de secuencias del _alfabeto_ que
cumplen ciertas restricciones.

Is importante notar que, en los dos niveles que hemos visto por ahora, el
concepto de _alfabeto_ es distinto. Para el análisis léxico o _scanning_ del
capítulo 4, el alfabeto era el conjunto de caracteres: `a`, `z`, `_`, `*`, etc,
y la salida son los tokens. En el análisis sintáctico en el que estamos ahora,
el alfabeto son los tokens, mientras que la salida es una secuencia de tokens
que forman una expresión.

#### Reglas de una gramática

Hemos visto que una gramática puede contener un conjunto infinito de secuencias
que pertenecen a la misma (Normalmente se habla de que la secuencia verifica la
gramática). Como podemos especificar este conjunto (Potencialmente) infinito?
Una forma es usado **reglas de producción**.

A partir de las reglas, se pueden ir aplicando para producir
secuencias que verifican la gramática. Las secuencias generadas de
esa manera se llaman **derivaciones**.

Las reglas constan de dos partes, la **cabeza de la regle** (_head_)
y el **cuerpo** (_body_). En su forma más simple
el cuerpo una secuencia de **símbolos**.

Los símbolos pueden ser de dos tipos:

- Un **terminal** es una letra del alfabeto de la gramática. En el nivel
sintáctico en que estamos ahora, podrían ser tokens directamente obtenidos
des análisis léxico, cosas como `it`, `3314` o `for`.
El nombre de "terminal" viene de que al llegar a ellos no se sigue
con las producciones (es decir, que no aparecen como cabeza de ninguna regla).

- Un **no terminal** (_Nonterminal_) es una referencia a otra regla. Es por
  estas referencias por lo que la gramática se compone, ya que las reglas
  están interrelacionadas.

Hay otra curiosidad de las reglas: Varias reglas pueden tener la misma cabeza. A
la hora de producir secuencias, cuando llegamos a una regla múltiple (Es decir,
un subconjunto de las reglas que comparten la misma cabeza), uno es libre de
elegir cualquiera de esas reglas.

La forma habitual de describir un conjunto de reglas es la llamada **Forma
de Backus-Nar** (_Backus-Naur Form_ o **BNF**). Hay variantes, pero en este
libro se sigue el siguiente convenio:

- Cada regla empieza con un nombre (La cabeza de la regla), seguido de una flecha `→`
  (Usaremos el carácter Unicode 2192), y seguida de una secuencia de símbolos,
  que terminan con un punto y coma `;` (El cuerpo de la regla).

- Los símbolos terminales se representa entre comillas dobles

- Los símbolo no terminales se representan con letras minúsculas.

Con esto valdría, pero se incluyen algunas reglas adicionales que simplifican la
expresión de las reglas:

- En vez de repetir una regla cada vez que se quiera añadir una producción
  diferente al mismo nombre o cabeza, podemos definir varias
  secuencias diferentes, separándolos con el carácter `|`.

  Por ejemplo, en vez de estas tres reglas:

  - `greek → alpha;` 
  - `greek → beta;` 
  - `greek → gamma;`

  Podemos escribir:

  - `greek → alpha | beta | gamma;`

- Podemos usar paréntesis para agrupar una secuencia de símbolos, y después usar
  `|` para definir secuencias diferentes.

  - `mapletter → ( alpha a ) | ( beta be ) | ( gamma | ce );

- Se puede usar la recursividad para definir una secuencia arbitraria de
  símbolos, pero for facilidad, se incluyen el `*` para indicar cero o más
  veces el símbolo anterior, `+` para indicar _una o más veces el símbolo
  anterior_, y `?` para _cero o una vez el símbolo anterior_ (Es decir,
  convierte un
  símbolo en opcional) 

Estas aportaciones definen una amplicación de las reglas BNF
llamada **EBNF** (_Extended Backus-Naur Form_)
  
## La gramática de Lox

Iremos construyendo la gramática de Lox gradualmente, porque la gramática
a nivel sintáctico es bastante más larga y compleja que la léxica. Empezaremos
con la gramática para _parsear_ solo unos cuantos tipos de expresiones:

- **Literles**: Por ahora, números, cadenas de texto, valores lógicos
  (_Booleanos_, `true` y `false`) y `nil` (El equivalente a `None` en Python o
  `null` en Java).

- **Expresiones unitarias**: Son operadores en forma de prefijo que alteran un
  valor lógico negándolo (`!`) o un valor numérico cambiándo su signo (`-`). 

- **Expresiones binarias**: Son operadores infijos, aritméticos (`+`, `-`, `*` y
  `/`) o lógicos (`==`, `!=`, `<`, `<=`, `>`, `>=') de toda la vida.

  **Parétesis**: Un par de simbolos de abrir y cerrar paréntesis, que nos
  permiten realizar agupaciones dentro de una expresión.

Esta sería la reglas de la gramática por ahora:

```
expresion → literal | unary | binary | grouping;
literal  → NUMBER | STRING | "true" | "false" | "nil";
grouping → "(" expression ")"
unary → ( "-" | "!" ) expression;
binary → expression operator expression;
operator -> "==" | "!=" | "<" | "<=" | ">" | ">=" | "+" | "-" | "*" | "/";
```

Usamos otra extensión de las reglas aquí: Palabras escritas todo en MAYÚSCULAS
para indicar literales compuestos por un solo lexema, pero cuya representación
textual puede variar. `NUMBER` representa cualquier número, y `STRING` es
cualquir cadena de texto (Más adelante usaremos también `IDENTIFIER`). 

Ejercicio: Comprobar que no podemos usar la gramática anterior
para generar "`1 + / 3`".


### Implementar árboles sintácticos


Antes usamos una única clase para representar los tokens, [`Token` en  `tokens.py`](./tokens.py),
con una clase de tipo `Enum` para definir valores constantes que nosidentifiquen
cada tipo, con la clase `TokenType`. Tiene sentido en ese momento porque los
tokens a nivel léxico son similares, pero las expresiones son más complicadas.
Algunas no tiene parámetros (Los literales, por ejemplo), otras tiene uno (El
operador binario `!`) y otros tienen dos (Como el operador `SUMA`).

Aqui usarmos otra estrategia, por lo tanto, para las expresiones. Tendremos
una clase base para las expresiones y tantas clases derivadas como tipos de
expresiones haya.

```python
from abc import ABC

class Expr(ABC):

    @abstractmethod
    def accept(self, visitor):
        raise NotImplementedError(
```

Esta sería la clase Base (Veremos más adelante el uso del método abstracto `accept`, por
ahora solo comentar que usaremos el patrón `Visitor` para poder trabajar con
las expresiones. 

Ahora, para implementar una expresión binaria, podemos hacer algo como:

```python

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
@dataclass
class Binary(Expr):
@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_binary(self)
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_binary(self)
        return visitor.visit_binary(self)#
```

Cada clase tendrá los atributos que necesite para los símbolos
no terminales de la regla. Los operador unitarios solo necesitan
uno, los binarios necesitarán dos.


En el libro se usa metaprogramación para definir las clases de Java. En Python tenemos las 
  [Data Clases](https://docs.python.org/3/library/dataclasses.html), que nos permiten
  definir muy fácilmente clases orientadas a ser contenedores de datos o poco
  más y que, por tanto, nos vienen ideal para las expresiones. 


## Trabajando con árboles

Ahora, entes de empezar a llenar le código de `if` o `match`, para tratar las
excepciones, vamos a considerar el problema que tenemos desde una perspectiva
más abierta.

Basicamente, el problema que tenemos ahora es que tenemos una familia de clases
(las expresiones) y queremos asociarles una serie de funcionalidades. En un
entorno de OOP, lo hariamos definiendo métodos en estas clases. Podriamos, por
ejemplo, definir un metodo `interpret` y en cada tipo de exoresión. 

Esto funciona bien en determinados escenarios, pero no escala nada bien.
Además, como se comenta en el libro, tanto los tokens como las expresiones
son objetos que se utilizan más como un medio de comunicación entre dos
área diferentes, el _scanner_ o análisis léxico y el análisis sintáctivo, y más
adelante, el análisis lexco con las siguientes fases.

Para mantener estos dominios desacoplados, lo ideal es que los tokens y las
expresiones sean simples contenedores de datos, y que no sepan nada de las fases
en las que se ven involucrados. De la misma forma que que el _scanner_ solo
necesita producir tokens, y no sabe que se va a hacer con ellos, el ananlisis
sintáctico acepta tokens, sin interesarse por como se han conseguido. Si
vinculamos los tokens al analizador lexico (o al sintáctico, da igual) tenemos
el código acoplado.

Si implementaramos `interpret` como un método de las clases, estariamos
mezclando los dominios. Este problema se conoce como el **problema de expresión**
o [_expression problem_](https://en.wikipedia.org/wiki/Expression_problem).

Para repsentarlo graficamente, el problema es que tenenos unas
funcionalidades o operaciones (Como `interpret`) que tenemos que
distribuir entre una serie de tipos de datos:

|           | `interpret()` | `resolve()` | `analyze()` ⌋
⌋-----------⌋---------------⌋-------------⌋-------------⌋
⌋ Binary    |     ....      |     ...     |    ...      ⌋
⌋ Grouping  ⌋     ....      |     ...     |    ...      ⌋
⌋ Literal   ⌋     ....      |     ...     |    ...      ⌋
⌋ Unary     ⌋     ....      |     ...     |    ...      ⌋

las columnas son tipos, y las filas operaciones. Cada celda contiene
la sección de código que debe procesar cada combinación, y que debe
tener una implementación específica.

En lenguajes que siguen el paradigma OOP, se asume que todo el código que
va en una fila debe agruparse. Que todas las cosas que se hacen con un
objetos están relacionadas entre si, y por lo tanto el lenguae facilita
hacer esta implementación. 

Esto hace que sea muy fácil añadir un nuevo
tipo, solo hay que definir una nueva clase, con los métodos correspondientes.
No hay que tocar el código preexistente.

El problema viene cuando queremos añadir _una nueva operacion_.  Esto significa
modificar todas las clases existentes hasta ahora.

En los lenguaes funcionales, las asumciones viene por el otro lado. Aqui  no hay
clases con métodos. Tipos y funciones son cosas totalmente diferentes, aunque
pueda parecer lo contrario. Para implementar una función que opere sobre
diferentes tipos de datos, se implementa una única función. Dentro de la función
se usa emparejamiento de patrones (_pattern matching_) para la implementación
especifica de cada tipo.

Esto hace trivial añadir nuevas funcionalidades: solo hay que implementar
una nueva función que contemple todos los tipos anteriores (De forma análoga
el caso de OOP, donde tenemos que definir todos los métodos de la nueva clase).
Pero complica el añadir un nuevo tipo de datos, porque necesitamos estar
seguros de que todas las funciones ya definidas son capaces de trabajar con
ese nuevo tipo.

Por simplificar, en nuestro esquema, los lenguajes funcionales hace fácil implementar nuevas
columnas (Operaciones). Los lenguajes orientados a objetos hacen fácil añadir nuevas filas
(Tipos de datos). **Ningún paradigma actual hace fáciles las dos**. Este es el
_expression problem_ que referenciamos antes.

Una forma de resolver este problema es el patron **Visitante** o **Visitor
pattern**


### El patrón visitante

Este patrón es uno de los más difíciles de entender, empezando por el nombre. El
patrón no tiene nada que ver con _visitar_ nada, y se suele usar para el nombre
del método la palabra `accept`, que támpoco  resulta ser de mucha utilidad.

Muchos piensan que este patrón tiene que vor con recorrer un árbol. Es verdad
que es un ejemplo muy típico, pero el patrón no está limitado a este tipo de
estructura de datos en absoluto. El patrón puede funcionar con otras estucturas
de datos o incluso con un dato único.

El patrón tiene más que ver con adoptar un estilo funcional dentro de un
lenguaje OOP. En otras palabras, nos permite anadir nuevas columnas facilmente.
Podemos definir un conjunto completo de funcionalidades a un conjunto de clases
**sin tener que tocar nada del código de estas**. ¿Cómo se consigue esta magia?
Con el mismo mecanismo que se resulve todo en programación: Añadiendo un nuevo
nivel de abstracción.


