# antp

Module & app for processing Jinja template files with json data and environment variables.

## Installation

```shell
python3 -m pip install antp
```

## Usage

```shell
python3 -m antp -t|--template <templatefile> [-o|--output <outputfile>] [-d|--data <json_datafile1,json_datafile2,...,json_datafileN>]
```

`Templatefile` is the jinja-template. Parameter can be omitted or parameter value set to dash to read template from stdin.
`Outputfile` is the filename where the output will be written. Parameter can be omitted or parameter value can be set to dash to write the output to stdout.
`Json_datafile` is the json-file with the data to be accessed in the templates. The data-parameter can have multiple datafiles, use comma to separate filenames.

Data from datafiles will be in the `data` variable. Variables from environment will be in the `env`variable.

## Examples

data1.json

```json
{
    "colors": {
        "black": "#000000",
        "white": "#FFFFFF",
        "red":   "#FF0000",
        "green": "#00FF00",
        "blue":  "#0000FF"
    },
    "food": [
        "vegetables",
        "meat",
        "fish"
    ]
}
```

data2.json

```json
{
    "capitals": {
      "Finland": "Helsinki",
      "Sweden":  "Stockholm",
      "Denmark": "Copenhagen"
    }
}
```

template.jinja

```jinja
The capital of Finland is {{ data["capitals"]["Finland"] }}.

Typical foods: {{ data["food"]|join(", ") }}.

Black is {{ data["colors"]["black"] }}.

Environment variable FOO is {{ env["FOO"] }}.
```

Run command:

```shell
FOO=bar python3 -m antp -t template.jinja -d data1.json,data2.json -o out.txt
```

out.txt

```text
The capital of Finland is Helsinki.

Typical foods: vegetables, meat, fish.

Black is #000000.

Environment variable FOO is bar.
```
