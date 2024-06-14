## Capítulo 4: Análisis léxico o _scanning_

El objetivo del **análisis léxico** (También llamado _scanning_, _lexing_ y,
hace más tiempo, _scanner_) es examinar un texto carácter a carácter y
agruparlos en trozos de texto, de forma que cada trozo de texto sea la cantidad
mínima de caracteres que representan un concepto o que les asignamos un
significado.

Estas agrupaciones de texto mínimas (Lo que en un lenguaje normal serían las
_palabras_) se llaman **lexemas**.

Por ejemplo, dada la secuencia de caracteres:

```
var language = "lax";
```

Los lexemas son:

```
┌─────┐ ┌──────────┐ ┌───┐ ┌───────┐ ┌───┐
│ var │ │ language │ │ = │ │ "lax" │ │ ; │
└─────┘ └──────────┘ └───┘ └───────┘ └───┘
```

Los lexemas son solo un fragmento de texto extraído del código fuente. Sin
embargo, durante el proceso de escaneo a veces obtenemos información
adicional que puede ser interesante después (Por ejemplo, el número de
línea en el código fuente). Cuando agrupamos el lexema con esta información
adicional, el resultado se suele llamar **token**.

Es muy útil organizar los tokens detectados por su tipo. En el ejemplo anterior
tendríamos un token de tipo `KEYWORD` (`var`), para indicar una palabra
reservada del lenguaje, un token de tipo `IDENTIFIER` (`language`), un token de
tipo `EQUAL` (`=`), otro de tipo `LITERAL` (`"lax"`) y finalmente uno de tipo
`SEMICOLON` (`;`). Tradicionalmente se usan mayúsculas para los nombres de los
tipos de tokens.


### Manejo de errores


El fichero de manejo de errores esta en `error
