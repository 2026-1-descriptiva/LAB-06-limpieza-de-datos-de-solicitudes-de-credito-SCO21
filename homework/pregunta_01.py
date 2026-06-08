"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import os
import pandas as pd


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    tabla_credito = pd.read_csv(
        "files/input/solicitudes_de_credito.csv",
        sep=";",
        index_col=0,
        dtype={"estrato": str},
    )

    def limpiar_columna_texto(
        columna_serie: pd.Series, *, recortar: bool = True
    ) -> pd.Series:
        texto_limpio = columna_serie.str.lower()
        if recortar:
            texto_limpio = texto_limpio.str.strip()
        return texto_limpio.str.replace(r"\s+", " ", regex=True)

    columnas_generales = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "línea_credito",
    ]
    for campo in columnas_generales:
        tabla_credito[campo] = limpiar_columna_texto(tabla_credito[campo])

    tabla_credito["barrio"] = limpiar_columna_texto(
        tabla_credito["barrio"], recortar=False
    )
    tabla_credito["barrio"] = tabla_credito["barrio"].str.replace(
        "_", " ", regex=False
    )
    tabla_credito["barrio"] = tabla_credito["barrio"].str.replace(
        "-", " ", regex=False
    )
    tabla_credito["barrio"] = limpiar_columna_texto(
        tabla_credito["barrio"], recortar=False
    )
    tabla_credito["barrio"] = tabla_credito["barrio"].str.replace(
        r"no\.\s*(\d+)", r"no. \1", regex=True
    )
    tabla_credito["barrio"] = limpiar_columna_texto(
        tabla_credito["barrio"], recortar=False
    )

    for campo in ["idea_negocio"]:
        tabla_credito[campo] = tabla_credito[campo].str.replace(
            "_", " ", regex=False
        )
        tabla_credito[campo] = tabla_credito[campo].str.replace(
            "-", " ", regex=False
        )
        tabla_credito[campo] = limpiar_columna_texto(tabla_credito[campo])

    tabla_credito["línea_credito"] = tabla_credito["línea_credito"].str.replace(
        "_", " ", regex=False
    )
    tabla_credito["línea_credito"] = tabla_credito["línea_credito"].str.replace(
        "-", " ", regex=False
    )
    tabla_credito["línea_credito"] = limpiar_columna_texto(
        tabla_credito["línea_credito"]
    )

    tabla_credito["estrato"] = (
        tabla_credito["estrato"].str.strip().astype(int).astype(str)
    )

    tabla_credito = tabla_credito.replace("", float("nan"))
    tabla_credito = tabla_credito.dropna()

    tabla_credito["monto_del_credito"] = (
        tabla_credito["monto_del_credito"].astype(str).str.strip()
    )
    tabla_credito["monto_del_credito"] = tabla_credito[
        "monto_del_credito"
    ].str.replace(r"[\$\s,]", "", regex=True)
    tabla_credito["monto_del_credito"] = tabla_credito[
        "monto_del_credito"
    ].str.replace(r"\.00$", "", regex=True)
    tabla_credito["monto_del_credito"] = tabla_credito[
        "monto_del_credito"
    ].astype(int)

    serie_fecha = tabla_credito["fecha_de_beneficio"].astype(str).str.strip()
    segmentos_fecha = serie_fecha.str.split("/", expand=True)
    anio_al_inicio = segmentos_fecha[0].str.len() == 4

    dia_final = segmentos_fecha[0].where(~anio_al_inicio, segmentos_fecha[2])
    mes_final = segmentos_fecha[1]
    anio_final = segmentos_fecha[2].where(~anio_al_inicio, segmentos_fecha[0])

    tabla_credito["fecha_de_beneficio"] = (
        dia_final.str.zfill(2) + "/" + mes_final.str.zfill(2) + "/" + anio_final
    )

    tabla_credito["comuna_ciudadano"] = tabla_credito[
        "comuna_ciudadano"
    ].astype(int)

    tabla_credito = tabla_credito.drop_duplicates()

    os.makedirs("files/output", exist_ok=True)
    tabla_credito.to_csv(
        "files/output/solicitudes_de_credito.csv", sep=";", index=False
    )