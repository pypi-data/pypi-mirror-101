from datawidgets.imports import *


def img_widget_from_fname(
    fname_or_url: Union[str, os.PathLike], width: int = 100
) -> widgets.Image:
    ""
    if "https://" in fname_or_url:
        img_bytes = requests.get(fname_or_url).content
    else:
        img_bytes = Path(fname_or_url).read_bytes()
    return widgets.Image(value=img_bytes, width=f"{width}%")


def get_flex_layout(width: int = 100) -> widgets.Layout:
    return widgets.Layout(
        display="flex",
        flex_flow="row wrap",
        width=f"{width}%",
        justify_content="center",
    )


def convert_single_row_to_series(row: pd.DataFrame):
    if isinstance(row, pd.DataFrame):
        if not len(row) == 1:
            raise ValueError(
                # f"Expected a `Series` or a `DataFrame` with one row, got {len(row)} rows"
                f"Only 1 image must be selected to compute similarity; {len(row)} are currently selected"
            )
        return row.iloc[0]
    else:
        return row